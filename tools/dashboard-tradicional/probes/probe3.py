"""Quem está no denominador do funil, e quanto cada candidato a corte muda o número."""
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

DIA = '2026-08-29'
cur.execute("""
    WITH steps AS (
        SELECT s.step_code, t.id AS type_id
        FROM dwh.registration_steps s
        JOIN dwh.player_event_types t ON t.name = s.step_code
        WHERE s.valid_to IS NULL
        UNION ALL
        SELECT x.code, t.id
        FROM (VALUES ('signup_started'), ('account_created')) AS x(code)
        JOIN dwh.player_event_types t ON t.name = x.code
    ),
    base AS (
        SELECT pe.json_data->>'registrationId' AS pid, s.step_code
        FROM dwh.player_events pe
        JOIN steps s ON s.type_id = pe.player_event_type_id
        LEFT JOIN public.entities e ON e.id = pe.entity_id
        WHERE pe.created >= DATE %(dia)s - interval '1 day'
          AND pe.created <  DATE %(dia)s + interval '8 days'
          AND ((pe.json_data->>'occurredAt')::timestamptz AT TIME ZONE 'America/Sao_Paulo')::date = DATE %(dia)s
          AND pe.json_data->>'registrationId' IS NOT NULL
          AND (pe.entity_id IS NULL
               OR e.created::date = ((pe.json_data->>'occurredAt')::timestamptz AT TIME ZONE 'America/Sao_Paulo')::date)
    ),
    por_pessoa AS (
        SELECT pid,
               bool_or(step_code = 'visit.site_entered') AS tem_visit,
               bool_or(step_code = 'signup_started')     AS tem_sst,
               bool_or(step_code = 'signup_page_view')   AS tem_spv,
               bool_or(step_code = 'account_created')    AS tem_acc
        FROM base GROUP BY pid
    )
    SELECT
      count(*)                                                          AS coorte_atual,
      count(*) FILTER (WHERE tem_visit)                                 AS emitiram_visit,
      count(*) FILTER (WHERE tem_sst)                                   AS emitiram_sst,
      count(*) FILTER (WHERE tem_acc)                                   AS emitiram_acc,
      count(*) FILTER (WHERE NOT tem_visit)                             AS coorte_sem_passo_visit,
      count(*) FILTER (WHERE NOT tem_sst)                               AS sem_sst,
      count(*) FILTER (WHERE NOT tem_sst AND NOT tem_spv)               AS sem_sst_nem_spv,
      count(*) FILTER (WHERE tem_acc AND NOT tem_sst)                   AS acc_sem_sst,
      count(*) FILTER (WHERE tem_sst OR tem_spv)                        AS coorte_entrada_real
    FROM por_pessoa
""", {"dia": DIA})
r = cur.fetchone()
print(f"=== {DIA} ===")
for k, v in r.items():
    print(f"  {k:26s} {v}")

acc, sst, coorte = r["emitiram_acc"], r["emitiram_sst"], r["coorte_atual"]
print()
print("Conversao ate conta criada, por denominador:")
print(f"  coorte atual (qualquer evento) {coorte:6d}  ->  {100*acc/coorte:5.1f}%   <- o que a aba mostra hoje")
print(f"  sem o passo 'Entrada no site'  {r['coorte_sem_passo_visit']:6d}  ->  {100*acc/r['coorte_sem_passo_visit']:5.1f}%   <- o corte que voce pediu")
print(f"  entrada real (SST ou SPV)      {r['coorte_entrada_real']:6d}  ->  {100*acc/r['coorte_entrada_real']:5.1f}%")
print(f"  topo = 'Cadastro iniciado'     {sst:6d}  ->  {100*acc/sst:5.1f}%")

# Quem esta na coorte sem ter iniciado cadastro? Por qual evento entrou?
print()
print("=== quem entra na coorte SEM emitir signup_started (por evento) ===")
cur.execute("""
    WITH steps AS (
        SELECT s.step_code, t.id AS type_id
        FROM dwh.registration_steps s
        JOIN dwh.player_event_types t ON t.name = s.step_code
        WHERE s.valid_to IS NULL
        UNION ALL
        SELECT x.code, t.id FROM (VALUES ('signup_started'), ('account_created')) AS x(code)
        JOIN dwh.player_event_types t ON t.name = x.code
    ),
    base AS (
        SELECT pe.json_data->>'registrationId' AS pid, s.step_code
        FROM dwh.player_events pe
        JOIN steps s ON s.type_id = pe.player_event_type_id
        LEFT JOIN public.entities e ON e.id = pe.entity_id
        WHERE pe.created >= DATE %(dia)s - interval '1 day'
          AND pe.created <  DATE %(dia)s + interval '8 days'
          AND ((pe.json_data->>'occurredAt')::timestamptz AT TIME ZONE 'America/Sao_Paulo')::date = DATE %(dia)s
          AND pe.json_data->>'registrationId' IS NOT NULL
          AND (pe.entity_id IS NULL
               OR e.created::date = ((pe.json_data->>'occurredAt')::timestamptz AT TIME ZONE 'America/Sao_Paulo')::date)
    ),
    sem_sst AS (
        SELECT pid FROM base GROUP BY pid HAVING NOT bool_or(step_code = 'signup_started')
    )
    SELECT b.step_code, count(DISTINCT b.pid) AS pessoas
    FROM base b JOIN sem_sst s ON s.pid = b.pid
    GROUP BY b.step_code ORDER BY pessoas DESC LIMIT 8
""", {"dia": DIA})
for x in cur.fetchall():
    print(f"  {x['step_code']:38s} {x['pessoas']}")

cur.close(); conn.close()
