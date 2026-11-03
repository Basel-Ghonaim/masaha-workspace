// What the 13 live spaces lack, completed for the demo. Prices in shekels (stored as agorot).
// Contacts: the live ones are kept; a space with no phone and no WhatsApp gets a visibly fictional
// number (0599 000 0xx). No social handle or site is invented.

export type Hours =
  | 'around-the-clock'
  | 'live'
  | { open: [string, string]; friday?: [string, string] | null; saturday?: [string, string] | null };

export interface RealSpace {
  slug: string;
  addressEn: string;
  hours: Hours;
  shifts?: { nameAr: string; nameEn: string; range: [string, string]; month: number }[];
  /** null: none published (a free space). 'live' keeps the live prices and adds these. */
  prices: null | {
    keepLive?: boolean;
    hour?: number;
    day?: number;
    week?: number;
    month?: number;
    studentHour?: number;
    studentDay?: number;
    studentMonth?: number;
  };
  /** Added to the live ones. */
  amenities: string[];
  ownAmenities?: [string, string?][];
  /** Fictional numbers, added only where the space has no phone and no WhatsApp. */
  fictional?: ['WHATSAPP' | 'PHONE', string][];
  owner?: { name: string; email: string; capacity: number };
  /** Days ago it was entered. */
  createdDaysAgo: number;
  /** A text the descriptions lack in English. */
  descriptionEn?: string;
}

export const REAL_SPACES: RealSpace[] = [
  {
    slug: 'pal-hub',
    addressEn: 'Al-Saraya, Jawwal building, Al-Rehab Mall',
    hours: { open: ['08:00', '22:00'], friday: ['12:00', '20:00'] },
    shifts: [
      { nameAr: 'صباحي', nameEn: 'Morning', range: ['08:00', '15:00'], month: 220 },
      { nameAr: 'مسائي', nameEn: 'Evening', range: ['15:00', '22:00'], month: 200 },
    ],
    prices: { hour: 5, day: 25, week: 120, month: 350, studentHour: 4, studentDay: 20, studentMonth: 280 },
    amenities: ['internet', 'solar_power', 'stable_power', 'hot_drinks', 'meeting_room', 'halls_for_rent'],
    ownAmenities: [['غرف خاصة للفرق', 'Private team rooms'], ['خزائن شخصية', 'Personal lockers']],
    fictional: [['WHATSAPP', '+970599000010'], ['PHONE', '+970599000020']],
    owner: { name: 'أحمد الشوا', email: 'demo-owner@example.com', capacity: 40 },
    createdDaysAgo: 66,
  },
  {
    slug: 'elevate-hub',
    addressEn: 'Nuseirat, north of Al-Zuhur junction, 50 m opposite Al-Razi Building',
    hours: { open: ['08:00', '20:00'], friday: ['14:00', '20:00'] },
    shifts: [
      { nameAr: 'صباحي', nameEn: 'Morning', range: ['08:00', '14:00'], month: 180 },
      { nameAr: 'مسائي', nameEn: 'Evening', range: ['14:00', '20:00'], month: 160 },
    ],
    prices: { hour: 4, day: 18, week: 90, month: 300, studentDay: 15 },
    amenities: ['internet', 'stable_power', 'solar_power', 'hot_drinks'],
    fictional: [['WHATSAPP', '+970599000012'], ['PHONE', '+970599000013']],
    owner: { name: 'محمد أبو شعبان', email: 'elevate.owner@example.com', capacity: 30 },
    createdDaysAgo: 17,
  },
  {
    slug: 'branch-hub',
    addressEn: 'Al-Thawra Street - Mushtaha Building',
    hours: 'live',
    prices: { keepLive: true, hour: 6, studentDay: 25 },
    amenities: [],
    owner: { name: 'خالد البطش', email: 'branch.owner@example.com', capacity: 45 },
    createdDaysAgo: 16,
  },
  {
    slug: 'number-one-hub',
    addressEn: 'Al-Shifa Street, near Al-Wehda Tower',
    hours: 'live',
    prices: { keepLive: true, studentDay: 12 },
    amenities: [],
    owner: { name: 'يوسف حمدان', email: 'numberone.owner@example.com', capacity: 35 },
    createdDaysAgo: 15,
  },
  {
    slug: 'focus-hub',
    addressEn: 'An-Nasr, west of Al-Mazanar, the first street on the left',
    hours: 'live',
    shifts: [
      { nameAr: 'صباحي', nameEn: 'Morning', range: ['08:00', '13:00'], month: 180 },
      { nameAr: 'مسائي', nameEn: 'Evening', range: ['13:00', '18:00'], month: 160 },
    ],
    prices: { keepLive: true, studentMonth: 250 },
    amenities: [],
    owner: { name: 'دعاء السقا', email: 'focus.owner@example.com', capacity: 25 },
    createdDaysAgo: 14,
  },
  {
    slug: 'garden-hub',
    addressEn: 'Gaza, Al-Garden Building, opposite the municipal park, third floor',
    hours: 'live',
    prices: { hour: 5, day: 25, week: 120, month: 380, studentMonth: 300 },
    amenities: ['stable_power', 'meeting_room'],
    owner: { name: 'رنا الخطيب', email: 'garden.owner@example.com', capacity: 30 },
    createdDaysAgo: 13,
  },
  {
    slug: 'jreas-hub',
    addressEn: 'Al-Jalaa Street, next to the new Al-Zaharna Building',
    hours: { open: ['09:00', '17:00'], friday: null },
    // Free: it publishes no price.
    prices: null,
    amenities: ['internet', 'solar_power'],
    ownAmenities: [['مجانية للطلاب والمستقلين', 'Free for students and freelancers']],
    fictional: [['WHATSAPP', '+970599000011']],
    createdDaysAgo: 12,
  },
  {
    slug: 'coma-io',
    addressEn: 'Nuseirat, Main Street, next to Al-Jabouni School, opposite Al-Saada Pharmacy, first floor',
    hours: { open: ['09:00', '21:00'], friday: null },
    prices: { hour: 4, day: 20, month: 320, studentDay: 15 },
    amenities: ['technical_training'],
    fictional: [['PHONE', '+970599000014']],
    createdDaysAgo: 11,
  },
  {
    slug: 'al-salam-hub',
    addressEn: 'Deir al-Balah, Al-Salam Street, behind Shaafout Restaurant, Abu Ghassan Al-Buhaisi Building, second floor',
    hours: { open: ['08:00', '18:00'], friday: null },
    prices: { hour: 3, day: 15, week: 80, month: 250, studentDay: 12 },
    amenities: ['internet', 'solar_power', 'hot_drinks', 'halls_for_rent', 'technical_training'],
    fictional: [['WHATSAPP', '+970599000015']],
    createdDaysAgo: 10,
  },
  {
    slug: 'masar-tech',
    addressEn: 'Khan Younis, Al-Mawasi, 100 m north of Al-Nuss junction, opposite Lotus Palace hall',
    hours: 'around-the-clock',
    prices: { hour: 3, day: 15, month: 260, studentHour: 2 },
    amenities: ['solar_power', 'stable_power', 'technical_training'],
    fictional: [['WHATSAPP', '+970599000016']],
    createdDaysAgo: 9,
  },
  {
    slug: 'golden-hub',
    addressEn: '50 m west of Al-Saraya junction, next to Haitham Al-Shawwa Shoes, above Zoom Optics, second floor',
    hours: { open: ['09:00', '21:00'], friday: ['14:00', '21:00'] },
    prices: { hour: 4, day: 20, week: 100, month: 330, studentDay: 15, studentMonth: 260 },
    amenities: ['internet', 'solar_power', 'hot_drinks', 'generator_line'],
    createdDaysAgo: 8,
  },
  {
    slug: 'masahat',
    addressEn: 'Gaza, Abu Hasira roundabout, opposite Al-Deira Hotel',
    hours: 'around-the-clock',
    prices: { hour: 5, day: 25, month: 400, studentDay: 20 },
    amenities: ['internet', 'stable_power', 'solar_power', 'hot_drinks', 'meeting_room'],
    ownAmenities: [['زوايا استراحة مجهّزة', 'Equipped lounge corners']],
    createdDaysAgo: 6,
  },
  {
    slug: 'white-space',
    addressEn: 'Al-Rimal, Ahmad Abdel Aziz Street, Golden Treasure Building',
    hours: { open: ['08:00', '20:00'], friday: null },
    prices: { hour: 6, day: 30, week: 150, month: 450 },
    amenities: [],
    createdDaysAgo: 4,
  },
];

/** The owner's photos (Downloads\spaceImg), matched by the supervisor: file → live slug. */
export const PHOTO_MAP: Record<string, string> = {
  'إلفييت هاب.jpg': 'elevate-hub',
  'السلام هب.jpg': 'al-salam-hub',
  'بال هب.jpg': 'pal-hub',
  'برانش هب.png': 'branch-hub',
  'جاردين هب.jpg': 'garden-hub',
  'جريس هاب.png': 'jreas-hub',
  'جولدن هب.jpg': 'golden-hub',
  'فوكس هب.png': 'focus-hub',
  'كوما سبيس.jpg': 'coma-io',
  'مساحات.png': 'masahat',
  'مسار تيك.jpg': 'masar-tech',
  'نمبر ون هب.jpg': 'number-one-hub',
  'وايت سبيس.jpg': 'white-space',
};

/** ~40 platform users (fictional), and the demo user. */
export const USERS: [string, string][] = [
  ['سلمى الأغا', 'demo-user@example.com'],
  ['عمر حمدونة', 'omar.hamdouna@example.com'],
  ['نادين أبو رمضان', 'nadine.aburamadan@example.com'],
  ['محمود الشريف', 'mahmoud.sharif@example.com'],
  ['آلاء عبد العال', 'alaa.abdelaal@example.com'],
  ['يزن الحسيني', 'yazan.husseini@example.com'],
  ['رغد أبو عيدة', 'raghad.abueida@example.com'],
  ['عبد الله صيام', 'abdullah.siam@example.com'],
  ['هديل الرملاوي', 'hadeel.ramlawi@example.com'],
  ['محمد الدلو', 'mohammed.dalu@example.com'],
  ['سجى أبو شمالة', 'saja.abushamala@example.com'],
  ['أحمد المقيد', 'ahmad.muqayyad@example.com'],
  ['ريما شحادة', 'rima.shehada@example.com'],
  ['فارس الغفري', 'fares.ghafari@example.com'],
  ['منى أبو سيف', 'mona.abusaif@example.com'],
  ['باسل عابد', 'basel.abed@example.com'],
  ['دعاء الهندي', 'duaa.hindi@example.com'],
  ['حسام قشطة', 'hossam.qeshta@example.com'],
  ['لانا الحداد', 'lana.haddad@example.com'],
  ['إسماعيل بارود', 'ismail.baroud@example.com'],
  ['رزان العمصي', 'razan.amsi@example.com'],
  ['مؤمن أبو دقة', 'moamen.abudaqqa@example.com'],
  ['ولاء البيطار', 'walaa.bitar@example.com'],
  ['سعيد الأشقر', 'saeed.ashqar@example.com'],
  ['هيا النجار', 'haya.najjar@example.com'],
  ['جهاد الزهارنة', 'jihad.zaharna@example.com'],
  ['أسيل عاشور', 'aseel.ashour@example.com'],
  ['أنور الكرنز', 'anwar.karanz@example.com'],
  ['تالا حجازي', 'tala.hijazi@example.com'],
  ['ماجد الوحيدي', 'majed.wuheidi@example.com'],
  ['نور الهدى سالم', 'noor.salem@example.com'],
  ['قصي أبو وطفة', 'qusai.abuwatfa@example.com'],
  ['بشرى المصري', 'bushra.masri@example.com'],
  ['يحيى الخضري', 'yahya.khudari@example.com'],
  ['فرح أبو نحل', 'farah.abunahl@example.com'],
  ['عز الدين ضاهر', 'ezz.daher@example.com'],
  ['مرح الجعبري', 'marah.jabari@example.com'],
  ['زكريا الشيخ خليل', 'zakaria.khalil@example.com'],
  ['إيمان البنا', 'iman.banna@example.com'],
  ['حازم أبو جبة', 'hazem.abujubba@example.com'],
  ['شيرين عرفات', 'shereen.arafat@example.com'],
];
