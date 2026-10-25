import pathlib
p = pathlib.Path(r"C:\dev\masaha\app\apps\web\src\features\desk\repository\deskRepository.unit.test.ts")
s = p.read_text(encoding="utf-8")
add = '''
  it('reads the uncollected visits’ page, and sends a payment, a debt, a write-off and its undo', async () => {
    const repository = createDeskRepository();
    const requests = serve((url) =>
      url === '/manage/spaces/7/uncollected-visits'
        ? {
            status: 200,
            data: {
              success: true,
              data: [{ visit: VISIT, paidAgorot: 0, balanceAgorot: 2500 }],
              meta: { currentPage: 2, pageSize: 20, totalRecords: 21, totalPages: 2 },
            },
          }
        : { status: 200, data: { success: true, data: VISIT } },
    );

    await expect(repository.uncollected(7, 2)).resolves.toEqual({
      data: [{ visit: VISIT, paidAgorot: 0, balanceAgorot: 2500 }],
      meta: { currentPage: 2, pageSize: 20, totalRecords: 21, totalPages: 2 },
    });
    await repository.receivePayment(
      7,
      { visitId: 12, amountAgorot: 1000, method: 'CASH', phone: '+970599000303' },
      'key-3',
    );
    await repository.leaveToCustomer(7, 12, { phone: '+970599000303', customerName: 'Omar' });
    await repository.writeOff(7, 12, { reason: 'Left the country' });
    await repository.undoWriteOff(7, 12);

    expect(requests.map(({ method, url }) => `${String(method)} ${String(url)}`)).toEqual([
      'get /manage/spaces/7/uncollected-visits',
      'post /manage/spaces/7/payments',
      'put /manage/spaces/7/visits/12/customer',
      'post /manage/spaces/7/visits/12/write-off',
      'delete /manage/spaces/7/visits/12/write-off',
    ]);
    expect(requests[0]?.params).toEqual({ page: 2 });
    expect(bodyOf(requests[1])).toEqual({
      visitId: 12,
      amountAgorot: 1000,
      method: 'CASH',
      phone: '+970599000303',
    });
    expect(bodyOf(requests[2])).toEqual({ phone: '+970599000303', customerName: 'Omar' });
    expect(bodyOf(requests[3])).toEqual({ reason: 'Left the country' });
    // A payment carries its key; «تسجيل دين», the write-off and its undo carry none (S3).
    expect(requests.map(({ headers }) => headers.get('Idempotency-Key'))).toEqual([
      undefined,
      'key-3',
      undefined,
      undefined,
      undefined,
    ]);
  });
'''
marker = "  it('hands back a check-in’s warnings, and none without them'"
assert marker in s
s = s.replace(marker, add.lstrip('\n') + '\n' + marker, 1)
p.write_text(s, encoding="utf-8", newline="")
