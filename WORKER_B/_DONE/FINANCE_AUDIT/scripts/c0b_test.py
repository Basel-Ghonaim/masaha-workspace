import io
import os

os.chdir(r'C:\dev\masaha\app-b\apps\api\src\modules\subscriptions\closures')


def edit(path, reps):
    s = io.open(path, encoding='utf-8', newline='').read()
    for a, b in reps:
        assert s.count(a) == 1, (path, a[:90])
        s = s.replace(a, b)
    io.open(path, 'w', encoding='utf-8', newline='').write(s)


edit('extension.api.test.ts', [
('''  key: string | null = randomUUID(),
) {
  const call = request(app)
    .post(pathOf(announcementId))''', '''  key: string | null = randomUUID(),
  space = spaceId,
) {
  const call = request(app)
    .post(pathOf(announcementId, space))'''),
("""another key is CLOSURE_ALREADY_EXTENDED; a key that extended another closure is a conflict', async () => {""",
 """another key is CLOSURE_ALREADY_EXTENDED; a key that extended another closure, or another space's, is a conflict', async () => {"""),
('''    expect(errorOf(reused).code).toBeUndefined();

    expect((await endsById()).get(covered.through.id)).toBe('2026-12-04');''', '''    expect(errorOf(reused).code).toBeUndefined();

    // Another space's owner, on their own space's URL, with this closure's id and its key.
    const otherOwner = await signInOwnerOf(otherSpaceId);
    const crossed = await extend(otherOwner, id, { days: 4 }, key, otherSpaceId);
    expect(crossed.status).toBe(409);
    expect(errorOf(crossed)).toMatchObject({ type: 'conflict' });
    expect(errorOf(crossed).code).toBeUndefined();
    expect(crossed.body).not.toHaveProperty('data');

    expect((await endsById()).get(covered.through.id)).toBe('2026-12-04');'''),
])
print('ok')
