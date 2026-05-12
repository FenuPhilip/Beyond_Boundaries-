# DARKMATTER — Django Web Application

**Engineering Beyond Boundaries**

A full-featured Django web application for the DarkMatter builder ecosystem with admin panel management.

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Migrations
```bash
python manage.py migrate
```

### 3. Create Admin User
```bash
python manage.py createsuperuser
```
Enter your username, email, and password when prompted.

### 4. Collect Static Files
```bash
python manage.py collectstatic
```

### 5. Run the Server
```bash
python manage.py runserver
```

---

## 🌐 Access

| URL | Description |
|-----|-------------|
| `http://127.0.0.1:8000/` | Main website (home page) |
| `http://127.0.0.1:8000/project-request/` | Project registration form |
| `http://127.0.0.1:8000/mentor-request/` | Mentor request form |
| `http://127.0.0.1:8000/builder-join/` | Builder/Mentor join form |
| `http://127.0.0.1:8000/admin/` | **Admin panel** |

---

## 🔧 Admin Panel Features

The Django admin at `/admin/` lets you:

- **View all Project Requests** — with domain/status color badges, WhatsApp links, filters by domain/status/date
- **Update project status** — Pending → Reviewing → Accepted → In Progress → Completed
- **View all Mentor Requests** — filter by domain, mentorship type, mode, date
- **View all Builder/Mentor Applications** — filter by role, domain, experience level; direct links to GitHub/LinkedIn

### Admin Customizations
- Color-coded domain and status badges
- Quick WhatsApp link from list view
- Collapsed/expanded fieldset sections
- Date hierarchy navigation
- Search across names, emails, WhatsApp

---

## 📁 Project Structure

```
darkmatter/
├── manage.py
├── requirements.txt
├── setup.sh
├── db.sqlite3          (auto-created)
├── darkmatter_site/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── core/
    ├── models.py       (ProjectRequest, MentorRequest, BuilderMentorJoin)
    ├── views.py
    ├── forms.py
    ├── admin.py        (Custom admin with badges and filters)
    ├── urls.py
    ├── templates/core/
    │   ├── base.html
    │   ├── home.html
    │   ├── project_request.html
    │   ├── mentor_request.html
    │   ├── builder_join.html
    │   └── success.html
    └── static/core/
        ├── css/style.css
        ├── js/main.js
        └── images/
            ├── DM_logo.png
            └── nameboard_and_logo.png
```

---

## 🎨 Design

- **Theme**: Dark tech / cyberpunk — obsidian black with circuit green accents
- **Fonts**: Orbitron (display), Exo 2 (body), Rajdhani (UI), Share Tech Mono (code/labels)
- **Color Palette**: `#050608` black, `#2dff7f` green, `#00e5ff` cyan
- **Features**: Animated hero, scroll-reveal, floating logo, circuit grid background, responsive mobile nav

---

## 📦 Models

### ProjectRequest
Full project registration with domain, deliverables checklist, deadline, file upload, status tracking.

### MentorRequest  
Mentorship request with domain, help description, mentorship type, current status, preferred contact mode.

### BuilderMentorJoin
Ecosystem application with role (Builder/Mentor/Both), domain, skills, portfolio links, contribution interests.

---

## ⚙️ Production Notes

For production deployment:
1. Set `DEBUG = False` in settings.py
2. Set a secure `SECRET_KEY`
3. Configure `ALLOWED_HOSTS` with your domain
4. Use PostgreSQL instead of SQLite
5. Configure email backend for notifications
6. Set up a proper web server (Nginx + Gunicorn)
