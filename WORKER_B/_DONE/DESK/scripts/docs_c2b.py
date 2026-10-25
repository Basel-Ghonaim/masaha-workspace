import io, os
os.chdir('C:/dev/masaha/app-b')


def sub(p, old, new):
    s = io.open(p, encoding='utf-8', newline='').read()
    assert s.count(old) == 1, (p, old[:60], s.count(old))
    io.open(p, 'w', encoding='utf-8', newline='').write(s.replace(old, new))


sub('docs/api/api-contract.md', "([security › Rate limits](../backend/security.md#rate-limits))",
    "([security › Rate limits](../backend/security.md#rate-limits-fixed-window))")
sub('docs/project/overview.md',
    "and a price typed by hand with its reason ([visits](../features/visits.md), [payments](../features/payments.md)).",
    "and a price typed by hand with its reason; the auto check-out of open stays at their due time ([visits](../features/visits.md), [payments](../features/payments.md)).")
m = 'docs/plans/v1-mvp.md'
sub(m, "a visit's quote and the desk's terms (#95, [api-contract › Front desk (managed)](../api/api-contract.md#front-desk-managed)); the rest of the step remains planned.",
    "a visit's quote and the desk's terms (#95, [api-contract › Front desk (managed)](../api/api-contract.md#front-desk-managed)); the auto check-out of open visits and subscription check-ins at their due time, run every 5 minutes (#PRNUM, [api-contract › Internal](../api/api-contract.md#internal)); the rest of the step remains planned.")
sub(m, "- **Settles:** the auto check-out scheduling mechanism, within ADR 0014.",
    "- **Settles:** the auto check-out scheduling mechanism, within ADR 0014. Done (#PRNUM): an in-process timer locally, and online an external cron calling a secret-protected endpoint ([conventions §12](../backend/conventions.md#12-environments-and-adapters)).")
print('ok')
