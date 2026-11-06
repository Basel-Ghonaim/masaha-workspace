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
    print("No < found inside tr() strings - OK")
print("strong count:", content.count("<strong>"))
print("ul count:", content.count("<ul"))
print("li count:", content.count("<li"))
# Check for the two Arabic word fixes
has_mushtarka = "\u0627\u0644\u0645\u0634\u062a\u0631\u0643\u0629" in content
has_salahiya = "\u0635\u0644\u0627\u062d\u064a\u0629 \u0643\u0644 \u0645\u0633\u062a\u062e\u062f\u0645" in content
has_salahiyyat = "\u0635\u0644\u0627\u062d\u064a\u0627\u062a \u0643\u0644 \u0645\u0633\u062a\u062e\u062f\u0645" in content
with open(r"C:\dev\masaha\workspace\TASKS\PRIVACY\verify_result.txt", "w", encoding="utf-8") as out:
    out.write("Has 'المشتركة': " + str(has_mushtarka) + "\n")
    out.write("Has 'صلاحية كل مستخدم': " + str(has_salahiya) + "\n")
    out.write("Has 'صلاحيات كل مستخدم': " + str(has_salahiyyat) + "\n")