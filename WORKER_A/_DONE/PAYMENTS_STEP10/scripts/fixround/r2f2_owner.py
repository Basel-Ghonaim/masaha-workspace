"""R2-F2, the owner's side and the sheet."""
import io

D = 'C:/dev/masaha/app/apps/web/src/features/data-reports/'


def edit(path, pairs):
    p = D + path
    s = io.open(p, encoding='utf8', newline='').read()
    for a, b in pairs:
        assert s.count(a) == 1, (path, a[:70])
        s = s.replace(a, b)
    io.open(p, 'w', encoding='utf8', newline='').write(s)
    print('ok', path)


edit('hooks/space/useSpaceReports.ts', [
    ("import { REPORT_CHIPS, type ReportChip } from '../../services/reportsQueryOf';",
     "import {\n  REPORT_CHIPS,\n  reportsParamsOf,\n  reportsQueryOf,\n  type ReportChip,\n} from '../../services/reportsQueryOf';"),
    ("const repository = createDataReportsRepository();\n",
     "const repository = createDataReportsRepository();\n\n/** The first page of «الكل», as its chip reads it: the same key, the same cache. */\nconst ALL_FIRST = reportsQueryOf(reportsParamsOf({ chip: 'all', page: 1 })).query;\n"),
    (" * while it is on it, so a decision made elsewhere shows there too.\n",
     " * while it is on it, so a decision made elsewhere shows there too; gone from the page while the sheet\n"
     " * is open — decided elsewhere, met under «جديدة» — it is read from the first page of «الكل».\n"),
    ("""  const latest =
    opened === null ? null : (reports.find((report) => report.id === opened.id) ?? opened);""",
     """  // The report opened, gone from the page shown (decided elsewhere, under «جديدة»): «الكل» holds it.
  const left =
    opened !== null &&
    answer !== undefined &&
    !result.isPlaceholderData &&
    !reports.some((report) => report.id === opened.id);
  const all = useQuery<Page<SpaceReport[]>, AppError>({
    queryKey: dataReportsKeys.space(spaceId, ALL_FIRST),
    queryFn: () => repository.spaceReports(spaceId, ALL_FIRST),
    enabled: left,
  });
  const latest =
    opened === null
      ? null
      : (reports.find((report) => report.id === opened.id) ??
        all.data?.data.find((report) => report.id === opened.id) ??
        opened);"""),
])

edit('hooks/decide/useDecideSheet.ts', [
    ("    status: statusView(report.status, words.statuses, 'staff'),",
     """    // Decided elsewhere and not read back yet: «تمت المراجعة», never the stale «جديد».
    status:
      refusal?.code === 'REPORT_ALREADY_DECIDED' && report.status === 'OPEN'
        ? { label: words.chips.decided, tone: 'neutral' as const }
        : statusView(report.status, words.statuses, 'staff'),"""),
])
