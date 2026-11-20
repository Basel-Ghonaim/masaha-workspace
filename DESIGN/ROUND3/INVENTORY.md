# Round 3 — the inventory

Built 2026-11-13T14:46 UTC by `tools\r3-inventory.mjs` at the head `4cff26c7de4ea1b4b8454ad48f1f440b9a0ae84b`. The routes come from the route files at that head (`apps/web/src/pages/site/routes.tsx`, `pages/dashboard/routes.tsx`, `pages/dashboard/navigation.ts`, `pages/site/navigation.ts`); the states from three read-only surveys of the source and the database copy (`tools\survey-site.md`, `survey-space.md`, `survey-admin.md`).

**Captured:** every base × 390 / 768 / 1440 × ar / en × light / dark (a state that exists at some widths only, such as a phone menu, at those). 390 and 768 are emulated as touch (coarse pointer); 1440 as a mouse.

**How a state is reached:** by address; by steps (clicks, typing, keys, by the catalogue's words in each language); a request held (loading); a failure or a 429 answered by the capture tool at the network layer (simulated, the contract's envelope, `Retry-After: 60`); a request answered with mocked data (an empty list, a recovery position); a real answer patched (one field set, one item added); the location granted or refused. Nothing a capture does writes to the database: every write a state needs is a **named state** (below), done before the capture.

## 1. Routes → screens → parts

| Route | Shell | Screen (foundation §13) | Part | Roles |
|---|---|---|---|---|
| `/` | site | 1 Home | PU | visitor, user |
| `/spaces` | site | 2 Directory (list; `?view=map` the map) | PU | visitor, user |
| `/spaces/:slug` | site | 3 Space details | PU | visitor, user |
| `/about` | site | 4 About / Contact | PU | visitor, user |
| `/privacy` | site | 33 Privacy policy | PU | visitor, user |
| `*` (site) | site | 8 404 | PU | visitor, user |
| `/login` | focus | 5 Sign in | AU | visitor |
| `/register` | focus | 6 Register | AU | visitor |
| `/forgot-password` | focus | 7 Forgot password | AU | visitor |
| `/reset-password#token=…` | focus | 7 Reset password | AU | anyone |
| `/change-password` | focus (sign-out only) | 9 (the forced change) | AU | user with a temporary password |
| `/me` | site › account | 9 Profile & settings | AU | user (any signed-in role) |
| `/me/favorites` | site › account | 10 Favourites | AU | user |
| `/me/reports` | site › account | 11 My reports | AU | user |
| `/dashboard` | none (redirect) | — the landing: to the admin, the owner's overview or reception's desk | SH | owner, reception, admin |
| `/dashboard/spaces/:id` | space dashboard | 12 Overview (O) | OW | owner |
| `/dashboard/spaces/:id/desk` | space dashboard | 13 Front desk (O+R) | DK | owner, reception |
| `/dashboard/spaces/:id/customers` | space dashboard | 14 Customers (O+R) | DK | owner, reception |
| `/dashboard/spaces/:id/customers/:customerId` | space dashboard | 15 Customer details (O+R); 16 New subscription opens from it and the desk | DK | owner, reception |
| `/dashboard/spaces/:id/payments` | space dashboard | 17 Payments (O: the ledger) | OW | owner |
| `/dashboard/spaces/:id/my-payments` | space dashboard | 17 Payments (R: my payments today) | DK | reception |
| `/dashboard/spaces/:id/finance` | space dashboard | 19 Finance & statistics (O) | OW | owner |
| `/dashboard/spaces/:id/packages` | space dashboard | 21 Prices & packages (O) | OW | owner |
| `/dashboard/spaces/:id/profile` | space dashboard | 20 Space profile (O) | OW | owner |
| `/dashboard/spaces/:id/announcements` | space dashboard | 18 Announcements (O+R) | OW (owner) · DK (reception's view) | owner, reception |
| `/dashboard/spaces/:id/reports` | space dashboard | 23 Data reports (O) | OW | owner |
| `/dashboard/spaces/:id/staff` | space dashboard | 22 Staff (O) | OW | owner |
| `/dashboard/spaces/:id/audit` | space dashboard | 31 Audit log (the owner's, O13) | OW | owner |
| `/dashboard/spaces/:id/settings` | space dashboard | 24 Settings (O) | OW | owner |
| `/dashboard/spaces/:id/*` | space dashboard | 404 / 403 inside the shell | SH | owner, reception |
| `/dashboard/admin` | admin dashboard | 25 Overview | AD | admin |
| `/dashboard/admin/spaces` | admin dashboard | 26 Spaces | AD | admin |
| `/dashboard/admin/spaces/new` | admin dashboard | 26 Spaces (add) | AD | admin |
| `/dashboard/admin/spaces/:spaceId` | admin dashboard | 26 Spaces (the editor; 27 linking an owner from it) | AD | admin |
| `/dashboard/admin/owners` | admin dashboard | 27 Space owners | AD | admin |
| `/dashboard/admin/reports` | admin dashboard | 28 Data reports | AD | admin |
| `/dashboard/admin/users` | admin dashboard | 29 Users | AD | admin |
| `/dashboard/admin/lookups` | admin dashboard | 30 Lookups | AD | admin |
| `/dashboard/admin/audit` | admin dashboard | 31 Audit log (the admin's) | AD | admin |
| `/dashboard/admin/settings` | admin dashboard | 32 Settings | AD | admin |
| `/dashboard/admin/*` | admin dashboard | 404 inside the shell | SH | admin |
| `/__showcase[/<category>[/<slug>]]` | development only | the design system (foundation §3, §12) | SH | anyone, development |

Shared by every part, judged by **SH**: the site header, the phone menu and the footer; the focus shell; the dashboard's sidebars, rail, drawer, top bar and account menu; toasts, dialogs and Sheets; loading, empty, failure, offline, 403 and 404 states; the identity across the product.

## 2. The base states, by part

### PU — 30 bases

| ID | Screen | State | Role | URL | How | Widths |
|---|---|---|---|---|---|---|
| PU-01 | 1 Home | default (guest) | visitor | `/` | by address | 390, 768, 1440 |
| PU-02 | 1 Home | signed in: account in the header, saved hearts | user | `/` | by address | 390, 768, 1440 |
| PU-03 | 1 Home | nearest to me, location granted in Gaza City | visitor | `/` | 1 step · location granted | 390, 768, 1440 |
| PU-04 | 1 Home | nearest to me, location refused | visitor | `/` | 1 step · location refused | 390, 768, 1440 |
| PU-05 | 2 Directory (list) | default | visitor | `/spaces` | by address | 390, 768, 1440 |
| PU-06 | 2 Directory (list) | a subscription chosen, sorted by its price (prices on the cards) | visitor | `/spaces?period=MONTH&sort=priceAsc` | by address | 390, 768, 1440 |
| PU-07 | 2 Directory (list) | filters bottom sheet open, an area and a subscription on | visitor | `/spaces?filters=open&area=2&period=MONTH` | by address | 390, 768 |
| PU-08 | 2 Directory (list) | no results (search) | visitor | `/spaces?q=zzzz` | by address | 390, 768, 1440 |
| PU-09 | 2 Directory (list) | page 2 of 3 | visitor | `/spaces?page=2` | by address | 390, 768, 1440 |
| PU-10 | 2 Directory (map) | default, every pin | visitor | `/spaces?view=map` | by address | 390, 768, 1440 |
| PU-11 | 2 Directory (map) | a space chosen on the map (card ≥768, bottom sheet <768) | visitor | `/spaces?view=map` | 2 steps | 390, 768, 1440 |
| PU-12 | 2 Directory (map) | placing my location by hand (after a refused location) | visitor | `/spaces?view=map` | 2 steps · location refused | 390, 768, 1440 |
| PU-13 | 3 Space details | verified, 4 photos, a running offer (Pal Hub) | visitor | `/spaces/pal-hub` | by address | 390, 768, 1440 |
| PU-14 | 3 Space details | verified, live status FULL (answer patched), hours in 3 groups, phone only | visitor | `/spaces/radwan-study-hall` | patched */api/v1/spaces/radwan-study-hall/occupancy | 390, 768, 1440 |
| PU-15 | 3 Space details | unverified, stale prices hidden, owners' notice | visitor | `/spaces/freelancers-house` | by address | 390, 768, 1440 |
| PU-16 | 3 Space details | a running closure | visitor | `/spaces/shati-sea-view` | by address | 390, 768, 1440 |
| PU-17 | 3 Space details | no Arabic name; live status not set up (no capacity) | visitor | `/spaces/zeitoun-works` | by address | 390, 768, 1440 |
| PU-18 | 3 Space details | a long Arabic name (named state NS4) | visitor | `/spaces/nuseirat-study-house` | by address | 390, 768, 1440 |
| PU-19 | 3 Space details | photo viewer open | visitor | `/spaces/pal-hub` | 1 step | 390, 768, 1440 |
| PU-20 | 3 Space details | a guest taps the heart: the sign-in prompt | visitor | `/spaces/pal-hub` | 1 step | 390, 768, 1440 |
| PU-21 | 3 Space details | report wrong information (signed in), sent empty | user | `/spaces/pal-hub` | 2 steps | 390, 768, 1440 |
| PU-22 | 3 Space details | unverified: the owners' contact dialog | visitor | `/spaces/freelancers-house` | 1 step | 390, 768, 1440 |
| PU-23 | 4 About / Contact | default | visitor | `/about` | by address | 390, 768, 1440 |
| PU-24 | 33 Privacy policy | default | visitor | `/privacy` | by address | 390, 768, 1440 |
| PU-25 | 8 404 | an unknown address | visitor | `/no-such-page` | by address | 390, 768, 1440 |
| PU-26 | 3 Space details | a space that does not exist | visitor | `/spaces/no-such-space` | by address | 390, 768, 1440 |
| PU-27 | 1 Home | evening: after Pal Hub's closing (Friday 20:00 Gaza; taken after 18:00 UTC) | visitor | `/` | by address | 390, 768, 1440 |
| PU-28 | 2 Directory (list) | evening: after Pal Hub's closing (Friday 20:00 Gaza; taken after 18:00 UTC) | visitor | `/spaces` | by address | 390, 768, 1440 |
| PU-29 | 2 Directory (map) | evening: after Pal Hub's closing (Friday 20:00 Gaza; taken after 18:00 UTC) | visitor | `/spaces?view=map` | by address | 390, 768, 1440 |
| PU-30 | 3 Space details | Pal Hub after Pal Hub's closing (Friday 20:00 Gaza; taken after 18:00 UTC) | visitor | `/spaces/pal-hub` | by address | 390, 768, 1440 |

### AU — 20 bases

| ID | Screen | State | Role | URL | How | Widths |
|---|---|---|---|---|---|---|
| AU-01 | 5 Sign in | default | visitor | `/login` | by address | 390, 768, 1440 |
| AU-02 | 5 Sign in | sent empty: field errors | visitor | `/login` | 1 step | 390, 768, 1440 |
| AU-03 | 5 Sign in | a wrong password (the API's real 401) | visitor | `/login` | 3 steps | 390, 768, 1440 |
| AU-04 | 5 Sign in | too many attempts (429 simulated, Retry-After 60) | visitor | `/login` | 3 steps · 429 on */api/v1/auth/login | 390, 768, 1440 |
| AU-05 | 6 Register | default | visitor | `/register` | by address | 390, 768, 1440 |
| AU-06 | 6 Register | sent empty: field errors and the password rules | visitor | `/register` | 1 step | 390, 768, 1440 |
| AU-07 | 6 Register | an email that has an account (the API's real 409, nothing written) | visitor | `/register` | 4 steps | 390, 768, 1440 |
| AU-08 | 7 Forgot / reset password | forgot: the request form | visitor | `/forgot-password` | by address | 390, 768, 1440 |
| AU-09 | 7 Forgot / reset password | forgot: the link sent (recovery position mocked) | visitor | `/forgot-password` | mocked */api/v1/auth/password/recovery | 390, 768, 1440 |
| AU-10 | 7 Forgot / reset password | reset: an expired or used link (the API's real refusal) | visitor | `/reset-password#token=abc123` | by address | 390, 768, 1440 |
| AU-11 | 7 Forgot / reset password | reset: the new-password form, sent empty (link check mocked) | visitor | `/reset-password#token=abc123` | 1 step · mocked */api/v1/auth/password/reset/check | 390, 768, 1440 |
| AU-12 | 9 Profile & settings (forced change) | a temporary password to change first (session patched: mustChangePassword) | user | `/me` | patched */api/v1/auth/refresh | 390, 768, 1440 |
| AU-13 | 9 Profile & settings | default | user | `/me` | by address | 390, 768, 1440 |
| AU-14 | 9 Profile & settings | the password form, saved empty | user | `/me` | 2 steps | 390, 768, 1440 |
| AU-15 | 9 Profile & settings | a Google-only account (answer patched: no password, Google linked) | user | `/me` | patched */api/v1/me | 390, 768, 1440 |
| AU-16 | 10 Favourites | 5 saved spaces | user | `/me/favorites` | by address | 390, 768, 1440 |
| AU-17 | 10 Favourites | a saved space that left the directory (answer patched) | user | `/me/favorites` | patched */api/v1/me/favorites* | 390, 768, 1440 |
| AU-18 | 10 Favourites | empty (mocked) | user | `/me/favorites` | mocked */api/v1/me/favorites* | 390, 768, 1440 |
| AU-19 | 11 My reports | 3 reports, two answered | user | `/me/reports` | by address | 390, 768, 1440 |
| AU-20 | 11 My reports | empty (mocked) | user | `/me/reports` | mocked */api/v1/me/reports* | 390, 768, 1440 |

### OW — 34 bases

| ID | Screen | State | Role | URL | How | Widths |
|---|---|---|---|---|---|---|
| OW-01 | 12 Overview (O) | the work queue, people present (NS1) | owner | `/dashboard/spaces/26` | by address | 390, 768, 1440 |
| OW-02 | 17 Payments (O) | a week with 70 payments, page 1 of 4 | owner | `/dashboard/spaces/26/payments?from=2026-10-27&to=2026-11-02` | by address | 390, 768, 1440 |
| OW-03 | 17 Payments (O) | voided payments shown | owner | `/dashboard/spaces/26/payments?from=2026-10-19&to=2026-10-25&voided=1` | by address | 390, 768, 1440 |
| OW-04 | 17 Payments (O) | today (the page's landing; NS2's payments) | owner | `/dashboard/spaces/26/payments` | by address | 390, 768, 1440 |
| OW-05 | 17 Payments (O) | filters that match nothing | owner | `/dashboard/spaces/26/payments?from=2026-11-01&to=2026-11-01&staff=3&method=TRANSFER&kind=SUBSCRIPTION` | by address | 390, 768, 1440 |
| OW-06 | 17 Payments (O) | filters bottom sheet open | owner | `/dashboard/spaces/26/payments` | 1 step | 390 |
| OW-07 | 17 Payments (O) | void a payment: confirmed with no reason | owner | `/dashboard/spaces/26/payments?from=2026-11-02&to=2026-11-02` | 3 steps | 390, 768, 1440 |
| OW-08 | 19 Finance & statistics (O) | income, this month | owner | `/dashboard/spaces/26/finance` | by address | 390, 768, 1440 |
| OW-09 | 19 Finance & statistics (O) | debts | owner | `/dashboard/spaces/26/finance?tab=debts` | by address | 390, 768, 1440 |
| OW-10 | 19 Finance & statistics (O) | occupancy, October | owner | `/dashboard/spaces/26/finance?tab=occupancy&month=2026-10` | by address | 390, 768, 1440 |
| OW-11 | 21 Prices & packages (O) | the published prices and 6 private packages (one paused) | owner | `/dashboard/spaces/26/packages` | by address | 390, 768, 1440 |
| OW-12 | 21 Prices & packages (O) | new package sheet, saved empty | owner | `/dashboard/spaces/26/packages` | 2 steps | 390, 768, 1440 |
| OW-13 | 20 Space profile (O) | the whole profile | owner | `/dashboard/spaces/26/profile` | by address | 390, 768, 1440 |
| OW-14 | 20 Space profile (O) | an open report's notice in its section | owner | `/dashboard/spaces/26/profile?report=1#report` | by address | 390, 768, 1440 |
| OW-15 | 20 Space profile (O) | hours sheet | owner | `/dashboard/spaces/26/profile?sheet=hours#hours` | by address | 390, 768, 1440 |
| OW-16 | 20 Space profile (O) | published prices sheet | owner | `/dashboard/spaces/26/profile?sheet=prices#prices` | by address | 390, 768, 1440 |
| OW-17 | 20 Space profile (O) | about sheet, the English name cleared and saved | owner | `/dashboard/spaces/26/profile?sheet=about#about` | 2 steps | 390, 768, 1440 |
| OW-18 | 20 Space profile (O) | discard question after an edit | owner | `/dashboard/spaces/26/profile?sheet=about#about` | 2 steps | 390, 768, 1440 |
| OW-19 | 20 Space profile (O) | photos in manage mode | owner | `/dashboard/spaces/26/profile#photos` | 1 step | 390, 768, 1440 |
| OW-20 | 18 Announcements (O+R) | active (owner) | owner | `/dashboard/spaces/26/announcements` | by address | 390, 768, 1440 |
| OW-21 | 18 Announcements (O+R) | ended, a closure already extended | owner | `/dashboard/spaces/26/announcements?state=ended` | by address | 390, 768, 1440 |
| OW-22 | 18 Announcements (O+R) | new announcement, a temporary closure chosen | owner | `/dashboard/spaces/26/announcements` | 2 steps | 390, 768, 1440 |
| OW-23 | 18 Announcements (O+R) | new announcement, published empty | owner | `/dashboard/spaces/26/announcements` | 2 steps | 390, 768, 1440 |
| OW-24 | 23 Data reports (O) | three reports, one new | owner | `/dashboard/spaces/26/reports` | by address | 390, 768, 1440 |
| OW-25 | 23 Data reports (O) | deciding a report: not accepted with no reply | owner | `/dashboard/spaces/26/reports?open=1` | 1 step | 390, 768, 1440 |
| OW-26 | 22 Staff (O) | one reception account | owner | `/dashboard/spaces/26/staff` | by address | 390, 768, 1440 |
| OW-27 | 22 Staff (O) | a row's menu (a held item with its reason) | owner | `/dashboard/spaces/26/staff` | 1 step | 390, 768, 1440 |
| OW-28 | 22 Staff (O) | add staff, sent empty | owner | `/dashboard/spaces/26/staff` | 2 steps | 390, 768, 1440 |
| OW-29 | 22 Staff (O) | remove access: the question | owner | `/dashboard/spaces/26/staff` | 2 steps | 390, 768, 1440 |
| OW-30 | 31 Audit log (O13, owner's) | last 30 days, page 1 of 45 | owner | `/dashboard/spaces/26/audit` | by address | 390, 768, 1440 |
| OW-31 | 31 Audit log (O13, owner's) | filters bottom sheet open | owner | `/dashboard/spaces/26/audit` | 1 step | 390 |
| OW-32 | 24 Settings (O) | every card | owner | `/dashboard/spaces/26/settings` | by address | 390, 768, 1440 |
| OW-33 | 24 Settings (O) | capacity 0 saved: unsaved changes and the field's error | owner | `/dashboard/spaces/26/settings` | 2 steps | 390, 768, 1440 |
| OW-34 | 12 Overview (O) | evening: after Pal Hub's closing (Friday 20:00 Gaza; taken after 18:00 UTC) | owner | `/dashboard/spaces/26` | by address | 390, 768, 1440 |

### DK — 32 bases

| ID | Screen | State | Role | URL | How | Widths |
|---|---|---|---|---|---|---|
| DK-01 | 13 Front desk (O+R) | now: people present (NS1), reception | reception | `/dashboard/spaces/26/desk` | by address | 390, 768, 1440 |
| DK-02 | 13 Front desk (O+R) | now: the owner's view | owner | `/dashboard/spaces/26/desk` | by address | 390, 768, 1440 |
| DK-03 | 13 Front desk (O+R) | search: a subscriber who owes | reception | `/dashboard/spaces/26/desk` | 1 step | 390, 768, 1440 |
| DK-04 | 13 Front desk (O+R) | search: nobody by that name | reception | `/dashboard/spaces/26/desk` | 1 step | 390, 768, 1440 |
| DK-05 | 13 Front desk (O+R) | check in a visit: sent with no name | reception | `/dashboard/spaces/26/desk` | 2 steps | 390, 768, 1440 |
| DK-06 | 13 Front desk (O+R) | check out a visitor: the charge and its payment (NS1) | reception | `/dashboard/spaces/26/desk` | 1 step | 390, 768, 1440 |
| DK-07 | 13 Front desk (O+R) | receive a payment: choose the customer | reception | `/dashboard/spaces/26/desk` | 2 steps | 390, 768, 1440 |
| DK-08 | 16 New subscription (O+R) | new customer from the desk: saved empty | reception | `/dashboard/spaces/26/desk` | 3 steps | 390, 768, 1440 |
| DK-09 | 13 Front desk (O+R) | check in a customer with no subscription: the choice | reception | `/dashboard/spaces/26/desk` | 2 steps | 390, 768, 1440 |
| DK-10 | 16 New subscription (O+R) | renew an expired subscription (from the desk's search) | reception | `/dashboard/spaces/26/desk` | 2 steps | 390, 768, 1440 |
| DK-11 | 13 Front desk (O+R) | the log of a past day (owner) | owner | `/dashboard/spaces/26/desk?view=log&logDay=2026-11-01` | by address | 390, 768, 1440 |
| DK-12 | 13 Front desk (O+R) | uncollected visits, expanded (owner) | owner | `/dashboard/spaces/26/desk#uncollected` | by address | 390, 768, 1440 |
| DK-13 | 13 Front desk (O+R) | write off a visit: confirmed with no reason (owner) | owner | `/dashboard/spaces/26/desk#uncollected` | 3 steps | 390, 768, 1440 |
| DK-14 | 13 Front desk (O+R) | collect an uncollected visit (reception) | reception | `/dashboard/spaces/26/desk#uncollected` | 1 step | 390, 768, 1440 |
| DK-15 | 13 Front desk (O+R) | the live status control open (P2) | reception | `/dashboard/spaces/26/desk` | 1 step | 390, 768, 1440 |
| DK-16 | 13 Front desk (O+R) | the phone's «⋯» menu | reception | `/dashboard/spaces/26/desk` | 1 step | 390 |
| DK-17 | 14 Customers (O+R) | 27 customers, page 1 (reception) | reception | `/dashboard/spaces/26/customers` | by address | 390, 768, 1440 |
| DK-18 | 14 Customers (O+R) | archived (owner) | owner | `/dashboard/spaces/26/customers?status=ARCHIVED` | by address | 390, 768, 1440 |
| DK-19 | 14 Customers (O+R) | a search that matches nobody | reception | `/dashboard/spaces/26/customers?q=zzzz` | by address | 390, 768, 1440 |
| DK-20 | 14 Customers (O+R) | filters bottom sheet open | reception | `/dashboard/spaces/26/customers` | 1 step | 390 |
| DK-21 | 14 Customers (O+R) | a row's menu (owner) | owner | `/dashboard/spaces/26/customers` | 1 step | 390, 768, 1440 |
| DK-22 | 14 Customers (O+R) | archive a customer who owes: the question (owner) | owner | `/dashboard/spaces/26/customers` | 2 steps | 390, 768, 1440 |
| DK-23 | 15 Customer details (O+R) | an active subscription that owes (owner) | owner | `/dashboard/spaces/26/customers/26` | by address | 390, 768, 1440 |
| DK-24 | 15 Customer details (O+R) | the statement open, a voided payment (owner) | owner | `/dashboard/spaces/26/customers/26` | 1 step | 390, 768, 1440 |
| DK-25 | 15 Customer details (O+R) | correct the subscription (owner) | owner | `/dashboard/spaces/26/customers/26` | 2 steps | 390, 768, 1440 |
| DK-26 | 15 Customer details (O+R) | in credit, usage-based (reception) | reception | `/dashboard/spaces/26/customers/11` | by address | 390, 768, 1440 |
| DK-27 | 15 Customer details (O+R) | no subscription, unpaid visits (owner) | owner | `/dashboard/spaces/26/customers/32` | by address | 390, 768, 1440 |
| DK-28 | 16 New subscription (O+R) | a new subscription for a customer who owes (reception) | reception | `/dashboard/spaces/26/customers/26` | 2 steps | 390, 768, 1440 |
| DK-29 | 15 Customer details (O+R) | a customer who is not there | owner | `/dashboard/spaces/26/customers/999999` | by address | 390, 768, 1440 |
| DK-30 | 17 Payments (R: my payments today) | today's own payments (NS2) | reception | `/dashboard/spaces/26/my-payments` | by address | 390, 768, 1440 |
| DK-31 | 18 Announcements (O+R) | reception's view | reception | `/dashboard/spaces/26/announcements` | by address | 390, 768, 1440 |
| DK-32 | 13 Front desk (O+R) | evening: after Pal Hub's closing (Friday 20:00 Gaza; taken after 18:00 UTC); the live status control held | reception | `/dashboard/spaces/26/desk` | by address | 390, 768, 1440 |

### AD — 33 bases

| ID | Screen | State | Role | URL | How | Widths |
|---|---|---|---|---|---|---|
| AD-01 | 25 Overview | the platform's work queue | admin | `/dashboard/admin` | by address | 390, 768, 1440 |
| AD-02 | 26 Spaces | 37 spaces, page 1 of 2 | admin | `/dashboard/admin/spaces` | by address | 390, 768, 1440 |
| AD-03 | 26 Spaces | the «stale or missing» chip on | admin | `/dashboard/admin/spaces?stale=true` | by address | 390, 768, 1440 |
| AD-04 | 26 Spaces | deleted spaces, restore | admin | `/dashboard/admin/spaces?status=deleted` | by address | 390, 768, 1440 |
| AD-05 | 26 Spaces | a search that matches nothing | admin | `/dashboard/admin/spaces?q=zzzz` | by address | 390, 768, 1440 |
| AD-06 | 26 Spaces | filters bottom sheet open | admin | `/dashboard/admin/spaces` | 1 step | 390 |
| AD-07 | 26 Spaces | a row's menu | admin | `/dashboard/admin/spaces` | 1 step | 390, 768, 1440 |
| AD-08 | 26 Spaces | delete a space: the question | admin | `/dashboard/admin/spaces` | 2 steps | 390, 768, 1440 |
| AD-09 | 26 Spaces (add) | add a space: sent empty | admin | `/dashboard/admin/spaces/new` | 1 step | 390, 768, 1440 |
| AD-10 | 26 Spaces (editor) | unverified, one group missing (A2) | admin | `/dashboard/admin/spaces/32` | by address | 390, 768, 1440 |
| AD-11 | 26 Spaces (editor) | verified: read-only, its owner named | admin | `/dashboard/admin/spaces/26` | by address | 390, 768, 1440 |
| AD-12 | 26 Spaces (editor) | stale prices: «still correct» | admin | `/dashboard/admin/spaces/10#prices` | by address | 390, 768, 1440 |
| AD-13 | 26 Spaces (editor) | prices sheet saved with an empty amount | admin | `/dashboard/admin/spaces/32?sheet=prices` | 1 step | 390, 768, 1440 |
| AD-14 | 26 Spaces (editor) | hours sheet, each day set | admin | `/dashboard/admin/spaces/10?sheet=hours` | 1 step | 390, 768, 1440 |
| AD-15 | 26 Spaces (editor) | amenities sheet (common and own) | admin | `/dashboard/admin/spaces/10?sheet=amenities` | by address | 390, 768, 1440 |
| AD-16 | 26 Spaces (editor) | contacts sheet | admin | `/dashboard/admin/spaces/10?sheet=contacts` | by address | 390, 768, 1440 |
| AD-17 | 26 Spaces (editor) | location sheet (map) | admin | `/dashboard/admin/spaces/24?sheet=location` | by address | 390, 768, 1440 |
| AD-18 | 27 Space owners (link) | link an owner: sent with no person | admin | `/dashboard/admin/spaces/32` | 2 steps | 390, 768, 1440 |
| AD-19 | 27 Space owners | 7 owners | admin | `/dashboard/admin/owners` | by address | 390, 768, 1440 |
| AD-20 | 27 Space owners | add an owner: sent empty | admin | `/dashboard/admin/owners?sheet=add` | 1 step | 390, 768, 1440 |
| AD-21 | 29 Users | the one-time password dialog (issue answer mocked, nothing written) | admin | `/dashboard/admin/users` | 3 steps · mocked */api/v1/admin/users/*/temporary-password | 390, 768, 1440 |
| AD-22 | 29 Users | 50 users, page 1 of 3 | admin | `/dashboard/admin/users` | by address | 390, 768, 1440 |
| AD-23 | 29 Users | an owner's menu: role change held, with its reason | admin | `/dashboard/admin/users?q=garden.owner%40example.com` | 1 step | 390, 768, 1440 |
| AD-24 | 29 Users | make a user an admin: the question | admin | `/dashboard/admin/users` | 2 steps | 390, 768, 1440 |
| AD-25 | 29 Users | suspend a user: the question | admin | `/dashboard/admin/users` | 2 steps | 390, 768, 1440 |
| AD-26 | 28 Data reports | 18 reports | admin | `/dashboard/admin/reports` | by address | 390, 768, 1440 |
| AD-27 | 28 Data reports | deciding (unverified space): not accepted with no reply | admin | `/dashboard/admin/reports?open=4` | 1 step | 390, 768, 1440 |
| AD-28 | 28 Data reports | a verified space's report: read only | admin | `/dashboard/admin/reports?open=1` | by address | 390, 768, 1440 |
| AD-29 | 30 Lookups | governorates and areas | admin | `/dashboard/admin/lookups` | by address | 390, 768, 1440 |
| AD-30 | 30 Lookups | amenities: add, saved empty | admin | `/dashboard/admin/lookups?tab=amenities` | 2 steps | 390, 768, 1440 |
| AD-31 | 31 Audit log | the platform's last 30 days | admin | `/dashboard/admin/audit` | by address | 390, 768, 1440 |
| AD-32 | 32 Settings | the three cards | admin | `/dashboard/admin/settings` | by address | 390, 768, 1440 |
| AD-33 | 32 Settings | freshness: 999 days saved (unsaved changes, the error) | admin | `/dashboard/admin/settings` | 2 steps | 390, 768, 1440 |

### SH — 30 bases

| ID | Screen | State | Role | URL | How | Widths |
|---|---|---|---|---|---|---|
| SH-01 | Showcase · actions | Button, toggles, DropdownMenu (the layer's own preview) | visitor | `/__showcase/preview/actions?theme={theme}&lang={lang}` | by address | 390, 768, 1440 |
| SH-02 | Showcase · fields | every field component | visitor | `/__showcase/preview/fields?theme={theme}&lang={lang}` | by address | 390, 768, 1440 |
| SH-03 | Showcase · display | Badge, Card, Avatar, StatCard, FilterTag, Meter, Logo | visitor | `/__showcase/preview/display?theme={theme}&lang={lang}` | by address | 390, 768, 1440 |
| SH-04 | Showcase · data | Table, DataTable, BarChart, Heatmap | visitor | `/__showcase/preview/data?theme={theme}&lang={lang}` | by address | 390, 768, 1440 |
| SH-05 | Showcase · feedback | Skeleton, Spinner, Alert, Toast, EmptyState, Refreshing | visitor | `/__showcase/preview/feedback?theme={theme}&lang={lang}` | by address | 390, 768, 1440 |
| SH-06 | Showcase · overlays | Tooltip, Dialog, AlertDialog, Sheet, Popover triggers | visitor | `/__showcase/preview/overlays?theme={theme}&lang={lang}` | by address | 390, 768, 1440 |
| SH-07 | Showcase · navigation | Tabs, Breadcrumb, Pagination, Sidebar | visitor | `/__showcase/preview/navigation?theme={theme}&lang={lang}` | by address | 390, 768, 1440 |
| SH-08 | Showcase · icons | the icon set and its mirroring | visitor | `/__showcase/preview/icons?theme={theme}&lang={lang}` | by address | 390, 768, 1440 |
| SH-09 | Site shell · phone menu | open, guest | visitor | `/spaces` | 1 step | 390 |
| SH-10 | Site shell · phone menu | open, signed-in user | user | `/spaces` | 1 step | 390 |
| SH-11 | Site shell · account menu | open (signed-in user) | user | `/spaces` | 1 step | 768, 1440 |
| SH-12 | Dashboard shell · phone drawer | open (owner) | owner | `/dashboard/spaces/26` | 1 step | 390 |
| SH-13 | Dashboard shell · phone drawer | open (admin, with the logo) | admin | `/dashboard/admin` | 1 step | 390 |
| SH-14 | Dashboard shell · account menu | open (owner) | owner | `/dashboard/spaces/26/customers` | 1 step | 768, 1440 |
| SH-15 | Dashboard shell · tablet rail | a rail item focused, its tooltip (admin) | admin | `/dashboard/admin/spaces` | 1 step | 768 |
| SH-16 | Every shell · skip link | the first Tab: the skip link shown | visitor | `/spaces` | 1 step | 390, 768, 1440 |
| SH-17 | States · loading | the directory's list loading (request held) | visitor | `/spaces` | held */api/v1/spaces?* | 390, 768, 1440 |
| SH-18 | States · loading | the desk loading (who is present: request held) | reception | `/dashboard/spaces/26/desk` | held */api/v1/manage/spaces/26/occupancy | 390, 768, 1440 |
| SH-19 | States · loading | the admin's spaces list loading (request held) | admin | `/dashboard/admin/spaces` | held */api/v1/admin/spaces?* | 390, 768, 1440 |
| SH-20 | States · loading | account settings loading (request held) | user | `/me` | held */api/v1/me | 390, 768, 1440 |
| SH-21 | States · failure | a space's page fails to load (500 simulated, with the retries) | visitor | `/spaces/pal-hub` | 500 on */api/v1/spaces/pal-hub | 390, 768, 1440 |
| SH-22 | States · failure | the customers list fails to load (500 simulated) | owner | `/dashboard/spaces/26/customers` | 500 on */api/v1/manage/spaces/26/customers?* | 390, 768, 1440 |
| SH-23 | States · failure | the admin's users list fails to load (500 simulated) | admin | `/dashboard/admin/users` | 500 on */api/v1/admin/users?* | 390, 768, 1440 |
| SH-24 | States · too many requests | the directory answered 429 (simulated, Retry-After 60) | visitor | `/spaces` | 429 on */api/v1/spaces?* | 390, 768, 1440 |
| SH-25 | States · too many requests | finance answered 429 (simulated) | owner | `/dashboard/spaces/26/finance` | 429 on */api/v1/manage/spaces/26/finance/income* | 390, 768, 1440 |
| SH-26 | States · offline | the directory with no connection (request aborted) | visitor | `/spaces` | aborted on */api/v1/spaces?* | 390, 768, 1440 |
| SH-27 | States · 403 | reception on an owner's page | reception | `/dashboard/spaces/26/payments` | by address | 390, 768, 1440 |
| SH-28 | States · 404 | an unknown page inside the dashboard | owner | `/dashboard/spaces/26/nope` | by address | 390, 768, 1440 |
| SH-29 | Feedback · toast | a success toast: the profile's public link copied | owner | `/dashboard/spaces/26/profile` | 1 step | 390, 768, 1440 |
| SH-30 | Feedback · toast | a toast with an undo: a favourite removed (write answered by the tool) | user | `/me/favorites` | 1 step · mocked */api/v1/me/favorites/* | 390, 768, 1440 |

## 3. Named states written to `masaha_dr_dev`

- **NS1** — people present at Pal Hub (space 26): two visits («ريم أبو عمرة», «Omar Saleh») and two subscribers (subscriptions 17 and 31) checked in by reception, through the API.
- **NS2** — payments today: reception 20 ₪ cash on subscription 20; the owner 50 ₪ by transfer on subscription 17, through the API.
- **NS4** — a long Arabic name on unverified space 19 («دار النصيرات للدراسة والعمل المشترك للطلاب والخريجين»), by SQL on `name_ar` only.
- `rate_limits` rows of `masaha_dr_dev` are cleared between capture batches (allowed by the prompt).

## 4. States not captured, and why

- **The closure extension dialog (O11):** the only closure is already extended; reaching it needs a write or two mocked answers whose shapes the review did not pin. Its text and rules are judged from the source by OW.
- **The price-a-visit dialog:** Pal Hub has no unpriced visit; it needs a write. DK judges it from the source.
- **The one-time password after adding an owner or staff:** needs an account created; the admin's users page shows the same dialog through a mocked issue answer (AD-21).
- **A space switcher with two live spaces:** the demo owner has one live space; needs a second link (a write).
- **A space FULL in the lists** (the directory's card and pin): a manual override lasts until closing (Friday 20:00 in Gaza); FULL is captured on a space's page through a patched answer (PU-14).
- **Hover states and motion:** a still frame cannot show them; SH checks them live and in the source.
- **Google sign-in itself:** not used (the prompt); its button is shown as the page draws it.
