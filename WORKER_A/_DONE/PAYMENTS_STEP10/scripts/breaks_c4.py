"""Adds commit 4's breaks (§10 tests 21–23) to breaks.json."""
import json
from pathlib import Path

PATH = Path("C:/dev/masaha/workspace/WORKER_A/PAYMENTS_STEP10/scripts/breaks.json")
sets = json.loads(PATH.read_text(encoding="utf-8"))
P = "src/features/payments"
sets["c4"] = [
    {
        "id": "21",
        "file": f"{P}/hooks/mine/useMyPaymentsToday.ts",
        "edits": [["const query: PaymentsQuery = { voided: 'INCLUDE', page, limit: 20 };", "const query: PaymentsQuery = { from: gazaClockOf(new Date()).date, to: gazaClockOf(new Date()).date, voided: 'INCLUDE', page, limit: 20 };"]],
        "lane": "component",
        "test": f"{P}/hooks/mine/useMyPaymentsToday.component.test.tsx -t \"never summed\"",
    },
    {
        "id": "22",
        "file": f"{P}/hooks/mine/useMyPaymentsToday.ts",
        "edits": [["              amount: money(totals.receivedAgorot),", "              amount: money(totals.receivedAgorot + totals.voided.amountAgorot),"]],
        "lane": "component",
        "test": f"{P}/hooks/mine/useMyPaymentsToday.component.test.tsx -t \"voided one\"",
    },
    {
        "id": "23",
        "file": f"{P}/components/mine/HandoverFigures.tsx",
        "edits": [["              <span className=\"text-label\">{transfer.label}</span>\n              <span className=\"text-caption text-muted-foreground\">{transfer.helper}</span>\n", "              <span className=\"text-label\">{transfer.label}</span>\n"]],
        "lane": "component",
        "test": f"{P}/components/mine/MyPaymentsToday.component.test.tsx -t \"at 390\"",
    },
]
PATH.write_text(json.dumps(sets, ensure_ascii=False, indent=2), encoding="utf-8")
print("c4 breaks:", len(sets["c4"]))
