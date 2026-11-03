import sys
path = r'C:\dev\masaha\app-lane-b\apps\web\src\pages\showcase\fixtures.json'
with open(path, encoding='utf8', newline='') as f:
    lines = f.read().split('\n')

AR = '''      "filterTag": {
        "title": "وسوم الفلاتر",
        "caption": "فلاتر مطبّقة، يُزال كلٌّ منها بزرّه",
        "tags": [
          { "label": "المساحة: نور هب", "removeLabel": "إزالة فلتر المساحة في العرض" },
          { "label": "الحقل: الأسعار", "removeLabel": "إزالة فلتر الحقل في العرض" }
        ],
        "clear": "مسح الفلاتر"
      }'''
EN = '''      "filterTag": {
        "title": "Filter tags",
        "caption": "Filters in force, each removed by its button",
        "tags": [
          { "label": "Space: Nour Hub", "removeLabel": "Remove the sample space filter" },
          { "label": "Field: Prices", "removeLabel": "Remove the sample field filter" }
        ],
        "clear": "Clear filters"
      }'''

en_start = lines.index('    "en": {')
# The ar section's last sample closes two lines above "en": its "      }" then "    },".
assert lines[en_start - 1] == '    },' and lines[en_start - 2] == '      }', lines[en_start - 2:en_start]
lines[en_start - 2] = '      },'
lines[en_start - 1:en_start - 1] = AR.split('\n')
# The en section ends the file: "      }", "    }", "  }", "}", "".
assert lines[-5:] == ['      }', '    }', '  }', '}', ''], lines[-5:]
lines[-5] = '      },'
lines[-4:-4] = EN.split('\n')
with open(path, 'w', encoding='utf8', newline='') as f:
    f.write('\n'.join(lines))
print('ok')
