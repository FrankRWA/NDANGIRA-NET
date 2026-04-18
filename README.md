# Serivasi — Flask Server

Rwanda's platform for affordable housing and trusted workers.

## Project structure

```
serivasi-flask/
├── app.py                  ← Flask app + all routes + REST API
├── requirements.txt
├── static/
│   ├── css/main.css        ← All styles (dark/light mode, responsive)
│   ├── js/                 ← Shared frontend helpers
│   └── uploads/            ← Uploaded house photos (auto-created)
└── templates/
    ├── base.html           ← Nav, footer, auth modals, theme toggle
    ├── index.html          ← Home — FYP with houses first
    ├── houses.html         ← House listings with filters
    ├── house_detail.html   ← Single house, comments, mark taken
    ├── post_house.html     ← Landlord listing form
    ├── workers.html        ← Worker search with filters
    ├── worker_profile.html ← Worker profile, reviews, star ratings
    ├── messages.html       ← Chat interface
    ├── employer_dashboard.html
    ├── worker_dashboard.html
    ├── notifications.html
    ├── about.html
    ├── help.html           ← FAQ + Seri chatbot
    └── 404.html
```

## Quick start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the server
python app.py

# 3. Open in browser
# http://localhost:5000
```

## REST API endpoints

### Houses
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/houses` | List houses (supports ?q=, ?price=, ?loc=, ?rooms=, ?avail=true) |
| POST | `/api/houses` | Create a listing (multipart/form-data with optional photo) |
| POST | `/api/houses/<id>/taken` | Mark house as taken |
| POST | `/api/houses/<id>/comments` | Post a comment on a listing |

### Workers
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/workers` | List workers (supports ?q=, ?skill=, ?loc=, ?avail=, ?verified=, ?top=) |
| POST | `/api/workers/<id>/availability` | Toggle availability |
| GET | `/api/workers/<id>/reviews` | Get reviews |
| POST | `/api/workers/<id>/reviews` | Post a review |
| POST | `/api/workers/<id>/reviews/<rid>/helpful` | Toggle helpful on a review |
| POST | `/api/workers/<id>/reviews/<rid>/comments` | Comment on a review |

### Messages
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/messages/<convo_id>` | Get messages in a conversation |
| POST | `/api/messages/<convo_id>` | Send a message |

### Notifications
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/notifications` | Get all notifications |
| POST | `/api/notifications/read-all` | Mark all as read |
| POST | `/api/notifications/<id>/read` | Mark one as read |

### Utilities
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/upload` | Upload a file, returns `{url}` |
| POST | `/api/bot` | Chat with Seri, send `{message}`, returns `{answer}` |

## Production deployment

For production, replace the in-memory `DB` dict in `app.py` with SQLAlchemy models
pointing to a PostgreSQL or SQLite database. Everything else stays the same.

```python
# Example: swap to SQLite
from flask_sqlalchemy import SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///serivasi.db"
db = SQLAlchemy(app)
```

You can also deploy directly to:
- **Railway** — push to GitHub, connect repo
- **Render** — add a `render.yaml` with `startCommand: python app.py`
- **Heroku** — add a `Procfile`: `web: python app.py`
