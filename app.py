from flask import (
    Flask, render_template, request, jsonify,
    redirect, url_for, session, send_from_directory
)
from werkzeug.utils import secure_filename
from datetime import datetime
import os, uuid, copy

app = Flask(__name__)
app.secret_key = "serivasi-dev-secret-2026"

UPLOAD_FOLDER = os.path.join("static", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10MB

# ─── IN-MEMORY DATABASE ──────────────────────────────────────────────────────
# In production you would swap this for SQLite / PostgreSQL via SQLAlchemy.

DB = {
    "houses": [
        {
            "id": 1, "title": "Cozy 2BR in Kicukiro", "loc": "Kicukiro, Kigali",
            "price": 65000, "rooms": 2, "taken": False,
            "landlord": "Jean Paul Nkurunziza", "landlord_ini": "JP",
            "landlord_bg": "#E6F1FB", "landlord_tc": "#0C447C",
            "desc": "Clean 2-bedroom house with outdoor space and reliable water. Close to Kicukiro market.",
            "features": ["Water included", "Outdoor space", "Near transport"],
            "photo": None,
            "comments": [
                {"id": "hc1", "author": "Marie K.", "ini": "MK",
                 "bg": "#EEEDFE", "tc": "#3C3489", "is_landlord": False,
                 "text": "Is the toilet indoor?", "date": "2 days ago"},
                {"id": "hc2", "author": "Jean Paul Nkurunziza", "ini": "JP",
                 "bg": "#E6F1FB", "tc": "#0C447C", "is_landlord": True,
                 "text": "Yes, fully indoor bathroom with hot water.", "date": "2 days ago"},
            ],
            "created_at": "2026-03-01",
        },
        {
            "id": 2, "title": "Affordable studio - Gasabo", "loc": "Gasabo, Kigali",
            "price": 35000, "rooms": 1, "taken": False,
            "landlord": "Claudine Uwase", "landlord_ini": "CU",
            "landlord_bg": "#FAECE7", "landlord_tc": "#993C1D",
            "desc": "Small studio perfect for one person or a couple. Quiet neighborhood, near Remera. Electricity included.",
            "features": ["Electricity included", "Furnished", "Near Remera"],
            "photo": None, "comments": [], "created_at": "2026-03-05",
        },
        {
            "id": 3, "title": "3BR family house - Nyarugenge", "loc": "Nyarugenge, Kigali",
            "price": 110000, "rooms": 3, "taken": False,
            "landlord": "Emmanuel Bizimana", "landlord_ini": "EB",
            "landlord_bg": "#E1F5EE", "landlord_tc": "#085041",
            "desc": "Spacious 3-bedroom house with a garden. Good for families. 10 min walk to market.",
            "features": ["Garden", "3 bedrooms", "Family-friendly"],
            "photo": None,
            "comments": [
                {"id": "hc3", "author": "Patrick N.", "ini": "PN",
                 "bg": "#EAF3DE", "tc": "#27500A", "is_landlord": False,
                 "text": "Is the house available in July?", "date": "1 week ago"},
            ],
            "created_at": "2026-03-10",
        },
        {
            "id": 4, "title": "Room for rent - Musanze", "loc": "Musanze",
            "price": 22000, "rooms": 1, "taken": True,
            "landlord": "Aline Mukeshimana", "landlord_ini": "AM",
            "landlord_bg": "#EAF3DE", "landlord_tc": "#27500A",
            "desc": "Single room in a shared compound. Safe and quiet area.",
            "features": ["Shared compound", "Safe area"],
            "photo": None, "comments": [], "created_at": "2026-02-20",
        },
        {
            "id": 5, "title": "2BR near Huye University", "loc": "Huye",
            "price": 48000, "rooms": 2, "taken": False,
            "landlord": "Robert Hategekimana", "landlord_ini": "RH",
            "landlord_bg": "#FAEEDA", "landlord_tc": "#633806",
            "desc": "Comfortable 2-bedroom house 5 minutes from Huye University.",
            "features": ["Near university", "Water & electricity"],
            "photo": None, "comments": [], "created_at": "2026-03-15",
        },
        {
            "id": 6, "title": "Modern studio - Kacyiru", "loc": "Kacyiru, Kigali",
            "price": 55000, "rooms": 1, "taken": False,
            "landlord": "Diane Uwimana", "landlord_ini": "DU",
            "landlord_bg": "#E1F5EE", "landlord_tc": "#085041",
            "desc": "Modern studio with good internet access. Close to ministries.",
            "features": ["Internet access", "Modern finish", "Central location"],
            "photo": None, "comments": [], "created_at": "2026-03-18",
        },
    ],

    "workers": [
        {"id": 1, "name": "Diane Uwimana", "role": "House maid", "loc": "Gasabo, Kigali",
         "age": 26, "rating": 4.9, "review_count": 34,
         "skills": ["House maid", "Cleaner"], "avail": True, "verified": True,
         "ini": "DU", "bg": "#E1F5EE", "tc": "#085041", "photo": None,
         "bio": "3 years of household experience in Kigali. Reliable, punctual and respectful."},
        {"id": 2, "name": "Jean Pierre Habimana", "role": "Plumber", "loc": "Kicukiro, Kigali",
         "age": 33, "rating": 4.7, "review_count": 21,
         "skills": ["Plumber", "Welder"], "avail": True, "verified": True,
         "ini": "JP", "bg": "#E6F1FB", "tc": "#0C447C", "photo": None,
         "bio": "Certified plumber with 7 years experience. Available for emergency calls."},
        {"id": 3, "name": "Emmanuel Nshimiyimana", "role": "Guard", "loc": "Nyarugenge, Kigali",
         "age": 41, "rating": 4.8, "review_count": 18,
         "skills": ["Guard (Umuzamu)"], "avail": True, "verified": False,
         "ini": "EN", "bg": "#FAEEDA", "tc": "#633806", "photo": None,
         "bio": "Experienced night guard. Former military service. Strong and reliable."},
        {"id": 4, "name": "Aline Mukamana", "role": "Driver", "loc": "Kigali",
         "age": 35, "rating": 4.9, "review_count": 47,
         "skills": ["Driver"], "avail": True, "verified": True,
         "ini": "AM", "bg": "#EAF3DE", "tc": "#27500A", "photo": None,
         "bio": "Professional driver with clean license. Knows all routes in Kigali."},
        {"id": 5, "name": "Thierry Nzabonimana", "role": "Gardener", "loc": "Gasabo, Kigali",
         "age": 24, "rating": 4.5, "review_count": 9,
         "skills": ["Gardener", "Cleaner"], "avail": True, "verified": False,
         "ini": "TN", "bg": "#EEEDFE", "tc": "#3C3489", "photo": None,
         "bio": "Creative gardener who loves plants. Can design and maintain any garden."},
        {"id": 6, "name": "Pacifique Mugisha", "role": "Carpenter", "loc": "Musanze",
         "age": 29, "rating": 4.6, "review_count": 12,
         "skills": ["Carpenter", "Welder"], "avail": False, "verified": True,
         "ini": "PM", "bg": "#FBEAF0", "tc": "#72243E", "photo": None,
         "bio": "Skilled carpenter and welder. Custom furniture and metal work."},
        {"id": 7, "name": "Claudine Uwase", "role": "Cleaner", "loc": "Kicukiro, Kigali",
         "age": 22, "rating": 4.7, "review_count": 16,
         "skills": ["Cleaner", "Laundry helper"], "avail": True, "verified": False,
         "ini": "CU", "bg": "#FAECE7", "tc": "#993C1D", "photo": None,
         "bio": "Fast and thorough cleaner. Available for one-off or regular visits."},
        {"id": 8, "name": "Olivier Irakoze", "role": "Welder", "loc": "Huye",
         "age": 38, "rating": 4.8, "review_count": 23,
         "skills": ["Welder", "Carpenter"], "avail": False, "verified": True,
         "ini": "OI", "bg": "#E1F5EE", "tc": "#085041", "photo": None,
         "bio": "Professional welder with 10 years experience. Gates, fences, furniture."},
    ],

    "reviews": {
        1: [
            {"id": "r1", "author": "Marie Kayitesi", "author_ini": "MK",
             "author_bg": "#EEEDFE", "author_tc": "#3C3489",
             "stars": 5, "date": "2 weeks ago", "helpful": 12, "liked": False,
             "body": "Diane is incredibly reliable and thorough. She cleaned every corner and was very respectful.",
             "comments": [
                 {"id": "rc1", "author": "Diane Uwimana", "ini": "DU",
                  "bg": "#E1F5EE", "tc": "#085041", "is_worker": True,
                  "text": "Murakoze cyane Marie! It was a pleasure working in your home.",
                  "date": "2 weeks ago"},
             ]},
            {"id": "r2", "author": "Patrick Nkurunziza", "author_ini": "PN",
             "author_bg": "#E6F1FB", "author_tc": "#0C447C",
             "stars": 5, "date": "1 month ago", "helpful": 8, "liked": False,
             "body": "Very professional and punctual. Arrived on time and finished everything in one morning.",
             "comments": []},
        ],
        2: [
            {"id": "r3", "author": "Eric Habimana", "author_ini": "EH",
             "author_bg": "#E1F5EE", "author_tc": "#085041",
             "stars": 5, "date": "3 weeks ago", "helpful": 9, "liked": False,
             "body": "Jean Pierre fixed a complicated leak quickly and cleanly. Very trustworthy.",
             "comments": []},
        ],
        4: [
            {"id": "r4", "author": "David Ndagijimana", "author_ini": "DN",
             "author_bg": "#E6F1FB", "author_tc": "#0C447C",
             "stars": 5, "date": "4 days ago", "helpful": 7, "liked": False,
             "body": "Aline drove me to the airport at 4am. Very calm driver, knows Kigali perfectly.",
             "comments": []},
        ],
    },

    "messages": {
        1: [
            {"dir": "in",  "text": "Hello, I am available for house maid work.", "time": "9:30 AM"},
            {"dir": "out", "text": "Hi Diane! Tell me about your experience.",   "time": "9:32 AM"},
            {"dir": "in",  "text": "I have 3 years of experience. I can start Monday.", "time": "9:34 AM"},
        ],
        2: [
            {"dir": "out", "text": "Jean Pierre, I have a leaking pipe.", "time": "2:10 PM"},
            {"dir": "in",  "text": "I can come tomorrow at 8am.",         "time": "2:15 PM"},
            {"dir": "in",  "text": "The pipe is fixed now!",              "time": "4:10 PM"},
        ],
        3: [
            {"dir": "out", "text": "Aline, I need a driver to the airport Thursday.", "time": "10:00 AM"},
            {"dir": "in",  "text": "I am free. What time is your flight?",           "time": "10:04 AM"},
        ],
    },

    "conversations": [
        {"id": 1, "name": "Diane Uwimana",       "ini": "DU", "bg": "#E1F5EE", "tc": "#085041", "role": "House maid", "online": True,  "unread": 2, "preview": "I can start Monday"},
        {"id": 2, "name": "Jean Pierre Habimana","ini": "JP", "bg": "#E6F1FB", "tc": "#0C447C", "role": "Plumber",    "online": True,  "unread": 0, "preview": "The pipe is fixed now!"},
        {"id": 3, "name": "Aline Mukamana",      "ini": "AM", "bg": "#EAF3DE", "tc": "#27500A", "role": "Driver",     "online": False, "unread": 1, "preview": "I am free. What time is your flight?"},
    ],

    "notifications": [
        {"id": 1, "unread": True,  "icon": "msg",    "link": "/messages",          "title": "New comment on your listing",  "sub": "Marie K. commented on \"Cozy 2BR in Kicukiro\"",      "time": "5 min ago"},
        {"id": 2, "unread": True,  "icon": "house",  "link": "/houses/2",           "title": "House listing approved",        "sub": "Your listing \"Modern studio\" is now live",           "time": "1 hr ago"},
        {"id": 3, "unread": True,  "icon": "verify", "link": "/worker-dashboard",   "title": "Verification complete",          "sub": "Your ID has been verified. Verified badge added.",    "time": "3 hrs ago"},
        {"id": 4, "unread": False, "icon": "job",    "link": "/messages",           "title": "Job request received",           "sub": "Patrick is looking for a house maid in Gasabo",      "time": "Yesterday"},
        {"id": 5, "unread": False, "icon": "star",   "link": "/workers/1",          "title": "New review",                    "sub": "You received a 5-star review from Chantal Uwimana",  "time": "2 days ago"},
        {"id": 6, "unread": False, "icon": "house",  "link": "/houses/4",           "title": "House marked as taken",          "sub": "Room for rent - Musanze has been marked as taken",   "time": "3 days ago"},
    ],

    "next_ids": {"house": 100, "review": 200, "comment": 300, "notif": 400, "user": 10},

    "users": [
        {"id": 1, "name": "Diane Uwimana",        "phone": "+250788000001", "email": "diane@serivasi.rw",   "password": "demo123", "role": "worker",   "loc": "Gasabo, Kigali",    "age": 26, "skills": ["House maid","Cleaner"],  "ini": "DU", "bg": "#E1F5EE", "tc": "#085041"},
        {"id": 2, "name": "Jean Paul Nkurunziza",  "phone": "+250788000002", "email": "jp@serivasi.rw",      "password": "demo123", "role": "employer",  "loc": "Kicukiro, Kigali",  "age": 38, "skills": [],                       "ini": "JP", "bg": "#E6F1FB", "tc": "#0C447C"},
        {"id": 3, "name": "Admin User",            "phone": "+250788000000", "email": "admin@serivasi.rw",   "password": "admin",   "role": "employer",  "loc": "Kigali",            "age": 30, "skills": [],                       "ini": "AD", "bg": "#FAEEDA", "tc": "#633806"},
    ],

    # employer profiles — name, location, ratings from workers they hired
    "employer_profiles": {
        2: {
            "id": 2, "name": "Jean Paul Nkurunziza", "loc": "Kicukiro, Kigali",
            "ini": "JP", "bg": "#E6F1FB", "tc": "#0C447C", "photo": None,
            "member_since": "Jan 2025", "total_hires": 3,
            "comments": [
                {"id": "ec1", "author": "Diane Uwimana", "ini": "DU", "bg": "#E1F5EE", "tc": "#085041",
                 "text": "Great employer, very respectful and pays on time.", "date": "1 month ago", "stars": 5},
                {"id": "ec2", "author": "Thierry Nzabonimana", "ini": "TN", "bg": "#EEEDFE", "tc": "#3C3489",
                 "text": "Clear instructions and friendly family. Would work again.", "date": "2 months ago", "stars": 5},
            ]
        },
        3: {
            "id": 3, "name": "Admin User", "loc": "Kigali",
            "ini": "AD", "bg": "#FAEEDA", "tc": "#633806", "photo": None,
            "member_since": "Dec 2024", "total_hires": 0,
            "comments": []
        },
    },

    # general profile comments — public notes left on worker or employer profiles
    "profile_comments": {
        "worker": {
            1: [{"id":"pc1","author":"Ngabo Eric","ini":"NE","bg":"#EAF3DE","tc":"#27500A",
                 "text":"Diane helped us move in. Very organised and hardworking.","date":"3 weeks ago"}],
        },
        "employer": {},
    },

    # media messages — stores base64 or file paths for photo/audio/video messages
    "media_messages": {},
}



# ─── HELPERS ─────────────────────────────────────────────────────────────────

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def next_id(key):
    DB["next_ids"][key] += 1
    return DB["next_ids"][key]

def now_time():
    return datetime.now().strftime("%I:%M %p")

def get_house(hid):
    return next((h for h in DB["houses"] if h["id"] == hid), None)

def get_worker(wid):
    return next((w for w in DB["workers"] if w["id"] == wid), None)

def add_notification(icon, title, sub, link=None):
    default_links = {"msg": "/messages", "house": "/houses", "verify": "/worker-dashboard",
                     "job": "/messages", "star": "/workers/1"}
    DB["notifications"].insert(0, {
        "id": next_id("notif"), "unread": True,
        "icon": icon, "title": title, "sub": sub, "time": "Just now",
        "link": link or default_links.get(icon, "/"),
    })

def find_user(phone_or_email):
    val = (phone_or_email or "").strip().lower()
    return next((u for u in DB["users"]
                 if u["phone"].lower() == val or u["email"].lower() == val), None)

def safe_user(u):
    """Return user dict without password."""
    return {k: v for k, v in u.items() if k != "password"}


# ─── AUTH API ─────────────────────────────────────────────────────────────────

@app.route("/api/auth/login", methods=["POST"])
def api_login():
    data  = request.json or {}
    phone = data.get("phone", "").strip()
    pw    = data.get("password", "").strip()

    if not phone or not pw:
        return jsonify({"error": "Phone/email and password are required."}), 400

    user = find_user(phone)
    if not user or user["password"] != pw:
        return jsonify({"error": "Incorrect phone number or password."}), 401

    session["user_id"] = user["id"]
    add_notification("verify", "Welcome back!", f'You signed in as {user["name"]}.')
    return jsonify({"user": safe_user(user)}), 200


@app.route("/api/auth/signup", methods=["POST"])
def api_signup():
    data  = request.json or {}
    name  = data.get("name", "").strip()
    phone = data.get("phone", "").strip()
    pw    = data.get("password", "").strip()
    role  = data.get("role", "employer")
    loc   = data.get("location", "Kigali")
    age   = int(data.get("age") or 0)
    skills = data.get("skills", [])

    if not name:  return jsonify({"error": "Full name is required."}), 400
    if not phone: return jsonify({"error": "Phone number is required."}), 400
    if not pw:    return jsonify({"error": "Password is required."}), 400
    if len(pw) < 6: return jsonify({"error": "Password must be at least 6 characters."}), 400

    if find_user(phone):
        return jsonify({"error": "An account with this phone number already exists."}), 409

    ini = "".join(w[0] for w in name.split()[:2]).upper()
    bgs = ["#E1F5EE","#E6F1FB","#FAEEDA","#EEEDFE","#EAF3DE","#FAECE7","#FBEAF0"]
    tcs = ["#085041","#0C447C","#633806","#3C3489","#27500A","#993C1D","#72243E"]
    idx = len(DB["users"]) % len(bgs)

    new_user = {
        "id":       next_id("user"),
        "name":     name,
        "phone":    phone,
        "email":    "",
        "password": pw,
        "role":     role,
        "loc":      loc,
        "age":      age,
        "skills":   skills,
        "ini":      ini,
        "bg":       bgs[idx],
        "tc":       tcs[idx],
    }
    DB["users"].append(new_user)

    if role == "worker":
        new_worker_id = next_id("user")
        DB["workers"].append({
            "id":           new_worker_id,
            "name":         name,
            "role":         skills[0] if skills else "Worker",
            "loc":          loc,
            "age":          age,
            "rating":       3.5,      # default rating for new workers
            "review_count": 0,
            "jobs_done":    0,
            "skills":       skills,
            "avail":        True,
            "verified":     False,
            "ini":          ini,
            "bg":           bgs[idx],
            "tc":           tcs[idx],
            "photo":        None,
            "bio":          "",
        })
        # seed empty profile comments slot
        DB["profile_comments"]["worker"][new_worker_id] = []

    session["user_id"] = new_user["id"]
    add_notification("verify", "Welcome to Serivasi!", f'Your account was created, {name}.')
    return jsonify({"user": safe_user(new_user)}), 201


@app.route("/api/auth/logout", methods=["POST"])
def api_logout():
    session.pop("user_id", None)
    return jsonify({"ok": True})


@app.route("/api/auth/forgot", methods=["POST"])
def api_forgot():
    data  = request.json or {}
    phone = data.get("phone", "").strip()
    user  = find_user(phone)
    if not user:
        return jsonify({"error": "No account found with that phone number or email."}), 404
    # In production: generate token, send SMS/email. Here we just simulate it.
    return jsonify({"message": f"Reset code sent to {user['phone'][-4:].rjust(len(user['phone']), '*')}. (Demo: code is 1234)"}), 200



@app.route("/")
def index():
    available_houses = [h for h in DB["houses"] if not h["taken"]][:4]
    available_workers = [w for w in DB["workers"] if w["avail"]][:4]
    return render_template("index.html",
                           houses=available_houses,
                           workers=available_workers)

@app.route("/houses")
def houses():
    return render_template("houses.html", houses=DB["houses"])

@app.route("/houses/<int:hid>")
def house_detail(hid):
    house = get_house(hid)
    if not house:
        return render_template("404.html"), 404
    return render_template("house_detail.html", house=house)

@app.route("/houses/post", methods=["GET"])
def post_house_page():
    return render_template("post_house.html")

@app.route("/workers")
def workers():
    return render_template("workers.html", workers=DB["workers"])

@app.route("/workers/<int:wid>")
def worker_profile(wid):
    worker = get_worker(wid)
    if not worker:
        return render_template("404.html"), 404
    reviews = DB["reviews"].get(wid, [])
    avg = round(sum(r["stars"] for r in reviews) / len(reviews), 1) if reviews else 0
    return render_template("worker_profile.html",
                           worker=worker, reviews=reviews, avg=avg)

@app.route("/messages")
def messages():
    return render_template("messages.html",
                           conversations=DB["conversations"],
                           messages=DB["messages"],
                           workers=DB["workers"])

@app.route("/employers/<int:eid>")
def employer_profile(eid):
    ep = DB["employer_profiles"].get(eid)
    if not ep:
        user = next((u for u in DB["users"] if u["id"] == eid), None)
        if not user:
            return render_template("404.html"), 404
        ini = "".join(w[0] for w in user["name"].split()[:2]).upper()
        ep = {"id": eid, "name": user["name"], "loc": user["loc"],
              "ini": ini, "bg": user.get("bg","#E1F5EE"), "tc": user.get("tc","#085041"),
              "photo": None, "member_since": "2025", "total_hires": 0, "comments": []}
    return render_template("employer_profile.html", ep=ep)


@app.route("/employer-dashboard")
def employer_dashboard():
    return render_template("employer_dashboard.html",
                           houses=DB["houses"],
                           workers=DB["workers"])

@app.route("/worker-dashboard")
def worker_dashboard():
    # Use session user if logged in, otherwise allow ?id= param for demo, else default
    uid = session.get("user_id")
    worker = None
    if uid:
        # find the worker entry matching the logged-in user
        user = next((u for u in DB["users"] if u["id"] == uid), None)
        if user:
            worker = next((w for w in DB["workers"] if w["name"] == user["name"]), None)
    # fallback: ?id= param lets any worker view their own dashboard
    if not worker:
        wid = request.args.get("id", type=int)
        if wid:
            worker = get_worker(wid)
    # final fallback for demo — use first worker
    if not worker:
        worker = get_worker(1)
    reviews = DB["reviews"].get(worker["id"], [])
    return render_template("worker_dashboard.html",
                           worker=worker, reviews=reviews)

@app.route("/notifications")
def notifications():
    return render_template("notifications.html",
                           notifications=DB["notifications"])

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/help")
def help_page():
    return render_template("help.html")


# ─── API: HOUSES ─────────────────────────────────────────────────────────────

@app.route("/api/houses", methods=["GET"])
def api_houses():
    q      = request.args.get("q", "").lower()
    price  = int(request.args.get("price", 0))
    loc    = request.args.get("loc", "").lower()
    rooms  = int(request.args.get("rooms", 0))
    avail  = request.args.get("avail", "false").lower() == "true"

    result = DB["houses"]
    if q:     result = [h for h in result if q in h["title"].lower() or q in h["loc"].lower()]
    if price: result = [h for h in result if h["price"] <= price]
    if loc:   result = [h for h in result if loc in h["loc"].lower()]
    if rooms == 1: result = [h for h in result if h["rooms"] == 1]
    if rooms == 2: result = [h for h in result if h["rooms"] == 2]
    if rooms == 3: result = [h for h in result if h["rooms"] >= 3]
    if avail: result = [h for h in result if not h["taken"]]

    return jsonify(result)

@app.route("/api/houses", methods=["POST"])
def api_create_house():
    data = request.form
    photo_url = None

    if "photo" in request.files:
        f = request.files["photo"]
        if f and allowed_file(f.filename):
            filename = str(uuid.uuid4()) + "_" + secure_filename(f.filename)
            f.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            photo_url = "/static/uploads/" + filename

    house = {
        "id":           next_id("house"),
        "title":        data.get("title", "Untitled"),
        "loc":          data.get("loc", "Kigali"),
        "price":        int(data.get("price", 0)),
        "rooms":        int(data.get("rooms", 1)),
        "taken":        False,
        "landlord":     data.get("landlord", "Landlord"),
        "landlord_ini": data.get("landlord_ini", "LL"),
        "landlord_bg":  "#E1F5EE",
        "landlord_tc":  "#085041",
        "desc":         data.get("desc", ""),
        "features":     data.getlist("features"),
        "photo":        photo_url,
        "comments":     [],
        "created_at":   datetime.now().strftime("%Y-%m-%d"),
    }
    DB["houses"].insert(0, house)
    add_notification("house", "Listing published", f'"{house["title"]}" is now live.')
    return jsonify({"ok": True, "id": house["id"]}), 201

@app.route("/api/houses/<int:hid>/taken", methods=["POST"])
def api_mark_taken(hid):
    house = get_house(hid)
    if not house:
        return jsonify({"error": "Not found"}), 404
    house["taken"] = True
    add_notification("house", "House marked as taken", f'"{house["title"]}" is now taken.')
    return jsonify({"ok": True})

@app.route("/api/houses/<int:hid>/comments", methods=["POST"])
def api_house_comment(hid):
    house = get_house(hid)
    if not house:
        return jsonify({"error": "Not found"}), 404
    data = request.json or {}
    comment = {
        "id":          f"hc{next_id('comment')}",
        "author":      data.get("author", "Guest"),
        "ini":         data.get("ini", "G"),
        "bg":          data.get("bg", "#E1F5EE"),
        "tc":          data.get("tc", "#085041"),
        "is_landlord": False,
        "text":        data.get("text", ""),
        "date":        "Just now",
    }
    house["comments"].append(comment)
    add_notification("msg", "New comment", f'{comment["author"]} commented on "{house["title"]}"',
                     link=f"/houses/{hid}")
    return jsonify({"ok": True, "comment": comment}), 201


# ─── API: WORKERS ─────────────────────────────────────────────────────────────

@app.route("/api/workers", methods=["GET"])
def api_workers():
    q        = request.args.get("q", "").lower()
    skill    = request.args.get("skill", "").lower()
    loc      = request.args.get("loc", "").lower()
    avail    = request.args.get("avail", "false").lower() == "true"
    verified = request.args.get("verified", "false").lower() == "true"
    top      = request.args.get("top", "false").lower() == "true"

    result = DB["workers"]
    if q:        result = [w for w in result if q in w["name"].lower() or q in " ".join(w["skills"]).lower()]
    if skill:    result = [w for w in result if skill in " ".join(w["skills"]).lower()]
    if loc:      result = [w for w in result if loc in w["loc"].lower()]
    if avail:    result = [w for w in result if w["avail"]]
    if verified: result = [w for w in result if w["verified"]]
    if top:      result = [w for w in result if w["rating"] >= 4.7]

    return jsonify(result)

@app.route("/api/workers/<int:wid>/availability", methods=["POST"])
def api_worker_availability(wid):
    worker = get_worker(wid)
    if not worker:
        return jsonify({"error": "Not found"}), 404
    data = request.json or {}
    worker["avail"] = data.get("avail", not worker["avail"])
    return jsonify({"ok": True, "avail": worker["avail"]})

@app.route("/api/workers/<int:wid>/photo", methods=["POST"])
def api_worker_photo(wid):
    worker = get_worker(wid)
    if not worker:
        return jsonify({"error": "Not found"}), 404
    if "photo" in request.files:
        f = request.files["photo"]
        if f and allowed_file(f.filename):
            filename = str(uuid.uuid4()) + "_" + secure_filename(f.filename)
            f.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            worker["photo"] = "/static/uploads/" + filename
            return jsonify({"ok": True, "photo": worker["photo"]}), 200
    # avatar colour preset
    data = request.json or {}
    if data.get("bg"):
        worker["bg"] = data["bg"]
        worker["tc"] = data.get("tc", worker["tc"])
        worker["photo"] = None
        return jsonify({"ok": True, "bg": worker["bg"], "tc": worker["tc"]}), 200
    return jsonify({"error": "No photo or avatar provided"}), 400

@app.route("/api/users/<int:uid>/photo", methods=["POST"])
def api_user_photo(uid):
    user = next((u for u in DB["users"] if u["id"] == uid), None)
    if not user:
        return jsonify({"error": "Not found"}), 404
    if "photo" in request.files:
        f = request.files["photo"]
        if f and allowed_file(f.filename):
            filename = str(uuid.uuid4()) + "_" + secure_filename(f.filename)
            f.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            user["photo"] = "/static/uploads/" + filename
            return jsonify({"ok": True, "photo": user["photo"]}), 200
    data = request.json or {}
    if data.get("bg"):
        user["bg"] = data["bg"]
        user["tc"] = data.get("tc", user.get("tc", "#085041"))
        user.pop("photo", None)
        return jsonify({"ok": True, "bg": user["bg"]}), 200
    return jsonify({"error": "No photo or avatar provided"}), 400

@app.route("/api/workers/<int:wid>/reviews", methods=["GET"])
def api_worker_reviews(wid):
    return jsonify(DB["reviews"].get(wid, []))

@app.route("/api/workers/<int:wid>/reviews", methods=["POST"])
def api_post_review(wid):
    worker = get_worker(wid)
    if not worker:
        return jsonify({"error": "Not found"}), 404
    data = request.json or {}
    review = {
        "id":         f"r{next_id('review')}",
        "author":     data.get("author", "Guest"),
        "author_ini": data.get("author_ini", "G"),
        "author_bg":  data.get("author_bg", "#E1F5EE"),
        "author_tc":  data.get("author_tc", "#085041"),
        "stars":      int(data.get("stars", 5)),
        "date":       "Just now",
        "helpful":    0,
        "liked":      False,
        "body":       data.get("body", ""),
        "comments":   [],
    }
    if wid not in DB["reviews"]:
        DB["reviews"][wid] = []
    DB["reviews"][wid].insert(0, review)
    # recalculate worker average
    revs = DB["reviews"][wid]
    worker["rating"] = round(sum(r["stars"] for r in revs) / len(revs), 1)
    worker["review_count"] = len(revs)
    add_notification("star", "New review", f'{review["author"]} left a review for {worker["name"]}')
    return jsonify({"ok": True, "review": review}), 201

@app.route("/api/workers/<int:wid>/reviews/<rid>/helpful", methods=["POST"])
def api_helpful(wid, rid):
    revs = DB["reviews"].get(wid, [])
    review = next((r for r in revs if r["id"] == rid), None)
    if not review:
        return jsonify({"error": "Not found"}), 404
    review["liked"] = not review["liked"]
    review["helpful"] += 1 if review["liked"] else -1
    return jsonify({"ok": True, "helpful": review["helpful"], "liked": review["liked"]})

@app.route("/api/workers/<int:wid>/reviews/<rid>/comments", methods=["POST"])
def api_review_comment(wid, rid):
    revs = DB["reviews"].get(wid, [])
    review = next((r for r in revs if r["id"] == rid), None)
    if not review:
        return jsonify({"error": "Not found"}), 404
    data = request.json or {}
    comment = {
        "id":        f"rc{next_id('comment')}",
        "author":    data.get("author", "Guest"),
        "ini":       data.get("ini", "G"),
        "bg":        data.get("bg", "#E1F5EE"),
        "tc":        data.get("tc", "#085041"),
        "is_worker": data.get("is_worker", False),
        "text":      data.get("text", ""),
        "date":      "Just now",
    }
    review["comments"].append(comment)
    return jsonify({"ok": True, "comment": comment}), 201


# ─── API: MESSAGES ───────────────────────────────────────────────────────────

@app.route("/api/messages/<int:convo_id>", methods=["GET"])
def api_get_messages(convo_id):
    return jsonify(DB["messages"].get(convo_id, []))

@app.route("/api/messages/<int:convo_id>", methods=["POST"])
def api_send_message(convo_id):
    data = request.json or {}
    msg = {
        "dir":  data.get("dir", "out"),
        "text": data.get("text", ""),
        "time": now_time(),
        "type": data.get("type", "text"),
        "media_url": data.get("media_url"),
    }
    if convo_id not in DB["messages"]:
        DB["messages"][convo_id] = []
    DB["messages"][convo_id].append(msg)
    convo = next((c for c in DB["conversations"] if c["id"] == convo_id), None)
    if convo:
        convo["preview"] = msg["text"] or f"[{msg['type']}]"
        convo["unread"] = max(0, convo.get("unread", 0) - 1) if msg["dir"] == "out" else convo.get("unread", 0) + 1
    return jsonify({"ok": True, "message": msg}), 201

@app.route("/api/messages/<int:convo_id>/media", methods=["POST"])
def api_send_media(convo_id):
    """Upload a photo, audio or video file and store it as a message."""
    if "file" not in request.files:
        return jsonify({"error": "No file"}), 400
    f = request.files["file"]
    media_type = request.form.get("type", "photo")
    ext = f.filename.rsplit(".", 1)[-1].lower() if "." in f.filename else "bin"
    allowed = {"photo": {"jpg","jpeg","png","gif","webp"},
               "audio": {"mp3","wav","ogg","m4a","webm"},
               "video": {"mp4","mov","webm","avi"}}
    if ext not in allowed.get(media_type, set()):
        return jsonify({"error": f"Invalid file type for {media_type}"}), 400
    filename = str(uuid.uuid4()) + "_" + secure_filename(f.filename)
    f.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
    url = "/static/uploads/" + filename
    msg = {
        "dir": "out",
        "text": f"[{media_type.capitalize()} attachment]",
        "time": now_time(),
        "type": media_type,
        "media_url": url,
    }
    if convo_id not in DB["messages"]:
        DB["messages"][convo_id] = []
    DB["messages"][convo_id].append(msg)
    convo = next((c for c in DB["conversations"] if c["id"] == convo_id), None)
    if convo:
        convo["preview"] = f"[{media_type.capitalize()}]"
    return jsonify({"ok": True, "message": msg, "url": url}), 201


# ─── API: PROFILE COMMENTS ────────────────────────────────────────────────────

@app.route("/api/workers/<int:wid>/profile-comments", methods=["GET"])
def api_get_worker_profile_comments(wid):
    return jsonify(DB["profile_comments"]["worker"].get(wid, []))

@app.route("/api/workers/<int:wid>/profile-comments", methods=["POST"])
def api_post_worker_profile_comment(wid):
    worker = get_worker(wid)
    if not worker:
        return jsonify({"error": "Not found"}), 404
    data = request.json or {}
    comment = {
        "id": f"pc{next_id('comment')}",
        "author": data.get("author", "Guest"),
        "ini": data.get("ini", "G"),
        "bg": data.get("bg", "#E1F5EE"),
        "tc": data.get("tc", "#085041"),
        "text": data.get("text", ""),
        "date": "Just now",
    }
    if wid not in DB["profile_comments"]["worker"]:
        DB["profile_comments"]["worker"][wid] = []
    DB["profile_comments"]["worker"][wid].append(comment)
    return jsonify({"ok": True, "comment": comment}), 201

@app.route("/api/employers/<int:eid>/profile-comments", methods=["GET"])
def api_get_employer_profile_comments(eid):
    ep = DB["employer_profiles"].get(eid, {})
    return jsonify(ep.get("comments", []))

@app.route("/api/employers/<int:eid>/profile-comments", methods=["POST"])
def api_post_employer_profile_comment(eid):
    ep = DB["employer_profiles"].get(eid)
    if not ep:
        # create on the fly
        user = next((u for u in DB["users"] if u["id"] == eid), None)
        if not user:
            return jsonify({"error": "Not found"}), 404
        ini = "".join(w[0] for w in user["name"].split()[:2]).upper()
        ep = {"id": eid, "name": user["name"], "loc": user["loc"],
              "ini": ini, "bg": user.get("bg","#E1F5EE"), "tc": user.get("tc","#085041"),
              "photo": None, "member_since": "2025", "total_hires": 0, "comments": []}
        DB["employer_profiles"][eid] = ep
    data = request.json or {}
    comment = {
        "id": f"ec{next_id('comment')}",
        "author": data.get("author", "Guest"),
        "ini": data.get("ini", "G"),
        "bg": data.get("bg", "#E1F5EE"),
        "tc": data.get("tc", "#085041"),
        "text": data.get("text", ""),
        "stars": int(data.get("stars", 5)),
        "date": "Just now",
    }
    ep["comments"].append(comment)
    return jsonify({"ok": True, "comment": comment}), 201

@app.route("/api/employers/<int:eid>", methods=["GET"])
def api_employer_profile(eid):
    ep = DB["employer_profiles"].get(eid)
    if not ep:
        user = next((u for u in DB["users"] if u["id"] == eid), None)
        if not user:
            return jsonify({"error": "Not found"}), 404
        ini = "".join(w[0] for w in user["name"].split()[:2]).upper()
        ep = {"id": eid, "name": user["name"], "loc": user["loc"],
              "ini": ini, "bg": user.get("bg","#E1F5EE"), "tc": user.get("tc","#085041"),
              "photo": None, "member_since": "2025", "total_hires": 0, "comments": []}
    return jsonify(ep)



@app.route("/api/notifications", methods=["GET"])
def api_notifications():
    return jsonify(DB["notifications"])

@app.route("/api/notifications/read-all", methods=["POST"])
def api_read_all():
    for n in DB["notifications"]:
        n["unread"] = False
    return jsonify({"ok": True})

@app.route("/api/notifications/<int:nid>/read", methods=["POST"])
def api_read_one(nid):
    notif = next((n for n in DB["notifications"] if n["id"] == nid), None)
    if notif:
        notif["unread"] = False
    return jsonify({"ok": True})


# ─── API: UPLOAD ─────────────────────────────────────────────────────────────

@app.route("/api/upload", methods=["POST"])
def api_upload():
    if "file" not in request.files:
        return jsonify({"error": "No file"}), 400
    f = request.files["file"]
    if not f or not allowed_file(f.filename):
        return jsonify({"error": "Invalid file type"}), 400
    filename = str(uuid.uuid4()) + "_" + secure_filename(f.filename)
    f.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
    url = "/static/uploads/" + filename
    return jsonify({"ok": True, "url": url}), 201


# ─── API: BOT ────────────────────────────────────────────────────────────────

BOT_KB = {
    "house":   ["find a house", "rent", "affordable", "accommodation", "find house", "looking for a place"],
    "post":    ["post a house", "list a house", "add listing", "new listing"],
    "free":    ["free", "cost", "price", "pay", "pricing", "how much"],
    "review":  ["review", "rating", "stars", "feedback", "rate"],
    "contact": ["contact", "message", "chat", "reach", "dm"],
    "verify":  ["verified", "verification", "trust", "badge", "id check"],
    "taken":   ["mark as taken", "taken", "no longer available"],
    "profile": ["create a profile", "sign up", "register", "join"],
    "find":    ["find a worker", "search worker", "hire", "need a maid"],
}

BOT_ANSWERS = {
    "house":   "Go to Houses in the menu. Use price and location filters to narrow results. Click any card to see full details and comment directly to the landlord.",
    "post":    "Click '+ Post house' in the nav. Add photos, price, location, bedrooms, description and features. It goes live after a quick review.",
    "free":    "Yes - Serivasi is completely free to join and use for both workers and employers.",
    "review":  "After a job, employers leave a star rating and written comment on the worker profile. All reviews are public.",
    "contact": "Open any worker card or house listing and click Message or DM to start a private chat.",
    "verify":  "Workers verify their phone and submit their national ID. Verified workers get a blue checkmark badge.",
    "taken":   "Open the listing or go to your Employer dashboard. Click 'Mark as taken' - it turns red and is hidden from searches.",
    "profile": "Click 'Join free' in the nav. Choose worker or employer, add your name, location, age and - if a worker - pick your skills.",
    "find":    "Go to Workers in the menu, type a name or skill, and use filters for location, availability, or verified-only.",
}

@app.route("/api/bot", methods=["POST"])
def api_bot():
    data = request.json or {}
    q = data.get("message", "").lower()
    answer = None
    for key, phrases in BOT_KB.items():
        if any(p in q for p in phrases):
            answer = BOT_ANSWERS[key]
            break
    if not answer:
        if any(w in q for w in ["hello", "hi", "muraho", "bonjour"]):
            answer = "Muraho! How can I help you today?"
        elif "thank" in q:
            answer = "You're welcome! Feel free to ask anything else."
        else:
            answer = "I'm not sure about that yet. Try asking about houses, workers, pricing, or verification."
    return jsonify({"answer": answer})


# ─── 404 ─────────────────────────────────────────────────────────────────────

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True, port=5000)
