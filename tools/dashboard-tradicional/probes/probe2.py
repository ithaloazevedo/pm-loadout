"""Cobertura real por passo, com os filtros corrigidos (ocorrência + coorte por dia)."""
import os, subprocess, psycopg2, psycopg2.extras

def token(host, port, region, user, profile):
    return subprocess.run(
        ["aws", "rds", "generate-db-auth-token", "--hostname", host, "--port", str(port),
         "--region", region, "--username", user, "--profile", profile],
        capture_output=True, text=True, check=True, timeout=20).stdout.strip()

HOST = "ar-trad-prd-cluster.cluster-ro-c44onum4sztb.us-east-1.rds.amazonaws.com"
USER, REGION, PROFILE = "ithalo_mendes", "us-east-1", "trad-prd-ithalo_mendes"
conn = psycopg2.connect(
    host=HOST, port=5432, dbname="trad_prd", user=USER,
    password=token(HOST, 5432, REGION, USER, PROFILE),
    sslmode="verify-full", sslrootcert=os.path.expanduser("~/global-bundle.pem"),
    connect_timeout=60, options="-c statement_timeout=300000",
)
cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

EXTRAS = ['signup_started', 'account_created', 'registration_completed']

# 1. Todos os step_codes do catálogo + extras resolvem para um type_id?
cur.execute("""
    WITH codes AS (
        SELECT step_code FROM dwh.registration_steps WHERE valid_to IS NULL
        UNION ALL SELECT unnest(%(extras)s::text[])
    )
    SELECT c.step_code, t.id AS type_id
    FROM codes c LEFT JOIN dwh.player_event_types t ON t.name = c.step_code
    ORDER BY (t.id IS NULL) DESC, c.step_code
""", {"extras": EXTRAS})
mapa = cur.fetchall()
faltando = [r["step_code"] for r in mapa if not r["type_id"]]
print("=== mapeamento step_code -> type_id ===")
print("total=%d  sem type_id=%d" % (len(mapa), len(faltando)))
if faltando:
    print("SEM MAPEAMENTO:", faltando)
print("amostra:", ", ".join("%s=%s" % (r["step_code"], r["type_id"]) for r in mapa[:6]))

# 2. Cobertura por passo: emissores reais por dia de ocorrência, com filtro de coorte.
print("\n=== emissores distintos por dia de ocorrencia (coorte filtrada) ===")
cur.execute("""
    WITH steps AS (
        SELECT s.step_code, s.step_order, s.is_gate, s.description, t.id AS type_id
        FROM dwh.registration_steps s
        JOIN dwh.player_event_types t ON t.name = s.step_code
        WHERE s.valid_to IS NULL
        UNION ALL
        SELECT x.code, x.ord, x.gate, x.code, t.id
        FROM (VALUES ('signup_started', -0.5, false),
                     ('account_created', 19.5, true),
                     ('registration_completed', 20.0, true)) AS x(code, ord, gate)
        JOIN dwh.player_event_types t ON t.name = x.code
    ),
    ev AS (
        SELECT s.step_order, s.description, s.is_gate,
               ((pe.json_data->>'occurredAt')::timestamptz AT TIME ZONE 'America/Sao_Paulo')::date AS dia,
               pe.json_data->>'registrationId' AS pid,
               pe.entity_id
        FROM dwh.player_events pe
        JOIN steps s ON s.type_id = pe.player_event_type_id
        WHERE pe.created >= DATE '2026-08-27' - interval '1 day'
          AND pe.created <  DATE '2026-08-31' + interval '8 days'
          AND pe.json_data->>'registrationId' IS NOT NULL
    )
    SELECT ev.step_order, ev.description, ev.is_gate,
           COUNT(DISTINCT ev.pid) FILTER (WHERE ev.dia = DATE '2026-08-27') AS d27,
           COUNT(DISTINCT ev.pid) FILTER (WHERE ev.dia = DATE '2026-08-28') AS d28,
           COUNT(DISTINCT ev.pid) FILTER (WHERE ev.dia = DATE '2026-08-29') AS d29,
           COUNT(DISTINCT ev.pid) FILTER (WHERE ev.dia = DATE '2026-08-30') AS d30,
           COUNT(DISTINCT ev.pid) FILTER (WHERE ev.dia = DATE '2026-08-31') AS d31
    FROM ev
    LEFT JOIN public.entities e ON e.id = ev.entity_id
    WHERE ev.dia BETWEEN DATE '2026-08-27' AND DATE '2026-08-31'
      AND (ev.entity_id IS NULL OR e.created::date = ev.dia)
    GROUP BY ev.step_order, ev.description, ev.is_gate
    ORDER BY ev.step_order
""")
rows = cur.fetchall()
print("%-6s %-1s %-44s %7s %7s %7s %7s %7s" % ("ord", "G", "passo", "27/08", "28/08", "29/08", "30/08", "31/08"))
for r in rows:
    print("%-6s %-1s %-44s %7s %7s %7s %7s %7s" % (
        r["step_order"], "*" if r["is_gate"] else " ", (r["description"] or "")[:44],
        r["d27"], r["d28"], r["d29"], r["d30"], r["d31"]))

# 3. Baseline: entidades criadas por dia
cur.execute("""
    SELECT created::date AS dia, COUNT(*) AS entidades
    FROM public.entities
    WHERE entity_type_id = 6 AND created::date BETWEEN DATE '2026-08-27' AND DATE '2026-08-31'
    GROUP BY 1 ORDER BY 1
""")
print("\n=== entities (type 6) por dia ===")
for r in cur.fetchall():
    print(r["dia"], r["entidades"])

cur.close(); conn.close()
