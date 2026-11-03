import io, re
p = r'C:\dev\masaha\app\apps\web\scripts\libraryChunks.unit.test.ts'
s = io.open(p, encoding='utf8', newline='').read()
start = s.index('    [String.raw`C:')
end = s.index("'calendar'],", start) + len("'calendar'],")
good = r"    [String.raw`C:\repo\node_modules\react-day-picker\dist\esm\DayPicker.js`, 'calendar'],"
s = s[:start] + good + s[end:]
io.open(p, 'w', encoding='utf8', newline='').write(s)
print(s[start-80:start+len(good)+10])
