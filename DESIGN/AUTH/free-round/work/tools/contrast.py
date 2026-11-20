"""Contrast ratios (WCAG 2.x). Usage: python contrast.py FG BG [FG BG ...]  (hex, with or without #)"""
import sys
def lum(h):
    h = h.lstrip('#'); r, g, b = (int(h[i:i+2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)
def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True); return (la + 0.05) / (lb + 0.05)
if __name__ == '__main__':
    a = sys.argv[1:]
    for i in range(0, len(a), 2):
        r = ratio(a[i], a[i+1]); print(f"{a[i]:>8} on {a[i+1]:>8}: {r:5.2f}  {'AA' if r>=4.5 else ('large/UI' if r>=3 else 'FAIL')}")
