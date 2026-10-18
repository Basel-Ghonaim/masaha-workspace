# R2-AD-TR report

HEAD = a82541b1435366854d253f88cfe9258f87d36b8d, origin/main = a82541b1435366854d253f88cfe9258f87d36b8d.

**Verdict:** The admin prototype stays within the data model and the contract; the only truth gap I found is that a user's hidden reception link can block a role change with no way to see it beforehand.

**Five most important points**
1. The role values offered on the users screen (`USER` / `ADMIN`) and the `OWNER`-follows-links rule match the contract and ADR 0009.
2. Link/unlink consequences (unverified on last owner, `RECEPTION_LINK_ACTIVE` refusal) are drawn where the contract raises them.
3. Verification and hidden are shown as two separate facts; deleted is its own list with restore.
4. Rima's all-deleted case and suspended owners are represented as the contract needs.
5. Stale/missing rules follow the thresholds and the `stale=true` OR of the two.

## Issues

**R2-AD-TR-001 — Users list cannot predict a reception link before a role change**
type: improvement · level: pattern · impact: medium
where: `46 · Admin — users` `Admin users.html?changerole=1` 1440, Arabic light, evidence `docs/design/screens/46-admin-users/05-change-role-desktop-1440.webp`
evidence: `C:\Users\basel\Downloads\r2-shots\AD-TR\R2-AD-TR-001.png`
what could be better: a role change can fail with `ACCOUNT_HAS_LINKS` because of a reception link, which the users row does not show (DI-24); the row offers no way to tell the admin who holds one before they try.
proposal: add the linked spaces (or a "has links" marker) to the users row, as the owners page already does, so the admin knows why before acting.
why: the refusal exists but is only discovered after the submit.
cost: M
rule: `docs/api/api-contract.md` §Users (PUT role), `ACCOUNT_HAS_LINKS`.

**R2-AD-TR-002 — Role-change action is drawn destructive both ways**
type: defect · level: component · impact: low
where: `46 · Admin — users` `Admin users.html?changerole=1` 1440, Arabic light, evidence `docs/design/screens/46-admin-users/05-change-role-desktop-1440.webp`
evidence: `C:\Users\basel\Downloads\r2-shots\AD-TR\R2-AD-TR-002.png`
what is wrong: both "make admin" and "make user" use the destructive action even though only the latter removes access; the former grants access.
proposal: make granting admin a primary (non-destructive) action and keep destructive only for removing it.
why: the button's colour should match its consequence, per P9.
cost: S
rule: `docs/development/workflow.md` P9.

## Decisions in doubt

None.

## Not reviewed

I did not run the running prototype against the API; this review is read-only against the archive and the documents. Dark, English and 768 views were not reopened because the truth points here do not change with them." 