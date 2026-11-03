# Stages a variant of some files: python stage_variant.py <variant.py>
# The variant defines VARIANTS = {rel_path: function(text) -> staged text} and PLAIN = [rel paths
# staged as they are]. Each variant file is backed up by copy, rewritten, `git add`ed, then restored
# by copy, so the working tree keeps the full version.
import os, runpy, shutil, subprocess, sys
REPO = r'C:\dev\masaha\app-lane-w1'
here = os.path.dirname(os.path.abspath(__file__))
spec = runpy.run_path(sys.argv[1])
for rel in spec.get('PLAIN', []):
    subprocess.run(['git', 'add', '--', rel], cwd=REPO, check=True)
for rel, change in spec.get('VARIANTS', {}).items():
    path = os.path.join(REPO, rel)
    bak = os.path.join(here, 'stage-bak-' + os.path.basename(rel))
    shutil.copyfile(path, bak)
    try:
        text = open(path, encoding='utf8', newline='').read()
        staged = change(text)
        assert staged != text or spec.get('ALLOW_SAME'), rel
        open(path, 'w', encoding='utf8', newline='').write(staged)
        subprocess.run(['git', 'add', '--', rel], cwd=REPO, check=True)
    finally:
        shutil.copyfile(bak, path)
print(subprocess.run(['git', 'status', '--short'], cwd=REPO, capture_output=True, text=True).stdout)
