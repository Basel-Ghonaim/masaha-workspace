# الأوامر المتبقية للجولة الثانية — بأداة Kilo CLI (2026-10-18)

ستة عشر تقريرًا. كل تقرير في **جلسة Kilo جديدة** مفتوحة في `C:\dev\masaha\design` (على آخر `main`).
ثلاث جلسات معًا على الأكثر. لكل جلسة نموذج قوي من القائمة، لا نموذج صغير.

**الصق الأمر، ثم هذا السطر بعده في الرسالة نفسها:**

```
Use ONLY the playwright MCP tools to see pages (browser_navigate, browser_resize, browser_take_screenshot, browser_press_key, browser_evaluate, browser_snapshot); never review from source alone and never write "no browser". Hard rules for every issue: (1) it reports what you OBSERVED on the rendered page, with the measured fact quoted (the browser_evaluate result, the focused element, the pixel size, the contrast numbers) — never "unverified", "ensure", "must be" or a restated decision; if you could not observe it, it is not an issue, it goes under "What was not reviewed"; (2) it has ITS OWN capture of ITS OWN frame, taken at its width and mode — one capture never serves two issues; (3) cover every page of the prompt's scope at every width and mode it names before writing the report. Save captures with the ABSOLUTE filename C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\<PART-AXIS>\<ID>.png (if refused, save relative and move it there). Write nothing else anywhere (no snapshot or note files in the repository). The prompt's §2 SHA check: if HEAD differs from origin/main, run `git diff --quiet HEAD origin/main -- docs/design` — exit 0 means the design is identical, so write both SHAs, note "design unchanged", and continue the review (do not stop); only a non-zero exit is a stop. Never save any file inside C:\dev\masaha\design; if a capture lands there, MOVE it to the shots folder (never delete a capture), then check git status is empty. Write the report in parts: first the SHAs, the verdict and the five most important points, then append the rest in short steps.
```

**التجربة الأولى (2026-10-18) رُفضت:** صورة واحدة دليلًا لخمس مشكلات في خمس صفحات، ومشكلات «يجب»
و«غير مؤكَّد» لا ملاحظات، وملف ملاحظات تُرك داخل المستودع. نُقلت إلى `REPORT\_superseded\` و`shots\_aborted\`.
**الشرط الآن:** نموذج أقوى بالاسم (لا «Auto»)، والسطر أعلاه بقواعده الثلاث.

## أولًا: تجربة واحدة (لا تبدأ غيرها قبل أن أتحقق منها)
```
Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-PU-AX.md whole and follow it.
```

## ثم البقية (بعد نجاح التجربة)
```
Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-AU-DF.md whole and follow it.
```
```
Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-DK-DF.md whole and follow it.
```
```
Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-OW-AX.md whole and follow it.
```
```
Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-OW-CP.md whole and follow it.
```
```
Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-OW-DF.md whole and follow it.
```
```
Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-OW-EX.md whole and follow it.
```
```
Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-OW-TR.md whole and follow it.
```
```
Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-PU-CP.md whole and follow it.
```
```
Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-PU-DF.md whole and follow it.
```
```
Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-PU-EX.md whole and follow it.
```
```
Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-PU-TR.md whole and follow it.
```
```
Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-SH-AX.md whole and follow it.
```
```
Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-SH-CP.md whole and follow it.
```
```
Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-SH-DF.md whole and follow it.
```
```
Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-SH-VD.md whole and follow it.
```

## بعد كل تقرير
أرسل للمحلل اسمه فقط؛ يتحقق أنه حقيقي (صور فعلية، لا «no browser»، الأقسام الستة) قبل أن يُحتسب.
بعد الستة عشر: الملخّصات الستة ثم الملخّص الشامل.
