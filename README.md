# DARKMATTER — Django Web Application

**Engineering Beyond Boundaries**

A full-featured Django web application for the DarkMatter builder ecosystem with admin panel management.


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
