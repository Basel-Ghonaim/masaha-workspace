p='apps/api/src/db/seed/run.ts'
s=open(p,encoding='utf-8',newline='').read()
start=s.index("const optional = ")
end=s.index("const parsed = envSchema")
s=s[:start]+s[end:]
s=s.replace("const parsed = envSchema.safeParse","const parsed = seedEnvSchema.safeParse")
s=s.replace("import { passwordSchema } from '@masaha/shared/users';\nimport { z } from 'zod';\n\n","")
s=s.replace("import { seed } from './seed.ts';\n","import { seed } from './seed.ts';\nimport { seedEnvSchema } from './seedEnv.ts';\n")
open(p,'w',encoding='utf-8',newline='').write(s)
