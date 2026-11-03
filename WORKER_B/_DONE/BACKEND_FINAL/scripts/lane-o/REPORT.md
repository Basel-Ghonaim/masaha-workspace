# Lane O — report (returned as text, saved by the lead)

Lane O: DONE · SERIOUS: none · lane/o head 32fcd35f on b0cd0ae4 (after the join and the lead's fold: 51f35f90,
b1ac98a4, 798f4708, d7e626d3).

Commits: 786cba71 feat(api): count what the owner's overview shows (48) · cbaaf3e0 feat(overview): read the owner's
overview (41) · 59c10b4d feat(api): count what the admin's overview shows (48) · 32fcd35f feat(overview): read the
admin's overview (41).

Tests red before code (TypeError … is not a function / expected 404 to be 200), then green: C8 U-O1 15/15, T-M1–T-M6
29/29; C9 T-O1–T-O6 6/6; C10 U-O2 7/7, T-M7–T-M10, listingQuery editable 11/11; C11 T-O7–T-O11 9/9 (T-O11's refusals
green before the route — /admin's guard — proven by B-O10).
Breaks (restored by copy, green after): B-O1 "expected 1 to be 2"; B-M1; B-M2 "expected 4 to be 2"; B-M3 "expected 3 to
be 2"; B-M4 "total 7 vs 6"; B-M5 ['CLOSURE','OFFER','EVENT']; B-M6; B-O3 (temporary payments edit) T-O1 red; B-O4
/agorot/i; B-O5 "expected 'FULL' to be 'AVAILABLE'"; B-O6; B-O7 "expected 200 to be 403"; B-O8 6 red 401; B-O2
'2026-10-11T08:00Z' vs '…21:00Z'; B-M7 "unverified 3 vs 2"; B-M8 "total 8 vs 7"; B-M9 "open 4 vs 3"; B-M10 "expected 1
to be 2"; B-O9 "newUsers 3 vs 2"; B-O10 refusals 200. B-M3/B-M5 stay green on T-O2 by design (one const; T-M3/T-M5 catch).

EC5 freshnessOf on the listing service (findPage by id, saved thresholds). EC8 endingSoon through customers.page (the
list's own rule, archived out). EC9 failed: hasPhotos dropped. EC11 listing const (in C9). EC14 files as listed.

Decisions: (1) OD3's `editable` in a second shared schema (ADMIN_SPACES_STATUSES / adminSpacesListQuerySchema): widening
the one schema breaks the web's typecheck, apps/web off-limits — finding 158 (Open); (2) endingSoon names through
customers.page; (3) glance(space, at?) and present.countsIn; (4) ListedSpace.stale with a pure freshness(); (5) T-O2
built the payments service in-test (the lead replaced it); (6) openCounts three counts in parallel; (7) listingQueryOf
Partial; (8) T-O3 case-insensitive; (9) nine sources, no figure missing.

Heavy runs (grants): lint 0; typecheck 0; test:unit 26/268, 73/893, 157/1075; test:api 107 files / 1292 tests (853 s).
No kill.

Docs: api-contract *Overview* (after Audit log; GroupsFreshness, OwnerOverview, AdminOverview), *Admin spaces* status
`editable`; conventions §7 overview row, §9 overview; security two bullets; foundation §13 screen 12 (OV8);
overview.md new; Behaviour + Who-uses-it lines in spaces, data-reports, visits, subscriptions, announcements,
occupancy, space-links, users; finding 158.
C16: v1-mvp step 12 Built, /admin/stats → GET /admin/overview (OD4), a GET …/overview row; overview.md Built Overview;
docs/README.md map overview.md; conventions Built: overview, lastDaysSince. Worker A: no «بدون صور» (EC9).
