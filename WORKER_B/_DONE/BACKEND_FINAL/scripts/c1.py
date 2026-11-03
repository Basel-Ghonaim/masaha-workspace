import re
p='apps/api/src/modules/platform-settings/publicContact.api.test.ts'
s=open(p,encoding='utf-8').read()
s=s.replace("import { dataOf, errorOf } from '../../../test/admin.ts';","import { adminRequest, dataOf, errorOf, signIn } from '../../../test/admin.ts';")
s=s.replace("""  it('a stored contact that fails its schema""","""  it('a contact stored in another form is answered as stored, to anyone and to the admin', async () => {
    await prisma.setting.createMany({
      data: [
        { key: 'contactEmail', value: 'Hello@Masaha.PS' },
        { key: 'contactWhatsapp', value: '+972591234567' },
      ],
    });
    const asStored = { email: 'Hello@Masaha.PS', whatsapp: '+972591234567' };

    const anyone = await contact();
    expect(anyone.status).toBe(200);
    expect(dataOf(anyone)).toEqual(asStored);

    const admin = await signIn('ADMIN');
    const card = await adminRequest(app, admin, 'get', '/settings/contact');
    expect(card.status).toBe(200);
    expect(dataOf(card)).toEqual(asStored);
  });

  it('a stored contact that fails its schema""")
open(p,'w',encoding='utf-8',newline='').write(s)

p='apps/api/src/modules/platform-settings/adminSettings.api.test.ts'
s=open(p,encoding='utf-8').read()
anchor="  it('a saved default is copied into the next space only"
assert anchor in s
s=s.replace(anchor,"""  it('saving a contact stored in another form stores its one form, audited from the stored to the saved', async () => {
    await prisma.setting.createMany({
      data: [
        { key: 'contactEmail', value: 'Hello@Masaha.PS' },
        { key: 'contactWhatsapp', value: '+972591234567' },
      ],
    });

    const saved = await card('put', 'contact', {
      email: 'Hello@Masaha.PS',
      whatsapp: '+972591234567',
    });

    expect(saved.status).toBe(200);
    expect(dataOf(saved)).toEqual({ email: 'hello@masaha.ps', whatsapp: '+970591234567' });
    expect(await stored()).toMatchObject({
      contactEmail: 'hello@masaha.ps',
      contactWhatsapp: '+970591234567',
    });
    expect(await auditEntries()).toEqual([
      {
        actorId: admin.id,
        action: 'platformSettings.contactEdited',
        entityType: 'platformSettings',
        entityId: null,
        spaceId: null,
        before: { email: 'Hello@Masaha.PS', whatsapp: '+972591234567' },
        after: { email: 'hello@masaha.ps', whatsapp: '+970591234567' },
      },
    ]);
  });

"""+anchor,1)
open(p,'w',encoding='utf-8',newline='').write(s)
