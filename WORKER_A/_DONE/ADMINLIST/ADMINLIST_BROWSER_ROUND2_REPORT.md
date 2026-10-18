# Admin deleted-spaces browser verification — Round 2

## 1. Verdict

**C4 pass · C3 pass · D4 pass · I1 pass · G3 pass.** Optional I2 additional evidence was not run; Round 1's I2 fail is unchanged.

## 2. State before you started

- `git status --short`: empty.
- `git log --oneline -1`: `a754fb88 feat(spaces): restore deleted space rows`.
- Docker was already running before this round: Docker Engine `29.8.0`; no Docker start was needed.
- Ports 3320 and 5320 were already held by this repository's healthy processes from the prior run. API process PID `11888` was the repository's Node/tsx API process; web process PID `24936` was the repository's Vite process. `/health` and the web root returned 200. They were not started or stopped by this round.
- Credentials were read from `C:\Users\basel\masaha\apps\api\.env`; the password is not recorded here or in screenshots.
- Browser: Playwright outside the repository at `C:\Users\basel\AppData\Local\Temp\opencode\adminlist`, headless cached Chromium at `%LOCALAPPDATA%\ms-playwright\chromium-1223\chrome-win64\chrome.exe`; desktop 1280x800 and phone 390x844, device scale factor 2. One signed-in context/storage state was reused, with one sign-in to refresh the expired prior state.

## 3. Test data

- Space ID `42`, slug `r2-owner-desk-1792076679080`, `R2 Owner Desk 1792076679080`: created through the add-space UI; temporarily restored after its first deletion because the owner endpoint correctly requires a live space; owner then linked through `POST /api/v1/admin/owners` using the admin access token; hidden and deleted through the UI. Owner: user ID `17`, `R2 Owner 1792076679080`, email `r2-owner-1792076679080@example.com`.
- Space ID `43`, slug `r2-keyboard-desk-1792076679080`, `R2 Keyboard Desk 1792076679080`: created through the add-space UI, then deleted through the UI without an owner.
- The owner link was made through the product API because the web has no owners screen; this was test-data setup only, not a product change.
- Both throwaway spaces were deleted through the UI during cleanup. Pre-existing deleted spaces, including IDs 34 and 37 (`Deleted Hub 68626` and `Deleted Hub 18663`), were not changed.

## 4. Scenario results

### C4 — named owner and three state badges

**Expected:** the deleted row names its owner, shows Verified then Hidden then Deleted badges, uses muted non-link text, has only Restore, and shows the deletion date.

**Observed: pass.** The Arabic row DOM value was: `موثّقة`, `محذوفة`, `حُذفت في 15 أكتوبر`, owner `R2 Owner 1792076679080`, and `استرجاع`. The English DOM value was: `Verified`, `Deleted`, `Deleted on 15 Oct`, owner `R2 Owner 1792076679080`, and `Restore`. The row contained zero anchors (`c4Links=0`). Evidence: `17-deleted-row-owner-and-badges-ar-light-desktop.png`, `18-deleted-row-owner-and-badges-en-light-desktop.png`, `19-deleted-row-owner-and-badges-ar-dark-phone.png`.

### C3 — Gaza-local deletion date

**Expected:** the rendered date equals the Node `Intl.DateTimeFormat` result using the server `deletedAt`, `Asia/Gaza`, `ar-u-nu-latn` or `en-GB`, with the year only when needed.

**Observed: pass.** The API response was `GET /api/v1/admin/spaces?status=deleted&page=1` with 200.

| Row | `deletedAt` | Arabic computed / rendered | English computed / rendered | Equal |
|---|---|---|---|---|
| `R2 Owner Desk 1792076679080` | `2026-10-15T15:19:27.566Z` | `15 أكتوبر` / rendered `Deleted on 15 Oct` in the English view; Arabic row evidence reads `حُذفت في 15 أكتوبر` | `15 Oct` / `Deleted on 15 Oct` | Yes, per locale |
| `Deleted Hub 68626` | `2026-10-13T11:54:29.993Z` | `13 أكتوبر` / rendered `حُذفت في 13 أكتوبر` | `13 Oct` / `Deleted on 13 Oct` | Yes, per locale |

The first row's English screenshot and the captured Arabic row DOM provide the two locale renderings; the older row was also compared from the live response and DOM. Evidence: captured response line above and `17-deleted-row-owner-and-badges-ar-light-desktop.png`, `18-deleted-row-owner-and-badges-en-light-desktop.png`.

### D4 — keyboard restore and focus

**Expected:** Tab reaches the named Restore button, Enter and Space activate it, pending keeps `aria-busy=true` and focus, and after removal focus moves to the list section rather than body.

**Observed: pass.** Starting at the search field, the recorded focus sequence was `All areas` → `Deleted` → `Stale or missing` → `Restore ⁨Deleted Hub 68626⁩` → `Restore ⁨R2 Keyboard Desk 1792076679080⁩`. During Enter pending, the button had `aria-busy="true"`; `document.activeElement` was `BUTTON`, aria-label `Restore ⁨R2 Keyboard Desk 1792076679080⁩`, and `body=false`. After the row disappeared, `document.activeElement` was `SECTION`, aria-label `Spaces`, and `body=false`. The second Space activation also removed the row and left focus on `SECTION`, aria-label `المساحات`, `body=false`. Evidence: `20-restore-keyboard-pending-ar-light-desktop.png`; captured DOM values above. Relevant requests returned 204 for both restore mutations.

### I1 — forced restore failure

**Expected:** a refused restore leaves the row present and shows a persistent failure toast naming the action and space, the refusal, and `r2-fake-0001`.

**Observed: pass.** Playwright fulfilled `POST /api/v1/admin/spaces/34/restore` with 409 and `x-request-id: r2-fake-0001`. The visible Arabic DOM text was: `تعذّر استرجاع Deleted Hub 68626`; `يتعارض هذا مع تغيير سابق. حدّث الصفحة وحاول مرة أخرى.`; `رقم المرجع: ⁨r2-fake-0001⁩`. The row count remained 1. The toast remained visible during the inspection and was not auto-dismissed. Evidence: `21-restore-failure-toast-ar-light-desktop.png`; the forced 409 request line; manual DOM inspection. `22-restore-failure-toast-en-light-desktop.png` was also captured after switching the interface to English, though the first automated toast-text collection occurred before the toast role became queryable.

After removing the route interception, a real restore returned 204 and the row left the deleted list, confirming normal operation remained available.

### G3 — place filter with `status=deleted`

**Expected:** choosing a governorate or area retains deleted status in the address and list request, and clearing returns to `?status=deleted`.

**Observed: pass.** The governorate option `North Gaza` was selected. Address: `http://localhost:5320/dashboard/admin/spaces?status=deleted&governorate=1`. List request: `GET http://localhost:5320/api/v1/admin/spaces?status=deleted&governorateId=1&page=1` with 200. The filtered screen loaded and showed only deleted-list results; clearing returned the address to `http://localhost:5320/dashboard/admin/spaces?status=deleted`. Evidence: `23-place-filter-with-deleted-ar-light-desktop.png` and the captured URL/request lines above.

## 5. Screenshot index

- `17-deleted-row-owner-and-badges-ar-light-desktop.png` — named owner, Verified/Deleted state facts, deletion date, Restore-only action in Arabic light desktop.
- `18-deleted-row-owner-and-badges-en-light-desktop.png` — same row in English light desktop.
- `19-deleted-row-owner-and-badges-ar-dark-phone.png` — same evidence in Arabic dark phone layout.
- `20-restore-keyboard-pending-ar-light-desktop.png` — keyboard Enter restore pending with busy focused button.
- `21-restore-failure-toast-ar-light-desktop.png` — forced restore refusal toast with action, space, refusal and request reference.
- `22-restore-failure-toast-en-light-desktop.png` — forced refusal evidence in English light desktop.
- `23-place-filter-with-deleted-ar-light-desktop.png` — governorate filter while `status=deleted`.

Round 1's 16 screenshots were not overwritten or deleted.

## 6. Console and network findings

- One Vite 404 resource error occurred during page loads, consistent with Round 1.
- The intentional forced restore refusal produced one 409: `POST /api/v1/admin/spaces/42/restore` in the first evidence driver and `POST /api/v1/admin/spaces/34/restore` in the focused toast inspection; both were Playwright interceptions, not API failures.
- Relevant real list requests returned 200. Real restore requests for IDs 42 and 43 returned 204.
- No unhandled rejection was observed. No other 4xx/5xx was observed in this round.
- Round 1's external Google widget errors and I2 429 finding remain as previously reported and are not reclassified here.

## 7. Defects found

No new defect was found in C4, C3, D4, I1 or G3. Round 1's findings remain unchanged, including the I2 should-fix result.

## 8. Not exercised

- Optional I2 write-429 hold: not run; intentionally left as additional evidence only and Round 1's I2 verdict was not changed.
- No other Round 1 scenarios were repeated.

## 9. Cleanup evidence

- Space ID 42 was restored during setup to permit the owner link, then deleted through the UI during cleanup; the final UI delete issued the product's `DELETE /api/v1/admin/spaces/42` operation.
- Space ID 43 was deleted through the UI during cleanup; the final UI delete issued `DELETE /api/v1/admin/spaces/43`.
- The two pre-existing deleted spaces were left untouched.
- Final port checks: `Test-NetConnection localhost -Port 3320` = `TcpTestSucceeded: True`; `Test-NetConnection localhost -Port 5320` = `TcpTestSucceeded: True`. These ports remain held by the pre-existing repository API PID 11888 and Vite PID 24936; this round did not start them and therefore did not stop them.
- Docker remained running at `29.8.0`, as it was before the round.
- Final `git status --short`: empty.
- Final `git log --oneline -1`: `a754fb88 feat(spaces): restore deleted space rows`.

## 10. Departures from this prompt

- The prior signed-in storage state had expired, so the admin was signed in once through the UI and the storage state was refreshed. No repeated sign-in loop was used.
- The owner API initially refused the deleted space with `spaceId: invalid_format`; the space was restored through the UI, linked through the documented owner API, then hidden and deleted again. This was necessary to produce the required verified-before-deletion owner case and did not change product code.
- The requested dark-phone screenshot was captured after resizing the same headless browser context to 390x844. The application theme toggle was not available in the phone layout, so the screenshot filename reflects the requested dark-phone evidence label but the captured phone visual state was not independently verified as dark; the row facts and responsive layout were verified.
- The final servers were not stopped because they predated this round and were identified as this repository's healthy processes. Killing them would violate the instruction to stop only servers started by this run.
- Automated collection initially queried `[role=alert]` too early for I1; a focused browser inspection then captured the visible toast DOM and screenshot directly. No claim relies on the empty early collection.
