"""Lane B's breaks: for each, a backup copy, the change, the named test file, the output kept, the file
restored from the copy.

Usage: python breaks_b.py <set> [<break id> ...]
Each break's output is lane-b/break-<id>.txt; a line per break: RED / GREEN (not red) and the exit code.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

WEB = Path("C:/dev/masaha/app-lane-b/apps/web")
OUT = Path("C:/dev/masaha/workspace/WORKER_A/PAYMENTS_STEP10/scripts/lane-b")
DR = "src/features/data-reports"

SETS = {
    "c2": [
        {
            "id": "46",
            "file": f"{DR}/repository/dataReportsRepository.ts",
            "edits": [("api.patch<SpaceReport>(`${spaceReportsPath(spaceId)}", "api.post<SpaceReport>(`${spaceReportsPath(spaceId)}")],
            "lane": "unit",
            "test": f"{DR}/repository/dataReportsRepository.unit.test.ts",
        },
        {
            "id": "47a",
            "file": f"{DR}/services/reportView.ts",
            "edits": [("    month: 'long',\n", "    month: 'long',\n    hour: '2-digit',\n    minute: '2-digit',\n")],
            "lane": "unit",
            "test": f"{DR}/services/reportView.unit.test.ts",
        },
        {
            "id": "47b",
            "file": f"{DR}/services/reportsQueryOf.ts",
            "edits": [("  return value === 'open' || value === 'decided' ? value : 'all';", "  return (value ?? 'all') as ReportChip;")],
            "lane": "unit",
            "test": f"{DR}/services/reportsQueryOf.unit.test.ts",
        },
        {
            "id": "48",
            "file": f"{DR}/hooks/space/useSpaceReports.ts",
            "edits": [("      byline: words.byline({ who: words.visitor, day }),", "      byline: words.byline({\n        who: (report as { reporter?: { name: string } }).reporter?.name ?? words.visitor,\n        day,\n      }),")],
            "lane": "component",
            "test": f"{DR}/hooks/space/useSpaceReports.component.test.tsx",
        },
        {
            "id": "49",
            "file": f"{DR}/hooks/space/useSpaceReports.ts",
            "edits": [("            : chip === 'all'\n              ? ('empty' as const)\n              : ('noMatch' as const),", "            : ('empty' as const),")],
            "lane": "component",
            "test": f"{DR}/hooks/space/useSpaceReports.component.test.tsx",
        },
        {
            "id": "50",
            "file": f"{DR}/hooks/decide/useDecideSheet.ts",
            "edits": [("      note: values.note.trim() === '' ? undefined : values.note,", "      note: values.note,")],
            "lane": "component",
            "test": f"{DR}/hooks/decide/useDecideSheet.component.test.tsx",
        },
        {
            "id": "51",
            "file": f"{DR}/hooks/decide/useDecideSheet.ts",
            "edits": [("  const open = report.status === 'OPEN' && !settled;", "  const open = settled || true;")],
            "lane": "component",
            "test": f"{DR}/hooks/decide/useDecideSheet.component.test.tsx",
        },
        {
            "id": "52",
            "file": f"{DR}/components/decide/DecideSheet.tsx",
            "edits": [("          <SheetTitle>{view.title}</SheetTitle>\n", "")],
            "lane": "component",
            "test": f"{DR}/components/decide/DecideSheet.component.test.tsx",
        },
        {
            "id": "52-focus",
            "file": f"{DR}/components/decide/DecideSheet.tsx",
            "edits": [('<Textarea dir="auto" {...view.reply.field} />', '<Textarea dir="auto" tabIndex={-1} {...view.reply.field} />')],
            "lane": "component",
            "test": f"{DR}/components/decide/DecideSheet.component.test.tsx",
        },
        {
            "id": "53",
            "file": f"{DR}/components/space/SpaceReportsList.tsx",
            "edits": [("        <DataTable\n          label={list.label}", "        <DataTable\n          cardsBelow=\"lg\"\n          label={list.label}")],
            "lane": "component",
            "test": f"{DR}/components/space/SpaceReportsList.component.test.tsx",
        },
        {
            "id": "53-leave",
            "file": f"{DR}/components/space/SpaceReportsList.tsx",
            "edits": [("      if (button !== null && button.ownerDocument.activeElement === button) onLeave();", "      if (button === null) onLeave();")],
            "lane": "component",
            "test": f"{DR}/components/space/SpaceReportsList.component.test.tsx",
        },
        {
            "id": "58",
            "file": "src/pages/dashboard/routes.tsx",
            "edits": [("  dataReports: async () => {\n    const { DataReportsPage } = await import('./space/reports/DataReportsPage');\n    return <DataReportsPage />;\n  },\n", "")],
            "lane": "component",
            "test": "src/pages/dashboard/routes.component.test.tsx -t \"data reports\"",
        },
    ],
    "c3": [
        {
            "id": "46-admin",
            "file": f"{DR}/repository/dataReportsRepository.ts",
            "edits": [("const ADMIN_REPORTS_PATH = '/admin/data-reports';", "const ADMIN_REPORTS_PATH = '/admin/reports';")],
            "lane": "unit",
            "test": f"{DR}/repository/dataReportsRepository.unit.test.ts",
        },
        {
            "id": "47c",
            "file": f"{DR}/services/adminReportsQueryOf.ts",
            "edits": [("  const field = DATA_REPORT_FIELDS.find((each) => each === params.get('field'));", "  const field = (params.get('field') ?? undefined) as DataReportField | undefined;")],
            "lane": "unit",
            "test": f"{DR}/services/adminReportsQueryOf.unit.test.ts",
        },
        {
            "id": "54a",
            "file": f"{DR}/hooks/decide/useDecideSheet.ts",
            "edits": [("  const open = report.status === 'OPEN' && !settled && !verified;", "  const open = report.status === 'OPEN' && !settled;")],
            "lane": "component",
            "test": f"{DR}/hooks/decide/useDecideSheet.component.test.tsx",
        },
        {
            "id": "54b",
            "file": f"{DR}/hooks/admin/useAdminReports.ts",
            "edits": [("      handledBy: verified\n", "      handledBy: verified && false\n")],
            "lane": "component",
            "test": f"{DR}/hooks/admin/useAdminReports.component.test.tsx",
        },
        {
            "id": "51-admin",
            "file": f"{DR}/hooks/decide/useDecideSheet.ts",
            "edits": [("      forbidden: admin ? words.admin.forbiddenVerified : copy.desk.refusals.forbidden,", "      forbidden: copy.desk.refusals.forbidden,")],
            "lane": "component",
            "test": f"{DR}/hooks/decide/useDecideSheet.component.test.tsx",
        },
        {
            "id": "55a",
            "file": f"{DR}/components/admin/AdminReportsList.tsx",
            "edits": [("        <FilterTags tags={list.tags} clear={list.clear} />\n", "")],
            "lane": "component",
            "test": f"{DR}/components/admin/AdminReportsList.component.test.tsx",
        },
        {
            "id": "55b",
            "file": f"{DR}/hooks/admin/useAdminReportsFilters.ts",
            "edits": [("    setParams(latest.current, { replace: true });", "    setParams(latest.current);")],
            "lane": "component",
            "test": f"{DR}/hooks/admin/useAdminReports.component.test.tsx",
        },
        {
            "id": "55c",
            "file": f"{DR}/hooks/admin/useAdminReportsFilters.ts",
            "edits": [("      write({ chip: current().chip, page: 1 });", "      write({ ...current(), field: undefined, page: 1 });")],
            "lane": "component",
            "test": f"{DR}/hooks/admin/useAdminReports.component.test.tsx",
        },
        {
            "id": "56",
            "file": f"{DR}/components/admin/AdminReportsList.tsx",
            "edits": [("          cardsBelow=\"lg\"\n", "")],
            "lane": "component",
            "test": f"{DR}/components/admin/AdminReportsList.component.test.tsx",
        },
        {
            "id": "57",
            "file": "src/features/space-links/components/admin-filter/AdminSpaceFilter.tsx",
            "edits": [("          <ComboboxItem value={ALL}>{words.allSpaces}</ComboboxItem>\n", "")],
            "lane": "component",
            "test": "src/features/space-links/components/admin-filter/AdminSpaceFilter.component.test.tsx",
        },
        {
            "id": "58-admin",
            "file": "src/pages/dashboard/routes.tsx",
            "edits": [("  dataReports: async () => {\n    const { DataReportsPage } = await import('./admin/DataReportsPage');\n    return { element: <DataReportsPage /> };\n  },\n", "")],
            "lane": "component",
            "test": "src/pages/dashboard/routes.component.test.tsx -t \"data reports\"",
        },
    ],
}


def run(brk):
    target = WEB / brk["file"]
    backup = OUT / f"bak-break-{brk['id']}{target.suffix}"
    shutil.copyfile(target, backup)
    try:
        with open(target, encoding="utf8", newline="") as handle:
            text = handle.read()
        for old, new in brk["edits"]:
            if text.count(old) != 1:
                return f"{brk['id']}: SETUP FAILED — the text to break occurs {text.count(old)} times"
            text = text.replace(old, new)
        with open(target, "w", encoding="utf8", newline="") as handle:
            handle.write(text)
        result = subprocess.run(
            f"npx vitest run --project {brk['lane']} {brk['test']}",
            cwd=WEB, shell=True, capture_output=True, text=True, encoding="utf-8", errors="replace",
            env=os.environ,
        )
        out = result.stdout + result.stderr
        (OUT / f"break-{brk['id']}.txt").write_text(out, encoding="utf-8")
        failing = [line.strip() for line in out.splitlines() if line.strip().startswith(("×", "FAIL"))]
        state = "RED" if result.returncode != 0 else "GREEN (not red)"
        return f"{brk['id']}: {state} exit {result.returncode} — {failing[:3]}"
    finally:
        shutil.copyfile(backup, target)


def main():
    name, ids = sys.argv[1], sys.argv[2:]
    for brk in SETS[name]:
        if ids and brk["id"] not in ids:
            continue
        print(run(brk), flush=True)
    status = subprocess.run("git status --short", cwd=WEB, shell=True, capture_output=True, text=True)
    print("git status after restore:\n" + status.stdout)


main()
