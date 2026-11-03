import re
def edit(p, pairs):
    s = open(p, encoding='utf8').read()
    for old, new in pairs:
        assert s.count(old) == 1, (p, old)
        s = s.replace(old, new)
    open(p, 'w', encoding='utf8', newline='').write(s)
R = r'C:\dev\masaha\app-lane-a1\apps\api'
edit(R + r'\src\modules\sessions\index.ts', [("export { createSessionsService, type Recovery, type SessionsService } from './sessions.service.ts';",
 "export { createSessionsService, type Recovery, type SessionsService } from './sessions.service.ts';\nexport { successorKeyOf } from './tokens.ts';")])
edit(R + r'\src\app.ts', [("""  createSessionsService,
} from './modules/sessions/index.ts';""", """  createSessionsService,
  successorKeyOf,
} from './modules/sessions/index.ts';"""),
 ("  const sessions = createSessionsService({ now: clock });", """  // A refresh token's successor is named under a key of its own, derived from the secret (S7).
  const sessions = createSessionsService({ successorKey: successorKeyOf(jwtSecret), now: clock });""")])
edit(R + r'\src\modules\users\users.service.ts', [("  sessions?: SessionsService;\n", "  sessions: SessionsService;\n"),
 ("  sessions = createSessionsService(),\n", "  sessions,\n")])
