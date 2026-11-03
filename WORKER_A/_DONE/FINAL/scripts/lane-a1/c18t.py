p = r'C:\dev\masaha\app-lane-a1\apps\api\src\modules\space-links\admin-users\adminUsers.api.test.ts'
s = open(p, encoding='utf8').read()
old = """  it('refuses an unknown role or state', async () => {"""
new = """  it('the users list’s email filter keeps the exact account only', async () => {
    await account('Maha', { role: 'OWNER', joined: '2026-02-01' });
    await account('Maha Saleh', { joined: '2026-03-01' });

    const exact = await list('?email=%20MAHA%40Example.com%20');
    expect(names(exact.rows)).toEqual(['Maha']);
    expect(exact.meta.totalRecords).toBe(1);
    expect(names((await list('?email=maha%40example.com&role=owner')).rows)).toEqual(['Maha']);
    expect((await list('?email=maha%40example.com&role=user')).rows).toEqual([]);
    const malformed = await adminRequest(app, admin, 'get', '/users?email=maha');
    expect(malformed.status).toBe(422);
    expect(errorOf(malformed).errors).toEqual({ email: ['invalid_format'] });
    expect((await list('?email=saleh%40example.com')).rows).toEqual([]);
  });

""" + old
assert s.count(old) == 1
s = s.replace(old, new)
open(p, 'w', encoding='utf8', newline='').write(s)
