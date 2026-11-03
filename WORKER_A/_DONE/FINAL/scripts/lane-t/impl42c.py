p = r'C:\dev\masaha\app-lane-t\apps\web\scripts\checkBuild.ts'
s = open(p, encoding='utf8').read()
def rep(old, new):
    global s
    assert s.count(old) == 1, old
    s = s.replace(old, new, 1)
rep("import { DASHBOARD_CHUNK, isDashboardModule } from './dashboardOnly.ts';",
    "import { DASHBOARD_CHUNK, DASHBOARD_SHARED_CHUNK, isDashboardModule } from './dashboardOnly.ts';")
rep("""/** Whether a chunk holds dashboard code: the dashboard's chunk, or a chunk made from its module. */
function isDashboardChunk(chunk: ManifestChunk | undefined): boolean {
  return (
    chunk?.name === DASHBOARD_CHUNK || (chunk?.src !== undefined && isDashboardModule(chunk.src))
  );
}""", """/**
 * Whether a chunk holds dashboard code: the dashboard's chunk, the chunk of what only the dashboard
 * imports, or a chunk made from a dashboard module.
 */
function isDashboardChunk(chunk: ManifestChunk | undefined): boolean {
  return (
    chunk?.name === DASHBOARD_CHUNK ||
    chunk?.name === DASHBOARD_SHARED_CHUNK ||
    (chunk?.src !== undefined && isDashboardModule(chunk.src))
  );
}""")
open(p, 'w', encoding='utf8', newline='').write(s)
