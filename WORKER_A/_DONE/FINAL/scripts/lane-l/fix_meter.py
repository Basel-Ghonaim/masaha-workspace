import json
p=r'C:\dev\masaha\app-lane-l\apps\web\src\pages\showcase\fixtures.json'
d=json.loads(open(p,encoding='utf8').read())
d['samples']['ar']['meter']={
 "title":"مقياس النسبة",
 "caption":"نسبة من كل: الإشغال، وبلون التنبيه حين يقترب من الامتلاء",
 "occupancy":{"label":"المقاعد المشغولة","value":27,"max":40,"text":"27 من 40"},
 "full":{"label":"المقاعد المشغولة في القاعة الصغيرة","value":11,"max":12,"text":"11 من 12"},
 "progressCaption":"تقدّم مهمة: رفع صورة",
 "upload":{"label":"رفع صورة المساحة","value":45}}
d['samples']['en']['meter']={
 "title":"Share meter",
 "caption":"A share of a whole: occupancy, and in the warning tone when nearly full",
 "occupancy":{"label":"Seats taken","value":27,"max":40,"text":"27 of 40"},
 "full":{"label":"Seats taken in the small room","value":11,"max":12,"text":"11 of 12"},
 "progressCaption":"A task's progress: uploading a photo",
 "upload":{"label":"Uploading the space's photo","value":45}}
open(p,'w',encoding='utf8',newline='').write(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
