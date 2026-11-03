# Lane W4 — the sub-agent's report (returned as text; saved by the lead)

Lane W4 · DONE but C9.4's WhatsApp line («لا يمكنك الوصول إلى بريدك؟» → wa.me) and T264, which need W2's C6.4
`usePlatformContact` (not yet on feat/final; the line still leads to /about#contact). Branch lane/w4 head 1ac69a7b (base
0a1979e1, rebased from 4550b5b2, no conflict).

Commits (order differs from §9.1: C9.2, C9.3, C9.6 after the rebase): 3ea6a4a0 refactor(users): one folder per operation
(41) · 40082337 fix(auth): keep next and the way back (37) · 1db98216 feat(forms): say when a password is too long (44) ·
fec9fec4 fix(site): announce a second retry while offline (48) · f1244db7 fix(site): finish Home and About (32) ·
328b289f fix(directory): finish the map and the results (46) · 5ab5b2de fix(directory): draw the marks as on light tiles
(48) · 6b12df8b fix(directory): wait for near me once permitted (47) · aca6d2ee fix(directory): hide area counts past the
pins (46) · 800a9c51 fix(directory): finish the space page (37) · 4016a64a fix(site): retry the route and give the 403 a
way (49) · 8d0144fe fix(favorites): show the list's line once ready (47) · c55e830a test(site): pin the footer, the areas
and the pick (50) · 301e520b feat(auth): welcome a first Google sign-in (42) · ab2fef6b feat(users): edit one's own
account (35) · 1ac69a7b feat(auth): keep a guest's action through a reset (49).

Red/green (outputs `scripts/lane-w4/`): C9.1 moves only (first tests of SiteLayout, SiteAccount, authPages,
changePasswordPage timed out at 3 s alone — finding 87, files untouched) · C9.4 red `c94-red.txt` (15 tests: "names the
way back to the space next points to", "offers another email under the resend at once", "welcomes the account back") ·
C9.5 B265 (counted in characters), B266 (4 rules on a short password) · C9.7 [] ≠ ['', 'ما زال الاتصال مفقودًا.'] · C9.8
T272 'المساحات الأقرب إليك' ≠ 'متاحة الآن', T274 both searches (maxLength 61 under a mocked constant), B273, B271, B275,
B275b, the About-focus break · C9.9 T276, T277, T279, T280 (off called 2 times; marks not the same array), B278 · C9.10
leaflet.css unit test (rule undefined), MapMarkSample and MarkerMap data-theme · C9.11 the prompt test ('denied' ≠
'locating'), the denied test, B282, B283 · C9.12 T284 · C9.13 six tests red · C9.14 three red · C9.15 five red · C9.16
B296, B297, B298, the range break · C9.3 T257, T258 · C9.2 code first, B250–B256 and B-accountEdited red (B254 green at
first → a test "a password account without Google shows no Google row" added, then red) · C9.6 code first, B267–B270 red.

Heavy checks (grant, 2026-10-31): typecheck 0 (tc3, tc4, tc5); lint whole 0 (lint5; lint3 had 4 errors in its tests,
fixed); unit web 165 / 1109; unit shared 28 / 277; component whole 314 files, 2 failed | 1855 passed — useAreaFilter's
expectation lacked `held` (its own, folded into C9.9; lookups 143/143), dashboard routes › "lists the owner's twelve
pages" 3,083 ms (finding 87, alone green); check:classes 1731 clean; check:links 3147.

Shared files: `shared/routing/index.ts` (RETURN_TOAST_ID, returnUrlOf, sitePage, the held-intent functions) ·
architecture §4 (held intent), §2 (RouteErrorState's retry, RequireRole's bare 403) · `docs/project/overview.md`
Directory line (carried 9) · foundation leaflet.css clause · copy forms, lookups, status, dataReports (new keys) ·
`shared/map/{PlaceMap,LeafletPlaceMap}` (the user mark, G3.3).

Findings closed: 82, 133, 134, 135, 136, 137, 138, 168, 32 (web half).

Decisions (none SERIOUS): LW4-D1 the WhatsApp line deferred (fold into C9.4 once W2 is joined) · LW4-D2 the held intent a
union (favourite {spaceId, name, path, at}; report {slug, path, at}), path from `sitePage()` · LW4-D3 a held action's
toast replaces the welcome back by one id `RETURN_TOAST_ID` (favoriteToasts.tsx edited) · LW4-D4 the route retry marks
`masaha.retried` in the location's state, re-runs by navigating to the same address with replace · LW4-D5 carried 11's
scroll needed no code (`page` from the answer); T278/B278 pin it · LW4-D6 with nothing saved the count is hidden, DI-52's
last focus target «تصفّح المساحات» · LW4-D7 the set-password link has no resend countdown; CURRENT_PASSWORD_INCORRECT
shows as the form's failure · LW4-D8 the stale age as of the last failed try · LW4-D9 near me's 'prompt' waits for
'granted' or an answer (Firefox's dismissed prompt to check in the real run) · LW4-D10 the bare 403 hardcodes '/' and
'/about#contact' in shared/routing · LW4-D11 About and Home tests warm their lazy modules in beforeAll.

Left out: T264 and C9.4's WhatsApp line. Commits split from one tree by staging lines, so typecheck/lint ran on the
whole tree, not per commit. Notes: real run R26 (dark marks), R27 (typing on the map), Firefox near-me prompt;
vite.config's unit lane empties `leaflet.css?raw`, so its test reads the file through `process.getBuiltinModule`.
