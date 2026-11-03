p = r'C:\dev\masaha\app-lane-a1\apps\api\src\modules\users\users.service.unit.test.ts'
s = open(p, encoding='utf8').read()
n = s.count("{ userId: 3, link: false }")
s = s.replace("{ userId: 3, link: false }", "{ userId: 3, link: false, created: false }")
old = """    expect(await found(null).accountForGoogle(google, undefined)).toEqual({
      userId: 3,
      link: true,
    });"""
assert s.count(old) == 1
s = s.replace(old, """    expect(await found(null).accountForGoogle(google, undefined)).toEqual({
      userId: 3,
      link: true,
      created: false,
    });""")
old = """  it('ends every session when it links, and none when the link was already made', async () => {"""
assert s.count(old) == 1
s = s.replace(old, """  it('says it created the account it creates', async () => {
    const { users } = setup({
      findByGoogleSubject: () => Promise.resolve(null),
      findByEmail: () => Promise.resolve(null),
      create: () => Promise.resolve({ account: sara }),
    });

    expect(await users.accountForGoogle(google, 'en')).toEqual({
      userId: 3,
      link: false,
      created: true,
    });
  });

""" + old)
open(p, 'w', encoding='utf8', newline='').write(s)
print(n)
p = r'C:\dev\masaha\app-lane-a1\apps\api\src\modules\auth\google.api.test.ts'
s = open(p, encoding='utf8').read()
old = """  it('creates one account when two first sign-ins race', async () => {"""
assert s.count(old) == 1
s = s.replace(old, """  it("Google's answer says created for a new account, not for a linked one", async () => {
    await createAccount({ email: 'sara@gmail.com' });

    const created = await signInWithGoogle('newcomer');
    const again = await signInWithGoogle('newcomer');
    const linked = await signInWithGoogle('gmail');

    expect(created.body).toMatchObject({ data: { created: true, linked: false } });
    expect(again.body).toMatchObject({ data: { created: false, linked: false } });
    expect(linked.body).toMatchObject({ data: { created: false, linked: true } });
  });

""" + old)
open(p, 'w', encoding='utf8', newline='').write(s)
