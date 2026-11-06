# PRIVACY — fix round for PR #134 (the prototype's privacy page)

You are the same worker, in `C:\dev\masaha\app-b`, on the branch `docs/privacy-page` (PR #134, head `341c3b3d`). The
supervisor reviewed the PR in the code and in your screenshots: it is **not mergeable yet**. Fix the five points
below, **fold each fix into the commit it belongs to** (`git commit --fixup <sha>`, then `GIT_SEQUENCE_EDITOR=: git
rebase -i --autosquash origin/main`; make a `backup/privacy-fix` branch first), re-run the checks, push with
`--force-with-lease`, and reply. Same rules as before: no tests lanes, no install, no file outside the PR's files, no
stop, never merge. Do not run any skill.

## The fixes

1. **Raw HTML shows on the page (must).** Two sentences put `<strong>…</strong>` *inside* a `tr("…")` string, so the
   page prints the tags as text: «يصل بلاغك عن مساحة إلى صاحبها <strong>دون اسمك</strong>.» (Who sees your data ›
   Reports) and «… عند طلب إيقافه، <strong>يُوقَف الحساب ولا يُحذف</strong> في …» (How long we keep data) — in both
   languages. Your 01 screenshot shows them. Split each sentence into `tr()` pieces with a real `<strong>` element
   between them, as the other bold leads on the page do, so the words show bold and no tag shows. Then search the
   whole file for any other `<` inside a `tr(` string.
2. **Two Arabic words differ from the approved text (must)** — the text must be word for word:
   - Introduction: «مساحة منصة تجمع مساحات العمل **المشتركة** في قطاع غزة» → «مساحة منصة تجمع مساحات العمل في قطاع غزة»
     (remove «المشتركة»; check the English twin says "the coworking spaces of the Gaza Strip", as approved).
   - How we protect your data: «**صلاحية** كل مستخدم تُفحص على الخادم في كل طلب.» → «**صلاحيات** كل مستخدم تُفحص على
     الخادم في كل طلب.»
   Then compare **every** Arabic and English sentence of the page with §7 of `1_PROMPT_PROTOTYPE.md` (in
   `C:\dev\masaha\workspace\TASKS\PRIVACY\`), one by one, and fix any other difference.
3. **The screen's number (must).** In `docs/frontend/design-system/foundation.md` §13 the new item is numbered `9.`,
   which collides with *My account*'s «9. Profile & settings». The privacy page is **screen 33** (as `SCREENS.md` says).
   Write it so the file reads 33 for it, not 9: end the *Public site* list after item 8, then a blank line, then the
   item as its own line starting `33\. **Privacy policy** — …` (the backslash keeps Markdown from renumbering it), the
   rest of the line unchanged. Check how it renders in a Markdown preview if you can.
4. **A stale count (small).** `docs/README.md` still says «SCREENS.md maps the 32 screens of foundation §13» —
   make it 33 (you already fixed that line's anchor).
5. **The lists (small).** In the approved text, the sections *What we collect*, *What we don't collect*, *How we use
   your data*, *Who sees your data*, *How we protect your data*, *How long we keep data* and *Your rights* are
   **bullet lists**; on the page they are plain paragraphs, so they read as one block (see *How we use your data*).
   Show them as bullet lists with the design system's list style used elsewhere in the prototype (find an existing
   `ul`/`list-disc` use, or the nearest equivalent the bundle's CSS really holds — `check-classes` must pass). The
   sentence «لا نبيع بياناتك…» after *How we use your data* stays a paragraph, as in the text.

## Checks and proof

```
node docs/design/scripts/check-parse.mjs
node docs/design/scripts/check-classes.mjs
npm run check:links
npm run check:conflicts
```

Retake the screenshots (Arabic light 1280 and 360, English 1280, dark 1280) into `TASKS\PRIVACY\shots\fix\` and
**open each one and look**: no `<strong>` or other tag visible anywhere, the two bold phrases bold, the lists with
bullets. Then push, watch CI to green and `CLEAN`.

## Reply

```
Status: READY FOR REVIEW | INCOMPLETE (what, why)
PR: #134 · head <sha> · CI <green/red> · <CLEAN/not CLEAN>
Fixes: 1 <done> · 2 <done; other differences found: …> · 3 <done> · 4 <done> · 5 <done>
Commits: <n>, folded (no fixup! left): yes/no
Checks: check-parse · check-classes · check:links · check:conflicts — <results>
Screenshots: shots\fix — <what you checked>
```
