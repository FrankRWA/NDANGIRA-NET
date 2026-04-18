// ── Serivasi shared data store ──

const DATA = {
  houses: [
    { id:1, title:"Cozy 2BR in Kicukiro", loc:"Kicukiro, Kigali", price:65000, rooms:2, taken:false,
      landlord:"Jean Paul Nkurunziza", landlordIni:"JP", landlordBg:"#E6F1FB", landlordTc:"#0C447C",
      desc:"Clean 2-bedroom house with outdoor space and reliable water. Close to Kicukiro market. Available immediately.",
      features:["Water included","Outdoor space","Near transport"], photo:null,
      comments:[
        {id:"hc1",author:"Marie K.",ini:"MK",bg:"#EEEDFE",tc:"#3C3489",isLL:false,text:"Is the toilet indoor?",date:"2 days ago"},
        {id:"hc2",author:"Jean Paul Nkurunziza",ini:"JP",bg:"#E6F1FB",tc:"#0C447C",isLL:true,text:"Yes, fully indoor bathroom with hot water.",date:"2 days ago"}
      ]
    },
    { id:2, title:"Affordable studio - Gasabo", loc:"Gasabo, Kigali", price:35000, rooms:1, taken:false,
      landlord:"Claudine Uwase", landlordIni:"CU", landlordBg:"#FAECE7", landlordTc:"#993C1D",
      desc:"Small studio perfect for one person or a couple. Quiet neighborhood, near Remera. Electricity included.",
      features:["Electricity included","Furnished","Near Remera"], photo:null, comments:[]
    },
    { id:3, title:"3BR family house - Nyarugenge", loc:"Nyarugenge, Kigali", price:110000, rooms:3, taken:false,
      landlord:"Emmanuel Bizimana", landlordIni:"EB", landlordBg:"#E1F5EE", landlordTc:"#085041",
      desc:"Spacious 3-bedroom house with a garden. Good for families. 10 min walk to Nyarugenge market.",
      features:["Garden","3 bedrooms","Family-friendly"], photo:null,
      comments:[
        {id:"hc3",author:"Patrick N.",ini:"PN",bg:"#EAF3DE",tc:"#27500A",isLL:false,text:"Is the house available in July?",date:"1 week ago"}
      ]
    },
    { id:4, title:"Room for rent - Musanze", loc:"Musanze", price:22000, rooms:1, taken:true,
      landlord:"Aline Mukeshimana", landlordIni:"AM", landlordBg:"#EAF3DE", landlordTc:"#27500A",
      desc:"Single room in a shared compound. Safe and quiet area.",
      features:["Shared compound","Safe area"], photo:null, comments:[]
    },
    { id:5, title:"2BR near Huye University", loc:"Huye", price:48000, rooms:2, taken:false,
      landlord:"Robert Hategekimana", landlordIni:"RH", landlordBg:"#FAEEDA", landlordTc:"#633806",
      desc:"Comfortable 2-bedroom house just 5 minutes from Huye University. Ideal for students or young professionals.",
      features:["Near university","Water & electricity"], photo:null, comments:[]
    },
    { id:6, title:"Modern studio - Kacyiru", loc:"Kacyiru, Kigali", price:55000, rooms:1, taken:false,
      landlord:"Diane Uwimana", landlordIni:"DU", landlordBg:"#E1F5EE", landlordTc:"#085041",
      desc:"Modern studio with good internet access. Close to ministries and offices.",
      features:["Internet access","Modern finish","Central location"], photo:null, comments:[]
    },
  ],

  workers: [
    { id:1, name:"Diane Uwimana", role:"House maid", loc:"Gasabo, Kigali", age:26, rating:4.9, reviews:34,
      skills:["House maid","Cleaner"], avail:true, verified:true, ini:"DU", bg:"#E1F5EE", tc:"#085041", photo:null,
      bio:"3 years of household experience in Kigali. Reliable, punctual and respectful."
    },
    { id:2, name:"Jean Pierre Habimana", role:"Plumber", loc:"Kicukiro, Kigali", age:33, rating:4.7, reviews:21,
      skills:["Plumber","Welder"], avail:true, verified:true, ini:"JP", bg:"#E6F1FB", tc:"#0C447C", photo:null,
      bio:"Certified plumber with 7 years experience. Available for emergency calls."
    },
    { id:3, name:"Emmanuel Nshimiyimana", role:"Guard", loc:"Nyarugenge, Kigali", age:41, rating:4.8, reviews:18,
      skills:["Guard (Umuzamu)"], avail:true, verified:false, ini:"EN", bg:"#FAEEDA", tc:"#633806", photo:null,
      bio:"Experienced night guard. Former military service. Strong and reliable."
    },
    { id:4, name:"Aline Mukamana", role:"Driver", loc:"Kigali", age:35, rating:4.9, reviews:47,
      skills:["Driver"], avail:true, verified:true, ini:"AM", bg:"#EAF3DE", tc:"#27500A", photo:null,
      bio:"Professional driver with clean license. Knows all routes in Kigali and beyond."
    },
    { id:5, name:"Thierry Nzabonimana", role:"Gardener", loc:"Gasabo, Kigali", age:24, rating:4.5, reviews:9,
      skills:["Gardener","Cleaner"], avail:true, verified:false, ini:"TN", bg:"#EEEDFE", tc:"#3C3489", photo:null,
      bio:"Creative gardener who loves plants. Can design and maintain any garden."
    },
    { id:6, name:"Pacifique Mugisha", role:"Carpenter", loc:"Musanze", age:29, rating:4.6, reviews:12,
      skills:["Carpenter","Welder"], avail:false, verified:true, ini:"PM", bg:"#FBEAF0", tc:"#72243E", photo:null,
      bio:"Skilled carpenter and welder. Specializes in custom furniture and metal work."
    },
    { id:7, name:"Claudine Uwase", role:"Cleaner", loc:"Kicukiro, Kigali", age:22, rating:4.7, reviews:16,
      skills:["Cleaner","Laundry helper"], avail:true, verified:false, ini:"CU", bg:"#FAECE7", tc:"#993C1D", photo:null,
      bio:"Fast and thorough cleaner. Available for one-off deep cleans or regular visits."
    },
    { id:8, name:"Olivier Irakoze", role:"Welder", loc:"Huye", age:38, rating:4.8, reviews:23,
      skills:["Welder","Carpenter"], avail:false, verified:true, ini:"OI", bg:"#E1F5EE", tc:"#085041", photo:null,
      bio:"Professional welder with 10 years experience. Gates, fences, furniture."
    },
  ],

  workerReviews: {
    1: [
      { id:"r1", author:"Marie Kayitesi", authorIni:"MK", authorBg:"#EEEDFE", authorTc:"#3C3489", stars:5, date:"2 weeks ago",
        body:"Diane is incredibly reliable and thorough. She cleaned every corner of my house and was very respectful. I will definitely hire her again.",
        helpful:12, liked:false,
        comments:[
          {id:"rc1",author:"Diane Uwimana",ini:"DU",bg:"#E1F5EE",tc:"#085041",isWorker:true,text:"Murakoze cyane Marie! It was a pleasure working in your home.",date:"2 weeks ago"}
        ]
      },
      { id:"r2", author:"Patrick Nkurunziza", authorIni:"PN", authorBg:"#E6F1FB", authorTc:"#0C447C", stars:5, date:"1 month ago",
        body:"Very professional and punctual. Arrived exactly on time and finished everything in one morning. My wife was very impressed.",
        helpful:8, liked:false, comments:[]
      },
      { id:"r3", author:"Chantal Uwimana", authorIni:"CU", authorBg:"#FAECE7", authorTc:"#993C1D", stars:4, date:"2 months ago",
        body:"Good work overall. She is gentle and careful with furniture. Took a little longer than expected but the result was great.",
        helpful:5, liked:false,
        comments:[
          {id:"rc2",author:"Diane Uwimana",ini:"DU",bg:"#E1F5EE",tc:"#085041",isWorker:true,text:"Thank you Chantal! I will work on being faster next time.",date:"2 months ago"}
        ]
      },
    ],
    2: [
      { id:"r4", author:"Eric Habimana", authorIni:"EH", authorBg:"#E1F5EE", authorTc:"#085041", stars:5, date:"3 weeks ago",
        body:"Jean Pierre fixed a complicated leak quickly and cleanly. Very trustworthy.", helpful:9, liked:false, comments:[]
      },
      { id:"r5", author:"Solange Mutesi", authorIni:"SM", authorBg:"#FAEEDA", authorTc:"#633806", stars:4, date:"5 weeks ago",
        body:"Solid work. Came the same day I called. Left the workspace very clean.", helpful:4, liked:false, comments:[]
      },
    ],
    3: [
      { id:"r6", author:"Jean-Claude Bizimana", authorIni:"JB", authorBg:"#EAF3DE", authorTc:"#27500A", stars:5, date:"1 week ago",
        body:"Emmanuel has been our night guard for 3 months. Very alert, responsible. We feel completely safe.", helpful:15, liked:false, comments:[]
      },
    ],
    4: [
      { id:"r7", author:"David Ndagijimana", authorIni:"DN", authorBg:"#E6F1FB", authorTc:"#0C447C", stars:5, date:"4 days ago",
        body:"Aline drove me to the airport at 4am without any issues. Very calm driver, knows Kigali perfectly.", helpful:7, liked:false, comments:[]
      },
      { id:"r8", author:"Immaculee Uwamariya", authorIni:"IU", authorBg:"#FBEAF0", authorTc:"#72243E", stars:5, date:"2 weeks ago",
        body:"Professional, quiet, and very safe driver. The car was clean. She was 10 minutes early.", helpful:6, liked:false, comments:[]
      },
    ],
  },

  messages: {
    1: [
      {dir:"in", text:"Hello, I saw your listing. I am available for house maid work.", time:"9:30 AM"},
      {dir:"out", text:"Hi Diane! Great. Can you tell me more about your experience?", time:"9:32 AM"},
      {dir:"in", text:"I have 3 years of experience. I can start Monday morning.", time:"9:34 AM"},
      {dir:"out", text:"That sounds perfect. What days are you available?", time:"9:37 AM"},
      {dir:"in", text:"I can work Monday to Friday, 7am to 3pm.", time:"9:41 AM"},
    ],
    2: [
      {dir:"out", text:"Hello Jean Pierre, I have a leaking pipe in my kitchen. Can you come check?", time:"2:10 PM"},
      {dir:"in", text:"Yes I can come tomorrow morning around 8am. Is that okay?", time:"2:15 PM"},
      {dir:"out", text:"Perfect, see you then.", time:"2:17 PM"},
      {dir:"in", text:"The pipe issue is fixed now. All good!", time:"4:10 PM"},
    ],
    3: [
      {dir:"out", text:"Aline, I need a driver this Thursday to the airport at 5am.", time:"10:00 AM"},
      {dir:"in", text:"Yes, I am free. What time is your flight?", time:"10:04 AM"},
      {dir:"in", text:"I will be there at 5am sharp.", time:"10:10 AM"},
    ],
  },

  conversations: [
    {id:1, name:"Diane Uwimana", ini:"DU", bg:"#E1F5EE", tc:"#085041", role:"House maid", online:true, unread:2, preview:"I can work Monday to Friday"},
    {id:2, name:"Jean Pierre Habimana", ini:"JP", bg:"#E6F1FB", tc:"#0C447C", role:"Plumber", online:true, unread:0, preview:"The pipe issue is fixed now"},
    {id:3, name:"Aline Mukamana", ini:"AM", bg:"#EAF3DE", tc:"#27500A", role:"Driver", online:false, unread:1, preview:"I will be there at 5am sharp"},
  ],

  notifications: [
    {id:1, unread:true, icon:"msg", title:"New comment on your listing", sub:"Marie K. commented on \"Cozy 2BR in Kicukiro\"", time:"5 min ago"},
    {id:2, unread:true, icon:"house", title:"House listing approved", sub:"Your listing \"Modern studio - Kacyiru\" is now live", time:"1 hr ago"},
    {id:3, unread:true, icon:"verify", title:"Verification complete", sub:"Your ID has been verified. Verified badge added.", time:"3 hrs ago"},
    {id:4, unread:false, icon:"job", title:"Job request received", sub:"Patrick is looking for a house maid in Gasabo", time:"Yesterday"},
    {id:5, unread:false, icon:"star", title:"New review", sub:"You received a 5-star review from Chantal Uwimana", time:"2 days ago"},
    {id:6, unread:false, icon:"house", title:"House marked as taken", sub:"Room for rent - Musanze has been marked as taken", time:"3 days ago"},
  ],

  faqs: [
    {q:"How do I find an affordable house?", a:"Go to the Houses page. Use the price and location filters to narrow results. Click any listing to see full details, photos, and comment directly to the landlord."},
    {q:"How do I post a house listing?", a:"Click '+ Post house' in the navigation bar. Fill in the title, price, location, bedrooms, description, and feature tags. Upload photos of the property. Your listing goes live after a quick review."},
    {q:"How do I mark my house as taken?", a:"Open your listing in the Employer dashboard or from the house detail page. Click 'Mark as taken'. The listing will show a red Taken badge and be hidden from available searches."},
    {q:"How do I create a profile?", a:"Click 'Join free' in the navigation. Choose whether you are a worker or employer, fill in your name, location, age, and if you are a worker, select your skills."},
    {q:"Is Serivasi free to use?", a:"Yes - creating a profile, listing a house, and searching for workers is completely free. Core features will always remain free for both workers and employers."},
    {q:"How are workers verified?", a:"Workers complete phone verification and submit their national ID. Verified workers receive a blue checkmark badge visible on their profile and cards."},
    {q:"How do reviews and comments work?", a:"After a job, employers leave star ratings and written reviews on a worker's profile. On house listings, anyone can comment publicly and the landlord can reply with a special Landlord badge."},
    {q:"What languages does Serivasi support?", a:"Kinyarwanda, French and English. Toggle between them using the language buttons in the top navigation bar."},
    {q:"How do I contact a worker or landlord?", a:"Open any worker card or house listing and click the Message or DM button to start a private chat with text, voice notes, photos and videos."},
    {q:"How do I reset my password?", a:"On the sign-in page, click Forgot password. Enter your phone number or email and you will receive a reset code within a few minutes."},
  ],

  botAnswers: {
    profile: "Tap 'Join free' in the nav. Choose worker or employer, add your name, location, age and - if a worker - pick your skills.",
    house: "Go to the Houses page. Use price and location filters to narrow results. Click any card to see full details and comment directly to the landlord.",
    post: "Click '+ Post house' in the navigation. Add photos, price, location, bedrooms, description and features. It goes live after review.",
    free: "Yes - Serivasi is completely free to join and use for both workers and employers.",
    review: "After a job, employers leave a star rating and written comment on the worker's profile. All reviews are public.",
    contact: "Open any worker card or house listing and click Message or DM to start a private chat.",
    verify: "Workers verify their phone and submit their national ID. Verified workers get a blue checkmark badge.",
    taken: "Open the house listing or go to your Employer dashboard. Click 'Mark as taken' - the listing turns red and is hidden from available searches.",
    find: "Go to the Workers page, type a name or skill, and use filters for location, availability, or verified-only.",
  },

  botKeywords: {
    profile: ["create a profile","sign up","register","join","make a profile","new account"],
    house: ["find a house","rent","affordable","accommodation","find house","looking for a place"],
    post: ["post a house","list a house","add listing","new listing","post listing"],
    free: ["free","cost","price","pay","pricing","how much","subscription"],
    review: ["review","rating","stars","feedback","rate"],
    contact: ["contact","message","chat","reach","dm","talk"],
    verify: ["verified","verification","trust","badge","check","id"],
    taken: ["mark as taken","taken","no longer available","remove listing"],
    find: ["find a worker","search worker","hire","looking for worker","need a maid","need a driver"],
  },
};

// ── helpers ──
function starsStr(n) {
  const full = Math.round(n);
  return "&#9733;".repeat(full) + "&#9734;".repeat(5 - full);
}

function fmtPrice(p) {
  return (p / 1000).toFixed(0) + "k RWF/mo";
}

function avgRating(wid) {
  const revs = DATA.workerReviews[wid] || [];
  if (!revs.length) return 0;
  return parseFloat((revs.reduce((s, r) => s + r.stars, 0) / revs.length).toFixed(1));
}

function getBotAnswer(q) {
  const lq = q.toLowerCase();
  for (const [key, phrases] of Object.entries(DATA.botKeywords)) {
    if (phrases.some(p => lq.includes(p))) return DATA.botAnswers[key];
  }
  if (lq.includes("hello") || lq.includes("hi") || lq.includes("muraho")) return "Muraho! How can I help you today?";
  if (lq.includes("thank")) return "You're welcome! Feel free to ask anything else.";
  return "I'm not sure about that yet. Try asking about houses, workers, pricing, or verification.";
}

function addNotification(icon, title, sub) {
  DATA.notifications.unshift({ id: Date.now(), unread: true, icon, title, sub, time: "Just now" });
  const dot = document.querySelector(".notif-dot");
  if (dot) dot.classList.add("show");
}

// ── theme ──
function applyTheme() {
  const saved = localStorage.getItem("sv_theme") || "light";
  document.body.className = saved;
}

function toggleTheme() {
  const current = document.body.classList.contains("dark") ? "dark" : "light";
  const next = current === "dark" ? "light" : "dark";
  document.body.className = next;
  localStorage.setItem("sv_theme", next);
}

// ── language ──
const LANG = {
  en: { heroTitle: "Find your next affordable home in Rwanda", heroSub: "Browse verified listings posted by real landlords near you.", navHouses: "Houses", navWorkers: "Workers", navMessages: "Messages", navAbout: "About", navHelp: "Help", navNotifs: "Notifications" },
  rw: { heroTitle: "Shaka inzu yawe yo gukodesha mu Rwanda", heroSub: "Reba inyubako zemewe zashyizwe n'abakodesha b'ukuri hafi yawe.", navHouses: "Inzu", navWorkers: "Abakozi", navMessages: "Ubutumwa", navAbout: "Ibyerekeye", navHelp: "Ubufasha", navNotifs: "Inkuru" },
  fr: { heroTitle: "Trouvez votre prochain logement abordable au Rwanda", heroSub: "Parcourez les annonces verifiees publiees par de vrais proprietaires pres de chez vous.", navHouses: "Maisons", navWorkers: "Travailleurs", navMessages: "Messages", navAbout: "A propos", navHelp: "Aide", navNotifs: "Notifications" },
};

let currentLang = localStorage.getItem("sv_lang") || "en";

function setLang(l) {
  currentLang = l;
  localStorage.setItem("sv_lang", l);
  document.querySelectorAll(".lang-btn").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.lang === l);
  });
  applyLangStrings();
}

function applyLangStrings() {
  const t = LANG[currentLang];
  if (!t) return;
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.dataset.i18n;
    if (t[key]) el.textContent = t[key];
  });
}

// mark active nav link
function markActiveNav() {
  const path = window.location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll(".nav-link").forEach(a => {
    a.classList.toggle("active", a.getAttribute("href") === path);
  });
}

// modal helpers
function openModal(id) { document.getElementById(id).classList.remove("hidden"); }
function closeModal(id) { document.getElementById(id).classList.add("hidden"); }
function closeModalOnOverlay(e, id) { if (e.target === document.getElementById(id)) closeModal(id); }
