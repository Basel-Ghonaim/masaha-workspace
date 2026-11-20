#!/usr/bin/env bash
# Renders each strip-*.svg to a PNG beside it (headless Chrome, 2x).
cd "$(dirname "$0")"
C="/c/Program Files/Google/Chrome/Application/chrome.exe"
for f in strip-*.svg; do
  "$C" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 --window-size=960,1080 --screenshot="$(cygpath -w "$PWD/${f%.svg}.png")" "file:///$(cygpath -m "$PWD/$f")" >/dev/null 2>&1
done
ls -la *.png | awk '{print $5, $9}'
