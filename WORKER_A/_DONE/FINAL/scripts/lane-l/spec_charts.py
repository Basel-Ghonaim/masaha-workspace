months_v=[[1200,3400],[980,3900],[1430,4100],[1610,3800]]
hours=['8','10','12','14','16','18']
days_v=[[2,9,14,12,6,1],[3,11,16,15,8,2],[1,7,10,9,4,0]]
AR={
 'barChart':{'title':'المخطّط العمودي','stackedCaption':'سلسلتان مكدّستان، بمفتاح الألوان','singleCaption':'سلسلة واحدة بالحجم الصغير، بلا مفتاح',
  'chart':'الدخل حسب الشهر','period':'الشهر','unit':'₪','series':['الزيارات','الاشتراكات'],
  'months':[{'label':l,'tick':t,'values':v} for (l,t),v in zip([('يوليو 2026','يوليو'),('أغسطس 2026','أغسطس'),('سبتمبر 2026','سبتمبر'),('أكتوبر 2026','أكتوبر')],months_v)]},
 'heatmap':{'title':'الخريطة الحرارية','caption':'الأيام في الساعات، بخمس درجات من الأقل إلى الأكثر',
  'chart':'أوقات الذروة','unit':'زيارات','day':'اليوم','fewer':'أقل','more':'أكثر','hours':hours,
  'days':[{'label':l,'values':v} for l,v in zip(['السبت','الأحد','الإثنين'],days_v)]}}
EN={
 'barChart':{'title':'Bar chart','stackedCaption':'Two stacked series, with a legend','singleCaption':'One series at the small size, without a legend',
  'chart':'Income by month','period':'Month','unit':'ILS','series':['Visits','Subscriptions'],
  'months':[{'label':l,'tick':t,'values':v} for (l,t),v in zip([('July 2026','Jul'),('August 2026','Aug'),('September 2026','Sep'),('October 2026','Oct')],months_v)]},
 'heatmap':{'title':'Heatmap','caption':'Days by hours, in five steps from fewer to more',
  'chart':'Busy hours','unit':'visits','day':'Day','fewer':'Fewer','more':'More','hours':hours,
  'days':[{'label':l,'values':v} for l,v in zip(['Saturday','Sunday','Monday'],days_v)]}}
