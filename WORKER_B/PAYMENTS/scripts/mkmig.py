"""Write payment_void_guard's migration: the payments migration's payments_guard_change, copied, with D9's read added."""
from pathlib import Path

MIG = Path(r"C:\dev\masaha\app-b\apps\api\prisma\migrations")
src = (MIG / "20260929120300_payments" / "migration.sql").read_bytes().decode("utf-8")
assert "\r\n" not in src
start = src.index('CREATE FUNCTION "payments_guard_change"()')
end_marker = "  RETURN NEW;\nEND;\n$$;\n"
end = src.index(end_marker, start)
body = src[start:end]  # up to (not including) RETURN NEW
assert body.count("CREATE FUNCTION") == 1

header = (
    "-- The ledger's fourth rule, both ways (2026-10-24, #PRNUM): a written-off visit takes no payment, and its\n"
    "-- payments are not voided until the write-off is undone, so a write-off keeps covering what the visit owed when\n"
    "-- it was written off. The function is the payments migration's, with only that read added after its checks.\n"
)
added = (
    '  IF NEW."visit_id" IS NOT NULL THEN\n'
    '    PERFORM 1 FROM "visits" WHERE "id" = NEW."visit_id" AND "written_off_at" IS NOT NULL FOR SHARE;\n'
    "    IF FOUND THEN\n"
    "      RAISE EXCEPTION 'payments_visit_written_off: a written-off visit''s payment is voided once the write-off is undone'\n"
    "        USING ERRCODE = 'check_violation', TABLE = 'payments', CONSTRAINT = 'payments_visit_written_off';\n"
    "    END IF;\n"
    "  END IF;\n"
)
sql = header + body.replace("CREATE FUNCTION", "CREATE OR REPLACE FUNCTION", 1) + added + end_marker
out = MIG / "20261024133344_payment_void_guard" / "migration.sql"
out.write_bytes(sql.encode("utf-8"))
print(sql)
