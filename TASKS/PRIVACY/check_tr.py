import re
filepath = r"C:\dev\masaha\app-b\docs\design\prototype\Privacy.html"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()
found = False
for m in re.finditer(r'tr\("[^"]*"', content):
    if "<" in m.group():
        print("FOUND < in tr():", m.group())
        found = True
if not found:
    print("No < found inside tr() strings")