"""O funil tem ramos? A coluna `branch` do catálogo pode explicar a 'sub-instrumentação'."""
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
    connect_timeout=60, options="-c statement_timeout=120000",
)
cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

print("=== catalogo com branch e owner_side ===")
cur.execute("""
    SELECT step_order, step_code, phase, branch, is_gate, owner_side, funnel_version
    FROM dwh.registration_steps WHERE valid_to IS NULL ORDER BY step_order
""")
rows = cur.fetchall()
print("%-6s %-34s %-9s %-14s %-5s %-10s %s" % ("ord","step_code","phase","branch","gate","owner","ver"))
for r in rows:
    print("%-6s %-34s %-9s %-14s %-5s %-10s %s" % (
        r["step_order"], r["step_code"], r["phase"] or "", r["branch"] or "—",
        "sim" if r["is_gate"] else "", r["owner_side"] or "", r["funnel_version"]))

print()
print("=== branches distintos ===")
cur.execute("""
    SELECT COALESCE(branch,'(nulo)') AS branch, count(*) AS passos,
           count(*) FILTER (WHERE is_gate) AS gates,
           string_agg(step_code, ', ' ORDER BY step_order) AS codes
    FROM dwh.registration_steps WHERE valid_to IS NULL
    GROUP BY 1 ORDER BY 2 DESC
""")
for r in cur.fetchall():
    print(" branch=%-14s passos=%-3s gates=%-3s" % (r["branch"], r["passos"], r["gates"]))
    print("   %s" % r["codes"][:300])

print()
print("=== versoes do catalogo (existe mais de uma?) ===")
cur.execute("""
    SELECT funnel_version, valid_from, valid_to, count(*) AS passos
    FROM dwh.registration_steps GROUP BY 1,2,3 ORDER BY 1
""")
for r in cur.fetchall():
    print("  v%-3s de %s ate %-12s %s passos" % (r["funnel_version"], r["valid_from"], r["valid_to"] or "vigente", r["passos"]))

cur.close(); conn.close()
