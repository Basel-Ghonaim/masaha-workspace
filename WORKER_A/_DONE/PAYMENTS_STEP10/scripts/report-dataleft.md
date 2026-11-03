- **The account menu** (reception, after the refresh window): desktop (ar 1440) «المفضّلة → /me/favorites | بلاغاتي →
  /me/reports | لوحة التحكم → /dashboard | تسجيل الخروج»; the phone menu (en 390) «… | Favourites → /me/favorites | My
  reports → /me/reports | Dashboard → /dashboard». Shots `4a-account-menu-*`.
- The servers stopped by their process ids (the API's tsx watch, server and pino; Vite), then once more after a short
  read-only start for the audit entry below; `Get-NetTCPConnection -LocalPort 3320,5320 -State Listen` → "listening: 0".

### Every write of the run, and what it left in `masaha_dev`

- **Data reports:** 1 (`masaha-demo` HOURS «تجربة: الساعات», RESOLVED by the owner, reply «صحّحنا الساعات»); 2
  (`noor-hub` PRICES, OPEN — a verified space's, the owner's to decide); 3 (`tuffah-place` OTHER «تجربة: أخرى», DISMISSED
  by the admin, «تجربة: لا يلزم تعديل»); 4 (`noor-hub` AMENITIES, OPEN, from the page; its repeat wrote nothing). All
  by `demo-reception`.
- **Favourites of `demo-reception`:** 48 `noor-hub` (saved on its page; removed and restored by «تراجع» on «المفضّلة»),
  49 `sada-space` (the guest's, on the return), 51 `radwan-study-hall` (Home's; the Directory's save had been undone).
- **Announcements of space 7:** 2 «إعلان تجربة» (GENERAL; posted, edited, ended, undone, ended, deleted), 3 «عرض تجربة»
  (OFFER; posted, started, deleted) — both deleted (soft); 4 «إغلاق تجربة» (CLOSURE, 27 October 08:00 → ended 28
  October 15:39, **extended**) — stays, in «منتهية».
- **The extension (the approval note's write, 1 day, no undo):** the audit entry `closure.subscriptionsExtended` →
  `{"days":1,"subscriptionIds":[3,5,7],"renewalIds":[6]}` — subscriptions 3, 5 and 7 of `masaha-demo` and the renewal 6
  moved by one day: the preview's 4.
- Nothing else was written: every other request of the run was a GET (the network logs, `run2-log.txt`).
