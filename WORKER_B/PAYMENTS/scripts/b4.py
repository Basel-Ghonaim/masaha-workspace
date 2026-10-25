"""B4: write the payments migration's payments_guard_change (old) or payment_void_guard's (new) as SQL files."""
from pathlib import Path

MIG = Path(r"C:\dev\masaha\app-b\apps\api\prisma\migrations")
OUT = Path(r"C:\dev\masaha\workspace\WORKER_B\PAYMENTS\scripts\breaks")
OUT.mkdir(parents=True, exist_ok=True)
src = (MIG / "20260929120300_payments" / "migration.sql").read_bytes().decode("utf-8")
start = src.index('CREATE FUNCTION "payments_guard_change"()')
end_marker = "END;\n$$;\n"
end = src.index(end_marker, start) + len(end_marker)
old = src[start:end].replace("CREATE FUNCTION", "CREATE OR REPLACE FUNCTION", 1)
(OUT / "b4-old.sql").write_bytes(old.encode("utf-8"))
new = (MIG / "20261024133344_payment_void_guard" / "migration.sql").read_bytes()
(OUT / "b4-new.sql").write_bytes(new)
print("written")
