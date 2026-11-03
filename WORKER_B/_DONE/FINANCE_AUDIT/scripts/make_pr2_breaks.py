import json
PS='apps/api/src/modules/platform-settings/'
T1=PS+'adminSettings.api.test.ts'
src=lambda p:'src/modules/platform-settings/'+p
b=[
 dict(id='B1',file='packages/shared/src/platform-settings/requests.ts',old='const days = z.int().min(1).max(STALENESS_DAYS_MAX);',new='const days = z.int().min(1);',lane='shared',test='src/platform-settings/requests.unit.test.ts'),
 dict(id='B2',file='packages/shared/src/space-settings/requests.ts',old='  .superRefine(roundingPair);\nexport type NewSpaceDefaults',new='  ;\nexport type NewSpaceDefaults',lane='shared',test='src/space-settings/requests.unit.test.ts',name='takes the four defaults'),
 dict(id='B3',file=PS+'settingsChange.ts',old='.filter((field) => becomes[field] !== was[field]);',new='.filter(() => true);',lane='unit',test=src('settingsChange.unit.test.ts')),
 dict(id='B4',file=PS+'platform-settings.service.ts',old='          if (isOptional(key)) return [key, null];\n',new='',lane='api',test=src('adminSettings.api.test.ts'),name='the admin reads each card'),
 dict(id='B5',file=PS+'platform-settings.service.ts',old='      if (!change) return card.fromValues(stored);\n',new='',lane='api',test=src('adminSettings.api.test.ts'),name='each card saves on its own'),
 dict(id='B6',file=PS+'platform-settings.service.ts',old='          await repository.write(key, values[key], tx);',new="          if (key !== 'newSpaceDefaults') await repository.write(key, values[key], tx);",lane='api',test=src('adminSettings.api.test.ts'),name='a saved default is copied'),
 dict(id='B7',file=PS+'platform-settings.repository.ts',old='        ORDER BY "key" FOR UPDATE`;',new='        ORDER BY "key"`;',lane='api',test=src('adminSettings.api.test.ts'),name='two saves of one card at once'),
 dict(id='B8',file=PS+'platform-settings.service.ts',old='      await repository.ensure(card.keys.filter(isOptional), tx);\n',new='',lane='api',test=src('adminSettings.api.test.ts'),name='two first saves of the contact'),
 dict(id='B9',file='apps/api/src/app.ts',old="  admin.use('/settings', createPlatformSettingsAdminRouter(platformSettingsController));\n",new='',
      edits=[["  admin.use('/settings', createPlatformSettingsAdminRouter(platformSettingsController));\n",""],
             ["  api.use('/settings', createPlatformSettingsPublicRouter(platformSettingsController));\n","  api.use('/settings', createPlatformSettingsPublicRouter(platformSettingsController));\n  api.use('/admin/settings', createPlatformSettingsAdminRouter(platformSettingsController));\n"]],
      lane='api',test=src('adminSettings.api.test.ts'),name='on the six routes'),
 dict(id='B10',file=PS+'platform-settings.controller.ts',old='      res.set(\'Cache-Control\', `public, max-age=${String(PUBLIC_CONTACT_MAX_AGE_SECONDS)}`);\n',new='',lane='api',test=src('publicContact.api.test.ts'),name='anyone reads the contact'),
 dict(id='B11',file=PS+'platform-settings.service.ts',old='        return [key, schemaOf(key).parse(row.value)];',new='        return [key, row.value];',lane='api',test=src('publicContact.api.test.ts'),name='fails its schema'),
 dict(id='B12',file='apps/api/src/modules/audit/platformEvents.ts',old="  'platformSettings.newSpaceDefaultsEdited',\n  'platformSettings.stalenessEdited',\n  'platformSettings.contactEdited',\n",new='',lane='api',test='src/modules/audit/platformAuditLog.api.test.ts',name='settings actions'),
]
json.dump(b,open('pr2-breaks.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
