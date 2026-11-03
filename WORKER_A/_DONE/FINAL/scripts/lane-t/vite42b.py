p = r'C:\dev\masaha\app-lane-t\apps\web\vite.config.ts'
s = open(p, encoding='utf8').read()
old = """              name: (id, { getModuleInfo }) =>
                isDashboardShared(id, getModuleInfo, dashboardShared)
                  ? DASHBOARD_SHARED_CHUNK
                  : null,"""
new = """              name: (id, context) =>
                isDashboardShared(id, (module) => context.getModuleInfo(module), dashboardShared)
                  ? DASHBOARD_SHARED_CHUNK
                  : null,"""
assert s.count(old) == 1
s = s.replace(old, new, 1)
open(p, 'w', encoding='utf8', newline='').write(s)
