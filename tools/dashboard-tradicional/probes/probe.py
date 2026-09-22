"""Sonda somente-leitura no trad_prd, reusando o padrão de auth IAM do geral_app."""
import os, subprocess, sys, psycopg2, psycopg2.extras

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
    connect_timeout=60, options="-c statement_timeout=120000",
)
cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

def show(titulo, sql, params=None):
    print("\n=== %s ===" % titulo)
    try:
        cur.execute(sql, params or {})
        rows = cur.fetchall()
    except Exception as e:
        conn.rollback()
        print("ERRO:", str(e)[:300])
        return []
    if not rows:
        print("(vazio)")
        return []
    cols = list(rows[0].keys())
    print(" | ".join(cols))
    for r in rows:
        print(" | ".join("" if r[c] is None else str(r[c])[:60] for c in cols))
    return rows

show("colunas de dwh.registration_steps", """
    SELECT column_name, data_type FROM information_schema.columns
    WHERE table_schema='dwh' AND table_name='registration_steps' ORDER BY ordinal_position
""")

show("catalogo vigente", """
    SELECT step_order, step_code, phase, is_gate, description
    FROM dwh.registration_steps WHERE valid_to IS NULL ORDER BY step_order
""")

show("colunas de dwh.player_event_types", """
    SELECT column_name, data_type FROM information_schema.columns
    WHERE table_schema='dwh' AND table_name='player_event_types' ORDER BY ordinal_position
""")

show("tipos de evento (id <-> code)", """
    SELECT * FROM dwh.player_event_types ORDER BY 1
""")

cur.close(); conn.close()
