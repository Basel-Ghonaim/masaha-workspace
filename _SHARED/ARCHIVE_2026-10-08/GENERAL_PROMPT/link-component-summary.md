# تقرير ملخص: بناء Link Component في Design System

## أولاً — أهم الـ Props

| Prop | النوع | الغرض |
|---|---|---|
| `to / href` | `string` | الوجهة. الأفضل توحيدها في prop واحد (`href`) والمكوّن يقرر داخلياً |
| `external` | `boolean` | يفرض التعامل كرابط خارجي (اختياري، لأن المكوّن يمكنه الاكتشاف تلقائياً) |
| `variant` | `'primary' \| 'subtle' \| 'inline'` | الشكل البصري (لون، underline، إلخ) — يُبنى على التوكنز الموجودة عندكم |
| `size` | `'sm' \| 'md' \| 'lg'` | من طبقة typography عندكم |
| `disabled` | `boolean` | يمنع التنقل + `aria-disabled` |
| `openInNewTab` | `boolean` | يضيف `target="_blank"` + `rel="noopener noreferrer"` تلقائياً |
| `showExternalIcon` | `boolean` | أيقونة للروابط الخارجية (من Icon Button/Icon الموجود عندكم) |
| `className` | `string` | للتوسّع عبر CSS Modules |
| `children` | `ReactNode` | المحتوى |
| `...rest` | `AnchorHTMLAttributes` | تمرير باقي خصائص `<a>` (`onClick`, `aria-label`, `id`...) |

### نقطتان مهمتان

- استخدم `forwardRef` (في React 19 يمكن تمرير `ref` كـ prop مباشرة).
- إذا كان `disabled`: لا تُصيّر `href` أصلاً، وأضف `tabIndex={-1}` لتجنب الوصول له بالكيبورد.

---

## ثانياً — هل يُبنى على react-router-dom؟

نعم، للروابط الداخلية يجب أن يستخدم `Link` من `react-router-dom` داخلياً، لأنه:

- يمنع إعادة تحميل الصفحة (client-side navigation).
- يحافظ على state الـ Redux وحالة التطبيق.
- يدعم `NavLink` لو احتجت حالة active في التنقّل الرئيسي.

لكن القاعدة الذهبية في الـ Design System:

> لا تُصدّر `react-router` للمستهلك. أي أن المكوّن يغلّف `RouterLink` داخلياً، وباقي المشروع يستورد `Link` من الـ Design System فقط.

هكذا إن تغيّر الراوتر مستقبلاً، يكون التعديل في ملف واحد.

---

## ثالثاً — الروابط الخارجية و `<a>`

نعم، الروابط الخارجية تُبنى على `<a>` عادي، لأن `RouterLink` لا يعرف كيف يتعامل مع دومين خارجي (سيعامله كمسار داخلي ويكسر التنقل).

### أفضل بنية

مكوّن واحد يتفرّع داخلياً — لا مكوّنين منفصلين.

```tsx
import { Link as RouterLink } from 'react-router-dom';
import styles from './Link.module.css';

const isExternalHref = (href: string) =>
  /^(https?:)?\/\//.test(href) || href.startsWith('mailto:') || href.startsWith('tel:');

export function Link({
  href, external, openInNewTab, disabled, variant = 'primary',
  size = 'md', className, children, ref, ...rest
}: LinkProps) {
  const isExternal = external ?? isExternalHref(href);
  const classes = [styles.link, styles[variant], styles[size], className].filter(Boolean).join(' ');
  const newTab = openInNewTab ?? isExternal;

  if (disabled) {
    return <a ref={ref} className={classes} aria-disabled tabIndex={-1} {...rest}>{children}</a>;
  }

  if (isExternal) {
    return (
      <a ref={ref} href={href} className={classes}
         target={newTab ? '_blank' : undefined}
         rel={newTab ? 'noopener noreferrer' : undefined} {...rest}>
        {children}
      </a>
    );
  }

  return <RouterLink ref={ref} to={href} className={classes} {...rest}>{children}</RouterLink>;
}
```

---

## ملاحظات ختامية

### الاكتشاف التلقائي + override
المكوّن يكتشف الرابط الخارجي من شكل الـ `href`، لكن prop `external` يسمح بالتجاوز اليدوي في الحالات الخاصة (مثلاً subdomain لنفس المنتج).

### الأمان
`rel="noopener noreferrer"` إلزامي مع `target="_blank"`.

### اتساق التصميم
نفس ملف CSS Module يخدم الفرعين، فالمظهر موحّد بغض النظر عن العنصر الأساسي.

### الاختبار
غلّف الاختبارات بـ `MemoryRouter` لأن `RouterLink` يحتاج سياق راوتر.

### Button vs Link
إن كان الفعل يغيّر حالة ولا ينقل لصفحة، استخدم `Button` الموجود عندكم لا `Link` — الفرق دلالي ومهم للوصولية.
