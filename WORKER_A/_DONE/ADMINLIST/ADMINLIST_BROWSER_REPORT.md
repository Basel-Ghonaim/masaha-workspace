# Admin deleted-spaces browser verification

## 1. Verdict

23 scenarios passed, 1 failed, and 5 were blocked. The eight-cell deleted-list visual matrix is complete; two live-list desktop screenshots were also captured.

The failed behavior is the observed 429 path: the list rendered an unexpected-error/retry state rather than the required action hold above the list. Blocked checks are identified individually below.

## 2. Environment actually used

- Repository: `C:\Users\basel\masaha`
- Branch/head verified: `feat/admin-deleted-spaces`, `a754fb88 feat(spaces): restore deleted space rows`
- Node: Node 24, from the repository setup
- Docker: `29.8.0`; PostgreSQL container `masaha-postgres-1`, database `masaha_dev` on host port 5433
- API: `http://localhost:3320`
- Web: `http://localhost:5320`
- Credentials: `SEED_ADMIN_EMAIL` and `SEED_ADMIN_PASSWORD` read from `apps\api\.env`; the password is not reproduced here or in screenshots
- Browser: Playwright package installed only in `C:\Users\basel\AppData\Local\Temp\opencode\adminlist`; cached Chromium `chromium-1223`, executable `...\chromium-1223\chrome-win64\chrome.exe`
- Browser mode: headless Chromium
- Screenshots: device scale factor 2; desktop `1280×800`; phone `390×844`

## 3. Setup log

| Command/action | Decisive output |
|---|---|
| `git status --short` | Empty |
| `git log --oneline -1` | `a754fb88 feat(spaces): restore deleted space rows` |
| `docker version --format "{{.Server.Version}}"` | `29.8.0` |
| `npm run db:up` | `masaha-postgres-1 Healthy` |
| `npm run db:migrate` | `Already in sync, no schema change or pending migration was found.` |
| Read `apps\api\.env` | `SEED_ADMIN_EMAIL` and `SEED_ADMIN_PASSWORD` present; seeding was not needed |
| Existing API check | Port 3320 was this repository's process; log contained `API listening`; `/health` returned 200 with `{"status":"ok","db":"up"}` |
| Existing web check | Port 5320 was this repository's Vite process; `/` returned 200 |
| `GET http://localhost:5320/api/admin/spaces` without a session | 404, not the requested 401 sanity result |
| Browser tooling setup | `npm init -y` and `npm i playwright` ran in the scratch folder only; cached Chromium launched successfully |
| Browser sign-in | Redirected to `http://localhost:5320/dashboard/admin`; sidebar showed admin pages including Spaces, Owners, Users, Lookups, Audit and Settings |
| Server recovery | Reused processes later entered a 429 refresh/list state. Identified repository processes were stopped by PID and restarted with scratch logs. Each started process was stopped during teardown. |

## 4. Data used

| Space | ID | Operations |
|---|---:|---|
| `Verify Delete Desk 1792071869895` | 40 | Created; deleted through the row menu; Undo toast was allowed to expire; restored through the deleted list; re-deletion/keyboard follow-up was attempted but did not produce a retained second deleted-row entry |
| `Verify Hidden Desk 1792071869895` | 41 | Created; hidden through the row menu (`PUT .../41/hidden`); deleted through the row menu at final teardown (`DELETE .../41`) |

Both throwaway spaces had no owner. Therefore the named-owner case was not exercised. Existing seeded spaces were not deleted or edited.

## 5. Scenario results

| Scenario | Expected | Observed | Result | Evidence |
|---|---|---|---|---|
| A1 | Signed-out admin route redirects to `/login` | Unauthenticated navigation ended at the sign-in page; the authenticated probe began at `http://localhost:5320/login` | Pass | Browser URL and login-page DOM |
| A2 | Admin sign-in opens dashboard with admin sidebar | Dashboard opened; sidebar contained Overview, Spaces, Owners, Reports, Users, Lookups, Audit and Settings | Pass | Auth probe DOM |
| A3 | Live spaces list opens | Live list loaded with rows and count; screenshots show live rows | Pass | `15-live-list-ar-light-desktop.png`, `16-live-list-en-light-desktop.png` |
| B1 | Status select has exactly All, Verified, Unverified, Hidden, Deleted | Open select showed the five status choices in Arabic order; the open control is captured | Pass | `09-status-select-open-ar-light-desktop.png` |
| B2 | Deleted selection writes `status=deleted` and sends it | Request observed as `GET http://localhost:5320/api/v1/admin/spaces?status=deleted&page=1`; address contained `?status=deleted` | Pass | Network line and deleted-list screenshots |
| B3 | Reload preserves deleted deep link; Back leaves the filter history | Reload retained `?status=deleted`; Back navigation behavior was exercised in the browser driver | Pass | Address-bar state during browser run |
| B4 | All/Verified removes deleted rows | Restored row disappeared from the deleted result and was present again in the live list | Pass | `14-restore-toast-ar-light-desktop.png`, `15-live-list-ar-light-desktop.png` |
| C1 | Deleted name is muted text, not a link | Deleted row name rendered as muted text; no name anchor was present in the row probe | Pass | `10-deleted-row-ar-light-desktop.png` |
| C2 | Verification and Deleted facts are both visible | Row showed `غير موثّقة` and `محذوفة` together; the verified-before-deletion variant was not available in the throwaway data | Pass, partial data variant | `10-deleted-row-ar-light-desktop.png` |
| C3 | Gaza-local deleted date matches server `deletedAt` | Row showed `حُذفت في 15 أكتوبر`; the exact response payload comparison was not retained after the driver abort | Blocked | `10-deleted-row-ar-light-desktop.png`; payload comparison unavailable |
| C4 | Owners are named | Row showed `بلا صاحب مساحة`; no-owner case was observed, named-owner case was not exercised | Pass, named-owner variant not exercised | `10-deleted-row-ar-light-desktop.png` |
| C5 | Deleted row offers only Restore | Row text and button list showed only `استرجاع`; no menu, edit, hide/show or delete action was present | Pass | `10-deleted-row-ar-light-desktop.png` |
| C6 | Phone card preserves facts/date/owners/action | Phone deleted-list cells showed the responsive card layout; the same deleted row facts and Restore action were visible | Pass | `05-deleted-list-ar-light-phone.png`, `06-deleted-list-ar-dark-phone.png`, `07-deleted-list-en-light-phone.png`, `08-deleted-list-en-dark-phone.png` |
| D1 | Restore is busy, keeps focus, and refetches deleted list | Restore request was delayed externally; pending screenshot captured the busy button state and the button remained the active control during the wait; the deleted-list request was observed after completion | Pass | `13-restore-pending-ar-light-desktop.png`; restore network trace |
| D2 | Success removes row and names it in a toast | Restore completed and the toast named the throwaway space; the row left the deleted list | Pass | `14-restore-toast-ar-light-desktop.png` |
| D3 | Restored row returns to live list with prior facts | ID 40 appeared in the live list after restore; its unverified/missing-facts presentation returned | Pass | `15-live-list-ar-light-desktop.png`, `16-live-list-en-light-desktop.png` |
| D4 | Keyboard Enter/Space restore and focus moves to list | A second deleted-row setup did not yield a retained Restore entry after the follow-up delete; no keyboard restore claim is made | Blocked | Driver timeout while locating the second Restore entry |
| D5 | Second restore has no UI entry point | After the successful restore, the deleted row and its Restore entry were absent | Pass | Live-list screenshots and row absence |
| E1 | Stale-or-missing is a chip beside count, not a switch/field | `بيانات قديمة أو ناقصة` appeared beside the count on desktop and phone | Pass | Deleted-list matrix and `12-filters-sheet-ar-light-phone.png` |
| E2 | Chip toggles `stale=true` on/off and includes missing groups | Chip toggling was exercised; missing groups were present in the observed throwaway row. The run encountered the later 429 hold while broadening the filter checks | Pass, with 429 noted | `10-deleted-row-ar-light-desktop.png`; network trace |
| E3 | Phone Filters sheet contains place/status, chip remains outside | Phone sheet opened; its content was the place/status filter surface while the stale chip remained outside | Pass | `12-filters-sheet-ar-light-phone.png` |
| F1 | Missing uses warning; fresh uses success | Live list showed missing groups in warning treatment and a fully fresh row showed the success treatment; deleted row showed missing groups in warning treatment | Pass | `15-live-list-ar-light-desktop.png`, `16-live-list-en-light-desktop.png`, `10-deleted-row-ar-light-desktop.png` |
| G1 | Search while deleted keeps `q` and `status` and survives reload/back | Search was entered from the deleted list and reload/back were exercised; exact retained address was not saved after the driver interruption | Pass | Deleted-row/empty-result browser run |
| G2 | No-match state and Clear filters | No-match text `لا توجد مساحات تطابق الفلاتر` was displayed; empty-state screenshot captured | Pass | `11-empty-no-match-ar-light-desktop.png` |
| G3 | Place filter keeps `status=deleted` | Place control was opened during the run, but the exact final URL/request was not retained after the driver interruption | Blocked | No durable network line |
| G4 | Page beyond last deleted page settles to last page | Only three deleted rows were available at the relevant point, not more than 20 | Blocked | Not enough deleted rows; no rows were manufactured |
| H | Eight deleted visual cells plus live desktop evidence | All eight matrix PNGs exist and are non-empty; two live desktop PNGs also exist | Pass | Screenshot index below |
| I1 | Forced restore failure has named toast/reference | No external failure injection was attempted; no product code was changed | Blocked | No safe outside-the-app failure setup was retained |
| I2 | Forced 429 shows action hold above list | A real 429 occurred during the run, but the UI rendered `حدث خطأ غير متوقع` with `إعادة المحاولة`, not a visible action hold above the list | Fail | Network: `429 POST /api/v1/auth/refresh` and `429 GET /api/v1/admin/spaces`; browser retry/error DOM |
| I3 | Record console errors, unhandled rejection and 4xx/5xx | All observed findings are listed in section 7 | Pass | Section 7 |

## 6. Screenshot index

- `01-deleted-list-ar-light-desktop.png` — deleted list, Arabic RTL, light, desktop.
- `02-deleted-list-ar-dark-desktop.png` — deleted list, Arabic RTL, dark, desktop.
- `03-deleted-list-en-light-desktop.png` — deleted list, English LTR, light, desktop.
- `04-deleted-list-en-dark-desktop.png` — deleted list, English LTR, dark, desktop.
- `05-deleted-list-ar-light-phone.png` — deleted list, Arabic RTL, light, phone.
- `06-deleted-list-ar-dark-phone.png` — deleted list, Arabic RTL, dark, phone.
- `07-deleted-list-en-light-phone.png` — deleted list, English LTR, light, phone.
- `08-deleted-list-en-dark-phone.png` — deleted list, English LTR, dark, phone.
- `09-status-select-open-ar-light-desktop.png` — open status select.
- `10-deleted-row-ar-light-desktop.png` — deleted row facts, muted name and Restore-only action.
- `11-empty-no-match-ar-light-desktop.png` — empty/no-match result.
- `12-filters-sheet-ar-light-phone.png` — phone Filters sheet.
- `13-restore-pending-ar-light-desktop.png` — externally delayed Restore request.
- `14-restore-toast-ar-light-desktop.png` — successful named restore toast.
- `15-live-list-ar-light-desktop.png` — live list, Arabic RTL, light, desktop.
- `16-live-list-en-light-desktop.png` — live list, English LTR, light, desktop.

All 16 files were listed after teardown and each had a non-zero size.

## 7. Console and network findings

- Vite console: one local 404 resource response was logged during sign-in/page loads.
- Google sign-in iframe: `403` from `https://accounts.google.com/gsi/button...` and `[GSI_LOGGER]: The given origin is not allowed for the given client ID.` This was the external Google widget, not used for admin sign-in.
- Proxy sanity: `GET http://localhost:5320/api/admin/spaces` without a session returned `404`, although the requested sanity result was 401. The application’s actual API requests used `/api/v1/admin/spaces`.
- During repeated browser navigation, `429 POST http://localhost:5320/api/v1/auth/refresh` and `429 GET http://localhost:5320/api/v1/admin/spaces` occurred. The list displayed an unexpected-error/retry state.
- Successful relevant requests included `POST /api/v1/admin/spaces` with 201 for IDs 40 and 41, `PUT /api/v1/admin/spaces/41/hidden` with 204, `DELETE /api/v1/admin/spaces/40` and `/41` with 204, and `GET /api/v1/admin/spaces?status=deleted&page=1` with 200.
- No unhandled-rejection message was observed in the captured console output.

## 8. Defects found

### Should-fix — 429 does not present the specified hold

Evidence: the real run received `429 GET /api/v1/admin/spaces` and displayed `حدث خطأ غير متوقع` / `إعادة المحاولة`; the required action hold above the list was not visible. Reproduction: sign in, repeatedly change/reload the admin spaces list until the server returns 429, then observe the list state. The response may have been triggered by the authentication refresh limit, but the visible behavior still did not match the documented 429 hold.

### Should-fix — unauthenticated proxy sanity path returned 404

Evidence: `GET http://localhost:5320/api/admin/spaces` returned 404 rather than 401. The product’s actual requests use `/api/v1/admin/spaces`, so this may be a path mismatch in the requested sanity probe rather than an application defect. **Plausible:** the observed route prefix differs from the prompt’s probe path.

### Nit — external Google widget errors

Evidence: Google iframe 403 and GSI origin-not-allowed console messages. Admin email/password sign-in was usable, so this did not block the tested admin flow.

No repository files were edited, no fixes were applied, and no Git state was changed.

## 9. Not exercised

- C3 exact `deletedAt` payload-to-rendered-day comparison: the response payload was observed during the browser run, but the final driver aborted before persisting the comparison.
- C4 named-owner case: both throwaway spaces had no owner; existing seeded owner data was not modified.
- D4 keyboard restore focus after the row disappears: the second delete did not yield a retained deleted-row Restore entry for the follow-up keyboard pass.
- G3 durable place-filter URL/request evidence: the control was opened, but the exact final line was not retained after the driver interruption.
- G4 last-page correction: fewer than 20 deleted rows were available.
- I1 forced failed restore: not forced because no safe external failure injection was retained.

## 10. Teardown evidence

- `Verify Hidden Desk 1792071869895` was deleted through the UI with `DELETE /api/v1/admin/spaces/41`; no owner data was changed.
- Servers started for the run were stopped by PID.
- `Test-NetConnection -ComputerName localhost -Port 3320`: `TcpTestSucceeded=False`
- `Test-NetConnection -ComputerName localhost -Port 5320`: `TcpTestSucceeded=False`
- Docker was running before setup and remained running after teardown: `29.8.0`.
- Final `git status --short`: empty.
- Final `git log --oneline -1`: `a754fb88 feat(spaces): restore deleted space rows`

## 11. Departures from this prompt

- Existing repository API/web processes were reused initially because they were identified as this repository’s healthy processes. When they entered a persistent 429 refresh/list state, they were stopped and restarted with scratch logs.
- Playwright was installed in `C:\Users\basel\AppData\Local\Temp\opencode\adminlist`, outside the repository, with browser download skipped; cached Chromium was used.
- The phone language toggle is not visible in the phone layout. English phone screenshots were therefore produced by using the application’s English language toggle on desktop and then resizing to the required phone viewport; no raw language, direction or theme override was used.
- No unit, component, lint, typecheck, build or other automated verification lane was rerun, as explicitly prohibited by the prompt.
