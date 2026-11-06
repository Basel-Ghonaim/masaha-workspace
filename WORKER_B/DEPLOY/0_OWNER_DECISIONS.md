# DEPLOY — the owner's decisions (2026-11-01)

Settled with the main supervisor in Arabic, 2026-11-01. The execution prompt `3_EXEC_PROMPT.md` binds them.

1. **Hosting:** ADR 0014 as it stands — Vercel (one origin: the web at `/`, the Express app as a function under
   `/api`) and Neon, both in Frankfurt. The owner approved it in words.
2. **The cron:** an external free cron (cron-job.org) calls `POST /api/v1/internal/jobs/run` **every 15 minutes**, not
   5. Reason: Neon's free tier suspends after 5 idle minutes and allows 100 compute-hours a month; a call every 5
   minutes keeps it awake all month (≈ 180 CU-hours at 0.25 CU) and the database would be suspended mid-month. A late
   run never corrupts data (the auto check-out records its due cut-off). The local server's timer stays 5 minutes.
3. **Previews off:** production deploys from `main` only; no preview deployments (they would need their own database,
   and Google sign-in and the CORS origin do not fit their changing addresses). Revisit with a Neon branch later.
4. **The online site starts empty** but for the admin (the demo seed stays refused in production); the owner adds a few
   spaces by hand from the admin's dashboard after the first deployment.
5. **Email:** Gmail SMTP with an app password, from a **new Gmail account** made for Masaha (not the owner's own).
6. **Google sign-in:** one OAuth client with both origins (localhost:5320 and the public address). **Amended
   2026-11-01:** the consent screen stays in *Testing* (Google's *Publish app* needs a homepage and a privacy policy
   URL; Masaha has no privacy page, outside v1). Google sign-in online works for the listed test users only (≤ 100);
   everyone else registers by email. Branding and publishing to be discussed with the owner on 2026-11-02. The
   runbook must say this, not "In production".
7. **Cloudinary:** the owner's existing account; `STORAGE_MODE=cloudinary` and `CLOUDINARY_URL` online only.
8. **Timing:** the deployment item is built now and **must be merged and live before the owner's presentation on
   2026-11-03** (a training course, not the graduation defence), so he can share the link. The presentation itself runs
   from the local development environment. The owner does the accounts and secrets himself, in parallel.
9. **Speed over the usual stop:** the worker writes and saves its plan, then executes in the same session without
   waiting for approval (the owner's explicit override of "plan saved, then stop", for the deadline). The supervisor
   reviews the PR.
10. **2026-11-05:** the privacy page shipped (#135); the Google consent screen's Branding filled (support email masahatgaza, no logo) and the app **published**: Google sign-in is open to everyone (item 6's Testing ends).
