def edit(p, old, new):
    s=open(p,encoding='utf8').read(); assert old in s, (p, old[:50]); s=s.replace(old,new,1)
    open(p,'w',encoding='utf8',newline='').write(s)
edit('packages/shared/src/core/errors.ts', """  'FAVORITES_LIMIT_REACHED',
] as const;""", """  'FAVORITES_LIMIT_REACHED',
  // a subscribe from a published price whose amount the desk showed differs from the price now:
  // nothing is written (subscriptions)
  'PUBLISHED_PRICE_CHANGED',
] as const;""")
edit('apps/web/src/shared/copy/arabic/errors.ts', """  FAVORITES_LIMIT_REACHED: 'امتلأت مفضّلتك؛ أزل مساحة أولًا.',
""", """  FAVORITES_LIMIT_REACHED: 'امتلأت مفضّلتك؛ أزل مساحة أولًا.',
  PUBLISHED_PRICE_CHANGED: 'تغيّر هذا السعر منذ فتحت النافذة. راجع المبلغ الجديد، ثم أكّد.',
""")
edit('apps/web/src/shared/copy/english/errors.ts', """  FAVORITES_LIMIT_REACHED: 'Your favourites are full; remove a space first.',
""", """  FAVORITES_LIMIT_REACHED: 'Your favourites are full; remove a space first.',
  PUBLISHED_PRICE_CHANGED: 'This price changed since the sheet opened. Check the new amount, then confirm.',
""")
edit('docs/api/api-contract.md', "`FAVORITES_LIMIT_REACHED` (409: a new favourite past the user's 200, 2026-10-25, #121).", "`FAVORITES_LIMIT_REACHED` (409: a new favourite past the user's 200, 2026-10-25, #121) · `PUBLISHED_PRICE_CHANGED` (409: a subscribe from a published price whose amount the desk showed differs from the price now, 2026-10-29, #PRNUM).")
