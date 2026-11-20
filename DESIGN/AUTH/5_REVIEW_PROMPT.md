# Review of the auth designs (masaha-prototype) — one reviewer, read-only

You review the three auth designs (Slate, Coast, Dots) the design lead built in the public repository
`masaha-prototype` (`C:\dev\masaha\masaha-prototype`), commits `a9871dc..f9dc0fc` on `main`. You are launched headless
by the main supervisor. **Read only:** git reads (`git show`, `git log`, `git diff`, `git grep`), Read, Grep, Glob on
files and images; never edit, checkout, commit, push, install, or run a server or a script. The only file you write is
your report. Work alone. Claude Code, Opus 5.5.

## Read
1. The brief, binding: `C:\dev\masaha\workspace\DESIGN\AUTH\2_VARIANTS_PROMPT.md` (§1 fixed points, §2 how the
   designs must differ, §3 pages and states, §4 the lab), `0_OWNER_DECISIONS.md` (A1–A5), `1_CRITIQUE_CHECKED.md`
   (the 11 points every design answers).
2. The lead's report `4_REPORT.md` and `masaha-prototype/decisions/auth.md`.
3. The repository's rules: `masaha-prototype/CLAUDE.md` and `README.md` (§ Variants).
4. The code: `git diff a9871dc~1..f9dc0fc` — `prototype/variants/_auth/` (the kit), each design's stylesheet, the
   pages' variant files, `prototype/Auth lab.html`, `prototype/variants/index.js`, the reset e-mail's pages.
5. The captures in `D:\MASAHA\DT\AUTH\variants\` (and `report.txt`): look at **every page's default** for the three
   designs at 390 and 1920, light and dark, and at the states the report names; compare with the originals.

## Judge — verified defects and real risks only, each with the file (or capture) and a concrete fix
- **The brief:** every §1 point in all three (A1's layout at the three widths; A2's Strip — artistic, no borders, the
  dots the 13 real spaces with the snapshot's date, inline SVG, reduced motion; the identity; Arabic first; the
  product's real words, new words marked as proposals; no fake data and nothing of *Not in v1*; the 11 critique
  points; accessibility). The three genuinely different (§2). Every state of §3 present and behaving the same across
  designs. The lab's controls, its address and «قارن التصاميم».
- **The repository's rules:** originals untouched; no shared module or sample data edited; new styles in the
  variants' own CSS; no class the bundle lacks used without its CSS; the global-scope trap (no object rest, no
  top-level `name`); commits Conventional, ≤ 50, with bodies, no attribution; `README.md` / `CLAUDE.md` untouched.
- **The design itself, as a senior product designer:** what works, what is weak or unfinished in each design (the
  panel's composition at 1920 — e.g. a Strip cropped so little of it shows; the phone; dark; English LTR), what would
  make each stronger. Be direct; no praise for its own sake.
- **Truth:** the Strip's dots against the snapshot (`DESIGN\ROUND3\directions\_shared\data\spaces\`): 13, real
  coordinates; nothing claims a number that is not real.

## Output — `C:\dev\masaha\workspace\DESIGN\AUTH\5_REVIEW.md`
```
# Review of the auth designs — Claude Code, Opus 5.5
Commits a9871dc..f9dc0fc · head moved: <yes/no>
Verdict: <ready for the owner to choose | ready after small fixes | not ready>
## Findings (most severe first): F1 — <blocker|should-fix|nit> · <title> — Where / Seen / Why / Fix
## The brief, point by point (all three)
## The three designs as design — strengths, weaknesses, how to strengthen each
## The lab
## Not checked, and why
```
Then a five-line Arabic summary for the owner at the top. Stop.
