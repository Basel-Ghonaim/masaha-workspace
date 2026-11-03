def edit(p, pairs):
    s = open(p, encoding='utf8').read()
    for old, new in pairs:
        assert s.count(old) == 1, (p, old)
        s = s.replace(old, new)
    open(p, 'w', encoding='utf8', newline='').write(s)
R = r'C:\dev\masaha\app-lane-a1\apps\api'
edit(R + r'\src\modules\users\users.service.ts', [("import { createSessionsService, type SessionsService } from '../sessions/index.ts';", "import type { SessionsService } from '../sessions/index.ts';")])
edit(R + r'\src\modules\space-links\admin-spaces\adminSpaces.api.test.ts', [
("import { accessTokens, createTestApp } from '../../../../test/app.ts';", "import { accessTokens, createTestApp, TEST_JWT_SECRET } from '../../../../test/app.ts';"),
("import { createPlatformSettingsService } from '../../platform-settings/index.ts';\n", "import { createPlatformSettingsService } from '../../platform-settings/index.ts';\nimport { createSessionsService, successorKeyOf } from '../../sessions/index.ts';\n"),
("""    receptionSpaceOf: () => Promise.resolve(null),
  }),""", """    receptionSpaceOf: () => Promise.resolve(null),
    sessions: createSessionsService({ successorKey: successorKeyOf(TEST_JWT_SECRET), now: clock }),
  }),"""),
])
