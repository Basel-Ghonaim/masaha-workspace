"""Adds commit 3's breaks (§10 tests 9–20) to breaks.json."""
import json
from pathlib import Path

PATH = Path("C:/dev/masaha/workspace/WORKER_A/PAYMENTS_STEP10/scripts/breaks.json")
sets = json.loads(PATH.read_text(encoding="utf-8"))
P = "src/features/payments"
sets["c3"] = [
    {
        "id": "9",
        "file": f"{P}/repository/paymentsRepository.ts",
        "edits": [["        params: query,\n      }),\n", "        params: query,\n      }).then(({ data }) => ({ data }) as never),\n"]],
        "lane": "unit",
        "test": f"{P}/repository/paymentsRepository.unit.test.ts",
    },
    {
        "id": "10",
        "file": f"{P}/services/ledgerQueryOf.ts",
        "edits": [["addDays(from, PAYMENTS_RANGE_MAX_DAYS - 1)", "addDays(from, PAYMENTS_RANGE_MAX_DAYS)"]],
        "lane": "unit",
        "test": f"{P}/services/ledgerQueryOf.unit.test.ts",
    },
    {
        "id": "11",
        "file": f"{P}/services/periodText.ts",
        "edits": [["    year: 'numeric',\n    timeZone: 'UTC',\n", "    year: 'numeric',\n"]],
        "lane": "unit",
        "test": f"{P}/services/periodText.unit.test.ts",
        "env": {"TZ": "America/New_York"},
    },
    {
        "id": "12",
        "file": f"{P}/services/paymentRowView.ts",
        "edits": [["              name: isolate(row.voided.by.name),\n", "              name: '',\n"]],
        "lane": "unit",
        "test": f"{P}/services/paymentRowView.unit.test.ts",
    },
    {
        "id": "13",
        "file": f"{P}/hooks/ledger/useLedgerFilters.ts",
        "edits": [["      write({ voided: false, page: 1 });", "      write({ voided: false, page: 1, from: current().from, to: current().to });"]],
        "lane": "component",
        "test": f"{P}/hooks/ledger/useLedgerFilters.component.test.tsx",
    },
    {
        "id": "14",
        "file": f"{P}/hooks/ledger/useLedger.ts",
        "edits": [["              received: money(totals.receivedAgorot),", "              received: money(rows.length === 0 ? 0 : (answer?.data ?? []).reduce((sum, row) => sum + row.amountAgorot, 0)),"]],
        "lane": "component",
        "test": f"{P}/hooks/ledger/useLedger.component.test.tsx -t \"server’s totals\"",
    },
    {
        "id": "15",
        "file": f"{P}/hooks/ledger/useLedger.ts",
        "edits": [["            : filters.anyApplied\n              ? ('noMatch' as const)\n              : ('emptyToday' as const),", "            : ('emptyToday' as const),"]],
        "lane": "component",
        "test": f"{P}/hooks/ledger/useLedger.component.test.tsx -t \"empty today\"",
    },
    {
        "id": "16",
        "file": f"{P}/hooks/ledger/useLedger.ts",
        "edits": [["            .sort((a, b) => Number(b.self) - Number(a.self))\n", "            .sort((a, b) => Number(b.self) - Number(a.self))\n            .filter((person) => person.active)\n"]],
        "lane": "component",
        "test": f"{P}/hooks/ledger/useLedger.component.test.tsx -t \"deactivated\"",
    },
    {
        "id": "17",
        "file": f"{P}/components/ledger/LedgerFilters.tsx",
        "edits": [["      {wide ? (", "      {wide && false ? ("]],
        "lane": "component",
        "test": f"{P}/components/ledger/PaymentsLedger.component.test.tsx -t \"five columns\"",
    },
    {
        "id": "18",
        "file": f"{P}/components/ledger/PaymentsLedger.tsx",
        "edits": [["  const { listRef, totalsRef, leave } = useFocusAfterLeave(ledger.rows.map((row) => row.key));\n", "  useFocusAfterLeave(ledger.rows.map((row) => row.key));\n  const listRef = { current: null };\n  const totalsRef = { current: null };\n  const leave = () => undefined;\n"]],
        "lane": "component",
        "test": f"{P}/components/ledger/PaymentsLedger.component.test.tsx -t \"focused row leaves\"",
    },
    {
        "id": "19",
        "file": "src/features/staff/hooks/people/useStaffPeople.ts",
        "edits": [
            ["import { useStaffQuery } from '../list/useStaffQuery';\n", "import { useQuery } from '@tanstack/react-query';\nimport { createStaffRepository } from '../../repository/staffRepository';\n"],
            ["  const query = useStaffQuery(spaceId);\n", "  const query = useQuery({ queryKey: ['space', spaceId, 'staffPeople'], queryFn: () => createStaffRepository().list(spaceId) });\n"],
        ],
        "lane": "component",
        "test": "src/features/staff/hooks/people/useStaffPeople.component.test.tsx",
    },
    {
        "id": "20a",
        "file": "src/pages/dashboard/routes.tsx",
        "edits": [["  payments: async () => {\n    const { PaymentsPage } = await import('./space/payments/PaymentsPage');\n    return <PaymentsPage />;\n  },\n", ""]],
        "lane": "component",
        "test": "src/pages/dashboard/routes.component.test.tsx -t \"the ledger under\"",
    },
]
PATH.write_text(json.dumps(sets, ensure_ascii=False, indent=2), encoding="utf-8")
print("c3 breaks:", len(sets["c3"]))
