def sub(p, pairs):
    s = open(p, encoding='utf8', newline='').read()
    for a, b in pairs:
        assert s.count(a) == 1, (p, a)
        s = s.replace(a, b)
    open(p, 'w', encoding='utf8', newline='').write(s)

sub('src/shared/jobs/jobs.api.test.ts', [(
"""    expect(await stored()).toMatchObject({
      checkedOutAt: new Date('2026-10-17T23:59:00+03:00'),
      checkoutMethod: 'AUTO',
    });
  });
});
""",
"""    expect(await stored()).toMatchObject({
      checkedOutAt: new Date('2026-10-17T23:59:00+03:00'),
      checkoutMethod: 'AUTO',
    });
  });

  it('a run whose failures fill the batch answers 500, the job named stalled in the log, the others still run', async () => {
    // The one due visit cannot be closed: a charge past the column's range fails its transaction.
    await prisma.visit.update({ where: { id: visitId }, data: { hourRateAgorot: 2_000_000_000 } });
    const { logger, lines } = recordingLogger();

    const response = await request(withSecret(logger))
      .post(RUN)
      .set('Authorization', `Bearer ${SECRET}`);

    expect(response.status).toBe(500);
    expect(errorOf(response).type).toBe('server');
    expect(lines.filter(({ msg }) => msg === 'job stalled')).toMatchObject([
      { level: 50, job: 'visits.autoCheckOut', failed: 1 },
    ]);
    expect(lines.filter(({ msg }) => msg === 'job ran')).toMatchObject([
      { job: 'visits.autoCheckOut', visits: 0, failed: 1, stalled: true },
      { job: 'subscriptions.autoCheckOut', checkIns: 0, failed: 0 },
    ]);
    expect(await stored()).toMatchObject({ checkedOutAt: null });
  });
});
""")])

sub('src/shared/jobs/jobs.unit.test.ts', [(
"""      jobs: [{ name: 'runs', done: { stays: 1, failed: 2 } }],
      failed: false,
    });
  });
});
""",
"""      jobs: [{ name: 'runs', done: { stays: 1, failed: 2 } }],
      failed: false,
      stalled: false,
    });
  });

  it('a run with one stalled job still runs the others, and is stalled, logged by name', async () => {
    const { logger, lines } = recordingLogger();
    const jobs = createJobs({
      jobs: [
        { name: 'stalls', run: () => Promise.resolve({ stays: 0, failed: 3, stalled: true }) },
        { name: 'runs', run: () => Promise.resolve({ stays: 2, failed: 0 }) },
      ],
      now: () => RAN_AT,
      logger,
    });

    expect(await jobs.run()).toEqual({
      ranAt: '2026-10-18T16:00:00.000Z',
      jobs: [
        { name: 'stalls', done: { stays: 0, failed: 3, stalled: true } },
        { name: 'runs', done: { stays: 2, failed: 0 } },
      ],
      failed: false,
      stalled: true,
    });
    expect(lines.filter(({ msg }) => msg === 'job stalled')).toMatchObject([
      { level: 50, job: 'stalls', failed: 3 },
    ]);
  });
});
"""),
("""        { name: 'runs', done: { stays: 2, failed: 0 } },
      ],
      failed: true,
    });""",
"""        { name: 'runs', done: { stays: 2, failed: 0 } },
      ],
      failed: true,
      stalled: false,
    });""")])
