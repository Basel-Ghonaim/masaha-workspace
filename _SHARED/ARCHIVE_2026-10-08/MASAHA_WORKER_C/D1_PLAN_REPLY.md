The plan is approved. Write it, with three small adjustments.

1. **No local paths in the repository.** The plan is a committed document that others (an examiner,
   a future worker) read without this machine. Cite sources by **PR number** (its description and its
   review), by **document › section**, and by **commit or file in the repository**. A decision whose
   only source is an analyst's prompt or reply is cited as "the Work Item's prompt (outside the
   repository), confirmed by <the code or PR that shows it>". Never write `C:\Users\…` or
   `D:\quick-tweets-app\…` paths; Quick Tweets is named only as the idea's origin, if at all.
2. **Ledger pointers must be checkable.** Each row's "lives now" names the document and its section
   heading (as a link with its anchor where one exists), so the execution's reviewer can open it
   directly; a short paraphrase of the fact, never a long quote.
3. **Show the effect.** For each platform document the ledger touches, give its current word count
   and the estimated words that leave it (moved or deleted as duplicates), so the owner sees how much
   lighter each becomes.

Everything else stands: the three inventories, your merge and code checks, the outline, ADR 0018,
the one commit, the checks (say if `node_modules` is missing), and the PR.
