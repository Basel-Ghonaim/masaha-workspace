p = r'C:\dev\masaha\app-lane-t\apps\web\vite.config.ts'
s = open(p, encoding='utf8').read()
def rep(old, new):
    global s
    assert s.count(old) == 1, old
    s = s.replace(old, new, 1)
rep("import { DASHBOARD_CHUNK, isDashboardModule } from './scripts/dashboardOnly.ts';",
    "import {\n  DASHBOARD_CHUNK,\n  DASHBOARD_SHARED_CHUNK,\n  isDashboardModule,\n  isDashboardShared,\n} from './scripts/dashboardOnly.ts';")
rep("""export default defineConfig(({ mode }) => ({""", """// What only the dashboard imports, answered once per module for a build (isDashboardShared).
const dashboardShared = new Map<string, boolean>();

export default defineConfig(({ mode }) => ({""")
rep("""            ...LIBRARY_CHUNKS.map(({ name, test }) => ({
              name,
              test,
              includeDependenciesRecursively: false,
            })),
""", """            ...LIBRARY_CHUNKS.map(({ name, test }) => ({
              name,
              test,
              includeDependenciesRecursively: false,
            })),
            // What only the dashboard imports besides its own code (a capability's dashboard parts,
            // @masaha/shared's dashboard schemas, TanStack Query's useQuery), in a chunk the
            // dashboard loads beside it: left to the bundler, it lands in a lazy dashboard page's
            // chunk, which then imports the dashboard's chunk back (finding 27). Last, so the groups
            // above take their modules first; what it takes imports no dashboard code, so the chunk
            // never imports the dashboard's back, which check:build proves.
            {
              name: (id, { getModuleInfo }) =>
                isDashboardShared(id, getModuleInfo, dashboardShared)
                  ? DASHBOARD_SHARED_CHUNK
                  : null,
              includeDependenciesRecursively: false,
            },
""")
open(p, 'w', encoding='utf8', newline='').write(s)
