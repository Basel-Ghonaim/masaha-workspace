# F-3 input — real survey data (owner: Basel Ghoneim, collected 2026-09-28)

This file is the owner's input for F-3. The lookups (areas, amenities) come from it. The six spaces below are **reference data for validating the schema**, not seed data: they are entered later through the admin screens. Where a value is marked **(OPEN)**, propose an answer in the plan step and let the owner decide.

## 1. Owner decisions that shape the schema

1. **Areas are two-level:** governorate → area/neighbourhood, covering the whole Gaza Strip. Each area has an **active/hidden flag** that the admin manages (areas beyond the yellow line can be hidden and restored later without deleting data). All six reference spaces are in Gaza City today.
2. **Seat prices:**
   - The periods are hour, day, week and month. Every period is optional per space: some spaces have no hourly or no weekly price.
   - A price can also have an **audience**: general, or student. Number One Hub has a separate student monthly price.
   - A space may add other labelled price rows later, so the price model must allow a custom label.
3. **Halls for rent and technical trainings** are **amenities (yes/no) in v1**. They have no prices and no booking; booking is *Not in v1*.
4. **Opening hours** differ by space: opening is 8, 9 or 10 am, and closing is anywhere from 5 pm to 10 pm. Hours are stored **per day of week**, with a closed flag. In the data collected so far every space uses one daily range. **Friday:** most spaces are closed, some open. So the default template for a new space is Saturday–Thursday open and Friday closed, and each space can change any day.
5. **Contact channels vary per space:** WhatsApp, mobile (Jawwal / Ooredoo), email, Instagram, Facebook and TikTok. So contacts are a **list of typed entries** per space (type + value), not fixed columns.
   - Phone numbers arrive in mixed formats (`00970…`, `+972…`, local `05…`). Normalise them to E.164 on save.
   - Numbers are displayed LTR.
6. **Capacity is private — decided by the owner (2026-09-28).**
   - No space publishes its seat count. Capacity is stored and visible **only to the space's owner** (dashboard). It never appears on public pages or in the public API.
   - **Public live status is a state, never a number.** The states are:
     - **Available** (متاح): open now, and fewer open check-ins than capacity;
     - **Full** (ممتلئ): open now, and open check-ins ≥ capacity;
     - **Closed now** (مغلق الآن): outside today's opening hours. This comes from the hours, not the seats, so a closed space is never shown as "Available".
   - Unverified spaces (no owner, no live data) show no live state ("لا تتوفر حالة مباشرة").
   - **Consequences to record in F-3:**
     - `data-model.md` *Derived values*: replace "Available seats" with this state rule.
     - The planned API: `GET /spaces/:slug/occupancy` returns `{ status: "AVAILABLE" | "FULL" | "CLOSED" }`, never counts.
     - The directory's "available now" filter uses the state.
     - The owner's dashboard still shows exact numbers (present / capacity).

7. **Price freshness:**
   - Prices have their own staleness threshold of **30 days**, adjustable in admin settings. Other fact groups use **60 days**.
   - **Unverified space with a stale price:** the number is hidden, "Price not up to date — contact the space" is shown, and the space is excluded from the price filter.
   - **Verified space with a stale price:** the price is shown with a "may have changed" note, plus a reminder in the owner's overview.
   - All prices below were known on **2026-09-28**.
8. **Addresses** are free text with landmarks (Arabic required, English optional), plus a map location (lat/lng). The owner will collect a map pin for each space before data entry.

## 2. Lookups (seed)

### Governorates
| عربي | English | Active? |
|---|---|---|
| شمال غزة | North Gaza | ☑ |
| غزة | Gaza City | ☑ |
| الوسطى (دير البلح) | Deir al-Balah (Middle Area) | ☑ |
| خان يونس | Khan Younis | ☑ |
| رفح | Rafah | ☐ hidden (wholly unreachable today) |

### Areas — the whole Strip
Confirmed by the owner (2026-09-28). An area is **Active** when it is reachable and in use today, and **Hidden** when it is unreachable (for example beyond the yellow line). Hidden rows stay in the database but do not appear in filters or forms. The admin changes the flag from the Lookups screen as the situation changes. Governorates carry the same flag.

| Governorate | عربي | English | Status |
|---|---|---|---|
| North Gaza | شمال قطاع غزة | North Gaza Strip | ☑ Active: one area for now; most of the governorate is unreachable, so Jabalia, Beit Lahia and Beit Hanoun are not separate areas yet |
| Gaza City | الرمال | Al-Rimal | ☑ Active |
| Gaza City | النصر | An-Nasr | ☑ Active |
| Gaza City | الشيخ رضوان | Sheikh Radwan | ☑ Active |
| Gaza City | تل الهوا | Tal al-Hawa | ☑ Active |
| Gaza City | الشيخ عجلين | Sheikh Ijlin | ☑ Active |
| Gaza City | الصبرة | Al-Sabra | ☑ Active |
| Gaza City | الزيتون | Al-Zeitoun | ☑ Active |
| Gaza City | الدرج | Al-Daraj | ☑ Active |
| Gaza City | التفاح | Al-Tuffah | ☑ Active |
| Gaza City | الشاطئ | Al-Shati (Beach) | ☑ Active |
| Gaza City | الشجاعية | Al-Shuja'iyya | ☐ Hidden |
| Deir al-Balah | دير البلح | Deir al-Balah | ☑ Active |
| Deir al-Balah | النصيرات | Nuseirat | ☑ Active |
| Deir al-Balah | البريج | Bureij | ☑ Active |
| Deir al-Balah | المغازي | Maghazi | ☑ Active |
| Deir al-Balah | الزوايدة | Al-Zawaida | ☑ Active |
| Khan Younis | خان يونس (المدينة) | Khan Younis (city) | ☑ Active |
| Khan Younis | المواصي | Al-Mawasi | ☑ Active |
| Khan Younis | بني سهيلا | Bani Suheila | ☐ Hidden |
| Khan Younis | عبسان | Abasan | ☐ Hidden |
| Khan Younis | القرارة | Al-Qarara | ☐ Hidden |
| Khan Younis | خزاعة | Khuza'a | ☐ Hidden |
| Rafah | رفح (المدينة) | Rafah (city) | ☐ Hidden |
| Rafah | تل السلطان | Tal al-Sultan | ☐ Hidden |

ZM Hub (شارع النفق) is in Gaza City. Its exact area is chosen when the space is entered, so nothing is needed for the seed.

### Amenities
| عربي | English | Note |
|---|---|---|
| إنترنت | Internet | one entry (owner decision): no fiber/fast distinction |
| كهرباء مستقرة | Stable power | |
| طاقة شمسية | Solar power | |
| خط كهرباء مولّد | Generator power line | |
| مشروبات ساخنة | Hot drinks | |
| قاعة اجتماعات | Meeting room | |
| قاعات للإيجار | Halls for rent | amenity only in v1, no price |
| دورات تدريبية تقنية | Technical training | amenity only in v1, no price |

## 3. Other lists (OPEN — propose in the plan step)
- **Membership types:** daily, weekly, monthly (the stress test also showed "seasonal").
- **Announcement types:** proposed general, power/internet outage, temporary closure, offer, event.
- **Data-report fields:** prices, hours, contact, location, amenities, other.
- **Default auto check-out:** at the space's closing time.
- **Admin account email, and the platform contact email / WhatsApp:** the owner provides these in `.env` and settings, never in the repo.

## 4. Reference spaces (schema validation only — not seeded)

| Space | Area | Capacity (private) | Hour | Day | Week | Month | Other | Hours | Amenities | Contact |
|---|---|---|---|---|---|---|---|---|---|---|
| Focus Hub · فوكس هاب | النصر، غرب المزنر | 40 | 3 | 15 | 90 | 300 | — | 08–18 | Internet, solar, generator, hot drinks | — |
| Number One Hub · نمبر ون هاب | النصر، قبل برج الوحدة | 50 | 3 | 15 | 90 | 300 | **student month 250** | 08–18 | Internet, solar, generator | — |
| Branch Hub · برانش هاب | الرمال، شارع الثورة، عمارة مشتهى | 80 | 4 | 30 | 150 | 500 | — | 08–22 | Internet, solar, generator, hot drinks, training, halls | — |
| ZM Hub | شارع النفق، بجوار منجرة العشي | 40 | 3 | 14 | — | 270 | — | 08–18 | Internet, stable power | WhatsApp, Ooredoo mobile |
| Golden Hub | غرب مفترق السرايا (الرمال) | — | 3 | 15 | — | 300 | — | 08–18 | Internet, stable power | WhatsApp, email, Instagram, TikTok |
| White Space | الرمال، شارع أحمد عبدالعزيز، عمارة الكنز الذهبي ط4 | — | — | 15 | 100 | 350 | — | 08–19 | Internet, stable power | WhatsApp, Ooredoo mobile, email, Instagram |

All prices are in ILS (₪) and were known on 2026-09-28. Contact values are kept in the owner's survey file and entered later; they are not needed for the schema.

**What these cases prove the schema must handle:**
- missing periods (no hourly, no weekly);
- a student price;
- the same hours every day, with room for per-day differences;
- a variable set of contact channels;
- private capacity;
- two kinds of power (solar and generator) as separate amenities.
