p = r'C:\dev\masaha\app-lane-t\apps\web\scripts\dashboardOnly.ts'
s = open(p, encoding='utf8').read()
old = """
export type ModuleGraph = (
  id: string,
) => { importers: readonly string[]; dynamicImporters: readonly string[] } | null;

export function isDashboardShared(
  _id: string,
  _graph: ModuleGraph,
  _known: Map<string, boolean>,
): boolean {
  return false;
}
"""
new = """
/** A module's importers, static and lazy, by its id, as the bundler knows them; null if unknown. */
export type ModuleGraph = (
  id: string,
) => { importers: readonly string[]; dynamicImporters: readonly string[] } | null;

/** The name of the chunk that holds what only the dashboard imports, besides its own code. */
export const DASHBOARD_SHARED_CHUNK = 'dashboard-shared';

/**
 * Whether a module, not dashboard code itself, is imported by the dashboard alone (finding 27): each
 * chain of its static importers ends in dashboard code, and none of them is loaded lazily, an entry
 * or unknown. Such a module has no other place: left to the bundler, it lands in a lazy dashboard
 * page's chunk, which then imports the dashboard's chunk and is imported by it. `known` keeps each
 * answer by id, so a build asks each module once.
 */
export function isDashboardShared(
  id: string,
  graph: ModuleGraph,
  known: Map<string, boolean>,
): boolean {
  const answer = known.get(id) ?? (!isDashboardModule(id) && importedByDashboardAlone(id, graph, known));
  known.set(id, answer);
  return answer;
}

/** Whether every chain of `id`'s static importers ends in dashboard code, none of them lazy. */
function importedByDashboardAlone(
  id: string,
  graph: ModuleGraph,
  known: Map<string, boolean>,
): boolean {
  const seen = new Set<string>();
  const pending = [id];
  for (let next = pending.pop(); next !== undefined; next = pending.pop()) {
    if (seen.has(next) || isDashboardModule(next) || known.get(next) === true) {
      continue;
    }
    seen.add(next);
    const info = graph(next);
    if (
      known.get(next) === false ||
      info === null ||
      info.importers.length === 0 ||
      info.dynamicImporters.length > 0
    ) {
      return false;
    }
    pending.push(...info.importers);
  }
  return true;
}
"""
assert s.count(old) == 1
s = s.replace(old, new, 1)
open(p, 'w', encoding='utf8', newline='').write(s)

p = r'C:\dev\masaha\app-lane-t\apps\web\scripts\checkBuild.ts'
s = open(p, encoding='utf8').read()
old = """export function dashboardCycleProblems(_manifest: Record<string, ManifestChunk>): string[] {
  return [];
}
"""
new = """/**
 * What is wrong with what the dashboard imports (finding 27): each chunk the dashboard's chunk
 * reaches through its static imports, deeply, that imports the dashboard's chunk back. Such a cycle
 * holds only while every use across it waits inside a function; a module-level use would fail when
 * the chunk is the first one loaded.
 */
export function dashboardCycleProblems(manifest: Record<string, ManifestChunk>): string[] {
  const dashboard = Object.keys(manifest).find((key) => manifest[key]?.name === DASHBOARD_CHUNK);
  if (dashboard === undefined) {
    return [];
  }
  return staticReach(manifest, manifest[dashboard]?.imports ?? [])
    .filter((key) => key !== dashboard && (manifest[key]?.imports ?? []).includes(dashboard))
    .map((key) => `${key} imports the dashboard chunk (${dashboard}), which imports it.`);
}
"""
assert s.count(old) == 1
s = s.replace(old, new, 1)
old = """  const problems = manifest
    ? dashboardProblems(manifest)
    : [`${MANIFEST} does not exist: the build writes no manifest.`];"""
new = """  const problems = manifest
    ? [...dashboardProblems(manifest), ...dashboardCycleProblems(manifest)]
    : [`${MANIFEST} does not exist: the build writes no manifest.`];"""
assert s.count(old) == 1
s = s.replace(old, new, 1)
old = """The site's first download must not reach the dashboard (ADR 0011): look for a static import of dashboard code outside the dashboard.`,"""
new = """The site's first download must not reach the dashboard (ADR 0011): look for a static import of dashboard code outside the dashboard. No chunk the dashboard imports may import it back (finding 27): look for what only the dashboard imports that the dashboard-shared group no longer takes.`,"""
assert s.count(old) == 1
s = s.replace(old, new, 1)
old = """    console.log("No dashboard code in the site's first download.");"""
new = """    console.log(
      "No dashboard code in the site's first download, and no chunk the dashboard imports imports it back.",
    );"""
assert s.count(old) == 1
s = s.replace(old, new, 1)
open(p, 'w', encoding='utf8', newline='').write(s)
