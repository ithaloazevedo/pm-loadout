"""
Dashboard Geral — Tradicional.bet.br
Abas: Geral, Turnover e Funil de Aquisição. Acesse: http://localhost:5051

Credenciais do banco vêm de variáveis de ambiente — ver README.md.
"""

import sys, os, json, sqlite3, subprocess, time, traceback, threading
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta
from flask import Flask, jsonify, request, send_from_directory
from decimal import Decimal
import psycopg2, psycopg2.extras

_executor = ThreadPoolExecutor(max_workers=4)

app = Flask(__name__)

# ── CAMINHOS ─────────────────────────────────────────────────────────────────
BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
CACHE_DB  = os.path.join(BASE_DIR, "cache.db")
FRONT_DIR = BASE_DIR
os.makedirs(BASE_DIR, exist_ok=True)

# ── BANCO (auth via token IAM da AWS, não senha fixa compartilhada) ───────────
# Cada execução usa a identidade AWS de quem roda o app (perfil local do
# usuário) — nada de credencial de banco fixa em variável de ambiente.
# O token IAM vale 15min; regeneramos a cada 10min com folga de segurança.
class _IamAuthDBConfig:
    _TOKEN_TTL_SECONDS = 600

    def __init__(self, host, port, dbname, user, region, profile, sslrootcert):
        self.host, self.port, self.dbname, self.user = host, port, dbname, user
        self.region, self.profile, self.sslrootcert = region, profile, sslrootcert
        self._lock = threading.Lock()
        self._token = None
        self._token_at = 0.0

    def _generate_token(self):
        result = subprocess.run(
            ["aws", "rds", "generate-db-auth-token",
             "--hostname", self.host, "--port", str(self.port),
             "--region", self.region, "--username", self.user,
             "--profile", self.profile],
            capture_output=True, text=True, check=True, timeout=15,
        )
        return result.stdout.strip()

    def _password(self):
        with self._lock:
            now = time.time()
            if self._token is None or (now - self._token_at) > self._TOKEN_TTL_SECONDS:
                self._token = self._generate_token()
                self._token_at = now
            return self._token

    # Protocolo de **desempacotamento** do Python (dict-like): permite
    # `psycopg2.connect(**DB)` continuar funcionando sem tocar nas rotas —
    # só que agora `DB["password"]` gera/renova o token IAM na hora.
    def keys(self):
        return ("host", "port", "dbname", "user", "password",
                "sslmode", "sslrootcert", "connect_timeout", "options")

    def __getitem__(self, key):
        if key == "password":
            return self._password()
        fixed = {
            "host": self.host, "port": self.port, "dbname": self.dbname, "user": self.user,
            "sslmode": "verify-full", "sslrootcert": self.sslrootcert,
            "connect_timeout": 60, "options": "-c statement_timeout=360000",
        }
        return fixed[key]

_sslrootcert = os.environ.get("SSL_ROOT_CERT", os.path.expanduser("~/global-bundle.pem"))
if not os.path.exists(_sslrootcert):
    sys.exit(
        f"Certificado SSL não encontrado em {_sslrootcert}. Baixe com:\n"
        f'  curl -sS -o "$HOME/global-bundle.pem" '
        f"https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem"
    )

DB = _IamAuthDBConfig(
    host=os.environ.get("DB_HOST", "ar-trad-prd-cluster.cluster-ro-c44onum4sztb.us-east-1.rds.amazonaws.com"),
    port=int(os.environ.get("DB_PORT", 5432)),
    dbname=os.environ.get("DB_NAME", "trad_prd"),
    user=os.environ.get("DB_USER", "ithalo_mendes"),
    region=os.environ.get("AWS_REGION", "us-east-1"),
    profile=os.environ.get("AWS_PROFILE", "trad-prd-ithalo_mendes"),
    sslrootcert=_sslrootcert,
)

FRENTE_CASE = """
CASE
  WHEN COALESCE(e.json_data->>'btag','') ILIKE '000004_DA'  THEN 'App'
  WHEN COALESCE(e.json_data->>'btag','') ILIKE '000004_%%'  THEN 'Tráfego'
  WHEN COALESCE(e.json_data->>'btag','') ILIKE '000007_%%'  THEN 'Tráfego'
  WHEN COALESCE(e.json_data->>'btag','') ILIKE '000006_e%%' THEN 'Tráfego'
  WHEN COALESCE(e.json_data->>'btag','') ILIKE '000006_%%'  THEN 'Mídias'
  WHEN COALESCE(e.json_data->>'btag','') ILIKE '000002_%%'  THEN 'Resultado Fácil'
  WHEN COALESCE(e.json_data->>'btag','') ILIKE '000003_%%'  THEN 'Resultado Fácil'
  WHEN COALESCE(e.json_data->>'btag','') ILIKE '000167_%%'  THEN 'Resultado Fácil'
  WHEN COALESCE(e.json_data->>'btag','') = ''               THEN 'Orgânico'
  ELSE 'Afiliados'
END
"""

# ── CACHE SQLITE ──────────────────────────────────────────────────────────────
def init_cache():
    c = sqlite3.connect(CACHE_DB)
    c.execute("""CREATE TABLE IF NOT EXISTS kpi_cache (
        cache_key  TEXT PRIMARY KEY,
        data_json  TEXT NOT NULL,
        cached_at  TEXT NOT NULL
    )""")
    c.commit(); c.close()

def cache_get(key):
    c = sqlite3.connect(CACHE_DB)
    row = c.execute("SELECT data_json, cached_at FROM kpi_cache WHERE cache_key=?", (key,)).fetchone()
    c.close()
    if not row: return None
    cached_at = datetime.fromisoformat(row[1])
    # hoje: expira em 5 min | dias passados: nunca expira
    is_today = str(date.today()) in key
    if is_today and (datetime.now() - cached_at).seconds > 300:
        return None
    return json.loads(row[0])

def cache_set(key, data):
    c = sqlite3.connect(CACHE_DB)
    c.execute("INSERT OR REPLACE INTO kpi_cache VALUES (?,?,?)",
              (key, json.dumps(data), datetime.now().isoformat()))
    c.commit(); c.close()

def cache_purge(pattern, keep=None):
    """Apaga entradas que casam com o LIKE `pattern`, preservando a chave `keep`.
    Necessário para chaves com bucket de tempo no nome (ex.: `eid|<hora>|...`): elas
    nunca colidem, então `INSERT OR REPLACE` nunca substitui nada e o cache cresce
    sem limite. cache_get expira a leitura, mas não remove a linha."""
    c = sqlite3.connect(CACHE_DB)
    if keep:
        c.execute("DELETE FROM kpi_cache WHERE cache_key LIKE ? AND cache_key <> ?", (pattern, keep))
    else:
        c.execute("DELETE FROM kpi_cache WHERE cache_key LIKE ?", (pattern,))
    apagadas = c.total_changes
    c.commit(); c.close()
    return apagadas

# ── QUERIES ───────────────────────────────────────────────────────────────────
def query_kpis_simples(dt_inicio, dt_fim):
    """Sem filtro de frente — query rápida sem join com entities."""
    sql = """
    SELECT
      SUM(deposits)::numeric(18,2)      AS depositos,
      SUM(deposits_qty)::int            AS qtd_depositos,
      SUM(withdrawals)::numeric(18,2)   AS saques,
      SUM(ftd_value)::numeric(18,2)     AS ftd,
      SUM(ggr)::numeric(18,2)           AS ggr,
      SUM(ngr)::numeric(18,2)           AS ngr,
      SUM(ggr_casino)::numeric(18,2)    AS ggr_casino,
      SUM(ggr_sport)::numeric(18,2)     AS ggr_sport,
      SUM(ggr_prog)::numeric(18,2)      AS ggr_loteria,
      SUM(games_casino)::numeric(18,2)  AS apo_casino,
      SUM(games_sport)::numeric(18,2)   AS apo_sport,
      SUM(games_prog)::numeric(18,2)    AS apo_loteria,
      SUM(reward)::numeric(18,2)        AS recompensas,
      COUNT(DISTINCT entity_id)         AS jogadores_ativos
    FROM public.vw_uw_balance
    WHERE created >= %(ini)s AND created <= %(fim)s
    """
    c = psycopg2.connect(**DB)
    cur = c.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(sql, {"ini": dt_inicio, "fim": dt_fim})
    row = cur.fetchone()
    c.close()
    return dict(row) if row else {}

def query_kpis_frente(dt_inicio, dt_fim, frente=None, btag=None, afiliado=None):
    """Com filtro de frente/btag/afiliado.

    Quando apenas frente (sem btag/afiliado): usa entity_ids cacheados — bem mais rápido.
    Com btag ou afiliado: JOIN inline (mais lento).
    """
    params = {"ini": dt_inicio, "fim": dt_fim}
    frentes = []
    if frente:
        frentes = frente if isinstance(frente, list) else [frente]
        frentes = [f for f in frentes if f and f != 'todas']

    # ── Frente-only: usa entity_ids do cache, sem JOIN com entities ──────────
    if frentes and not btag and not afiliado:
        entity_ids = get_entity_ids_for_frentes(frentes)
        if entity_ids is not None:
            if not entity_ids:
                return {}  # frente sem nenhum jogador
            params["ids"] = entity_ids
            sql = """
            SELECT
              SUM(deposits)::numeric(18,2)      AS depositos,
              SUM(deposits_qty)::int            AS qtd_depositos,
              SUM(withdrawals)::numeric(18,2)   AS saques,
              SUM(ftd_value)::numeric(18,2)     AS ftd,
              SUM(ggr)::numeric(18,2)           AS ggr,
              SUM(ngr)::numeric(18,2)           AS ngr,
              SUM(ggr_casino)::numeric(18,2)    AS ggr_casino,
              SUM(ggr_sport)::numeric(18,2)     AS ggr_sport,
              SUM(ggr_prog)::numeric(18,2)      AS ggr_loteria,
              SUM(games_casino)::numeric(18,2)  AS apo_casino,
              SUM(games_sport)::numeric(18,2)   AS apo_sport,
              SUM(games_prog)::numeric(18,2)    AS apo_loteria,
              SUM(reward)::numeric(18,2)        AS recompensas,
              COUNT(DISTINCT entity_id)         AS jogadores_ativos
            FROM public.vw_uw_balance
            WHERE created >= %(ini)s AND created <= %(fim)s
              AND entity_id IN (SELECT UNNEST(%(ids)s::bigint[]))
            """
            c = psycopg2.connect(**DB)
            cur = c.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute(sql, params)
            row = cur.fetchone()
            c.close()
            return dict(row) if row else {}

    # ── Com btag/afiliado (ou fallback): JOIN inline ──────────────────────────
    where_extra = ""

    if frentes:
        placeholders = ','.join([f'%(frente_{i})s' for i in range(len(frentes))])
        where_extra += f" AND ({FRENTE_CASE}) IN ({placeholders})"
        for i, f in enumerate(frentes):
            params[f'frente_{i}'] = f

    if btag:
        where_extra += " AND COALESCE(e.json_data->>'btag','') ILIKE %(btag)s"
        params["btag"] = f"%{btag}%"

    if afiliado:
        where_extra += """ AND EXISTS (
            SELECT 1 FROM affiliates.affiliates af
            JOIN public.entities ae ON ae.id = af.entity_id
            WHERE af.id IN (
                SELECT affiliate_id FROM affiliates.clients cl WHERE cl.entity_id = v.entity_id
            )
            AND (ae.json_data->>'name' ILIKE %(afi)s OR ae.json_data->>'fullName' ILIKE %(afi)s)
        )"""
        params["afi"] = f"%{afiliado}%"

    sql = f"""
    SELECT
      SUM(v.deposits)::numeric(18,2)      AS depositos,
      SUM(v.deposits_qty)::int            AS qtd_depositos,
      SUM(v.withdrawals)::numeric(18,2)   AS saques,
      SUM(v.ftd_value)::numeric(18,2)     AS ftd,
      SUM(v.ggr)::numeric(18,2)           AS ggr,
      SUM(v.ngr)::numeric(18,2)           AS ngr,
      SUM(v.ggr_casino)::numeric(18,2)    AS ggr_casino,
      SUM(v.ggr_sport)::numeric(18,2)     AS ggr_sport,
      SUM(v.ggr_prog)::numeric(18,2)      AS ggr_loteria,
      SUM(v.games_casino)::numeric(18,2)  AS apo_casino,
      SUM(v.games_sport)::numeric(18,2)   AS apo_sport,
      SUM(v.games_prog)::numeric(18,2)    AS apo_loteria,
      SUM(v.reward)::numeric(18,2)        AS recompensas,
      COUNT(DISTINCT v.entity_id)         AS jogadores_ativos
    FROM public.vw_uw_balance v
    JOIN public.entities e ON e.id = v.entity_id
    WHERE v.created >= %(ini)s AND v.created <= %(fim)s
    {where_extra}
    """
    c = psycopg2.connect(**DB)
    cur = c.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(sql, params)
    row = cur.fetchone()
    c.close()
    return dict(row) if row else {}

def query_top_ggr(dt_ini, dt_fim, frentes=None, btag=None, afiliado=None):
    """Top GGR positivo e negativo com nome — respeita data, frente, btag e afiliado."""
    c = psycopg2.connect(**DB)
    cur = c.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        if frentes or btag or afiliado:
            entity_ids = fetch_filtered_entity_ids(cur, frentes or [], btag or '', afiliado or '')
            if not entity_ids:
                return {"positivos": [], "negativos": []}
            id_filter = "AND entity_id IN (SELECT UNNEST(%(ids)s::bigint[]))"
            base_params = {"ini": dt_ini, "fim": dt_fim, "ids": entity_ids}
        else:
            id_filter = ""
            base_params = {"ini": dt_ini, "fim": dt_fim}

        cur.execute(f"""
            SELECT entity_id, SUM(ggr)::numeric(18,2) AS ggr
            FROM public.vw_uw_balance
            WHERE created >= %(ini)s AND created <= %(fim)s {id_filter}
            GROUP BY entity_id ORDER BY ggr DESC LIMIT 10
        """, base_params)
        pos_rows = [dict(r) for r in cur.fetchall()]

        cur.execute(f"""
            SELECT entity_id, SUM(ggr)::numeric(18,2) AS ggr
            FROM public.vw_uw_balance
            WHERE created >= %(ini)s AND created <= %(fim)s {id_filter}
            GROUP BY entity_id ORDER BY ggr ASC LIMIT 10
        """, base_params)
        neg_rows = [dict(r) for r in cur.fetchall()]

        all_ids  = list(set([r['entity_id'] for r in pos_rows + neg_rows]))
        pos_ids  = [r['entity_id'] for r in pos_rows]
        neg_ids  = [r['entity_id'] for r in neg_rows]
        nomes    = {}
        jogos_pos = {}
        jogos_neg = {}
        afiliados = {}

        if all_ids:
            # 2. Nomes
            cur.execute("""
                SELECT id, COALESCE(
                    NULLIF(json_data->>'fullname',''),
                    NULLIF(json_data->>'fullName',''),
                    NULLIF(json_data->>'name',''),
                    'Sem nome'
                ) AS nome
                FROM public.entities WHERE id = ANY(%s)
            """, (all_ids,))
            nomes = {r['id']: r['nome'] for r in cur.fetchall()}

            # 3. Jogo de MAIOR GGR (para positivos)
            jogos_pos = {}
            if pos_ids:
                cur.execute("""
                    SELECT DISTINCT ON (entity_id) entity_id, jogo
                    FROM (
                        SELECT ges.entity_id, gc.name AS jogo, SUM(ges.ggr) AS jogo_ggr
                        FROM integration.game_entity_sale_statistics ges
                        JOIN integration.games g ON g.id = ges.game_id
                        JOIN integration.game_categories gc ON gc.id = g.game_category_id
                        WHERE ges.entity_id = ANY(%s) AND ges.created::date >= %s AND ges.created::date <= %s
                        GROUP BY ges.entity_id, gc.name
                    ) t ORDER BY entity_id, jogo_ggr DESC
                """, (pos_ids, dt_ini, dt_fim))
                jogos_pos = {r['entity_id']: r['jogo'] for r in cur.fetchall()}

            # 4. Jogo de MENOR GGR (para negativos)
            jogos_neg = {}
            if neg_ids:
                cur.execute("""
                    SELECT DISTINCT ON (entity_id) entity_id, jogo
                    FROM (
                        SELECT ges.entity_id, gc.name AS jogo, SUM(ges.ggr) AS jogo_ggr
                        FROM integration.game_entity_sale_statistics ges
                        JOIN integration.games g ON g.id = ges.game_id
                        JOIN integration.game_categories gc ON gc.id = g.game_category_id
                        WHERE ges.entity_id = ANY(%s) AND ges.created::date >= %s AND ges.created::date <= %s
                        GROUP BY ges.entity_id, gc.name
                    ) t ORDER BY entity_id, jogo_ggr ASC
                """, (neg_ids, dt_ini, dt_fim))
                jogos_neg = {r['entity_id']: r['jogo'] for r in cur.fetchall()}

            # 5. Tags: Novo/Recorrente/VIP
            current_month_start = date(dt_fim.year, dt_fim.month, 1)
            ftd_dates = {}
            lifetime_deps = {}
            tags_map = {}
            try:
                cur.execute("""
                    SELECT entity_id, MIN(created) AS first_dep
                    FROM public.vw_uw_balance
                    WHERE ftd_value > 0 AND entity_id = ANY(%s)
                    GROUP BY entity_id
                """, (all_ids,))
                ftd_dates = {r['entity_id']: r['first_dep'] for r in cur.fetchall()}

                cur.execute("""
                    SELECT entity_id, SUM(deposits)::numeric(18,2) AS total_dep
                    FROM public.vw_uw_balance
                    WHERE entity_id = ANY(%s)
                    GROUP BY entity_id
                """, (all_ids,))
                lifetime_deps = {r['entity_id']: float(r['total_dep'] or 0) for r in cur.fetchall()}

                for eid in all_ids:
                    tags = []
                    first = ftd_dates.get(eid)
                    if first and (first if isinstance(first, date) else first.date()) >= current_month_start:
                        tags.append('Novo')
                    else:
                        tags.append('Recorrente')
                    if lifetime_deps.get(eid, 0) >= 20000:
                        tags.append('VIP')
                    tags_map[eid] = tags
            except Exception as t_err:
                print(f"Tags warning: {t_err}")

            # 6. Fallback de jogo via vw_uw_balance (sempre disponível)
            try:
                cur.execute("""
                    SELECT entity_id,
                           CASE
                             WHEN ABS(ggr_casino) >= ABS(ggr_sport) AND ABS(ggr_casino) >= ABS(ggr_prog) THEN 'Cassino'
                             WHEN ABS(ggr_sport) >= ABS(ggr_prog) THEN 'Esporte'
                             ELSE 'Loteria'
                           END AS jogo
                    FROM (
                        SELECT entity_id,
                               SUM(ggr_casino) AS ggr_casino,
                               SUM(ggr_sport)  AS ggr_sport,
                               SUM(ggr_prog)   AS ggr_prog
                        FROM public.vw_uw_balance
                        WHERE created >= %s AND created <= %s AND entity_id = ANY(%s)
                        GROUP BY entity_id
                    ) t
                """, (dt_ini, dt_fim, all_ids))
                jogo_fallback = {r['entity_id']: r['jogo'] for r in cur.fetchall()}
                # Usar fallback onde game_entity_sale_statistics não retornou
                for eid in all_ids:
                    if eid not in jogos_pos:
                        jogos_pos[eid] = jogo_fallback.get(eid, '—')
                    if eid not in jogos_neg:
                        jogos_neg[eid] = jogo_fallback.get(eid, '—')
            except Exception as jf_err:
                print(f"Jogo fallback warning: {jf_err}")

            # 6. Afiliados
            afiliados = {}
            try:
                cur.execute("""
                    SELECT DISTINCT ON (cl.entity_id) cl.entity_id,
                           COALESCE(
                               NULLIF(ae.json_data->>'name',''),
                               NULLIF(ae.json_data->>'fullName',''),
                               NULLIF(ae.json_data->>'fullname',''),
                               'Orgânico'
                           ) AS afiliado
                    FROM affiliates.clients cl
                    JOIN affiliates.affiliates af ON af.id = cl.affiliate_id
                    JOIN public.entities ae ON ae.id = af.entity_id
                    WHERE cl.entity_id = ANY(%s)
                    ORDER BY cl.entity_id, cl.created DESC
                """, (all_ids,))
                afiliados = {r['entity_id']: r['afiliado'] for r in cur.fetchall()}
            except Exception as ae_err:
                print(f"Afiliados warning: {ae_err}")

        def enrich(rows, jogos_map):
            return [{
                'entity_id': r['entity_id'],
                'ggr': float(r['ggr']),
                'nome': nomes.get(r['entity_id'], '—'),
                'jogo': jogos_map.get(r['entity_id'], '—'),
                'afiliado': afiliados.get(r['entity_id'], 'Orgânico'),
                'tags': tags_map.get(r['entity_id'], ['Recorrente']),
            } for r in rows]

        return {"positivos": enrich(pos_rows, jogos_pos), "negativos": enrich(neg_rows, jogos_neg)}
    except Exception as e:
        print(f"Top GGR error: {e}")
        return {"positivos": [], "negativos": []}
    finally:
        c.close()

def periodo(filtro, custom_ini=None, custom_fim=None):
    hoje = date.today()
    if filtro == "hoje":       return hoje, hoje
    if filtro == "ontem":      return hoje - timedelta(days=1), hoje - timedelta(days=1)
    if filtro == "mes":        return date(hoje.year, hoje.month, 1), hoje
    if filtro == "mes_ant":
        m = hoje.month-1 or 12
        a = hoje.year if hoje.month > 1 else hoje.year-1
        ultimo = date(hoje.year, hoje.month, 1) - timedelta(days=1)
        return date(a, m, 1), ultimo
    if filtro == "ano":        return date(hoje.year, 1, 1), hoje
    if filtro == "custom" and custom_ini and custom_fim:
        return date.fromisoformat(custom_ini), date.fromisoformat(custom_fim)
    return hoje, hoje

def floatify(d):
    """Converte Decimal/int para float para JSON."""
    result = {}
    for k, v in d.items():
        if v is None:
            result[k] = 0
        elif isinstance(v, Decimal):
            result[k] = float(v)
        elif isinstance(v, (int, float)):
            result[k] = v
        else:
            try:
                result[k] = float(v)
            except:
                result[k] = 0
    return result

def get_entity_ids_for_frentes(frentes_lista):
    """Retorna entity_ids para as frentes — cache por hora (nova hora = nova busca)."""
    if not frentes_lista:
        return None
    # Chave inclui a hora atual → cache expira naturalmente a cada hora
    hour_bucket = datetime.now().strftime("%Y-%m-%d-%H")
    frentes_sufixo = '|'.join(sorted(frentes_lista))
    cache_key = f"eid|{hour_bucket}|{frentes_sufixo}"
    cached = cache_get(cache_key)
    if cached:
        return cached.get("ids")
    # Buckets de horas anteriores desta mesma combinação de frentes são lixo: a lista
    # de ids chega a 3,8 MB por linha e uma nova nasce a cada hora. Sem isto o cache.db
    # passou de 1,4 GB em três semanas.
    # O curinga é '_'*13 (largura exata de YYYY-MM-DD-HH), não '%': com '%' o padrão
    # casaria também com outras combinações de frente (ex.: 'eid|%|Tráfego' pegaria
    # 'eid|<hora>|Mídias|Tráfego') e apagaria cache que não é desta chave.
    cache_purge(f"eid|{'_' * 13}|{frentes_sufixo}", keep=cache_key)
    try:
        c = psycopg2.connect(**DB)
        cur = c.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        pls = ','.join([f'%(ff_{i})s' for i in range(len(frentes_lista))])
        fc = FRENTE_CASE.replace('e.json_data', 'json_data')
        cur.execute(f"SELECT id FROM public.entities WHERE ({fc}) IN ({pls})",
                    {f'ff_{i}': f for i, f in enumerate(frentes_lista)})
        ids = [r['id'] for r in cur.fetchall()]
        c.close()
        cache_set(cache_key, {"ids": ids})
        print(f"Entity IDs cache: {len(ids)} IDs para {frentes_lista}")
        return ids
    except Exception as e:
        print(f"Entity IDs warning: {e}")
        return None


def build_entity_filter(frentes_lista, btag_str, afiliado_str, params_out, prefix=""):
    """
    Constrói filtro SQL de entity_ids com base nos filtros.
    Se apenas frentes_lista (sem btag/afiliado): usa IDs cacheados via ANY(array) — mais rápido.
    Caso contrário: usa subquery inline.
    """
    col = prefix if prefix else "entity_id"

    # ── Caso 1: apenas frentes, sem btag/afiliado — usa cache de entity_ids ──
    if frentes_lista and not btag_str and not afiliado_str:
        cached_ids = get_entity_ids_for_frentes(frentes_lista)
        if cached_ids is not None:
            uid = id(params_out)  # chave única para não colidir
            key = f'cached_eids_{uid}'
            params_out[key] = cached_ids
            return f"AND {col} IN (SELECT UNNEST(%({key})s::bigint[]))"
        # Fallback: subquery inline se o cache falhar
        pls = ','.join([f'%(ff_{i})s' for i in range(len(frentes_lista))])
        fc = FRENTE_CASE.replace('e.json_data', 'json_data')
        for i, f2 in enumerate(frentes_lista):
            params_out[f'ff_{i}'] = f2
        return f"AND {col} IN (SELECT id FROM public.entities WHERE ({fc}) IN ({pls}))"

    # ── Caso 2: btag e/ou afiliado (subquery completa) ────────────────────────
    ent_conds, ent_params = [], {}

    if frentes_lista:
        pls = ','.join([f'%(ff_{i})s' for i in range(len(frentes_lista))])
        fc = FRENTE_CASE.replace('e.json_data', 'json_data')
        ent_conds.append(f"({fc}) IN ({pls})")
        for i, f2 in enumerate(frentes_lista):
            ent_params[f'ff_{i}'] = f2

    if btag_str:
        bl = [b.strip() for b in btag_str.split(',') if b.strip()]
        if bl:
            pls = ','.join([f'%(bt_{i})s' for i in range(len(bl))])
            ent_conds.append(f"COALESCE(json_data->>'btag','') IN ({pls})")
            for i, b2 in enumerate(bl):
                ent_params[f'bt_{i}'] = b2

    afi_sub = ""
    if afiliado_str:
        afis = [a.strip() for a in afiliado_str.split(',') if a.strip()]
        if afis:
            afi_c = ' OR '.join([
                f"ae.json_data->>'name' ILIKE %(af_{i})s OR ae.json_data->>'fullName' ILIKE %(af_{i})s"
                for i in range(len(afis))
            ])
            afi_sub = f"""AND e.id IN (
                SELECT DISTINCT cl.entity_id
                FROM affiliates.clients cl
                JOIN affiliates.affiliates aff ON aff.id = cl.affiliate_id
                JOIN public.entities ae ON ae.id = aff.entity_id
                WHERE {afi_c}
            )"""
            for i, a2 in enumerate(afis):
                ent_params[f'af_{i}'] = f'%{a2}%'

    if not ent_conds and not afi_sub:
        return ""

    where_clause = f"WHERE {' AND '.join(ent_conds)}" if ent_conds else "WHERE TRUE"
    sub = f"(SELECT e.id FROM public.entities e {where_clause} {afi_sub})"
    params_out.update(ent_params)
    return f"AND {col} IN {sub}"


def fetch_filtered_entity_ids(cur, frentes_lista, btag_str, afiliado_str):
    """Retorna lista de entity_ids aplicando frente + btag + afiliado, ou None se sem filtro."""
    if not frentes_lista and not btag_str and not afiliado_str:
        return None
    if frentes_lista and not btag_str and not afiliado_str:
        return get_entity_ids_for_frentes(frentes_lista)
    params = {}
    fragment = build_entity_filter(frentes_lista, btag_str, afiliado_str, params)
    if not fragment:
        return None
    adapted = fragment.replace("AND entity_id IN", "AND id IN", 1)
    cur.execute(f"SELECT id FROM public.entities WHERE entity_type_id=6 {adapted}", params)
    return [r['id'] for r in cur.fetchall()]


def clean(obj):
    """Converte Decimal, date e datetime em qualquer estrutura aninhada."""
    if isinstance(obj, Decimal):            return float(obj)
    if isinstance(obj, (date, datetime)):   return str(obj)
    if isinstance(obj, dict):               return {k: clean(v) for k,v in obj.items()}
    if isinstance(obj, list):               return [clean(i) for i in obj]
    return obj

# ── ROTAS API ─────────────────────────────────────────────────────────────────
@app.route("/api/geral_completo")
def api_geral_completo():
    """Retorna cards E tabela diária em UMA única query — garante consistência."""
    filtro     = request.args.get("data", "hoje")
    frente     = request.args.get("frente", "todas")
    btag       = request.args.get("btag", "").strip()
    afiliado   = request.args.get("afiliado", "").strip()
    custom_ini = request.args.get("ini", "")
    custom_fim = request.args.get("fim", "")
    force      = request.args.get("force", "0") == "1"

    dt_ini, dt_fim = periodo(filtro, custom_ini, custom_fim)
    frentes_lista = [f.strip() for f in frente.split(',') if f.strip() and f.strip() != 'todas'] if frente != 'todas' else []
    tem_filtro = bool(frentes_lista) or btag or afiliado

    cache_key = f"completo|{dt_ini}|{dt_fim}|{frente}|{btag}|{afiliado}"
    cached = None if force else cache_get(cache_key)
    if cached:
        return jsonify({"ok": True, "data": cached, "cache": True,
                        "periodo": {"ini": str(dt_ini), "fim": str(dt_fim)}})

    # Dispara top_ggr em paralelo com as queries principais
    top_ggr_future = _executor.submit(query_top_ggr, dt_ini, dt_fim, frentes_lista or None, btag or None, afiliado or None)

    try:
        c = psycopg2.connect(**DB)
        cur = c.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        params_base = {"ini": dt_ini, "fim": dt_fim}

        # ── ESTRATÉGIA: 1 scan no vw_uw_balance, agregação em Python ──────────
        # Com filtro: busca rows brutas por entity+dia e agrega no Python.
        # Sem filtro: query GROUP BY diretamente (já rápido, evita trazer muitos dados).

        if tem_filtro:
            entity_filter_sql = build_entity_filter(frentes_lista, btag, afiliado, params_base, "entity_id")

            # 1 ÚNICO scan — retorna por entity_id+dia
            cur.execute(f"""
                SELECT
                    entity_id,
                    created::date                                      AS dt,
                    COALESCE(deposits,0)::numeric(18,2)                AS dep,
                    COALESCE(deposits_qty,0)::int                      AS dep_qty,
                    COALESCE(withdrawals,0)::numeric(18,2)             AS wdw,
                    COALESCE(ftd_value,0)::numeric(18,2)               AS ftd,
                    COALESCE(ggr,0)::numeric(18,2)                     AS ggr,
                    COALESCE(ngr,0)::numeric(18,2)                     AS ngr,
                    COALESCE(reward,0)::numeric(18,2)                  AS rwd,
                    COALESCE(ggr_casino,0)::numeric(18,2)              AS ggr_c,
                    COALESCE(ggr_sport,0)::numeric(18,2)               AS ggr_s,
                    COALESCE(ggr_prog,0)::numeric(18,2)                AS ggr_p,
                    COALESCE(games_casino,0)::numeric(18,2)            AS gm_c,
                    COALESCE(games_sport,0)::numeric(18,2)             AS gm_s,
                    COALESCE(games_prog,0)::numeric(18,2)              AS gm_p
                FROM public.vw_uw_balance
                WHERE created >= %(ini)s AND created <= %(fim)s
                {entity_filter_sql}
            """, params_base)
            raw_rows = cur.fetchall()

            # Agrega diário + NR + saques tudo em Python (sem query extra)
            by_date   = defaultdict(lambda: dict(dep=0,dep_qty=0,wdw=0,ftd=0,ggr=0,ngr=0,rwd=0,
                                                  ggr_c=0,ggr_s=0,ggr_p=0,gm_c=0,gm_s=0,gm_p=0,
                                                  jog=set(),apo=set(),ftd_cnt=set()))
            by_entity = defaultdict(lambda: dict(dep=0,dep_qty=0,ftd=0,ggr=0,rwd=0,apostas=0,apostou=False))

            for r in raw_rows:
                eid  = r['entity_id']
                d    = str(r['dt'])
                dep  = float(r['dep']   or 0)
                dqty = int(r['dep_qty'] or 0)
                wdw  = float(r['wdw']   or 0)
                ftd  = float(r['ftd']   or 0)
                ggr  = float(r['ggr']   or 0)
                ngr  = float(r['ngr']   or 0)
                rwd  = float(r['rwd']   or 0)
                gc   = float(r['ggr_c'] or 0)
                gs   = float(r['ggr_s'] or 0)
                gp   = float(r['ggr_p'] or 0)
                mc   = float(r['gm_c']  or 0)
                ms   = float(r['gm_s']  or 0)
                mp   = float(r['gm_p']  or 0)
                apo  = mc + ms + mp

                bd = by_date[d]
                bd['dep']+=dep; bd['dep_qty']+=dqty; bd['wdw']+=wdw; bd['ftd']+=ftd
                bd['ggr']+=ggr; bd['ngr']+=ngr; bd['rwd']+=rwd
                bd['ggr_c']+=gc; bd['ggr_s']+=gs; bd['ggr_p']+=gp
                bd['gm_c']+=mc; bd['gm_s']+=ms; bd['gm_p']+=mp
                bd['jog'].add(eid)
                if apo > 0: bd['apo'].add(eid)
                if ftd > 0: bd['ftd_cnt'].add(eid)

                be = by_entity[eid]
                be['dep']+=dep; be['dep_qty']+=dqty; be['ftd']+=ftd
                be['ggr']+=ggr; be['rwd']+=rwd; be['apostas']+=apo
                if apo > 0: be['apostou'] = True

            rows = []
            for d in sorted(by_date.keys()):
                bd = by_date[d]
                rows.append({
                    'data': d,
                    'deposito':  bd['dep'],  'qtd_dep': bd['dep_qty'],
                    'apostas':   bd['gm_c']+bd['gm_s']+bd['gm_p'],
                    'ggr':       bd['ggr'],  'ngr':      bd['ngr'],
                    'recompensas': bd['rwd'],
                    'ggr_casino': bd['ggr_c'], 'ggr_sport': bd['ggr_s'], 'ggr_loteria': bd['ggr_p'],
                    'apo_casino': bd['gm_c'],  'apo_sport': bd['gm_s'],  'apo_loteria': bd['gm_p'],
                    'jogadores':   len(bd['jog']),
                    'apostadores': len(bd['apo']),
                    'ftd_count':   len(bd['ftd_cnt']),
                })

            saques_total = sum(float(r['wdw'] or 0) for r in raw_rows)

            # NR — agrega por entity (is_novo = teve ftd no período)
            nr_data = {"novos": {}, "recorrentes": {}, "total": {}}
            nr_acc  = {"novos": defaultdict(float), "recorrentes": defaultdict(float)}
            nr_cnts = {"novos": {"dep": 0, "apo": 0}, "recorrentes": {"dep": 0, "apo": 0}}
            for eid, be in by_entity.items():
                t = "novos" if be['ftd'] > 0 else "recorrentes"
                acc = nr_acc[t]
                acc['depositos']    += be['dep']
                acc['ftd']          += be['ftd']
                acc['qtd_depositos']+= be['dep_qty']
                acc['ggr']          += be['ggr']
                acc['recompensas']  += be['rwd']
                acc['apostas']      += be['apostas']
                if be['dep'] > 0:  nr_cnts[t]['dep'] += 1
                if be['apostou']:  nr_cnts[t]['apo'] += 1

            for t in ("novos", "recorrentes"):
                acc  = nr_acc[t]
                n_d  = nr_cnts[t]['dep']
                n_a  = nr_cnts[t]['apo']
                val_d = acc['depositos']; qtd_d = acc['qtd_depositos']
                ggr_r = acc['ggr']; apo_r = acc['apostas']; rec_r = acc['recompensas']
                nr_data[t] = {
                    "depositantes": n_d,
                    "ftd": acc['ftd'], "depositos": val_d, "qtd_depositos": int(qtd_d),
                    "tm_deposito":    round(val_d/qtd_d, 2) if qtd_d else 0,
                    "tm_depositante": round(val_d/n_d, 2)   if n_d   else 0,
                    "frequencia":     round(qtd_d/n_d, 2)   if n_d   else 0,
                    "ggr": ggr_r, "recompensas": rec_r,
                    "apostas": apo_r, "apostadores": n_a,
                    "tm_apostador": round(apo_r/n_a, 2) if n_a else 0,
                }
            n2  = nr_data.get("novos", {}); r3 = nr_data.get("recorrentes", {})
            tot_d = n2.get("depositos",0)+r3.get("depositos",0)
            tot_q = n2.get("qtd_depositos",0)+r3.get("qtd_depositos",0)
            tot_e = n2.get("depositantes",0)+r3.get("depositantes",0)
            tot_apo  = n2.get("apostas",0)+r3.get("apostas",0)
            tot_apos = n2.get("apostadores",0)+r3.get("apostadores",0)
            nr_data["total"] = {
                "depositantes": tot_e, "ftd": n2.get("ftd",0)+r3.get("ftd",0),
                "depositos": tot_d, "qtd_depositos": tot_q,
                "tm_deposito":    round(tot_d/tot_q,2) if tot_q else 0,
                "tm_depositante": round(tot_d/tot_e,2) if tot_e else 0,
                "frequencia":     round(tot_q/tot_e,2) if tot_e else 0,
                "ggr": n2.get("ggr",0)+r3.get("ggr",0),
                "recompensas": n2.get("recompensas",0)+r3.get("recompensas",0),
                "apostas": tot_apo, "apostadores": tot_apos,
                "tm_apostador": round(tot_apo/tot_apos,2) if tot_apos else 0,
            }

        else:
            # Sem filtro: GROUP BY no banco (rápido, sem entity join)
            cur.execute("""
                SELECT
                    to_char(created, 'YYYY-MM-DD')                    AS data,
                    COALESCE(SUM(deposits),0)::numeric(18,2)           AS deposito,
                    COALESCE(SUM(deposits_qty),0)::int                 AS qtd_dep,
                    COALESCE(SUM(COALESCE(games_casino,0)+COALESCE(games_sport,0)+COALESCE(games_prog,0)),0)::numeric(18,2) AS apostas,
                    COALESCE(SUM(ggr),0)::numeric(18,2)                AS ggr,
                    COALESCE(SUM(reward),0)::numeric(18,2)             AS recompensas,
                    COALESCE(SUM(ngr),0)::numeric(18,2)                AS ngr,
                    COALESCE(SUM(withdrawals),0)::numeric(18,2)        AS wdw,
                    COALESCE(SUM(ggr_casino),0)::numeric(18,2)         AS ggr_casino,
                    COALESCE(SUM(ggr_sport),0)::numeric(18,2)          AS ggr_sport,
                    COALESCE(SUM(ggr_prog),0)::numeric(18,2)           AS ggr_loteria,
                    COALESCE(SUM(games_casino),0)::numeric(18,2)       AS apo_casino,
                    COALESCE(SUM(games_sport),0)::numeric(18,2)        AS apo_sport,
                    COALESCE(SUM(games_prog),0)::numeric(18,2)         AS apo_loteria,
                    COUNT(DISTINCT entity_id)                          AS jogadores,
                    COUNT(DISTINCT CASE WHEN COALESCE(games_casino,0)+COALESCE(games_sport,0)+COALESCE(games_prog,0) > 0 THEN entity_id END) AS apostadores,
                    COUNT(DISTINCT CASE WHEN ftd_value > 0 THEN entity_id END) AS ftd_count
                FROM public.vw_uw_balance
                WHERE created >= %(ini)s AND created <= %(fim)s
                GROUP BY to_char(created, 'YYYY-MM-DD')
                ORDER BY to_char(created, 'YYYY-MM-DD')
            """, params_base)
            raw = [dict(r) for r in cur.fetchall()]
            rows = [{**r, 'deposito': float(r['deposito'] or 0),
                     'apostas': float(r['apostas'] or 0), 'ggr': float(r['ggr'] or 0),
                     'ngr': float(r['ngr'] or 0), 'recompensas': float(r['recompensas'] or 0),
                     'ggr_casino': float(r['ggr_casino'] or 0), 'ggr_sport': float(r['ggr_sport'] or 0),
                     'ggr_loteria': float(r['ggr_loteria'] or 0),
                     'apo_casino': float(r['apo_casino'] or 0), 'apo_sport': float(r['apo_sport'] or 0),
                     'apo_loteria': float(r['apo_loteria'] or 0),
                     'qtd_dep': int(r['qtd_dep'] or 0), 'jogadores': int(r['jogadores'] or 0),
                     'apostadores': int(r['apostadores'] or 0), 'ftd_count': int(r['ftd_count'] or 0),
                    } for r in raw]

            saques_total = sum(float(r.get('wdw') or 0) for r in rows)

            # NR — query separada pois GROUP BY entity é pesado sem filtro
            nr_data = {"novos": {}, "recorrentes": {}, "total": {}}
            try:
                cur.execute("""
                    WITH ent AS (
                        SELECT entity_id,
                               SUM(ftd_value) > 0   AS is_novo,
                               SUM(deposits)         AS dep,
                               SUM(ftd_value)        AS ftd,
                               SUM(deposits_qty)     AS dep_qty,
                               SUM(ggr)              AS ggr,
                               SUM(reward)           AS recompensas,
                               SUM(COALESCE(games_casino,0)+COALESCE(games_sport,0)+COALESCE(games_prog,0)) AS apostas,
                               SUM(COALESCE(games_casino,0)+COALESCE(games_sport,0)+COALESCE(games_prog,0)) > 0 AS apostou
                        FROM public.vw_uw_balance
                        WHERE created >= %(ini)s AND created <= %(fim)s
                        GROUP BY entity_id
                    )
                    SELECT CASE WHEN is_novo THEN 'Novo' ELSE 'Recorrente' END AS tipo,
                           COUNT(CASE WHEN dep > 0 THEN 1 END)        AS depositantes,
                           SUM(CASE WHEN dep > 0 THEN ftd ELSE 0 END)::numeric(18,2) AS ftd,
                           SUM(dep)::numeric(18,2)                    AS depositos,
                           SUM(dep_qty)::bigint                       AS qtd_dep,
                           SUM(ggr)::numeric(18,2)                    AS ggr,
                           SUM(recompensas)::numeric(18,2)            AS recompensas,
                           SUM(apostas)::numeric(18,2)                AS apostas,
                           COUNT(CASE WHEN apostou THEN 1 END)        AS apostadores
                    FROM ent GROUP BY 1
                """, params_base)
                for r in cur.fetchall():
                    t = "novos" if r["tipo"] == "Novo" else "recorrentes"
                    n_dep = int(r["depositantes"] or 0)
                    val_d = float(r["depositos"] or 0); qtd_d = int(r["qtd_dep"] or 0)
                    ggr_r = float(r["ggr"] or 0); apo_r = float(r.get("apostas") or 0)
                    apos_r = int(r.get("apostadores") or 0); rec_r = float(r.get("recompensas") or 0)
                    nr_data[t] = {
                        "depositantes": n_dep,
                        "ftd": float(r["ftd"] or 0), "depositos": val_d, "qtd_depositos": qtd_d,
                        "tm_deposito":    round(val_d/qtd_d,2) if qtd_d else 0,
                        "tm_depositante": round(val_d/n_dep,2) if n_dep else 0,
                        "frequencia":     round(qtd_d/n_dep,2) if n_dep else 0,
                        "ggr": ggr_r, "recompensas": rec_r,
                        "apostas": apo_r, "apostadores": apos_r,
                        "tm_apostador": round(apo_r/apos_r,2) if apos_r else 0,
                    }
                n2  = nr_data.get("novos", {}); r3 = nr_data.get("recorrentes", {})
                tot_d = n2.get("depositos",0)+r3.get("depositos",0)
                tot_q = n2.get("qtd_depositos",0)+r3.get("qtd_depositos",0)
                tot_e = n2.get("depositantes",0)+r3.get("depositantes",0)
                tot_apo  = n2.get("apostas",0)+r3.get("apostas",0)
                tot_apos = n2.get("apostadores",0)+r3.get("apostadores",0)
                nr_data["total"] = {
                    "depositantes": tot_e, "ftd": n2.get("ftd",0)+r3.get("ftd",0),
                    "depositos": tot_d, "qtd_depositos": tot_q,
                    "tm_deposito":    round(tot_d/tot_q,2) if tot_q else 0,
                    "tm_depositante": round(tot_d/tot_e,2) if tot_e else 0,
                    "frequencia":     round(tot_q/tot_e,2) if tot_e else 0,
                    "ggr": n2.get("ggr",0)+r3.get("ggr",0),
                    "recompensas": n2.get("recompensas",0)+r3.get("recompensas",0),
                    "apostas": tot_apo, "apostadores": tot_apos,
                    "tm_apostador": round(tot_apo/tot_apos,2) if tot_apos else 0,
                }
            except Exception as nr_err:
                print(f"NR warning: {nr_err}")

        # Cadastros — query leve, independente do filtro de frente
        cadastros_count = 0
        try:
            cur.execute("""
                SELECT COUNT(*) AS n FROM public.entities
                WHERE created::date >= %(ini)s AND created::date <= %(fim)s
                  AND (deleted IS NULL OR deleted = TIMESTAMP '1970-01-01 00:00:00')
            """, {"ini": dt_ini, "fim": dt_fim})
            r = cur.fetchone()
            cadastros_count = int((r or {}).get('n', 0) or 0)
        except Exception as ce:
            print(f"Cadastros warning: {ce}")

        c.close()

        # Agrega tudo em RESUMO (soma de todos os dias) + DIÁRIO (lista por dia)
        kpis = {
            "depositos": 0, "qtd_depositos": 0, "apostas": 0,
            "ggr": 0, "ngr": 0, "recompensas": 0,
            "ggr_casino": 0, "ggr_sport": 0, "ggr_loteria": 0,
            "apo_casino": 0, "apo_sport": 0, "apo_loteria": 0,
            "jogadores_ativos": 0, "apostadores": 0, "ftd_count": 0,
        }
        diario = []
        all_jog = set()

        for r in rows:
            dep   = float(r.get('deposito') or 0)
            apo   = float(r.get('apostas') or 0)
            ggr_v = float(r.get('ggr') or 0)
            rec   = float(r.get('recompensas') or 0)
            qtd   = int(r.get('qtd_dep') or 0)
            ngr_v = float(r.get('ngr') or 0)
            jog   = int(r.get('jogadores') or 0)

            kpis["depositos"]    += dep
            kpis["qtd_depositos"] += qtd
            kpis["apostas"]      += apo
            kpis["ggr"]          += ggr_v
            kpis["ngr"]          += ngr_v
            kpis["recompensas"]  += rec
            kpis["ggr_casino"]   += float(r.get('ggr_casino') or 0)
            kpis["ggr_sport"]    += float(r.get('ggr_sport') or 0)
            kpis["ggr_loteria"]  += float(r.get('ggr_loteria') or 0)
            kpis["apo_casino"]   += float(r.get('apo_casino') or 0)
            kpis["apo_sport"]    += float(r.get('apo_sport') or 0)
            kpis["apo_loteria"]  += float(r.get('apo_loteria') or 0)
            kpis["jogadores_ativos"] += jog
            kpis["apostadores"]      += int(r.get('apostadores') or 0)
            kpis["ftd_count"]        += int(r.get('ftd_count') or 0)

            tur_dep = round(apo/dep, 2) if dep else 0
            ggr_dep = round(ggr_v/dep*100, 2) if dep else 0
            rec_ggr = round(rec/ggr_v*100, 1) if ggr_v else 0
            diario.append({
                "data": r['data'], "deposito": dep, "qtd_dep": qtd,
                "apostas": apo, "ggr": ggr_v, "ngr": ngr_v,
                "recompensas": rec, "tur_dep": tur_dep,
                "ggr_dep": ggr_dep, "rec_ggr": rec_ggr,
            })

        # Métricas derivadas
        dep_t = kpis["depositos"]; apo_t = kpis["apostas"]
        ggr_t = kpis["ggr"]; rec_t = kpis["recompensas"]
        qtd_t = kpis["qtd_depositos"] or 1; jog_t = kpis["jogadores_ativos"] or 1
        apo_t = kpis["apostas"]; apo_t = apo_t
        kpis["apo_total"]        = apo_t
        kpis["pct_ggr_dep"]      = round(ggr_t/dep_t*100, 2) if dep_t else 0
        kpis["pct_ggr_apo"]      = round(ggr_t/apo_t*100, 2) if apo_t else 0
        kpis["pct_recomp_ggr"]   = round(rec_t/ggr_t*100, 2) if ggr_t else 0
        kpis["ticket_dep"]       = round(dep_t/qtd_t, 2) if qtd_t else 0
        kpis["ticket_dep_jog"]   = round(dep_t/jog_t, 2) if jog_t else 0
        apos_reais = kpis.get("apostadores", 1) or 1
        kpis["tm_apostador"]     = round(apo_t/apos_reais, 2) if apos_reais else 0
        kpis["cadastros"]        = cadastros_count
        kpis["saques"]           = saques_total

        # Força consistência: totais da tabela NR devem ser idênticos aos KPI cards.
        # O CTE entity-level pode divergir do GROUP BY diário por acumulação de floats
        # ou por diferenças nos registros agrupados. O valor autoritativo é kpis[].
        tot_d_kpi = kpis.get("depositos", 0)
        tot_q_kpi = kpis.get("qtd_depositos", 0)
        tot_e_nr  = nr_data.get("total", {}).get("depositantes", 0)
        tot_ftd_nr = nr_data.get("total", {}).get("ftd", 0)
        tot_apo_nr = nr_data.get("total", {}).get("apostas", 0)
        tot_apos_nr = nr_data.get("total", {}).get("apostadores", 0)
        tot_freq_nr = nr_data.get("total", {}).get("frequencia", 0)
        nr_data["total"] = {
            "depositantes":  tot_e_nr,
            "ftd":           tot_ftd_nr,
            "depositos":     tot_d_kpi,
            "qtd_depositos": tot_q_kpi,
            "tm_deposito":   round(tot_d_kpi / tot_q_kpi, 2) if tot_q_kpi else 0,
            "tm_depositante": round(tot_d_kpi / tot_e_nr, 2) if tot_e_nr else 0,
            "frequencia":    tot_freq_nr,
            "ggr":           kpis.get("ggr", 0),
            "recompensas":   kpis.get("recompensas", 0),
            "apostas":       tot_apo_nr,
            "apostadores":   tot_apos_nr,
            "tm_apostador":  round(tot_apo_nr / tot_apos_nr, 2) if tot_apos_nr else 0,
        }

        # Coleta resultado do top_ggr (que rodou em paralelo)
        top_ggr_data = {"positivos": [], "negativos": []}
        try:
            top_ggr_data = clean(top_ggr_future.result(timeout=30))
        except Exception as tge:
            print(f"Top GGR warning: {tge}")

        result = clean({"kpis": kpis, "diario": diario, "nr": nr_data, "top_ggr": top_ggr_data})
        cache_set(cache_key, result)
        return jsonify({"ok": True, "data": result, "cache": False,
                        "periodo": {"ini": str(dt_ini), "fim": str(dt_fim)}})

    except Exception as e:
        top_ggr_future.cancel()
        tb = traceback.format_exc()
        print(f"\n❌ GERAL COMPLETO ERRO:\n{tb}")
        return jsonify({"ok": False, "error": str(e), "trace": tb}), 500


@app.route("/api/geral_diario")
def api_geral_diario():
    filtro     = request.args.get("data", "hoje")
    custom_ini = request.args.get("ini", "")
    custom_fim = request.args.get("fim", "")
    frente     = request.args.get("frente", "todas")
    btag       = request.args.get("btag", "").strip()
    afiliado   = request.args.get("afiliado", "").strip()
    dt_ini, dt_fim = periodo(filtro, custom_ini, custom_fim)

    frentes_lista = [f.strip() for f in frente.split(',') if f.strip() and f.strip() != 'todas'] if frente != 'todas' else []
    tem_filtro = bool(frentes_lista) or btag or afiliado

    cache_key = f"geral_diario4|{dt_ini}|{dt_fim}|{frente}|{btag}|{afiliado}"
    cached = cache_get(cache_key)
    if cached:
        return jsonify({"ok": True, "data": cached, "cache": True,
                        "periodo": {"ini": str(dt_ini), "fim": str(dt_fim)}})
    try:
        c = psycopg2.connect(**DB)
        cur = c.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        id_filter = ""
        params = {"ini": dt_ini, "fim": dt_fim}
        if tem_filtro:
            eids = fetch_filtered_entity_ids(cur, frentes_lista, btag, afiliado)
            if not eids:
                c.close()
                return jsonify({"ok": True, "data": [], "cache": False,
                                "periodo": {"ini": str(dt_ini), "fim": str(dt_fim)}})
            id_filter = "AND entity_id IN (SELECT UNNEST(%(ids)s::bigint[]))"
            params["ids"] = eids

        cur.execute(f"""
            WITH session_uap AS (
                SELECT dia, COUNT(DISTINCT entity_id) AS uap
                FROM (
                    SELECT entity_id, created::date AS dia
                    FROM integration.entity_sessions
                    WHERE created::date >= %(ini)s AND created::date <= %(fim)s
                    {id_filter}
                    UNION
                    SELECT entity_id, created::date AS dia
                    FROM public.vw_uw_balance
                    WHERE created >= %(ini)s AND created <= %(fim)s {id_filter}
                ) combined
                GROUP BY dia
            ),
            balance AS (
                SELECT
                    created::date                                                        AS dia,
                    COALESCE(SUM(deposits),0)::numeric(18,2)                            AS deposito,
                    COALESCE(SUM(deposits_qty),0)::int                                  AS qtd_dep,
                    COALESCE(SUM(COALESCE(games_casino,0)+COALESCE(games_sport,0)+COALESCE(games_prog,0)),0)::numeric(18,2) AS apostas,
                    COALESCE(SUM(ggr),0)::numeric(18,2)                                 AS ggr,
                    COALESCE(SUM(reward),0)::numeric(18,2)                              AS recompensas,
                    COALESCE(SUM(ngr),0)::numeric(18,2)                                 AS ngr,
                    COUNT(DISTINCT entity_id)                                           AS jogadores
                FROM public.vw_uw_balance
                WHERE created >= %(ini)s AND created <= %(fim)s {id_filter}
                GROUP BY created::date
            )
            SELECT
                to_char(b.dia, 'YYYY-MM-DD')   AS data,
                b.deposito, b.qtd_dep, b.apostas, b.ggr,
                b.recompensas, b.ngr, b.jogadores,
                COALESCE(s.uap, 0)             AS uap
            FROM balance b
            LEFT JOIN session_uap s ON s.dia = b.dia
            ORDER BY b.dia
        """, params)
        rows = [dict(r) for r in cur.fetchall()]
        c.close()
        result = clean(rows)
        cache_set(cache_key, result)
        return jsonify({"ok": True, "data": result, "cache": False,
                        "periodo": {"ini": str(dt_ini), "fim": str(dt_fim)}})
    except Exception as e:
        tb = traceback.format_exc()
        print(f"\n❌ GERAL DIARIO ERRO:\n{tb}")
        return jsonify({"ok": False, "error": str(e), "trace": tb}), 500


@app.route("/api/apostas_diario")
def api_apostas_diario():
    filtro     = request.args.get("data", "mes_ant")
    frente     = request.args.get("frente", "todas")
    btag_p     = request.args.get("btag", "").strip()
    afiliado_p = request.args.get("afiliado", "").strip()
    custom_ini = request.args.get("ini", "")
    custom_fim = request.args.get("fim", "")
    force      = request.args.get("force", "0") == "1"
    dt_ini, dt_fim = periodo(filtro, custom_ini, custom_fim)
    frentes_lista = [f.strip() for f in frente.split(',') if f.strip() and f.strip() != 'todas'] if frente != 'todas' else []
    tem_filtro = bool(frentes_lista) or btag_p or afiliado_p

    cache_key = f"apostas_diario|{dt_ini}|{dt_fim}|{frente}|{btag_p}|{afiliado_p}"
    cached = None if force else cache_get(cache_key)
    if cached:
        return jsonify({"ok": True, "data": cached, "cache": True,
                        "periodo": {"ini": str(dt_ini), "fim": str(dt_fim)}})
    try:
        c = psycopg2.connect(**DB)
        cur = c.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        bp = {"ini": dt_ini, "fim": dt_fim}

        # Filtro de entities — usando helper build_entity_filter (SQL correto)
        ges_sub = uwb_sub = sb_sub = lg_sub = ""
        if tem_filtro:
            ges_sub = build_entity_filter(frentes_lista, btag_p, afiliado_p, bp, "ges.entity_id")
            uwb_sub = build_entity_filter(frentes_lista, btag_p, afiliado_p, bp, "entity_id")
            sb_sub  = build_entity_filter(frentes_lista, btag_p, afiliado_p, bp, "entity_id")
            lg_sub  = build_entity_filter(frentes_lista, btag_p, afiliado_p, bp, "entity_id")

        # Cassino sub-categorias por dia
        cur.execute(f"""
            SELECT
                to_char(ges.created::date, 'YYYY-MM-DD') AS data,
                CASE
                    WHEN g.game_category_id IN (5,14,7,13)              THEN 'Crash'
                    WHEN g.game_category_id = 9                         THEN 'Slot'
                    WHEN g.game_category_id IN (1,11)                   THEN 'Bingo'
                    WHEN g.game_category_id IN (8,15,18,19,16,17,21,23) THEN 'Ao Vivo'
                    ELSE 'Outros'
                END AS categoria,
                SUM(ges.vl_jogo)::numeric(18,2) AS turnover,
                SUM(ges.ggr)::numeric(18,2)     AS ggr
            FROM integration.game_entity_sale_statistics ges
            JOIN integration.games g ON g.id = ges.game_id
            WHERE ges.created::date >= %(ini)s AND ges.created::date <= %(fim)s
              AND COALESCE(ges.is_test_account, false) = false
              {ges_sub}
            GROUP BY 1, 2
            ORDER BY 1
        """, bp)
        cas_rows = cur.fetchall()

        # Esporte: turnover de sport_bets, GGR da vw_uw_balance (correto)
        cur.execute(f"""
            SELECT to_char(created::date,'YYYY-MM-DD') AS data,
                   SUM(value)::numeric(18,2) AS turnover
            FROM integration.sport_bets
            WHERE created::date >= %(ini)s AND created::date <= %(fim)s {sb_sub}
            GROUP BY 1 ORDER BY 1
        """, bp)
        esp_turn = {r['data']: float(r['turnover'] or 0) for r in cur.fetchall()}

        # Loteria: turnover de lottery_games, GGR da vw_uw_balance (correto)
        cur.execute(f"""
            SELECT to_char(created::date,'YYYY-MM-DD') AS data,
                   SUM(value)::numeric(18,2) AS turnover
            FROM public.lottery_games
            WHERE created::date >= %(ini)s AND created::date <= %(fim)s {lg_sub}
            GROUP BY 1 ORDER BY 1
        """, bp)
        lot_turn = {r['data']: float(r['turnover'] or 0) for r in cur.fetchall()}

        # GGR correto por dia de esporte e loteria via vw_uw_balance
        cur.execute(f"""
            SELECT to_char(created,'YYYY-MM-DD') AS data,
                   COALESCE(SUM(ggr_sport),0)::numeric(18,2) AS ggr_esporte,
                   COALESCE(SUM(ggr_prog),0)::numeric(18,2)  AS ggr_loteria
            FROM public.vw_uw_balance
            WHERE created >= %(ini)s AND created <= %(fim)s {uwb_sub}
            GROUP BY 1 ORDER BY 1
        """, bp)
        ggr_rows = {r['data']: r for r in cur.fetchall()}

        c.close()

        # Organizar por data
        by_date = defaultdict(lambda: {
            'Crash':{'t':0,'g':0}, 'Slot':{'t':0,'g':0},
            'Bingo':{'t':0,'g':0}, 'Ao Vivo':{'t':0,'g':0},
            'Outros':{'t':0,'g':0}, 'Esporte':{'t':0,'g':0},
            'Loteria':{'t':0,'g':0}
        })

        for r in cas_rows:
            d = str(r['data'])
            by_date[d][r['categoria']]['t'] += float(r['turnover'] or 0)
            by_date[d][r['categoria']]['g'] += float(r['ggr'] or 0)

        # Junta todos os dias encontrados
        all_dates = set(by_date.keys()) | set(esp_turn.keys()) | set(lot_turn.keys()) | set(ggr_rows.keys())
        for d in all_dates:
            by_date[d]['Esporte']['t'] = esp_turn.get(d, 0)
            by_date[d]['Esporte']['g'] = float(ggr_rows.get(d, {}).get('ggr_esporte', 0) or 0)
            by_date[d]['Loteria']['t'] = lot_turn.get(d, 0)
            by_date[d]['Loteria']['g'] = float(ggr_rows.get(d, {}).get('ggr_loteria', 0) or 0)

        dias = []
        for data_str in sorted(by_date.keys()):
            d = by_date[data_str]
            tot_t = sum(v['t'] for v in d.values())
            tot_g = sum(v['g'] for v in d.values())
            hold = round(tot_g / tot_t * 100, 2) if tot_t else 0
            dias.append({
                "data": data_str,
                "crash":   d['Crash'],
                "slot":    d['Slot'],
                "bingo":   d['Bingo'],
                "ao_vivo": d['Ao Vivo'],
                "outros":  d['Outros'],
                "esporte": d['Esporte'],
                "loteria": d['Loteria'],
                "total":   {"t": tot_t, "g": tot_g, "hold": hold}
            })

        result = clean(dias)
        cache_set(cache_key, result)
        return jsonify({"ok": True, "data": result, "cache": False,
                        "periodo": {"ini": str(dt_ini), "fim": str(dt_fim)}})
    except Exception as e:
        tb = traceback.format_exc()
        print(f"\n❌ APOSTAS DIARIO ERRO:\n{tb}")
        return jsonify({"ok": False, "error": str(e), "trace": tb}), 500


@app.route("/api/apostas")
def api_apostas():
    filtro     = request.args.get("data", "mes_ant")
    frente     = request.args.get("frente", "todas")
    btag_p     = request.args.get("btag", "").strip()
    afiliado_p = request.args.get("afiliado", "").strip()
    custom_ini = request.args.get("ini", "")
    custom_fim = request.args.get("fim", "")
    force      = request.args.get("force", "0") == "1"

    dt_ini, dt_fim = periodo(filtro, custom_ini, custom_fim)
    frentes_lista = [f.strip() for f in frente.split(',') if f.strip() and f.strip() != 'todas'] if frente != 'todas' else []
    tem_filtro = bool(frentes_lista) or btag_p or afiliado_p

    # Período anterior para % retenção
    delta = dt_fim - dt_ini
    dt_ant_ini = dt_ini - (delta + timedelta(days=1))
    dt_ant_fim = dt_ini - timedelta(days=1)

    cache_key = f"apostas2|{dt_ini}|{dt_fim}|{frente}|{btag_p}|{afiliado_p}"
    cached = None if force else cache_get(cache_key)
    if cached:
        return jsonify({"ok": True, "data": cached, "cache": True,
                        "periodo": {"ini": str(dt_ini), "fim": str(dt_fim)}})

    try:
        c = psycopg2.connect(**DB)
        cur = c.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        base_p = {"ini": dt_ini, "fim": dt_fim}
        ant_p  = {"ini": dt_ant_ini, "fim": dt_ant_fim}

        CAT_IDS = [9, 5, 14, 7, 13, 8, 15, 18, 19, 16, 17, 21, 23, 1, 11]
        CAT_MAP = {9:'Slot', 5:'Crash', 14:'Crash', 7:'Crash', 13:'Crash',
                   8:'Ao Vivo', 15:'Ao Vivo', 18:'Ao Vivo', 19:'Ao Vivo',
                   16:'Ao Vivo', 17:'Ao Vivo', 21:'Ao Vivo', 23:'Ao Vivo',
                   1:'Bingo', 11:'Bingo'}

        # Filtro de entities — usando helper build_entity_filter (SQL correto)
        entity_sub_uwb = entity_sub_ges = entity_sub_sb = entity_sub_lg = ""
        if tem_filtro:
            entity_sub_uwb = build_entity_filter(frentes_lista, btag_p, afiliado_p, base_p, "entity_id")
            entity_sub_ges = build_entity_filter(frentes_lista, btag_p, afiliado_p, base_p, "ges.entity_id")
            entity_sub_sb  = build_entity_filter(frentes_lista, btag_p, afiliado_p, base_p, "entity_id")
            entity_sub_lg  = build_entity_filter(frentes_lista, btag_p, afiliado_p, base_p, "entity_id")

        # Novos no período (FTD)
        cur.execute(f"""
            SELECT DISTINCT entity_id FROM public.vw_uw_balance
            WHERE created >= %(ini)s AND created <= %(fim)s AND ftd_value > 0 {entity_sub_uwb}
        """, base_p)
        novos_ids = set(r['entity_id'] for r in cur.fetchall())

        def agg(rows, id_field='entity_id'):
            n = {"apo": 0, "ggr": 0, "ids": set()}
            r2 = {"apo": 0, "ggr": 0, "ids": set()}
            for row in rows:
                eid = row[id_field]
                apo = float(row.get('apostado') or 0)
                ggr = float(row.get('ggr') or 0)
                if eid in novos_ids:
                    n["apo"] += apo; n["ggr"] += ggr; n["ids"].add(eid)
                else:
                    r2["apo"] += apo; r2["ggr"] += ggr; r2["ids"].add(eid)
            def mk(d):
                cnt = len(d["ids"]) or 1
                return {"apostado": d["apo"], "ggr": d["ggr"],
                        "apostadores": len(d["ids"]),
                        "tm_aposta": d["apo"]/cnt, "tm_ggr": d["ggr"]/cnt}
            nov = mk(n); rec = mk(r2)
            tot_apo = nov["apostado"] + rec["apostado"]
            tot_ggr = nov["ggr"] + rec["ggr"]
            tot_cnt = (nov["apostadores"] + rec["apostadores"]) or 1
            tot = {"apostado": tot_apo, "ggr": tot_ggr,
                   "apostadores": nov["apostadores"] + rec["apostadores"],
                   "tm_aposta": tot_apo/tot_cnt, "tm_ggr": tot_ggr/tot_cnt}
            return nov, rec, tot

        # Cassino sub-categorias
        cur.execute(f"""
            SELECT ges.entity_id, g.game_category_id,
                   SUM(ges.vl_jogo)::numeric(18,2) AS apostado,
                   SUM(ges.ggr)::numeric(18,2) AS ggr
            FROM integration.game_entity_sale_statistics ges
            JOIN integration.games g ON g.id = ges.game_id
            WHERE ges.created::date >= %(ini)s AND ges.created::date <= %(fim)s
              AND g.game_category_id = ANY(%(cats)s)
              AND COALESCE(ges.is_test_account, false) = false
              {entity_sub_ges}
            GROUP BY ges.entity_id, g.game_category_id
        """, {**base_p, "cats": CAT_IDS})
        cas_rows = cur.fetchall()

        from collections import defaultdict
        by_cat = defaultdict(list)
        for r in cas_rows:
            nome = CAT_MAP.get(r['game_category_id'], 'Outros')
            by_cat[nome].append(r)

        subs = []
        cas_n_tot = {"apo": 0, "ggr": 0, "ids": set()}
        cas_r_tot = {"apo": 0, "ggr": 0, "ids": set()}
        for nome in ['Crash', 'Slot', 'Ao Vivo', 'Bingo']:
            n, r2, t = agg(by_cat.get(nome, []))
            subs.append({"nome": nome, "novos": n, "recorrentes": r2, "total": t})
            for eid in by_cat.get(nome, []):
                if eid['entity_id'] in novos_ids:
                    cas_n_tot["apo"] += float(eid.get('apostado') or 0)
                    cas_n_tot["ggr"] += float(eid.get('ggr') or 0)
                    cas_n_tot["ids"].add(eid['entity_id'])
                else:
                    cas_r_tot["apo"] += float(eid.get('apostado') or 0)
                    cas_r_tot["ggr"] += float(eid.get('ggr') or 0)
                    cas_r_tot["ids"].add(eid['entity_id'])

        # Outros cassino
        cur.execute(f"""
            SELECT ges.entity_id,
                   SUM(ges.vl_jogo)::numeric(18,2) AS apostado,
                   SUM(ges.ggr)::numeric(18,2) AS ggr
            FROM integration.game_entity_sale_statistics ges
            JOIN integration.games g ON g.id = ges.game_id
            WHERE ges.created::date >= %(ini)s AND ges.created::date <= %(fim)s
              AND g.game_category_id != ALL(%(cats)s)
              AND COALESCE(ges.is_test_account, false) = false
              {entity_sub_ges}
            GROUP BY ges.entity_id
        """, {**base_p, "cats": CAT_IDS})
        outros_rows = cur.fetchall()
        n_out, r_out, t_out = agg(outros_rows)
        subs.append({"nome": "Outros", "novos": n_out, "recorrentes": r_out, "total": t_out})

        # Rebuild cassino totals from all rows
        all_cas_rows = list(cas_rows) + list(outros_rows)
        n_cas, r_cas, t_cas = agg(all_cas_rows)

        # Esporte — turnover de sport_bets, GGR correto de vw_uw_balance
        cur.execute(f"""
            SELECT entity_id, SUM(value)::numeric(18,2) AS apostado
            FROM integration.sport_bets
            WHERE created::date >= %(ini)s AND created::date <= %(fim)s {entity_sub_sb}
            GROUP BY entity_id
        """, base_p)
        esp_turn = {r['entity_id']: float(r['apostado'] or 0) for r in cur.fetchall()}

        cur.execute(f"""
            SELECT entity_id,
                   SUM(ggr_sport)::numeric(18,2) AS ggr
            FROM public.vw_uw_balance
            WHERE created >= %(ini)s AND created <= %(fim)s {entity_sub_uwb}
              AND ggr_sport != 0
            GROUP BY entity_id
        """, base_p)
        esp_ggr = {r['entity_id']: float(r['ggr'] or 0) for r in cur.fetchall()}

        all_esp_ids = set(esp_turn.keys()) | set(esp_ggr.keys())
        esp_rows = [{"entity_id": eid, "apostado": esp_turn.get(eid,0), "ggr": esp_ggr.get(eid,0)} for eid in all_esp_ids]
        n_esp, r_esp, t_esp = agg(esp_rows)

        # Loteria — turnover de lottery_games, GGR correto de vw_uw_balance
        cur.execute(f"""
            WITH ap AS (SELECT entity_id, SUM(value) AS apo FROM public.lottery_games
                        WHERE created::date >= %(ini)s AND created::date <= %(fim)s {entity_sub_lg} GROUP BY entity_id)
            SELECT entity_id, apo::numeric(18,2) AS apostado FROM ap
        """, base_p)
        lot_turn = {r['entity_id']: float(r['apostado'] or 0) for r in cur.fetchall()}

        cur.execute(f"""
            SELECT entity_id,
                   SUM(ggr_prog)::numeric(18,2) AS ggr
            FROM public.vw_uw_balance
            WHERE created >= %(ini)s AND created <= %(fim)s {entity_sub_uwb}
              AND ggr_prog != 0
            GROUP BY entity_id
        """, base_p)
        lot_ggr = {r['entity_id']: float(r['ggr'] or 0) for r in cur.fetchall()}

        all_lot_ids = set(lot_turn.keys()) | set(lot_ggr.keys())
        lot_rows = [{"entity_id": eid, "apostado": lot_turn.get(eid,0), "ggr": lot_ggr.get(eid,0)} for eid in all_lot_ids]
        n_lot, r_lot, t_lot = agg(lot_rows)

        # % retenção mês anterior
        cur.execute("""
            SELECT COUNT(DISTINCT ges.entity_id) AS n
            FROM integration.game_entity_sale_statistics ges
            JOIN integration.games g ON g.id = ges.game_id
            WHERE ges.created::date >= %(ini)s AND ges.created::date <= %(fim)s
              AND COALESCE(ges.is_test_account, false) = false
        """, ant_p)
        ant_cas = (cur.fetchone() or {}).get('n', 0) or 1

        cur.execute("SELECT COUNT(DISTINCT entity_id) AS n FROM integration.sport_bets WHERE created::date >= %(ini)s AND created::date <= %(fim)s", ant_p)
        ant_esp = (cur.fetchone() or {}).get('n', 0) or 1

        cur.execute("SELECT COUNT(DISTINCT entity_id) AS n FROM public.lottery_games WHERE created::date >= %(ini)s AND created::date <= %(fim)s", ant_p)
        ant_lot = (cur.fetchone() or {}).get('n', 0) or 1

        c.close()

        categorias = [
            {"nome": "Cassino", "icon": "🎰", "subs": subs,
             "novos": n_cas, "recorrentes": {**r_cas, "pct_ret": round(r_cas["apostadores"]/ant_cas*100,1)},
             "total": t_cas},
            {"nome": "Esporte", "icon": "⚽", "subs": [],
             "novos": n_esp, "recorrentes": {**r_esp, "pct_ret": round(r_esp["apostadores"]/ant_esp*100,1)},
             "total": t_esp},
            {"nome": "Loteria", "icon": "🎟️", "subs": [],
             "novos": n_lot, "recorrentes": {**r_lot, "pct_ret": round(r_lot["apostadores"]/ant_lot*100,1)},
             "total": t_lot},
        ]

        def tot_sum(field):
            return sum(c[field].get("apostado",0) for c in categorias), \
                   sum(c[field].get("ggr",0) for c in categorias), \
                   sum(c[field].get("apostadores",0) for c in categorias)

        def mk_tot(field):
            a, g, n2 = tot_sum(field); n2 = n2 or 1
            return {"apostado":a, "ggr":g, "apostadores":n2, "tm_aposta":a/n2, "tm_ggr":g/n2}

        result = clean({
            "categorias": categorias,
            "totais_novos": mk_tot("novos"),
            "totais_rec": mk_tot("recorrentes"),
            "totais": mk_tot("total"),
        })
        cache_set(cache_key, result)
        return jsonify({"ok": True, "data": result, "cache": False,
                        "periodo": {"ini": str(dt_ini), "fim": str(dt_fim)}})

    except Exception as e:
        tb = traceback.format_exc()
        print(f"\n❌ APOSTAS ERRO:\n{tb}")
        return jsonify({"ok": False, "error": str(e), "trace": tb}), 500


@app.route("/api/filtros")
def api_filtros():
    """Retorna btags e afiliados organizados por frente para os filtros cascateados."""
    try:
        sql = """
        SELECT
            CASE
                WHEN TRIM(c.tag) ILIKE '000004_DA'  THEN 'App'
                WHEN TRIM(c.tag) ILIKE '000004_%%'  THEN 'Tráfego'
                WHEN TRIM(c.tag) ILIKE '000007_%%'  THEN 'Tráfego'
                WHEN TRIM(c.tag) ILIKE '000006_e%%' THEN 'Tráfego'
                WHEN TRIM(c.tag) ILIKE '000006_%%'  THEN 'Mídias'
                WHEN TRIM(c.tag) ILIKE '000002_%%'  THEN 'Resultado Fácil'
                WHEN TRIM(c.tag) ILIKE '000003_%%'  THEN 'Resultado Fácil'
                WHEN TRIM(c.tag) ILIKE '000167_%%'  THEN 'Resultado Fácil'
                ELSE 'Afiliados'
            END AS frente,
            TRIM(c.tag) AS btag,
            COALESCE(
                NULLIF(e.json_data->>'name',''),
                NULLIF(e.json_data->>'fullName',''),
                NULLIF(e.json_data->>'fullname',''),
                'Sem nome'
            ) AS nome_afiliado
        FROM affiliates.campaigns c
        LEFT JOIN affiliates.affiliates a ON a.id = c.affiliate_id
        LEFT JOIN public.entities e ON e.id = a.entity_id
        WHERE c.tag IS NOT NULL AND c.tag != ''
        ORDER BY frente, nome_afiliado, btag
        """
        conn = psycopg2.connect(**DB)
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(sql)
        rows = cur.fetchall()
        conn.close()

        result = {}
        for row in rows:
            f = row['frente']
            if f not in result:
                result[f] = {'btags': [], 'afiliados': set()}
            if row['btag'] not in result[f]['btags']:
                result[f]['btags'].append(row['btag'])
            result[f]['afiliados'].add(row['nome_afiliado'])

        # Converter sets para listas ordenadas
        for f in result:
            result[f]['afiliados'] = sorted(list(result[f]['afiliados']))
            result[f]['btags'] = sorted(result[f]['btags'])

        return jsonify({"ok": True, "data": result})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route("/")
def index():
    return send_from_directory(FRONT_DIR, "dashboard.html")

@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(FRONT_DIR, filename)

@app.route("/api/funil_cadastro")
def api_funil_cadastro():
    filtro     = request.args.get("data", "mes")
    custom_ini = request.args.get("ini", "")
    custom_fim = request.args.get("fim", "")
    frente     = request.args.get("frente", "").strip()
    btag       = request.args.get("btag", "").strip()
    afiliado   = request.args.get("afiliado", "").strip()
    force      = request.args.get("force", "0") == "1"

    dt_ini, dt_fim = periodo(filtro, custom_ini, custom_fim)
    cache_key = f"funil_cad2|{dt_ini}|{dt_fim}|{frente}|{btag}|{afiliado}"
    cached = None if force else cache_get(cache_key)
    if cached:
        return jsonify({"ok": True, "data": cached, "cache": True,
                        "periodo": {"ini": str(dt_ini), "fim": str(dt_fim)}})
    try:
        c = psycopg2.connect(**DB)
        cur = c.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        params = {"ini": dt_ini, "fim": dt_fim}

        frentes_lista = [f.strip() for f in frente.split(',') if f.strip() and f.strip() != 'todas'] if frente else []
        frente_filter = ""
        if frentes_lista or btag or afiliado:
            eids = fetch_filtered_entity_ids(cur, frentes_lista, btag, afiliado)
            if eids is not None:
                params["cad_eids"] = eids
                frente_filter = "AND id IN (SELECT UNNEST(%(cad_eids)s::bigint[]))"

        # depositante = converteu no mesmo dia do cadastro (FTD no mesmo dia)
        # Isso evita que dados históricos melhorem com o tempo por conversões futuras
        cur.execute(f"""
            WITH same_day_ftd AS (
                SELECT DISTINCT e.id
                FROM public.entities e
                JOIN public.vw_uw_balance v
                  ON v.entity_id = e.id
                 AND v.ftd_value > 0
                 AND v.created::date = e.created::date
                WHERE e.entity_type_id = 6
                  AND e.created::date >= %(ini)s
                  AND e.created::date <= %(fim)s
                  {frente_filter}
            )
            SELECT
                created::date                                                                     AS dia,
                COUNT(*)                                                                          AS pre_cadastros,
                COUNT(*) FILTER (WHERE json_data->>'dddPhone' IS NOT NULL)                       AS tel_preenchido,
                COUNT(*) FILTER (WHERE json_flags->>'isValidatedPhone' = 'true')                 AS tel_verificado,
                COUNT(*) FILTER (WHERE json_data->>'email' IS NOT NULL
                                   AND json_data->>'email' != '')                                AS email_preenchido,
                COUNT(*) FILTER (WHERE json_flags->>'isValidatedEmail' = 'true')                 AS cadastrado,
                COUNT(*) FILTER (WHERE json_flags->>'registerFace' IS NOT NULL
                                    OR json_flags->>'registerFaceSerasaex' IS NOT NULL)          AS verificado,
                COUNT(*) FILTER (WHERE id IN (SELECT id FROM same_day_ftd))                      AS depositante
            FROM public.entities
            WHERE entity_type_id = 6
              AND created::date >= %(ini)s
              AND created::date <= %(fim)s
              {frente_filter}
            GROUP BY created::date
            ORDER BY created::date
        """, params)
        rows = cur.fetchall()
        c.close()

        dias = {}
        totals = {k: 0 for k in ("pre_cadastros","tel_preenchido","tel_verificado",
                                   "email_preenchido","cadastrado","verificado","depositante")}
        for r in rows:
            key = str(r["dia"])
            entry = {
                "pre_cadastros":    int(r["pre_cadastros"]    or 0),
                "tel_preenchido":   int(r["tel_preenchido"]   or 0),
                "tel_verificado":   int(r["tel_verificado"]   or 0),
                "email_preenchido": int(r["email_preenchido"] or 0),
                "cadastrado":       int(r["cadastrado"]       or 0),
                "verificado":       int(r["verificado"]       or 0),
                "depositante":      int(r["depositante"]      or 0),
            }
            dias[key] = entry
            for k in totals:
                totals[k] += entry[k]

        result = clean({"dias": dias, "total": totals})
        cache_set(cache_key, result)
        return jsonify({"ok": True, "data": result, "cache": False,
                        "periodo": {"ini": str(dt_ini), "fim": str(dt_fim)}})
    except Exception as e:
        tb = traceback.format_exc()
        print(f"\n❌ FUNIL CADASTRO ERRO:\n{tb}")
        return jsonify({"ok": False, "error": str(e), "trace": tb}), 500

@app.route('/api/funil_aquisicao')
def api_funil_aquisicao():
    """Funil FTD → REC: quantos jogadores com FTD no período chegaram ao 2°, 3°... 7°+ depósito."""
    filtro     = request.args.get('data', 'mes')
    custom_ini = request.args.get('ini', '')
    custom_fim = request.args.get('fim', '')
    frentes_param = request.args.get('frentes', request.args.get('frente', ''))
    btag      = request.args.get('btag', '').strip()
    afiliado  = request.args.get('afiliado', '').strip()
    force = request.args.get('force', '0') == '1'
    dt_ini, dt_fim = periodo(filtro, custom_ini, custom_fim)
    ini, fim = str(dt_ini), str(dt_fim)
    frente_list = [f.strip() for f in frentes_param.split(',') if f.strip() and f.strip() != 'todas'] if frentes_param else []

    cache_key = f"funil_aq3|{ini}|{fim}|{frentes_param}|{btag}|{afiliado}"
    cached = None if force else cache_get(cache_key)
    if cached:
        return jsonify({"ok": True, "data": cached, "cache": True,
                        "periodo": {"ini": ini, "fim": fim}})

    id_filter = ""
    params = {"ini": ini, "fim": fim}
    if frente_list or btag or afiliado:
        try:
            c_tmp = psycopg2.connect(**DB)
            cur_tmp = c_tmp.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            eids = fetch_filtered_entity_ids(cur_tmp, frente_list, btag, afiliado)
            c_tmp.close()
        except Exception:
            eids = None
        if eids is not None:
            if not eids:
                result = {"ftd": 0, "d2": 0, "d3": 0, "d4": 0, "d5": 0, "d6": 0, "rec": 0}
                cache_set(cache_key, result)
                return jsonify({"ok": True, "data": result, "cache": False,
                                "periodo": {"ini": ini, "fim": fim}})
            params["eids"] = eids
            id_filter = "AND v.entity_id IN (SELECT UNNEST(%(eids)s::bigint[]))"

    try:
        c = psycopg2.connect(**DB)
        cur = c.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cur.execute(f"""
            WITH new_players AS (
                SELECT DISTINCT v.entity_id
                FROM public.vw_uw_balance v
                WHERE v.ftd_value > 0
                  AND v.created BETWEEN %(ini)s AND %(fim)s
                  {id_filter}
            ),
            player_deps AS (
                SELECT np.entity_id, COALESCE(SUM(v.deposits_qty), 0) AS total_deps
                FROM new_players np
                JOIN public.vw_uw_balance v ON v.entity_id = np.entity_id
                WHERE v.created BETWEEN %(ini)s AND %(fim)s
                GROUP BY np.entity_id
            )
            SELECT
                COUNT(*) FILTER (WHERE total_deps >= 1) AS d1,
                COUNT(*) FILTER (WHERE total_deps >= 2) AS d2,
                COUNT(*) FILTER (WHERE total_deps >= 3) AS d3,
                COUNT(*) FILTER (WHERE total_deps >= 4) AS d4,
                COUNT(*) FILTER (WHERE total_deps >= 5) AS d5,
                COUNT(*) FILTER (WHERE total_deps >= 6) AS d6,
                COUNT(*) FILTER (WHERE total_deps >= 7) AS d7
            FROM player_deps
        """, params)
        r = cur.fetchone() or {}
        c.close()
    except Exception as ex:
        tb = traceback.format_exc()
        print(f"\n❌ FUNIL AQUISICAO ERRO:\n{tb}")
        return jsonify({"ok": False, "error": str(ex), "trace": tb}), 500

    result = {
        "ftd": int(r.get('d1') or 0),
        "d2":  int(r.get('d2') or 0),
        "d3":  int(r.get('d3') or 0),
        "d4":  int(r.get('d4') or 0),
        "d5":  int(r.get('d5') or 0),
        "d6":  int(r.get('d6') or 0),
        "rec": int(r.get('d7') or 0),
    }
    cache_set(cache_key, result)
    return jsonify({"ok": True, "data": result, "cache": False,
                    "periodo": {"ini": ini, "fim": fim}})

# ── FUNIL DE AQUISIÇÃO — jornada granular por eventos (dwh.player_events) ──
# Migrado em 28/08/2026: a fonte era entities.json_flags.cadastroProgresso (instrumentado
# em 05/08/2026), que sobrescrevia timestamp por chave e não tinha dispositivo por passo
# (ver task ClickUp 868kv6jk6 — "Migrar a telemetria do cadastro para eventos"). Desde o
# go-live de 26/08/2026, cada passo é um evento append-only em dwh.player_events
# (`json_data->>'registrationId'` como pessoa — vale antes mesmo de existir entity_id,
# cobrindo topo de funil que a fonte antiga não via). A ordem/fase oficial dos passos vem
# do catálogo versionado dwh.registration_steps (funnel_version vigente).
#
# ⚠️ REVISÃO DE 02/09/2026 — o funil por eventos divergia 4x do Funil de Cadastro
# (flags de estado) da aba Geral: 1.700 contas criadas contra 336 entidades no mesmo dia.
# Três defeitos foram corrigidos aqui; ler antes de mexer:
#
# 1. `registration_completed` (RGC) NÃO é conclusão de cadastro e foi REMOVIDO do funil.
#    O fluxo de revalidação de liveness no login reaproveita a instrumentação do cadastro,
#    então dispara signup_started/kyc_*/registration_completed para conta antiga que está
#    só entrando. 96% dos disparos vinham de conta preexistente (mediana de 195 dias de
#    idade). Mesmo depois do filtro de coorte abaixo, o RGC limpo fica em ~19% do
#    account_created — erra nos dois sentidos. O marco de conclusão é `account_created`
#    (ACC), que fecha 97,5–99,0% com public.entities em todos os dias medidos.
#
# 2. `pe.created` é data de INGESTÃO, não de ocorrência. 41% do volume que chega num dia
#    ocorreu antes (p90 de atraso: 3,4 dias; máximo observado: 6d04h). O recorte agora usa
#    OCC_DATE_SQL. Cuidado com o fuso: `created` está em horário de Brasília e `occurredAt`
#    em UTC (confirmado — `created` é `timestamp without time zone` e o cluster roda com
#    timezone `UTC+3`, que em sintaxe POSIX significa UTC−03:00). Usar
#    `(occurredAt)::timestamp` sem o AT TIME ZONE joga o evento 3h para trás e realoca
#    16–19% dos eventos para o dia errado.
#
# 3. Sem filtro de coorte, o topo do funil vinha inflado ~27% pela revalidação de login.
#    JORNADA_COORTE_SQL mantém quem ainda não tem entidade (tráfego anônimo, abandono
#    legítimo) e quem tem entidade nascida no MESMO dia de ocorrência do evento.
#
# ⚠️ O funil NÃO é monotônico, e isso é instrumentação incompleta, não fricção. Em
# 29/08/2026: account_created = 946, mas email.submitted = 509, consent.submitted = 267 e
# kyc.provider_handoff_completed = 219. Não se cria conta sem passar por esses gates, logo
# eles estão sub-instrumentados. A leitura antiga era high-water-mark (`maior >= n`), o que
# forçava o funil a descer e ESCONDIA o problema: exibia 2.182 pessoas em "Endereço
# concluído" quando só 33 emitiram o evento. Agora `pessoas` é contagem real de emissores
# e cada passo carrega `cobertura_pct` + `instrumentacao_parcial`; conversão só é calculada
# entre marcos confiáveis (ver _jornada_marcos_confiaveis). A cadeia que fecha hoje é
# signup_started (3.971) → phone.submitted (899) → account_created (946): ~23% de quem
# começa cria conta, e a perda real está no passo do telefone.
#
# ⚠️ Só existem dados desde 26/08/2026 (dia parcial e quebrado — SST/SPV começaram às
# 14:11 e o resto às 16:28). Primeiro dia inteiro utilizável: 27/08/2026. Períodos de
# 30d/90d vão mostrar série truncada.
# ⚠️ Os últimos ~3 dias são provisórios: D0 captura só ~83% dos eventos client-side e
# amadurece por 3 dias. O número de ontem ainda vai subir.
# ⚠️ Não confundir com o Funil de Cadastro (flags de estado) da aba Geral, nem com o bloco
# de KYC legado (kyc_link_generated/kyc_result_received) — populações diferentes.
# ⚠️ Eventos legacy (PV, LOG, KYC, STAV...) não têm occurredAt nem registrationId. Não
# misturar com a família instrumentada: não existe expressão de data única para as duas.

REGISTRATION_EXTRA_STEPS = [
    # (step_order, step_code, fase, is_gate, rotulo) — fora de dwh.registration_steps.
    # `registration_completed` foi removido de propósito (ver item 1 do bloco acima).
    (-0.50, 'signup_started',  'signup',    False, 'Cadastro iniciado'),
    (19.50, 'account_created', 'conclusao', True,  'Cadastro concluído (conta criada)'),
]

# Passo cujo volume serve de referência de cobertura para os demais: é o único marco que
# reconcilia com public.entities, então "quantas das contas criadas passaram por X" é a
# medida honesta de instrumentação de X.
STEP_REFERENCIA = 'account_created'

# Topo do funil: denominador de `pct_do_topo`.
#
# ⚠️ Não use "pessoas com qualquer evento do catálogo" como denominador — era o que a aba
# fazia e contaminava toda porcentagem. Em 29/08/2026 essa coorte crua dava 4.721 pessoas,
# mas 750 delas nunca emitiram signup_started: 705 entraram na conta só por
# `kyc.camera_granted` e 156 por `kyc.camera_denied` (eventos de câmera aparecem em fluxo
# que não é cadastro novo). Resultado: a conversão até conta criada aparecia como
# 946/4.721 = 20,0% quando contra o topo real é 946/3.971 = 23,8%.
STEP_TOPO = 'signup_started'

# Passos que existem no catálogo mas estão fora do funil por instrumentação morta —
# manter um passo com volume irrelevante como primeira etapa produz uma linha de barra
# zerada no topo da lista e não informa nada.
# `visit.site_entered`: 4 pessoas em 29/08/2026 contra 3.971 de signup_started. Foi o que
# o PM apontou como "não faz sentido". Removê-lo, sozinho, mexe pouco no número
# (20,0% → 20,1%); o que corrigiu a porcentagem foi o STEP_TOPO acima.
PASSOS_FORA_DO_FUNIL = {'visit.site_entered'}

# Gate anterior ao ACC com QUALQUER déficit de volume contra o ACC está sub-instrumentado.
#
# ⚠️ Havia uma folga de 10% aqui e ela produziu um número impossível. Em 29/08/2026
# "Telefone enviado" tinha 899 contra 946 contas criadas (95,0%), passou pela folga e virou
# marco confiável — e o painel publicou "3.072 pessoas perdidas no telefone" quando a perda
# TOTAL do funil era 3.971 − 946 = 3.025. O excedente de 47 é exatamente 946 − 899, a
# subcontagem do próprio evento. Um passo não pode perder mais gente do que o funil inteiro.
#
# A regra é exata porque o déficit não é ruído: 899 < 946 significa que ao menos 47 contas
# nasceram sem o evento, logo 899 é **piso**, não nível — e a diferença contra o topo
# superestima a perda em exatamente a subcontagem. Sem tolerância, sem exceção.
COBERTURA_MIN_GATE = 1.0

# ⚠️ `cobertura_pct` é medida sobre quem CONCLUIU (pessoas do passo ÷ contas criadas). Ela
# responde "esse evento dispara para quem termina?" — e não diz nada sobre quem abandonou.
# O padrão de subemissão que gera esses números (evento no 200 do servidor, ou na navegação
# para a próxima tela) é justamente o que dispara para o concluinte e silencia no
# abandonador. Ou seja: a subemissão está correlacionada com o desfecho que o funil tenta
# medir, e cobertura alta NÃO é atestado de que o passo mede perda corretamente.
COBERTURA_CONDICIONADA_A_CONCLUINTES = True

# Data/hora de OCORRÊNCIA do evento em horário de Brasília (ver item 2 do bloco acima).
OCC_TS_SQL   = "((pe.json_data->>'occurredAt')::timestamptz AT TIME ZONE 'America/Sao_Paulo')"
OCC_DATE_SQL = f"({OCC_TS_SQL})::date"

# Coorte sem revalidação de login: quem ainda não tem entidade, ou cuja entidade nasceu no
# mesmo dia do evento. O critério é por DIA (e não ">= início da janela") porque o segundo
# degrada conforme a janela cresce — num recorte de 30 dias deixava passar 287 RGC de conta
# antiga contra 144 no critério diário.
JORNADA_COORTE_SQL = f"(pe.entity_id IS NULL OR e.created::date = {OCC_DATE_SQL})"

# Prefiltro por data de ingestão, só para o índice (player_event_type_id, created) poder
# ser usado — a tabela tem 362M linhas / 207 GB e não há índice em json_data.
# A janela se estende para FRENTE do fim do período: o evento chega DEPOIS de ocorrer.
# +8d cobre o atraso máximo observado (6d04h) com folga; -1d cobre clock skew negativo de
# cliente (máximo observado: -1h).
INGEST_LOOKBACK  = timedelta(days=1)
INGEST_LOOKAHEAD = timedelta(days=8)

def _registration_steps_catalog(cur):
    """Catálogo oficial de passos (dwh.registration_steps, versão vigente) + os
    eventos-bookend acima, cada um resolvido para o seu player_event_type_id.
    Cacheado 1x/dia — o catálogo é versionado e não muda no dia a dia.

    Retorna [(n, step_code, type_id, fase, is_gate, rotulo_numerado), ...] ordenado.

    O filtro tem de ser por `player_event_type_id`, não por `detail`: só o primeiro é
    indexado — a mesma agregação de 3 dias levou 14,7s por `detail` e 2,3s por type_id.
    O vínculo é `dwh.player_event_types.name = step_code`.

    is_gate marca conversão oficial; False é telemetria de UX dentro da fase — é normal um
    passo opcional (reenvio, troca de destino) ter volume baixo sem significar perda."""
    cache_key = f"reg_steps_catalog_v5|{date.today()}"
    cached = cache_get(cache_key)
    if cached:
        return [tuple(s) for s in cached["steps"]]
    cur.execute("""
        SELECT s.step_order, s.step_code, s.phase, s.is_gate, s.description, t.id AS type_id
        FROM dwh.registration_steps s
        LEFT JOIN dwh.player_event_types t ON t.name = s.step_code
        WHERE s.valid_to IS NULL
        ORDER BY s.step_order
    """)
    rows = [(float(r["step_order"]), r["step_code"], r["type_id"], r["phase"],
             bool(r["is_gate"]), r["description"] or r["step_code"])
            for r in cur.fetchall()]

    extras = [(chave, ordem, fase, is_gate, rotulo)
              for ordem, chave, fase, is_gate, rotulo in REGISTRATION_EXTRA_STEPS]
    cur.execute("SELECT id, name FROM dwh.player_event_types WHERE name = ANY(%(names)s::text[])",
                {"names": [e[0] for e in extras]})
    tipos_extra = {r["name"]: r["id"] for r in cur.fetchall()}
    rows += [(ordem, chave, tipos_extra.get(chave), fase, is_gate, rotulo)
             for chave, ordem, fase, is_gate, rotulo in extras]

    # Passo sem type_id não é filtrável pelo índice; deixá-lo entrar viraria uma etapa
    # fantasma com zero pessoas, indistinguível de perda total.
    sem_tipo = [chave for _, chave, type_id, _, _, _ in rows if not type_id]
    if sem_tipo:
        print(f"⚠️  Passos sem player_event_type_id (fora do funil): {sem_tipo}")
    rows = [r for r in rows if r[2] and r[1] not in PASSOS_FORA_DO_FUNIL]

    rows.sort(key=lambda r: r[0])
    steps = [(i + 1, chave, type_id, fase, is_gate, f"{i+1:02d} {rotulo}")
             for i, (_, chave, type_id, fase, is_gate, rotulo) in enumerate(rows)]
    cache_set(cache_key, {"steps": steps})
    return steps

def _sql_lit(s):
    return s.replace("'", "''")

def _jornada_passos_sql(steps):
    """VALUES com o catálogo, para juntar contra os eventos dentro do próprio SQL."""
    rows = ",\n        ".join(
        f"({n}, '{_sql_lit(type_id)}', '{_sql_lit(fase)}', "
        f"{'true' if is_gate else 'false'}, '{_sql_lit(rotulo)}')"
        for n, _chave, type_id, fase, is_gate, rotulo in steps
    )
    return f"SELECT * FROM (VALUES\n        {rows}\n    ) AS v(n, type_id, fase, is_gate, rotulo)"

def _jornada_base_sql(type_ids, dt_ini, dt_fim, frente_filter, params, com_ts=False):
    """CTE base da jornada: uma linha por evento já recortado por data de OCORRÊNCIA e
    limpo de revalidação de login. Compartilhada pelas quatro rotas da aba para que elas
    não voltem a divergir entre si.

    `com_ts=True` adiciona o timestamp de ocorrência (necessário só no tempo entre passos).
    """
    params["type_ids"] = list(type_ids)
    params["ing_ini"]  = dt_ini - INGEST_LOOKBACK
    params["ing_fim"]  = dt_fim + INGEST_LOOKAHEAD
    params["occ_ini"]  = dt_ini
    params["occ_fim"]  = dt_fim
    col_ts = f",\n                   {OCC_TS_SQL} AS occ_ts" if com_ts else ""
    return f"""
            SELECT pe.json_data->>'registrationId' AS person_id,
                   pe.player_event_type_id         AS type_id,
                   {OCC_DATE_SQL}                  AS dia{col_ts}
            FROM dwh.player_events pe
            LEFT JOIN public.entities e ON e.id = pe.entity_id
            WHERE pe.player_event_type_id = ANY(%(type_ids)s::text[])
              AND pe.created >= %(ing_ini)s AND pe.created < %(ing_fim)s
              AND {OCC_DATE_SQL} BETWEEN %(occ_ini)s AND %(occ_fim)s
              AND pe.json_data->>'registrationId' IS NOT NULL
              AND {JORNADA_COORTE_SQL}
              {frente_filter}
    """

def _jornada_marcos_confiaveis(rows):
    """Preenche cobertura/conversão sobre as linhas já contadas do funil.

    Regras, todas derivadas do dado e não de premissa:
    - `cobertura_pct`: pessoas do passo sobre pessoas do ACC — **condicionada a quem
      concluiu** (ver COBERTURA_CONDICIONADA_A_CONCLUINTES). Não é atestado de qualidade.
    - `instrumentacao_parcial`: gate anterior ao ACC com qualquer déficit contra o ACC.
      Não é perda de usuário — é evento que não foi emitido, e a contagem do passo é
      **piso**, não nível.
    - conversão (`pct_da_etapa_anterior` / `perdidos_nesta_etapa`) só é calculada entre
      marcos confiáveis consecutivos, e só é marcada como LOCALIZADA se não houver gate
      sub-instrumentado entre os dois. Com um gate cego no meio, o delta ainda é uma perda
      real no agregado, mas não se sabe em que passo ela aconteceu — e apresentá-la
      colada a um passo específico foi exactamente o erro que produziu o número impossível
      de "3.072 perdidos no telefone" contra uma perda total de 3.025.
    """
    ref = next((r["pessoas"] for r in rows if r["chave"] == STEP_REFERENCIA), None)
    n_ref = next((r["etapa"] for r in rows if r["chave"] == STEP_REFERENCIA), None)
    notas = []

    # Topo do funil = o passo de entrada declarado (STEP_TOPO), não "quem teve qualquer
    # evento". O topo âncora também a cadeia de conversão mesmo não sendo gate: sem ele o
    # primeiro gate não teria com o que ser comparado e a maior perda ficaria invisível.
    topo = next((r for r in rows if r["chave"] == STEP_TOPO), None)
    if topo is None:
        # Catálogo sem o passo de entrada: cai para o passo de maior volume, para o painel
        # não ficar sem denominador. Vale avisar, porque muda o significado da coluna.
        topo = max(rows, key=lambda r: r["pessoas"], default=None)
        if topo is not None:
            notas.append(
                f'Passo de entrada "{STEP_TOPO}" não está no catálogo do período; '
                f'"{topo["nome"]}" foi usado como topo por ser o de maior volume.'
            )
    n_topo = topo["etapa"] if topo else None
    base_topo = topo["pessoas"] if topo else 0

    # Primeira passada: cobertura e diagnóstico de instrumentação por passo.
    for r in rows:
        r["pct_do_topo"] = round(100.0 * r["pessoas"] / base_topo, 1) if base_topo else None
        r["cobertura_pct"] = round(100.0 * r["pessoas"] / ref, 1) if ref else None
        r["cobertura_condicionada"] = COBERTURA_CONDICIONADA_A_CONCLUINTES
        r["instrumentacao_parcial"] = bool(
            r["is_gate"] and ref and n_ref is not None
            and r["etapa"] < n_ref and r["pessoas"] < COBERTURA_MIN_GATE * ref
        )
        r["marco_confiavel"] = (
            (bool(r["is_gate"]) or r["etapa"] == n_topo) and not r["instrumentacao_parcial"]
        )
        r["pct_da_etapa_anterior"] = None
        r["perdidos_nesta_etapa"]  = None
        r["comparado_com"]         = None
        r["perda_localizada"]      = None

    # Segunda passada: conversão entre marcos confiáveis consecutivos.
    cegos = [r for r in rows if r["instrumentacao_parcial"]]
    anterior = None
    for r in rows:
        if not r["marco_confiavel"]:
            continue
        if anterior is not None:
            base = anterior["pessoas"]
            if base and r["pessoas"] <= base:
                # A perda é real (os dois extremos são confiáveis), mas só é LOCALIZÁVEL se
                # não houver gate cego entre eles. Havendo, sabe-se o quanto se perdeu, não
                # onde — e é isso que o painel tem de dizer, em vez de colar o número no
                # passo mais próximo.
                entre = [c for c in cegos if anterior["etapa"] < c["etapa"] < r["etapa"]]
                r["pct_da_etapa_anterior"] = round(100.0 * r["pessoas"] / base, 1)
                r["perdidos_nesta_etapa"]  = base - r["pessoas"]
                r["comparado_com"]         = anterior["nome"]
                r["perda_localizada"]      = not entre
                if entre:
                    r["gates_cegos_no_intervalo"] = [c["nome"] for c in entre]
            elif base:
                # Passo posterior com MAIS pessoas que o anterior: ninguém "desconverteu",
                # o passo anterior é que não registrou todo mundo. Com COBERTURA_MIN_GATE
                # exata isso não deve mais acontecer entre gates, mas fica o tratamento.
                notas.append(
                    f'"{r["nome"]}" ({r["pessoas"]}) é maior que "{anterior["nome"]}" '
                    f'({base}): o passo anterior deixou de registrar ao menos '
                    f'{r["pessoas"] - base} pessoa(s), então a conversão entre os dois '
                    f'não é calculável — não é ganho de usuário.'
                )
        anterior = r

    if cegos:
        notas.append(
            f"Não é possível localizar a perda: {len(cegos)} gate(s) obrigatório(s) estão "
            f"cegos, com cobertura de {min(c['cobertura_pct'] for c in cegos):.1f}% a "
            f"{max(c['cobertura_pct'] for c in cegos):.1f}% das contas criadas. Toda "
            f"contagem intermediária é piso, não nível, e a cobertura é medida sobre quem "
            f"concluiu — então ela nada diz sobre quem abandonou. A perda total do funil é "
            f"confiável; o passo em que ela ocorre, não."
        )
    return rows, notas

# Go-live da instrumentação nova. 26/08 existe mas é dia quebrado (SST/SPV começaram às
# 14:11 e o resto às 16:28), então o primeiro dia inteiro comparável é 27/08.
JORNADA_PRIMEIRO_DIA = date(2026, 8, 27)

# Dias que ainda vão receber ingestão tardia e por isso não fecharam (D0 captura ~83% dos
# eventos client-side e amadurece por ~3 dias).
JORNADA_DIAS_PROVISORIOS = 3

def _jornada_avisos(dt_ini, dt_fim, rows):
    """Ressalvas que o número não carrega sozinho. Sem isto o leitor confunde
    sub-instrumentação com perda de usuário e série truncada com queda real."""
    avisos = []
    if dt_ini < JORNADA_PRIMEIRO_DIA:
        avisos.append(
            f"Série truncada: a instrumentação por eventos começou em "
            f"{JORNADA_PRIMEIRO_DIA.strftime('%d/%m/%Y')}. O período pedido começa em "
            f"{dt_ini.strftime('%d/%m/%Y')}, e não existe dado antes disso — "
            f"os dias anteriores aparecem vazios, não em queda."
        )
    corte = date.today() - timedelta(days=JORNADA_DIAS_PROVISORIOS)
    if dt_fim >= corte:
        avisos.append(
            f"Números provisórios: os últimos {JORNADA_DIAS_PROVISORIOS} dias ainda "
            f"recebem eventos por ingestão tardia e vão subir. Para comparar tendência, "
            f"use período que termine antes de {corte.strftime('%d/%m/%Y')}."
        )
    parciais = [r["nome"] for r in rows if r.get("instrumentacao_parcial")]
    if parciais:
        avisos.append(
            f"{len(parciais)} gate(s) com instrumentação parcial — há gente que criou "
            f"conta sem gerar o evento, então o volume baixo NÃO é perda de usuário e não "
            f"entra no ranking de perdas: {', '.join(parciais)}."
        )
    return avisos

def _jornada_frente_filter(cur, frente, btag, afiliado, params):
    """Filtra a jornada por frente/btag — direto no json_data->>'btag' do próprio evento
    (disponível desde o primeiro evento, antes mesmo de existir entidade) — e por afiliado
    via entity_id (só cobre quem já tem entidade criada; inerente ao dado, não dá para
    saber o afiliado de quem ainda não completou o cadastro)."""
    conds = []
    frentes_lista = [f.strip() for f in frente.split(',') if f.strip() and f.strip() != 'todas'] if frente else []

    if frentes_lista:
        fc = FRENTE_CASE.replace('e.json_data', 'pe.json_data')
        placeholders = ','.join([f'%(frente_{i})s' for i in range(len(frentes_lista))])
        conds.append(f"({fc}) IN ({placeholders})")
        for i, f in enumerate(frentes_lista):
            params[f'frente_{i}'] = f

    if btag:
        conds.append("COALESCE(pe.json_data->>'btag','') ILIKE %(btag)s")
        params["btag"] = f"%{btag}%"

    if afiliado:
        eids = fetch_filtered_entity_ids(cur, [], '', afiliado)
        if eids is not None:
            params["afi_eids"] = eids
            conds.append("pe.entity_id IN (SELECT UNNEST(%(afi_eids)s::bigint[]))")

    return f"AND {' AND '.join(conds)}" if conds else ""

def _jornada_request_args():
    filtro     = request.args.get("data", "mes")
    custom_ini = request.args.get("ini", "")
    custom_fim = request.args.get("fim", "")
    frente     = request.args.get("frente", "").strip()
    btag       = request.args.get("btag", "").strip()
    afiliado   = request.args.get("afiliado", "").strip()
    force      = request.args.get("force", "0") == "1"
    dt_ini, dt_fim = periodo(filtro, custom_ini, custom_fim)
    return dt_ini, dt_fim, frente, btag, afiliado, force

@app.route("/api/funil_jornada")
def api_funil_jornada():
    """Funil consolidado por eventos — alimenta a visao de funil completo e o
    ranking de etapas com mais perdas (mesma resposta, duas leituras no frontend)."""
    dt_ini, dt_fim, frente, btag, afiliado, force = _jornada_request_args()
    cache_key = f"jornada6|{dt_ini}|{dt_fim}|{frente}|{btag}|{afiliado}"
    cached = None if force else cache_get(cache_key)
    if cached:
        return jsonify({"ok": True, "data": cached, "cache": True,
                        "periodo": {"ini": str(dt_ini), "fim": str(dt_fim)}})
    try:
        c = psycopg2.connect(**DB)
        cur = c.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        steps = _registration_steps_catalog(cur)
        chave_por_etapa = {n: chave for n, chave, _, _, _, _ in steps}
        params = {}
        frente_filter = _jornada_frente_filter(cur, frente, btag, afiliado, params)
        base_sql = _jornada_base_sql([t for _, _, t, _, _, _ in steps],
                                     dt_ini, dt_fim, frente_filter, params)

        cur.execute(f"""
            WITH base AS ({base_sql}),
            eventos AS (SELECT DISTINCT person_id, type_id FROM base),
            passos AS (
                {_jornada_passos_sql(steps)}
            ),
            p AS (SELECT DISTINCT person_id AS id FROM base),
            st AS (
                SELECT s.n, s.fase, s.is_gate, s.rotulo,
                    (SELECT count(*) FROM p)              AS coorte,
                    count(DISTINCT ev.person_id)          AS pessoas
                FROM passos s
                LEFT JOIN eventos ev ON ev.type_id = s.type_id
                GROUP BY s.n, s.fase, s.is_gate, s.rotulo
            )
            SELECT
                st.n        AS etapa,
                st.fase     AS fase,
                st.is_gate  AS is_gate,
                st.rotulo   AS nome,
                st.coorte   AS coorte_bruta,
                st.pessoas
            FROM st
            ORDER BY st.n
        """, params)
        rows = [clean(dict(r)) for r in cur.fetchall()]

        # `pessoas` agora é contagem real de emissores do evento, então cobertura e
        # conversão são derivadas aqui — sob dados não-monotônicos o lag() do SQL
        # produzia taxa acima de 100% e perda negativa.
        for r in rows:
            r["chave"] = chave_por_etapa.get(r["etapa"])
        rows, notas = _jornada_marcos_confiaveis(rows)

        ref  = next((r["pessoas"] for r in rows if r["chave"] == STEP_REFERENCIA), 0)
        topo = next((r for r in rows if r["chave"] == STEP_TOPO), None)
        base_topo = topo["pessoas"] if topo else 0

        # Validação contra a fonte independente. O painel afirmava "o marco final confere
        # com a tabela de entidades" SEM nunca consultá-la — afirmação fabricada num painel
        # cuja premissa é rigor. Agora o número é medido, e a divergência é publicada.
        #
        # Consequência que a própria regra do painel impõe: o marco final também subconta
        # (946 contra 956 entidades = 99,0%, abaixo de 100%). Logo a conversão publicada é
        # PISO, não estimativa, e a perda publicada é TETO. Ver `validacao` no payload.
        cur.execute("""
            SELECT count(*) AS entidades
            FROM public.entities
            WHERE entity_type_id = 6
              AND created::date BETWEEN %(ini)s AND %(fim)s
        """, {"ini": dt_ini, "fim": dt_fim})
        entidades = int(cur.fetchone()["entidades"] or 0)
        divergencia_pct = round(100.0 * (entidades - ref) / entidades, 1) if entidades else None
        validacao = {
            "fonte": "public.entities (entity_type_id=6)",
            "entidades": entidades,
            "marco_final": ref,
            "cobertura_pct": round(100.0 * ref / entidades, 1) if entidades else None,
            "divergencia_pct": divergencia_pct,
            # Acima deste limite a leitura do painel deixa de ser confiável e vira alarme.
            "limite_aceitavel_pct": 3.0,
            "ok": bool(divergencia_pct is not None and abs(divergencia_pct) <= 3.0),
        }
        c.close()

        # Funil confirmado: só os passos cujo nível o dado sustenta. É o que pode ser
        # renderizado com barra e porcentagem. O resto vai para a tabela de saúde de
        # instrumentação, sem barra — barra e ordem sequencial AFIRMAM nível, e um selo de
        # ressalva não desfaz o que a barra afirma.
        confirmados = [r for r in rows if r["marco_confiavel"]]

        # Perda: os dois extremos são medidos, mas o marco final subconta contra a
        # `entities`, então o número é TETO, não estimativa — e a conversão é PISO. Assinar
        # isso é a própria regra do painel aplicada a si mesmo; sem isso o painel exige do
        # dado um rigor que não exige de si.
        #
        # E o rótulo é "não concluíram no mesmo dia", não "perdidos": a coorte é de mesmo
        # dia, então quem termina o cadastro em D+1 entra aqui como se tivesse abandonado.
        perda_total = None
        if base_topo and ref:
            cegos = [r["nome"] for r in rows if r["instrumentacao_parcial"]]
            perda_total = {
                "pessoas": base_topo - ref,
                "pct_do_topo": round(100.0 * (base_topo - ref) / base_topo, 1),
                "de": topo["nome"] if topo else None,
                "para": next((r["nome"] for r in rows if r["chave"] == STEP_REFERENCIA), None),
                "localizada": not cegos,
                "gates_cegos": cegos,
                # Limite superior: com o marco final subcontando, a perda real é menor.
                "e_teto": bool(entidades and ref < entidades),
                "pessoas_ajustado_por_entidades": (base_topo - entidades) if entidades else None,
                "rotulo": "não concluíram no mesmo dia",
            }

        # Conversão ponta a ponta: PISO, pelo mesmo motivo.
        conversao = None
        if base_topo:
            conversao = {
                "pct": round(100.0 * ref / base_topo, 1),
                "e_piso": bool(entidades and ref < entidades),
                "pct_ajustado_por_entidades": (round(100.0 * entidades / base_topo, 1)
                                               if entidades else None),
            }

        result = {
            "etapas": rows,
            "funil_confirmado": confirmados,
            "perda_total": perda_total,
            "conversao": conversao,
            "validacao": validacao,
            # `coorte` é o topo do funil (denominador de pct_do_topo). `coorte_bruta` é
            # quem teve qualquer evento — fica só como diagnóstico, não é denominador.
            "coorte": base_topo,
            "coorte_bruta": rows[0]["coorte_bruta"] if rows else 0,
            "topo": {"chave": STEP_TOPO, "nome": topo["nome"] if topo else None,
                     "pessoas": base_topo},
            "referencia": {"chave": STEP_REFERENCIA, "pessoas": ref,
                           "cobertura_min_gate": COBERTURA_MIN_GATE,
                           "condicionada_a_concluintes": COBERTURA_CONDICIONADA_A_CONCLUINTES},
            "avisos": _jornada_avisos(dt_ini, dt_fim, rows) + notas,
        }
        cache_set(cache_key, result)
        return jsonify({"ok": True, "data": result, "cache": False,
                        "periodo": {"ini": str(dt_ini), "fim": str(dt_fim)}})
    except Exception as e:
        tb = traceback.format_exc()
        print(f"\n❌ FUNIL JORNADA ERRO:\n{tb}")
        return jsonify({"ok": False, "error": str(e), "trace": tb}), 500

@app.route("/api/funil_jornada_diario")
def api_funil_jornada_diario():
    """Evolucao por dia dos passos do funil de cadastro — mesma leitura por-dia da aba
    Geral, aplicada à jornada granular de eventos. Devolve tambem o catalogo (nome/fase
    por etapa) para o frontend montar o cabecalho sem depender de lista hardcoded."""
    dt_ini, dt_fim, frente, btag, afiliado, force = _jornada_request_args()
    cache_key = f"jornada_dia5|{dt_ini}|{dt_fim}|{frente}|{btag}|{afiliado}"
    cached = None if force else cache_get(cache_key)
    if cached:
        return jsonify({"ok": True, "data": cached, "cache": True,
                        "periodo": {"ini": str(dt_ini), "fim": str(dt_fim)}})
    try:
        c = psycopg2.connect(**DB)
        cur = c.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        steps = _registration_steps_catalog(cur)
        params = {}
        frente_filter = _jornada_frente_filter(cur, frente, btag, afiliado, params)
        base_sql = _jornada_base_sql([t for _, _, t, _, _, _ in steps],
                                     dt_ini, dt_fim, frente_filter, params)

        # Emissores reais de cada passo no dia, não high-water-mark: o dia é o dia de
        # OCORRÊNCIA do evento, então a pessoa conta em cada dia em que agiu.
        step_exprs = [
            f"count(DISTINCT person_id) FILTER (WHERE type_id = '{_sql_lit(type_id)}') AS etapa_{n:02d}"
            for n, _, type_id, _, _, _ in steps
        ]
        select_cols = ",\n                ".join(step_exprs)

        cur.execute(f"""
            WITH base AS ({base_sql})
            SELECT
                dia,
                {select_cols}
            FROM base
            GROUP BY dia
            ORDER BY dia
        """, params)
        rows = cur.fetchall()
        c.close()

        dias = {}
        for r in rows:
            d = dict(r)
            key = str(d.pop("dia"))
            dias[key] = {k: int(v or 0) for k, v in d.items()}

        catalogo = [{"key": f"etapa_{n:02d}", "nome": rotulo, "fase": fase, "is_gate": is_gate}
                    for n, _, _, fase, is_gate, rotulo in steps]

        result = clean({"dias": dias, "catalogo": catalogo,
                        "avisos": _jornada_avisos(dt_ini, dt_fim, [])})
        cache_set(cache_key, result)
        return jsonify({"ok": True, "data": result, "cache": False,
                        "periodo": {"ini": str(dt_ini), "fim": str(dt_fim)}})
    except Exception as e:
        tb = traceback.format_exc()
        print(f"\n❌ FUNIL JORNADA DIARIO ERRO:\n{tb}")
        return jsonify({"ok": False, "error": str(e), "trace": tb}), 500

# Sinais de atrito: agora lidos direto do step_code do evento, sem inferencia — a
# instrumentacao antiga precisava adivinhar a partir de chaves soltas no json_flags.
FRICTION_SIGNALS = [
    ('phone.channel_chosen',      'Escolheu o canal do código (SMS/WhatsApp)', 'normal'),
    ('phone.code_resent',         'Reenviou o código do telefone',             'atrito'),
    ('phone.destination_changed', 'Trocou o telefone',                         'atrito'),
    ('email.code_resent',         'Reenviou o código do e-mail',               'atrito'),
    ('email.destination_changed', 'Trocou o e-mail',                          'atrito'),
    ('kyc.camera_denied',         'Câmera negada pelo navegador',              'atrito'),
    ('kyc.camera_granted',        'Câmera permitida',                          'normal'),
]

@app.route("/api/funil_atrito")
def api_funil_atrito():
    """Sinais de atrito da jornada (reenvios, trocas, camera negada, endereco pulado)."""
    dt_ini, dt_fim, frente, btag, afiliado, force = _jornada_request_args()
    cache_key = f"atrito5|{dt_ini}|{dt_fim}|{frente}|{btag}|{afiliado}"
    cached = None if force else cache_get(cache_key)
    if cached:
        return jsonify({"ok": True, "data": cached, "cache": True,
                        "periodo": {"ini": str(dt_ini), "fim": str(dt_fim)}})
    try:
        c = psycopg2.connect(**DB)
        cur = c.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        # O type_id vem do mesmo catálogo das outras rotas — o filtro precisa ser por
        # player_event_type_id para usar o índice (ver _registration_steps_catalog).
        tipo_por_chave = {chave: type_id for _, chave, type_id, _, _, _ in
                          _registration_steps_catalog(cur)}
        extras = ['address.started', 'kyc.intro_viewed']
        sinais = [(tipo_por_chave[code], nome, tipo)
                  for code, nome, tipo in FRICTION_SIGNALS if code in tipo_por_chave]
        faltando = [c_ for c_, _, _ in FRICTION_SIGNALS if c_ not in tipo_por_chave] \
                 + [c_ for c_ in extras if c_ not in tipo_por_chave]
        if faltando:
            print(f"⚠️  Sinais de atrito sem type_id no catálogo (ignorados): {faltando}")
        friction_type_ids = [t for t, _, _ in sinais] + \
                            [tipo_por_chave[c_] for c_ in extras if c_ in tipo_por_chave]

        params = {}
        frente_filter = _jornada_frente_filter(cur, frente, btag, afiliado, params)
        base_sql = _jornada_base_sql(friction_type_ids, dt_ini, dt_fim, frente_filter, params)
        friction_values_sql = ",\n                ".join(
            f"('{_sql_lit(type_id)}', '{_sql_lit(nome)}', '{tipo}')" for type_id, nome, tipo in sinais
        )
        tipo_addr = tipo_por_chave.get('address.started', '')
        tipo_kyiv = tipo_por_chave.get('kyc.intro_viewed', '')

        cur.execute(f"""
            WITH base AS ({base_sql}),
            eventos AS (SELECT DISTINCT person_id, type_id FROM base),
            p AS (SELECT DISTINCT person_id AS id FROM base),
            skip_addr AS (
                SELECT p.id,
                       bool_or(ev.type_id = '{_sql_lit(tipo_addr)}') AS tem_addr,
                       bool_or(ev.type_id = '{_sql_lit(tipo_kyiv)}') AS tem_kyc
                FROM p
                LEFT JOIN eventos ev ON ev.person_id = p.id
                GROUP BY p.id
            )
            SELECT v.rotulo                                                            AS sinal,
                   count(DISTINCT ev.person_id) FILTER (WHERE ev.type_id = v.type_id)  AS pessoas,
                   round(100.0 * count(DISTINCT ev.person_id) FILTER (WHERE ev.type_id = v.type_id)
                         / nullif((SELECT count(*) FROM p), 0), 1)                      AS pct_da_coorte,
                   v.tipo                                                               AS tipo
            FROM (VALUES
                {friction_values_sql}
            ) AS v(type_id, rotulo, tipo)
            LEFT JOIN eventos ev ON ev.type_id = v.type_id
            GROUP BY v.rotulo, v.tipo

            UNION ALL
            SELECT
                'Pulou a tela de endereço (CPF já trouxe CEP)',
                count(*) FILTER (WHERE NOT tem_addr AND tem_kyc),
                round(100.0 * count(*) FILTER (WHERE NOT tem_addr AND tem_kyc)
                      / nullif((SELECT count(*) FROM p), 0), 1),
                'normal'
            FROM skip_addr
            ORDER BY 2 DESC NULLS LAST
        """, params)
        rows = [clean(dict(r)) for r in cur.fetchall()]
        c.close()

        result = {"sinais": rows, "avisos": _jornada_avisos(dt_ini, dt_fim, [])}
        cache_set(cache_key, result)
        return jsonify({"ok": True, "data": result, "cache": False,
                        "periodo": {"ini": str(dt_ini), "fim": str(dt_fim)}})
    except Exception as e:
        tb = traceback.format_exc()
        print(f"\n❌ FUNIL ATRITO ERRO:\n{tb}")
        return jsonify({"ok": False, "error": str(e), "trace": tb}), 500

@app.route("/api/funil_tempo_passos")
def api_funil_tempo_passos():
    """Mediana/p90 de tempo entre passos consecutivos — acha o gargalo que NAO
    aparece como queda: a etapa onde quem continua leva muito tempo para continuar."""
    dt_ini, dt_fim, frente, btag, afiliado, force = _jornada_request_args()
    cache_key = f"tempo_passos5|{dt_ini}|{dt_fim}|{frente}|{btag}|{afiliado}"
    cached = None if force else cache_get(cache_key)
    if cached:
        return jsonify({"ok": True, "data": cached, "cache": True,
                        "periodo": {"ini": str(dt_ini), "fim": str(dt_fim)}})
    try:
        c = psycopg2.connect(**DB)
        cur = c.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        steps = _registration_steps_catalog(cur)
        params = {}
        frente_filter = _jornada_frente_filter(cur, frente, btag, afiliado, params)
        base_sql = _jornada_base_sql([t for _, _, t, _, _, _ in steps],
                                     dt_ini, dt_fim, frente_filter, params, com_ts=True)

        # `quando` tem de ser o instante de OCORRÊNCIA. Com o timestamp de ingestão
        # (`pe.created`), o intervalo entre passos misturava o tempo do usuário com o
        # atraso da esteira de dados — que varia de segundos a 6 dias.
        cur.execute(f"""
            WITH base AS ({base_sql}),
            eventos AS (
                SELECT person_id, type_id, min(occ_ts) AS quando
                FROM base
                GROUP BY person_id, type_id
            ),
            passos AS (
                {_jornada_passos_sql(steps)}
            ),
            ts AS (
                SELECT ev.person_id, s.n, s.rotulo, ev.quando
                FROM eventos ev
                JOIN passos s ON s.type_id = ev.type_id
            ),
            pares AS (
                SELECT t.person_id, t.n, t.rotulo,
                       t.quando - lag(t.quando) OVER (PARTITION BY t.person_id ORDER BY t.n) AS dur
                FROM ts t
            )
            SELECT
                n                                                                    AS passo,
                rotulo                                                               AS nome,
                count(dur)                                                           AS pessoas,
                round(percentile_cont(0.5) WITHIN GROUP
                      (ORDER BY extract(epoch FROM dur))::numeric, 1)                AS mediana_seg,
                round(percentile_cont(0.9) WITHIN GROUP
                      (ORDER BY extract(epoch FROM dur))::numeric, 1)                AS p90_seg
            FROM pares
            WHERE dur IS NOT NULL AND dur > interval '0'
            GROUP BY n, rotulo
            ORDER BY n
        """, params)
        rows = [clean(dict(r)) for r in cur.fetchall()]
        c.close()

        result = {"passos": rows, "avisos": _jornada_avisos(dt_ini, dt_fim, [])}
        cache_set(cache_key, result)
        return jsonify({"ok": True, "data": result, "cache": False,
                        "periodo": {"ini": str(dt_ini), "fim": str(dt_fim)}})
    except Exception as e:
        tb = traceback.format_exc()
        print(f"\n❌ FUNIL TEMPO PASSOS ERRO:\n{tb}")
        return jsonify({"ok": False, "error": str(e), "trace": tb}), 500

@app.route("/api/loteria_diario")
def api_loteria_diario():
    filtro     = request.args.get("data", "mes")
    custom_ini = request.args.get("ini", "")
    custom_fim = request.args.get("fim", "")
    force      = request.args.get("force", "0") == "1"

    dt_ini, dt_fim = periodo(filtro, custom_ini, custom_fim)
    cache_key = f"lot_diario|{dt_ini}|{dt_fim}"
    cached = None if force else cache_get(cache_key)
    if cached:
        return jsonify({"ok": True, "data": cached, "cache": True,
                        "periodo": {"ini": str(dt_ini), "fim": str(dt_fim)}})
    try:
        c = psycopg2.connect(**DB)
        cur = c.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        params = {"ini": dt_ini, "fim": dt_fim}

        # Turnover real de apostas de loteria (da tabela lottery_games)
        cur.execute("""
            SELECT
                to_char(created::date, 'YYYY-MM-DD') AS data,
                SUM(value)::numeric(18,2)             AS turnover,
                COUNT(DISTINCT entity_id)             AS jogadores
            FROM public.lottery_games
            WHERE created::date >= %(ini)s AND created::date <= %(fim)s
            GROUP BY created::date
            ORDER BY created::date
        """, params)
        lot_rows = {r['data']: {"turnover": float(r['turnover'] or 0),
                                 "jogadores": int(r['jogadores'] or 0)}
                    for r in cur.fetchall()}

        # GGR/NGR/reward de loteria via vw_uw_balance (games_prog > 0)
        # ngr = ggr_prog - reward (reward proporcional ao canal loteria)
        cur.execute("""
            SELECT
                to_char(created, 'YYYY-MM-DD')                                          AS data,
                COALESCE(SUM(ggr_prog),0)::numeric(18,2)                                AS ggr,
                COALESCE(SUM(ngr_prog),0)::numeric(18,2)                                AS ngr,
                COALESCE(SUM(reward_prog),0)::numeric(18,2)                             AS reward,
                COUNT(DISTINCT entity_id)                                               AS jogadores_uwb
            FROM public.vw_uw_balance
            WHERE created >= %(ini)s AND created <= %(fim)s
              AND COALESCE(games_prog, 0) > 0
            GROUP BY created::date
            ORDER BY created::date
        """, params)
        uwb_rows = {r['data']: {"ggr": float(r['ggr'] or 0),
                                 "ngr": float(r['ngr'] or 0),
                                 "reward": float(r['reward'] or 0),
                                 "jogadores_uwb": int(r['jogadores_uwb'] or 0)}
                    for r in cur.fetchall()}

        c.close()

        all_dates = sorted(set(lot_rows.keys()) | set(uwb_rows.keys()))
        dias = {}
        kpis = {"turnover": 0.0, "ggr": 0.0, "ngr": 0.0, "reward": 0.0, "jogadores": 0}

        for d in all_dates:
            lt = lot_rows.get(d, {"turnover": 0.0, "jogadores": 0})
            uw = uwb_rows.get(d, {"ggr": 0.0, "ngr": 0.0, "reward": 0.0, "jogadores_uwb": 0})
            # Jogadores: prefer lottery_games count (real bettors); fallback to vw_uw_balance
            jogadores = lt["jogadores"] if lt["jogadores"] > 0 else uw["jogadores_uwb"]
            entry = {
                "turnover": lt["turnover"],
                "ggr":      uw["ggr"],
                "ngr":      uw["ngr"],
                "reward":   uw["reward"],
                "jogadores": jogadores,
            }
            dias[d] = entry
            kpis["turnover"] += entry["turnover"]
            kpis["ggr"]      += entry["ggr"]
            kpis["ngr"]      += entry["ngr"]
            kpis["reward"]   += entry["reward"]
            kpis["jogadores"] += jogadores

        kpis["turnover"] = round(kpis["turnover"], 2)
        kpis["ggr"]      = round(kpis["ggr"], 2)
        kpis["ngr"]      = round(kpis["ngr"], 2)
        kpis["reward"]   = round(kpis["reward"], 2)

        result = clean({"kpis": kpis, "dias": dias})
        cache_set(cache_key, result)
        return jsonify({"ok": True, "data": result, "cache": False,
                        "periodo": {"ini": str(dt_ini), "fim": str(dt_fim)}})
    except Exception as e:
        tb = traceback.format_exc()
        print(f"\n❌ LOTERIA DIARIO ERRO:\n{tb}")
        return jsonify({"ok": False, "error": str(e), "trace": tb}), 500


TODAS_FRENTES = ['App', 'Tráfego', 'Mídias', 'Resultado Fácil', 'Orgânico', 'Afiliados']

def prewarm_entity_cache():
    """Pré-carrega entity_ids para todas as frentes em background.
    Roda ao iniciar o servidor e depois a cada 55 minutos.
    """
    print("🔄 Pré-carregando entity_ids por frente...", flush=True)
    for frente in TODAS_FRENTES:
        try:
            ids = get_entity_ids_for_frentes([frente])
            print(f"   ✓ {frente}: {len(ids or [])} entidades", flush=True)
        except Exception as e:
            print(f"   ⚠ {frente}: {e}", flush=True)
    print("✅ Cache de entity_ids pronto.", flush=True)
    # Re-agenda a pré-carga para a próxima hora
    t = threading.Timer(55 * 60, prewarm_entity_cache)
    t.daemon = True
    t.start()

@app.route("/api/prewarm")
def api_prewarm():
    """Força recarga do cache de entity_ids (útil após reiniciar o servidor)."""
    threading.Thread(target=prewarm_entity_cache, daemon=True).start()
    return jsonify({"ok": True, "msg": "Pré-carga iniciada em background"})

# ── MAIN ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    init_cache()

    print("\n" + "="*50)
    print("  Dashboard Geral/Turnover — Tradicional.bet.br")
    print(f"  http://0.0.0.0:{os.environ.get('PORT', 5051)}")
    print("="*50 + "\n")
    # Pré-aquece o cache de entity_ids em background (não bloqueia o start)
    t = threading.Thread(target=prewarm_entity_cache, daemon=True)
    t.start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5051)), debug=False)
