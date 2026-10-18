One more unit for PR #47, in this same session, **before** the PR is reviewed and merged: the
owner wants a worker to read exactly what its task needs — never the whole documentation set, never
less than the essentials — and to resolve related findings instead of letting them pile up. It
touches the files this PR already edits, so it goes here as **a ninth commit** (a new unit, not a
fixup). Plan it briefly in plan mode first (the wording and where each rule lives), then write it.

## Where each rule lives (one owner per fact)
- **The rules live in `docs/development/workflow.md`** (it owns how work is executed). The
  `start-work-item` skill **links them and carries them out**; it never restates them. CLAUDE.md's
  session checklist only points to them. The map only guides.

## 1. The map gains "read it when" (`docs/README.md`)
Each document's entry becomes **what it owns · read it when …**, at most two short lines. Examples of
the shape (wording is yours): "`backend/security.md` — tokens, passwords, cookies, authorization,
rate limits · read it when your task signs someone in, checks who may act, or limits a request";
"`docs/features/<module>.md` — one capability's flows, decisions and code map · read it first when
your task changes that capability". The map stays a guide to documents, never a list of code files.

## 2. Reading before work (a short rule in `workflow.md`, for example in §2 *Work Item*)
- **Always:** CLAUDE.md, this workflow, and the map.
- **By the kind of task:** code → `engineering-principles.md`, `testing.md`, and the architecture
  document of each layer it touches (`frontend/architecture.md`, `backend/conventions.md`), plus
  `backend/security.md` when it signs in, authorizes or limits; documents →
  `architecture/documentation.md`.
- **Then the capability's document,** when the task changes a capability that has one, and **only
  the sections it or the prompt links.** A capability without a document (not yet at its stable core)
  is worked on as before, from the prompt and the platform documents.
- **Open a document only when its "read it when" line matches the task.** Skipping a document the
  task needs is a defect, like reading the whole set.

## 3. Related findings (a short rule in `workflow.md`, for example in §4 *Scope control*)
- At the start of a Work Item, read the **open** findings' titles and their *Resolves when* lines
  (not the whole file), then open in full only those that touch the item.
- The plan lists them in a **"Related findings"** section: for each, fold it into this item or not,
  why, and its cost. **The owner decides;** a folded finding is resolved in the same PR, with its
  status and a resolution line.

## 4. The skill and the pointer
- `start-work-item`: its reading step follows §2's rule (map first, then the set for the task's kind,
  then the capability's document), and its planning step adds the "Related findings" section (§3).
  Links, not restatements.
- CLAUDE.md's *Session checklist*: one pointer to the reading rule, if its current step 2 doesn't
  already cover it; keep CLAUDE.md a pointer.

## Rules
- Documents only. One owner per fact: if `docs/architecture/documentation.md` or another document
  already says part of this, link it instead of repeating it.
- Commit subject ≤ 50 characters, for example `docs: add the reading guide and findings step`.
- No local checks (as before); a plain push (a new commit, no rewrite). Update the PR description
  (the ninth commit, from the owner's request). Report once CI is green. Don't merge. No subagents.
