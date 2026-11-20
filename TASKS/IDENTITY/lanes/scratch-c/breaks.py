"""Lane C's breaks: each from a backup copy, the test run through the grant, restored by copy.

  python -I breaks.py <name> [<name> ...]      names: t13 t14 t15 t22-sea t22-underline
"""
import filecmp
import os
import shutil
import subprocess
import sys

REPO = r"C:\dev\masaha\app-design-lane-c"
HERE = os.path.dirname(os.path.abspath(__file__))
HEAVY = r"C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs"
WEB_TEST = ["npx", "vitest", "run", "--project", "unit", "scripts/browserIcons.unit.test.ts", "--root", "apps/web"]
API_TEST = ["npx", "vitest", "run", "--project", "unit", "src/modules/auth/email/resetEmail.unit.test.ts", "--root", "apps/api"]


def edit_text(path, old, new):
    def apply():
        with open(path, encoding="utf-8", newline="") as f:
            text = f.read()
        assert text.count(old) == 1, (path, old[:60])
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(text.replace(old, new))
    return apply


def replace_file(path, source):
    def apply():
        shutil.copyfile(source, path)
    return apply


BREAKS = {
    "t13": (
        os.path.join(REPO, r"apps\web\index.html"),
        edit_text(
            os.path.join(REPO, r"apps\web\index.html"),
            '    <link rel="icon" href="/favicon.svg" type="image/svg+xml" />\n',
            "",
        ),
        WEB_TEST,
    ),
    "t14": (
        os.path.join(REPO, r"apps\web\public\favicon.svg"),
        edit_text(
            os.path.join(REPO, r"apps\web\public\favicon.svg"),
            "@media (prefers-color-scheme:dark){.ink{fill:#f7fbff}.spark{fill:#d27ed0}}",
            "",
        ),
        WEB_TEST,
    ),
    "t15": (
        os.path.join(REPO, r"apps\web\public\favicon.ico"),
        replace_file(os.path.join(REPO, r"apps\web\public\favicon.ico"), os.path.join(HERE, r"out\break-32-only.ico")),
        WEB_TEST,
    ),
    "t22-sea": (
        os.path.join(REPO, r"apps\api\src\modules\auth\email\resetEmail.ts"),
        edit_text(
            os.path.join(REPO, r"apps\api\src\modules\auth\email\resetEmail.ts"),
            "ink: '#1a1f25',",
            "ink: '#02787d',",
        ),
        API_TEST,
    ),
    "t22-underline": (
        os.path.join(REPO, r"apps\api\src\modules\auth\email\resetEmail.ts"),
        edit_text(
            os.path.join(REPO, r"apps\api\src\modules\auth\email\resetEmail.ts"),
            ";text-decoration:underline;",
            ";",
        ),
        API_TEST,
    ),
}

for name in sys.argv[1:]:
    target, apply, test = BREAKS[name]
    backup = os.path.join(HERE, "backup-" + os.path.basename(target))
    shutil.copy2(target, backup)
    try:
        apply()
        assert not filecmp.cmp(target, backup, shallow=False), "the break changed nothing"
        result = subprocess.run(["node", HEAVY, "lane-c", *test], cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace")
        log = os.path.join(HERE, f"break-{name}.log")
        with open(log, "w", encoding="utf-8", newline="") as f:
            f.write(result.stdout + "\n--- stderr ---\n" + result.stderr)
        print(f"== {name}: exit {result.returncode}, log {log}")
        for line in result.stdout.splitlines():
            if "FAIL" in line or "Tests " in line or "AssertionError" in line or line.strip().startswith(("-", "+", "Expected", "Received")):
                print("   " + line.rstrip()[:220])
    finally:
        shutil.copyfile(backup, target)
        print(f"   restored {target}: {'identical to the backup' if filecmp.cmp(target, backup, shallow=False) else 'DIFFERS'}")
