# Masaha wordmark — prompt for an external image tool (2026-11-11)

**Use:** Recraft (vector output; preferred) and/or ChatGPT's image tool — the **same prompt** in both, as a check
that the ideas are real and not one tool's habit.

**Attach two images:**
1. `C:\dev\masaha\workspace\TASKS\LOGO\reference\oyoun-academy-logo.png` — the reference whose **principles** we
   want (not its look). *It is the company's logo: the owner decides whether to upload it to a third-party tool.*
2. Optional: `C:\dev\masaha\workspace\TASKS\LOGO\wordmark\round1.png` — Claude's 10 drafts, so the tool goes
   elsewhere instead of repeating them.

**Rounds:** run the prompt 2–3 times (≈ 10 results), keep the 2–3 best, then a second run that describes what to
keep. Every kept result is checked at 24 px and 16 px. The tool's image is a **reference**: the final wordmark is
rebuilt from a real open-licensed font (or redrawn cleanly) as SVG.

---

## The prompt (paste as is)

```text
Design 10 distinct wordmark logos for "Masaha" — the word alone, no symbol, no icon.

About the product: Masaha is a calm, trustworthy, practical web platform that lists coworking spaces in the
Gaza Strip and shows which ones are open right now. Its users are freelancers and students looking for a
desk with power and internet, and the space owners who run them. The interface is modern and quiet.

The attached logo (Oyoun Academy) is a REFERENCE FOR PRINCIPLES ONLY. Do NOT copy or imitate its look:
no circle-plus-triangle "OA" monogram, no pairing of a light wide name with a heavy oblique word, no
"NAME." styling like it. Take only these principles and apply them in your own way to the word "Masaha":
1. A geometric skeleton (circles, straight lines, consistent angles) — calm and rational.
2. ONE memorable letter-level detail, at most: two letters sharing a stroke (a ligature), a part of a letter
   left open so negative space completes it, or one deliberate cut. Never more than one trick per logo.
3. Restraint: no decoration, no swashes, no 3D, no gradients, no shadows, no outlines, no mock-up scenes.
4. Strong at small sizes: it must still read as "Masaha" at 24 px and 16 px tall.
5. A clear weight choice (light, regular or heavy) used consistently through the word.

Vary across the 10: lowercase "masaha" vs. capitalised "Masaha" vs. all capitals "MASAHA"; light vs. heavy;
tight vs. open spacing; geometric vs. humanist; the kind of single detail (ligature, open counter, cut,
a subtle unique letter such as the single-storey "a" or the "h").

Spelling must be exactly M-A-S-A-H-A (six letters). No other words, no tagline, no Arabic letters.
Solid black on a plain white background, flat, each logo on its own, numbered 1–10.
```

## After the run

Save the kept results in `C:\dev\masaha\workspace\TASKS\LOGO\wordmark\external\` (names `ext-01.png`, …) and bring
them to the main supervisor's conversation: they are compared with Claude's round 1 on one sheet, at the same sizes.
