# Masaha — the sign-in page, a free design round

You are a designer, starting fresh. This round has one purpose: **to see what you make when you are free.**
Earlier rounds on this page were correct, careful and forgettable. Each one was handed a long list of what it
could not do, and every designer ended up with the same quiet answer. This time you get principles to start from,
the page's real requirements, and three references the owner loves. Everything else is yours to decide.

Give it your full ambition. The aim is a page that someone remembers: confident, crafted, with a character that
could only belong to this product. It should not read like a template, and it should not look as if a machine made it.

## 1. The product

**Masaha (مساحة, "space")** is a live, bilingual web platform for the coworking spaces of the **Gaza Strip**. It is
Arabic first, with English as its second language.

- **The people.** Students, freelancers and remote workers need two things to work: power and internet, and both
  are scarce. A coworking space that is open right now is news they need. Most of them are on a phone, often on a
  weak connection.
- **What Masaha gives them.** A directory of the real spaces (13 today, in Gaza City, Nuseirat, Deir al-Balah and
  Al-Mawasi), each with its hours, prices, amenities and how to reach it. Many spaces also show a live state:
  available, full or closed now.
- **The owners.** Owners and their reception staff run their space from a dashboard: the front desk, customers,
  payments and the space's public page.
- **Why people sign in.**
  - A visitor signs in to save favourite spaces and follow the reports they send about wrong information.
  - An owner or a receptionist signs in to reach their dashboard.
- **Its character.** Everyday life and work going on: practical, warm, resilient, local. People rely on it daily.

## 2. The three references the owner chose

They are in `materials/references/`. Here is what in each one speaks to this product, as the supervisor reads it.
Take their spirit, not their look. No part of your page should be a copy of theirs.

- **Tabby** (`tabby.png`, an Arabic-first fintech app). The brand's colour owns the whole page. The Arabic
  headline is heavy and sure of itself. The illustration has personality.
- **Careem** (`careem.png`, an Arabic-first app for rides and deliveries). The city is the hero: a dark map, with
  the brand's colour glowing along its streets. The product's own world is the image.
- **Thmanyah / ثمانية** (`thmanyah.jpg`, an Arabic media house). This is Arabic editorial craft: a typeface with
  character, a warm paper ground, and hand-drawn illustration instead of stock photos.

## 3. Principles to start from (the design system)

These are where you begin. Wherever your direction is stronger for leaving one, leave it, and say why in its
DESIGN.md.

- **Identity.** The logo is in `materials/logo/`: «مساحة» over "MASAHA", with the ة's two dots in the berry. Its
  two colours are an **ink** and a **berry**:
  - light theme: ink `#1A1F25`, berry `#B55BB3`, ground `#F7FBFF`;
  - dark theme: ink `#F7FBFF`, berry `#D27ED0`, ground `#0D1217`.

  How much berry, where it goes and what it does are yours to decide. Notice that the three references use their
  brand colour boldly. Add other colours if your direction needs them.
- **Arabic first.** Design right to left first, in Arabic. The English page is the same design read left to right,
  built on logical sides (start and end, not left and right). Arabic display type at real size can carry a page by
  itself.
- **Type.** Choose freely. Any free font works (Google Fonts loads here), and Arabic display faces are welcome. The
  product uses IBM Plex Sans Arabic today: keep it or replace it. Load only the weights you use, since your readers
  are on weak connections.
- **Rhythm.** An 8 px grid for spacing and sizes.
- **Two themes.** Light and dark, each one designed, not inverted.
- **Usable by everyone, as part of the craft:**
  - body text at 4.5 : 1 contrast or more, large text and controls at 3 : 1;
  - one clear focus ring;
  - touch targets of 44 px;
  - every field with its label;
  - the page's title as its `h1`.
- **Light on the network.** Inline SVG and CSS go a long way. If you use an image, keep it small.

## 4. The page

**Type of page:** a sign-in page with two ways in. One is for people coming back. The other is for people new to
Masaha. The composition is yours.

**What the page holds.** These are production's real words. You may propose better or new words, in both languages,
marked as proposals.

- **The logo,** and two switches: language (English / العربية) and theme (light / dark).
- **The title and description:**
  - «تسجيل الدخول» / "Sign in";
  - «سجّل الدخول لحفظ مساحاتك المفضّلة ومتابعة بلاغاتك، أو لإدارة مساحتك.» / "Sign in to save your favourite
    spaces and follow your reports, or to run your space."
- **Google sign-in:** «المواصلة باستخدام Google» / "Continue with Google". This is Google's own button: Google
  renders it, in its light style or its dark style, 40 px tall and up to 400 px wide. Draw it as Google draws it.
  The divider after it is «أو» / "or".
- **The form:**
  - email: «البريد الإلكتروني» / "Email", placeholder `name@example.com`, typed left to right;
  - password: «كلمة المرور» / "Password";
  - the link «نسيت كلمة المرور؟» / "Forgot password?";
  - the submit button «تسجيل الدخول» / "Sign in".
- **The way in for new people:**
  - «ليس لديك حساب؟» / "No account?" with «إنشاء حساب» / "Create account";
  - the owners' note «تدير مساحة عمل؟ حسابات أصحاب المساحات ينشئها فريق مساحة.» / "Run a coworking space? Space
    owner accounts are created by the Masaha team.", followed by «تواصل معنا» / "Contact us".
- **A way back:** «العودة إلى الرئيسية» / "Back to home". When the person came from a space's page, it reads
  «العودة إلى <the space>».
- **The privacy link:** «سياسة الخصوصية» / "Privacy policy".
- **The states, each shown somewhere in your pages:**
  - wrong credentials: «تعذّر تسجيل الدخول» with «البريد الإلكتروني أو كلمة المرور غير صحيحة.» / "Couldn't sign
    in" with "The email or password is incorrect.";
  - too many attempts: «محاولات كثيرة. انتظر قليلًا ثم حاول مرة أخرى.» / "Too many attempts. Please wait a moment
    and try again.";
  - no connection: «لا يوجد اتصال. تحقّق من الإنترنت وحاول مرة أخرى.» / "No connection. Check your internet and try
    again.";
  - submitting: the button is busy;
  - Google failed: «تعذّرت المتابعة باستخدام Google» / "Couldn't continue with Google";
  - a session ended for inactivity, a note above the form: «انتهت جلستك بعد 15 دقيقة دون نشاط. سجّل الدخول من
    جديد.» / "Your session ended after 15 minutes with no activity. Sign in again.";
  - field errors: «تحقّق من كتابة البريد الإلكتروني، مثل name@example.com» / "Check the email address, like
    name@example.com", and «أدخل كلمة المرور» / "Enter your password". A failed submit moves the focus to the first
    field with an error.
- **Anything that looks like data is real.** The 13 real spaces, with their names, areas and coordinates, are in
  `materials/spaces.json`. An approximate outline of the Strip (north up, the sea to the west) is in
  `materials/strip-outline.json`. People's details are placeholders (`name@example.com`). Any number you show is a
  true one.

## 5. How to work

1. **Start** by loading the skills `frontend-design:frontend-design` and `website-design:design-system`. They are
   good company for finding a direction.
2. **Think first,** in `work/NOTES.md`:
   - what you see in the three references;
   - then **three directions**, one paragraph each.

   Make them genuinely different ideas: in composition, in what carries the brand, in the berry's role and in the
   voice of the type. When two choices are close, take the bolder one.
3. **Draw each direction** in `work/<direction>/`, as HTML pages that open by themselves, from a double-click or a
   tiny static server. Start in Arabic, light, at 1440 and 390. Then do dark, then English. Write one `DESIGN.md`
   per direction: its colours, type, spacing, surfaces, components and the berry's role.
4. **Look at your work while you make it.** Capture it (§7), open each capture, fix what you see, and capture again.
   A direction is done when you would be proud to show it.
5. **After the first full draft, get a second opinion:**
   - review with `ui-design-review:review` or `design:design-critique`, and the Vectorlab `anti-slop`, `typography`
     and `spacing` skills. Take what makes a design stronger, and leave what would make it blander;
   - then read `materials/foundation-reference.md`, the product's current design system. For each direction, write
     what it keeps from the system and what it would change.
6. **When you are unsure,** decide in favour of the better page and write down why. The owner wants to see your
   choices, so do not stop to ask.

## 6. What to hand over, then stop

- **Per direction:** its pages, its `DESIGN.md`, and captures in `work/captures/`, named
  `<direction>-<width>-<lang>-<theme>.png`:
  - 1440 and 390, Arabic and English, light and dark;
  - plus Arabic light at 390 and 1440 for two states: wrong credentials, and submitting
    (`<direction>-<width>-ar-light-<state>.png`).
- **`work/REPORT.md`:**
  - each direction in three lines, and what to look at first;
  - its weakest point, said honestly;
  - which one you recommend, and why;
  - what you could not check.

Then stop. The owner looks at the pictures and chooses. Nothing here is committed or pushed: this folder is not a
repository.

## 7. The machine

- Windows 11, with Git Bash and PowerShell. Everything you make lives in this folder, `C:\dev\masaha\free-round`.
- **Captures:** use headless Chrome at `C:\Program Files\Google\Chrome\Application\chrome.exe`:
  `chrome.exe --headless=new --disable-gpu --hide-scrollbars --user-data-dir=<work/chrome-profile>
  --window-size=1440,900 --virtual-time-budget=5000 --screenshot=<png> <file:///…>`.
  - For a taller page, make the window taller.
  - On a right-to-left page, capture the viewport at the page's size, never a full-page capture: headless Chrome
    shifts RTL pages sideways when it captures beyond the viewport.
  - For the phone, let the page fill the window (`width: 100%`), not a fixed-width box, and use
    `--window-size=390,<height>`.
- **Memory:** about 15 GB in all, often 3–7 GB free. Run one Chrome at a time. If free memory is under 4 GB, wait a
  minute first. You can check it with PowerShell:
  `(Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory/1MB`.
- If a run is killed for memory, retry it once.
