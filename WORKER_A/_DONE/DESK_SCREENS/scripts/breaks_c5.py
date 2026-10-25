# Each break: back the file up, apply one change, run the test file, record its output, restore, check equal.
import pathlib, shutil, subprocess, sys, filecmp
APP = pathlib.Path(r"C:\dev\masaha\app")
WEB = APP / "apps/web/src/features/desk"
OUT = pathlib.Path(r"C:\dev\masaha\workspace\WORKER_A\DESK_SCREENS\scripts")
BREAKS = {
  "38": ("hooks/unpriced/useUnpricedQuery.ts",
         "    enabled,",
         "    enabled: enabled || true,",
         "src/features/desk/hooks/unpriced", "component"),
  "31": ("hooks/uncollected/useUncollectedCard.ts",
         "    title: words.title({ count: total }),",
         "    title: `${words.title({ count: total })} · ${priceText((answer?.data ?? []).reduce((sum, row) => sum + (row.balanceAgorot ?? 0), 0), language)}`,",
         "src/features/desk/hooks/uncollected", "component"),
  "32": ("hooks/uncollected/useUncollectedCard.ts",
         "        abilities.writeOff && balanceAgorot !== null",
         "        balanceAgorot !== null",
         "src/features/desk/hooks/uncollected", "component"),
  "33": ("hooks/collect/useCollectDialog.ts",
         "  const needsDebt = customer === null && money.left > 0;",
         "  const needsDebt = false && customer === null && money.left > 0;",
         "src/features/desk/hooks/collect", "component"),
  "34": ("repository/deskRepository.ts",
         "      api.put<DeskVisit>(`${visit(spaceId, visitId)}/customer`, body),",
         "      api.put<DeskVisit>(`${visit(spaceId, visitId)}/customer`, body, withIdempotencyKey(crypto.randomUUID())),",
         "src/features/desk/hooks/debt", "component"),
  "36": ("hooks/write-off/useWriteOffDialog.ts",
         "    fieldLines: { reason: { required: words.writeOff.reasonRequired } },\n    failureLines: words.refusals,",
         "    fieldLines: { reason: { required: words.writeOff.reasonRequired } },",
         "src/features/desk/hooks/write-off", "component"),
  "41": ("repository/deskRepository.ts",
         "      api.post<DeskVisit>(`${visit(spaceId, visitId)}/write-off`, body),",
         "      api.post<DeskVisit>(`${visit(spaceId, visitId)}/write-off`, body, withIdempotencyKey(crypto.randomUUID())),",
         "src/features/desk/hooks/write-off", "component"),
}
for name in sys.argv[1:]:
    rel, old, new, tests, lane = BREAKS[name]
    path = WEB / rel
    backup = OUT / f"bak-break-c5-{name}{path.suffix}"
    shutil.copyfile(path, backup)
    text = path.read_text(encoding="utf-8")
    assert text.count(old) == 1, (name, old)
    path.write_text(text.replace(old, new), encoding="utf-8", newline="")
    try:
        run = subprocess.run(f"npm run test:{lane} -w @masaha/web -- {tests}", cwd=APP, shell=True,
                             capture_output=True, text=True, encoding="utf-8", errors="replace")
        out = run.stdout + run.stderr
        (OUT / f"break-c5-{name}.txt").write_text(out, encoding="utf-8")
        lines = [l for l in out.splitlines() if "×" in l or "Tests " in l]
        print(f"break {name}: exit {run.returncode}")
        for l in lines[:8]: print("   ", l.strip())
    finally:
        shutil.copyfile(backup, path)
        print("   restored", filecmp.cmp(backup, path, shallow=False))
