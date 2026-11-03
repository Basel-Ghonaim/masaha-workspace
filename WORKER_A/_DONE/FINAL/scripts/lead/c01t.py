def edit(p, old, new):
    s=open(p,encoding='utf8').read(); assert old in s, (p, old[:50]); s=s.replace(old,new,1)
    open(p,'w',encoding='utf8',newline='').write(s)
p='apps/api/src/shared/errors/errorHandler.api.test.ts'
edit(p, """router.get('/bug', () => {""", """router.get('/owned', () => {
  throw AppError.conflict('ALREADY_OWNER', undefined, undefined, { userId: 7 });
});
router.get('/bug', () => {""")
edit(p, """  it('answers an unknown route under /api/v1 with not_found', async () => {""", """  it('carries the details of a refusal that names a record', async () => {
    const response = await request(app).get('/api/v1/owned');

    expect(response.status).toBe(409);
    expect(response.body).toEqual({
      success: false,
      error: {
        type: 'conflict',
        code: 'ALREADY_OWNER',
        message: 'Conflict',
        details: { userId: 7 },
        requestId: response.headers['x-request-id'],
      },
    });
  });

  it('answers an unknown route under /api/v1 with not_found', async () => {""")
p='apps/web/src/shared/errors/toAppError.unit.test.ts'
edit(p, """  it('drops a domain code the client does not know', () => {""", """  it('keeps the record a refusal names, in the contract’s shape only', () => {
    const named = toAppError(
      failed({
        status: 409,
        data: envelope({ type: 'conflict', code: 'ALREADY_OWNER', details: { userId: 7 } }),
      }),
    );
    const malformed = toAppError(
      failed({ status: 409, data: envelope({ type: 'conflict', details: { userId: '7' } }) }),
    );

    expect(named.details).toEqual({ userId: 7 });
    expect(malformed.details).toBeUndefined();
  });

  it('drops a domain code the client does not know', () => {""")
