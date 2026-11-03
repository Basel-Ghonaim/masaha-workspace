import io
import os

os.chdir(r'C:\dev\masaha\app-b\apps\api\src')


def edit(path, reps):
    s = io.open(path, encoding='utf-8', newline='').read()
    for a, b in reps:
        assert s.count(a) == 1, (path, a[:90])
        s = s.replace(a, b)
    io.open(path, 'w', encoding='utf-8', newline='').write(s)


edit('app.ts', [
('''} from './modules/announcements/index.ts';
import {
  createAuthController,''', '''} from './modules/announcements/index.ts';
import {
  createAuditController,
  createAuditManageRouter,
  createAuditService,
} from './modules/audit/index.ts';
import {
  createAuthController,'''),
('''  const adminUsers = createAdminUsersService({ users, spaces });
''', '''  const auditLog = createAuditService({ now: clock });
  const adminUsers = createAdminUsersService({ users, spaces });
'''),
('''  manage.use('/staff', createStaffManageRouter({ staff: createStaffController(staff), limiter }));
''', '''  manage.use('/staff', createStaffManageRouter({ staff: createStaffController(staff), limiter }));
  const auditController = createAuditController(auditLog);
  manage.use('/audit-log', createAuditManageRouter(auditController));
'''),
])
print('ok')
