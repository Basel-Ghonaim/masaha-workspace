"""Second version of render.mjs: the 120 drawn whole-pixel (no resampled seam), a crop to look at,
and the Chrome's PID checked gone after taskkill."""
P = r"C:\dev\masaha\workspace\TASKS\IDENTITY\lanes\scratch-c\render.mjs"
s = open(P, encoding="utf-8", newline="").read()


def sub(old, new):
    global s
    assert s.count(old) == 1, old[:80]
    s = s.replace(old, new)


sub(
    """  // The 120: the mark's drawn pixels measured (bounding box, farthest pixel from its centre), then
  // scaled so that farthest pixel sits at 80 % of the circle's radius, centred: a round crop keeps
  // 12 px clear of the mark at its closest.
""",
    """  // The 120: the mark at 96 px, centred (12 px of white all round its square), whole pixels so Chrome
  // draws the SVG at its size and never resamples a bitmap (a fractional size left a light seam where
  // the mark's two mirrored halves meet). The mark's drawn pixels are measured first, to prove its
  // farthest pixel stays within 80 % of the 120's circle (48 px): a round crop keeps >= 12 px clear.
""",
)
sub(
    """  const scale = 48 / measure.maxR;
  const layout = { size: N * scale, left: 60 - measure.cx * scale, top: 60 - measure.cy * scale };
""",
    """  const layout = { size: 96, left: 12, top: 12 };
  const farthest = (measure.maxR * layout.size) / N;
  const offCentre = [measure.cx, measure.cy].map((c) => (c / N - 0.5) * layout.size);
  if (farthest > 48) throw new Error(`the mark's farthest pixel at ${farthest} px > 48`);
  console.log('the 120: farthest pixel', farthest.toFixed(2), 'px; the drawing\\'s centre off by', offCentre.map((d) => d.toFixed(2)).join(', '), 'px');
""",
)
sub(
    """    file: out('preview-120.png'),
  });
""",
    """    file: out('preview-120.png'),
  });
  // The bottom of the mark, close: the owner's mark at 778 px (one viewBox unit a pixel), its last 140
  // rows shown at 3x; and the 32 px favicon at 12x.
  await capture({
    width: 900,
    height: 820,
    background: WHITE,
    body: `<div style="width:${778 * 1}px;height:140px;overflow:hidden;transform:scale(1.1);transform-origin:0 0"><img src="${svg(MARK)}" width="778" height="778" style="margin-top:-638px" alt=""></div><div style="margin-top:60px">${tile(png(out('favicon-light-32.png')), 32, 12)}${tile(png(out('reference-light-64.png')), 64, 6)}</div>`,
    file: out('preview-bottom.png'),
  });
""",
)
sub(
    """  try {
    execFileSync('taskkill', ['/PID', String(chrome.pid), '/T', '/F'], { stdio: 'pipe' });
    console.log(`stopped chrome pid ${chrome.pid}`);
  } catch (error) {
    console.log(`taskkill ${chrome.pid}: ${String(error.stderr ?? error.message).trim()}`);
  }
""",
    """  try {
    execFileSync('taskkill', ['/PID', String(chrome.pid), '/T', '/F'], { stdio: 'pipe' });
  } catch (error) {
    // A child already gone makes taskkill report an error; the check below is what counts.
    console.log(`taskkill ${chrome.pid}: ${String(error.stderr ?? error.message).trim()}`);
  }
  await new Promise((done) => setTimeout(done, 1000));
  const left = execFileSync('tasklist', ['/FI', `PID eq ${chrome.pid}`, '/NH'], { encoding: 'utf8' });
  console.log(
    left.includes(String(chrome.pid)) ? `chrome pid ${chrome.pid} STILL RUNNING` : `chrome pid ${chrome.pid} stopped, none left`,
  );
""",
)
open(P, "w", encoding="utf-8", newline="").write(s)
print("ok")
