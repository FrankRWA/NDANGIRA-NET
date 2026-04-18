// ── Serivasi shared UI components ──

// ── NAV HTML (injected into every page) ──
function renderNav() {
  const nav = document.getElementById("nav-placeholder");
  if (!nav) return;
  nav.innerHTML = `
    <nav class="nav">
      <a href="index.html" class="logo">
        <span class="logo-dot"></span>Serivasi
      </a>
      <div class="nav-links">
        <a class="nav-link" href="index.html">Home</a>
        <a class="nav-link" href="houses.html" data-i18n="navHouses">Houses</a>
        <a class="nav-link" href="workers.html" data-i18n="navWorkers">Workers</a>
        <a class="nav-link" href="messages.html" data-i18n="navMessages">Messages</a>
        <a class="nav-link" href="employer-dashboard.html">Employer</a>
        <a class="nav-link" href="worker-dashboard.html">Worker</a>
        <a class="nav-link" href="about.html" data-i18n="navAbout">About</a>
        <a class="nav-link" href="help.html" data-i18n="navHelp">Help</a>
        <a class="nav-link" href="notifications.html" data-i18n="navNotifs">Notifications</a>
      </div>
      <div class="nav-right">
        <button class="lang-btn ${currentLang === 'en' ? 'active' : ''}" data-lang="en" onclick="setLang('en')">EN</button>
        <button class="lang-btn ${currentLang === 'rw' ? 'active' : ''}" data-lang="rw" onclick="setLang('rw')">RW</button>
        <button class="lang-btn ${currentLang === 'fr' ? 'active' : ''}" data-lang="fr" onclick="setLang('fr')">FR</button>
        <button class="dm-toggle" onclick="toggleTheme()" title="Toggle dark/light mode">
          <div class="dm-knob"></div>
        </button>
        <a class="notif-btn" href="notifications.html">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M8 1a5 5 0 0 1 5 5v3l1.5 2.5H1.5L3 9V6a5 5 0 0 1 5-5z"/>
            <path d="M6.5 14a1.5 1.5 0 0 0 3 0"/>
          </svg>
          <span class="notif-dot ${DATA.notifications.some(n => n.unread) ? 'show' : ''}"></span>
        </a>
        <button class="btn" onclick="openModal('modal-login')">Sign in</button>
        <button class="btn btn-primary" onclick="openModal('modal-signup')">Join free</button>
        <a class="btn btn-primary" href="post-house.html" style="text-decoration:none">+ Post house</a>
      </div>
    </nav>
  `;
  markActiveNav();
  applyLangStrings();
}

// ── FOOTER HTML ──
function renderFooter() {
  const footer = document.getElementById("footer-placeholder");
  if (!footer) return;
  footer.innerHTML = `
    <footer class="footer">
      <div class="footer-inner">
        <div class="footer-logo"><span class="logo-dot"></span>Serivasi</div>
        <div class="footer-links">
          <a href="houses.html">Houses</a>
          <a href="workers.html">Workers</a>
          <a href="about.html">About</a>
          <a href="help.html">Help</a>
          <a href="notifications.html">Notifications</a>
        </div>
        <div class="footer-copy">&copy; 2026 Serivasi. Made for Rwanda.</div>
      </div>
    </footer>
  `;
}

// ── AUTH MODALS ──
function renderAuthModals() {
  const container = document.getElementById("modals-placeholder");
  if (!container) return;
  container.innerHTML = `
    <!-- Login modal -->
    <div id="modal-login" class="modal-overlay hidden" onclick="closeModalOnOverlay(event,'modal-login')">
      <div class="modal-box" style="max-width:380px">
        <div class="modal-header">
          <div class="modal-title">Sign in to Serivasi</div>
          <button class="modal-close" onclick="closeModal('modal-login')">&times;</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>Phone number or email</label>
            <input type="text" placeholder="+250 788 000 000">
          </div>
          <div class="form-group">
            <label>Password</label>
            <input type="password" placeholder="Your password">
          </div>
          <div style="font-size:12px;color:var(--g);cursor:pointer;margin-bottom:14px">Forgot password?</div>
        </div>
        <div class="modal-footer">
          <button class="btn" onclick="closeModal('modal-login')">Cancel</button>
          <button class="btn btn-primary" onclick="closeModal('modal-login')">Sign in</button>
        </div>
        <div style="text-align:center;font-size:12px;color:var(--t2);padding:0 18px 16px">
          Don't have an account?
          <span style="color:var(--g);cursor:pointer" onclick="closeModal('modal-login');openModal('modal-signup')">Join free</span>
        </div>
      </div>
    </div>

    <!-- Signup modal -->
    <div id="modal-signup" class="modal-overlay hidden" onclick="closeModalOnOverlay(event,'modal-signup')">
      <div class="modal-box" style="max-width:420px">
        <div class="modal-header">
          <div class="modal-title">Create your profile</div>
          <button class="modal-close" onclick="closeModal('modal-signup')">&times;</button>
        </div>
        <div class="modal-body">
          <div class="role-selector">
            <button class="role-btn" id="role-employer" onclick="selectRole('employer')">I'm an employer</button>
            <button class="role-btn" id="role-worker" onclick="selectRole('worker')">I'm a worker</button>
          </div>
          <div class="form-grid">
            <div class="form-group"><label>Full name</label><input type="text" placeholder="Your name"></div>
            <div class="form-group"><label>Age</label><input type="number" placeholder="28" min="16" max="99"></div>
          </div>
          <div class="form-group"><label>Phone number</label><input type="text" placeholder="+250 788 000 000"></div>
          <div class="form-group">
            <label>Location / District</label>
            <select>
              <option>Gasabo, Kigali</option><option>Kicukiro, Kigali</option>
              <option>Nyarugenge, Kigali</option><option>Musanze</option>
              <option>Huye</option><option>Rubavu</option><option>Other</option>
            </select>
          </div>
          <div class="form-group" id="skills-section" style="display:none">
            <label>Your skills (select all that apply)</label>
            <div class="skills-grid" style="margin-top:6px">
              ${["House commissioning","House maid","Guard (Umuzamu)","Driver","Plumber","Welder","Carpenter","Gardener","Cleaner","Laundry helper"]
                .map(s => `<button class="skill-chip" onclick="this.classList.toggle('selected')">${s}</button>`)
                .join("")}
            </div>
          </div>
          <div class="form-group"><label>Password</label><input type="password" placeholder="Create a password"></div>
        </div>
        <div class="modal-footer">
          <button class="btn" onclick="closeModal('modal-signup')">Cancel</button>
          <button class="btn btn-primary" onclick="closeModal('modal-signup')">Create profile</button>
        </div>
      </div>
    </div>
  `;
}

function selectRole(r) {
  document.querySelectorAll(".role-btn").forEach(b => b.classList.remove("selected"));
  document.getElementById("role-" + r).classList.add("selected");
  const ss = document.getElementById("skills-section");
  if (ss) ss.style.display = r === "worker" ? "block" : "none";
}

// ── HOUSE CARD ──
function houseCardHTML(h) {
  return `
    <a class="house-card${h.taken ? " taken" : ""}" href="house-detail.html?id=${h.id}">
      <div class="house-img-placeholder">
        ${h.photo
          ? `<img src="${h.photo}" class="house-img" alt="${h.title}">`
          : `<svg width="44" height="44" viewBox="0 0 48 48" fill="none" stroke="var(--t3)" stroke-width="1.3">
               <path d="M5 20 24 6l19 14V43a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V20z"/>
               <path d="M18 44V30h12v14"/>
             </svg>`
        }
      </div>
      <div class="house-body">
        <div class="house-price">${fmtPrice(h.price)}</div>
        <div class="house-title">${h.title}</div>
        <div class="house-loc">
          <svg width="9" height="11" viewBox="0 0 10 12" fill="none" stroke="currentColor" stroke-width="1.3">
            <circle cx="5" cy="4.5" r="2"/><path d="M5 12S1 7.5 1 4.5a4 4 0 0 1 8 0C9 7.5 5 12 5 12z"/>
          </svg>
          ${h.loc}
        </div>
        <div class="house-footer">
          <div class="house-meta">
            <span>${h.rooms} bed${h.rooms > 1 ? "s" : ""}</span>
            <span>${h.comments.length} comment${h.comments.length !== 1 ? "s" : ""}</span>
          </div>
          <span class="badge ${h.taken ? "badge-red" : "badge-green"}">${h.taken ? "Taken" : "Available"}</span>
        </div>
      </div>
    </a>
  `;
}

// ── WORKER CARD ──
function workerCardHTML(w) {
  return `
    <a class="worker-card${w.rating >= 4.8 ? " featured" : ""}" href="worker-profile.html?id=${w.id}">
      ${w.rating >= 4.8 ? '<span class="badge badge-green" style="margin-bottom:8px;display:inline-block">Top rated</span>' : ""}
      <div class="avatar av-md" style="background:${w.bg};color:${w.tc};margin-bottom:10px">
        ${w.photo ? `<img src="${w.photo}" alt="${w.name}">` : w.ini}
      </div>
      <div style="font-size:13px;font-weight:500;color:var(--t1)">
        ${w.name}
        ${w.verified ? `<span class="verified-badge">
          <svg width="9" height="9" viewBox="0 0 10 10" fill="none" stroke="#185FA5" stroke-width="1.6"><path d="M1.5 5l2.5 3 5-6"/></svg>
        </span>` : ""}
      </div>
      <div style="font-size:11px;color:var(--t2);margin:2px 0 4px">${w.role}</div>
      <div style="font-size:11px;color:var(--t3);margin-bottom:5px">${w.loc}</div>
      <div><span class="stars">${starsStr(w.rating)}</span> <span style="font-size:10px;color:var(--t2)">${w.rating} (${w.reviews})</span></div>
      <div class="tags">${w.skills.map(s => `<span class="tag">${s}</span>`).join("")}</div>
      <div class="avail-pill" style="margin-top:7px;font-size:11px;color:${w.avail ? "var(--g)" : "var(--t3)"}">
        ${w.avail ? `<span class="avail-dot"></span> Available` : "Not available"}
      </div>
    </a>
  `;
}

// ── COMMENT HTML ──
function commentHTML(c) {
  return `
    <div class="comment">
      <div class="avatar av-xs" style="background:${c.bg || c.authorBg};color:${c.tc || c.authorTc}">
        ${c.ini || c.authorIni}
      </div>
      <div class="comment-bubble">
        <div class="comment-author">
          ${c.author}
          ${(c.isLL || c.isWorker) ? `<span class="badge badge-amber">${c.isLL ? "Landlord" : "Worker"}</span>` : ""}
          <span class="comment-date">${c.date}</span>
        </div>
        <div class="comment-text">${c.text}</div>
      </div>
    </div>
  `;
}

// ── NOTIFICATION HTML ──
function notifHTML(n) {
  const icons = {
    msg: `<svg width="15" height="15" viewBox="0 0 16 16" fill="none" stroke="#185FA5" stroke-width="1.4"><path d="M14 3H2a1 1 0 0 0-1 1v7a1 1 0 0 0 1 1h3l3 3 3-3h3a1 1 0 0 0 1-1V4a1 1 0 0 0-1-1z"/></svg>`,
    house: `<svg width="15" height="15" viewBox="0 0 16 16" fill="none" stroke="#0F6E56" stroke-width="1.4"><path d="M2 6.5 8 2l6 4.5V14a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V6.5z"/></svg>`,
    verify: `<svg width="15" height="15" viewBox="0 0 16 16" fill="none" stroke="#185FA5" stroke-width="1.4"><path d="M2 8l4 4 8-8"/></svg>`,
    job: `<svg width="15" height="15" viewBox="0 0 16 16" fill="none" stroke="#854F0B" stroke-width="1.4"><rect x="2" y="6" width="12" height="8" rx="1"/><path d="M5 6V4a3 3 0 0 1 6 0v2"/></svg>`,
    star: `<svg width="15" height="15" viewBox="0 0 16 16" fill="none" stroke="#EF9F27" stroke-width="1.4"><path d="M8 2l1.8 3.6L14 6.4l-3 2.9.7 4.1L8 11.4l-3.7 2 .7-4.1L2 6.4l4.2-.8z"/></svg>`,
  };
  const bgs = { msg:"#E6F1FB", house:"#E1F5EE", verify:"#E6F1FB", job:"#FAEEDA", star:"#FAEEDA" };
  return `
    <div class="notif-item${n.unread ? " unread" : ""}" onclick="markNotifRead(${n.id})">
      <div class="notif-icon" style="background:${bgs[n.icon] || "#E1F5EE"}">${icons[n.icon] || ""}</div>
      <div class="notif-content">
        <div class="notif-title">${n.title}</div>
        <div class="notif-sub">${n.sub}</div>
      </div>
      <div class="notif-time">${n.time}</div>
    </div>
  `;
}

function markNotifRead(id) {
  const n = DATA.notifications.find(x => x.id === id);
  if (n) {
    n.unread = false;
    const el = document.querySelector(`.notif-item[onclick="markNotifRead(${id})"]`);
    if (el) el.classList.remove("unread");
  }
}

// ── BOT CHAT ──
function botSend(inputId, containerID) {
  const inp = document.getElementById(inputId);
  if (!inp) return;
  const q = inp.value.trim();
  if (!q) return;
  inp.value = "";
  botAppend(containerID, q, "user");
  const typing = botAppend(containerID, '<div class="typing"><span></span><span></span><span></span></div>', "bot");
  setTimeout(() => {
    typing.remove();
    botAppend(containerID, getBotAnswer(q), "bot");
  }, 800);
}

function botAppend(containerID, text, role) {
  const c = document.getElementById(containerID);
  if (!c) return null;
  const div = document.createElement("div");
  div.className = `bot-msg ${role}`;
  div.innerHTML = text;
  c.appendChild(div);
  c.scrollTop = c.scrollHeight;
  return div;
}

// ── INIT (called on every page load) ──
document.addEventListener("DOMContentLoaded", function () {
  applyTheme();
  renderNav();
  renderFooter();
  renderAuthModals();
  applyLangStrings();
  // run page-specific init if defined
  if (typeof pageInit === "function") pageInit();
});
