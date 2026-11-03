for rel, extra_import in [(r'src\app\App.component.test.tsx', True), (r'src\app\router.component.test.tsx', False)]:
    import os; p = os.path.join('C:/dev/masaha/app-lane-t/apps/web', rel.replace(chr(92), '/'))
    s = open(p, encoding='utf8').read()
    i = s.index("beforeAll(\n  () =>\n    warm(")
    end = "  60_000,\n);\n"
    j = s.index(end, i)
    s = s[:i] + "beforeAll(() => warm(...routeLoaders(routes, '/')), 60_000);\n" + s[j+len(end):]
    s = s.replace("import { warm } from '../test/warmLazy';", "import { routeLoaders, warm } from '../test/warmLazy';", 1)
    if extra_import:
        s = s.replace("import { bootstrap } from './bootstrap';\n", "import { bootstrap } from './bootstrap';\nimport { routes } from './router';\n", 1)
    open(p, 'w', encoding='utf8', newline='').write(s)
