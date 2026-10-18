Decision on placeOf: move it to its own file, pages/dashboard/placeOf.ts,
and add 'placeOf.ts' to ROUTE_DEFINITIONS in scripts/dashboardOnly.ts, with
its rule test updated. It draws nothing, so it belongs with the route
definitions. Fold it into `refactor(dashboard): one responsibility per file`
(fixup + autosquash, --force-with-lease); the list change goes in the commit
that owns ROUTE_DEFINITIONS. Run check:build, then report once CI is green
on the new head.

The flaky dashboard routes test: if it is a lazy page timing out under load,
record it as a finding (one line, its symptom); do not change the test.

Size cap: no subagents, no workflows.
