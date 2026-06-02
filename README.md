# cake_baker_final-django  

A Django‑based web application that simulates a simple “cake bakery” platform. It demonstrates core Django concepts (models, forms, admin, migrations) together with a lightweight blockchain‑style voting system for cake‑related decisions.

---  

## Overview  

`cake_baker_final-django` is a learning project that showcases how to build a full‑stack Django app from scratch. The repository contains:

| Path | Description |
|------|-------------|
| `manage.py` | Django command‑line utility. |
| `myapp/` | Main application package (models, views, forms, admin, blockchain logic, URLs). |
| `myapp/migrations/` | Database schema evolution scripts. |
| `cakes/cs304p.PNG` | Sample image used in the UI (e.g., cake illustration). |
| `myapp/__pycache__/` | Compiled Python files (auto‑generated). |

The app lets users register, create a profile, submit cake ideas, and vote on them using a simple blockchain‑like ledger to ensure vote integrity.

---  

## Features  

- **User & Profile Management** – Registration, login, and editable profile (age, gender, picture, etc.).  
- **Cake Submission** – Users can create and edit cake entries with images and descriptions.  
- **Blockchain‑Style Voting** – Each vote is recorded as an immutable block (`myapp/blockchain.py`).  
- **Admin Interface** – Full CRUD access for admins via Django’s built‑in admin panel.  
- **Comment System** – Users can leave comments on cake entries; sentiment labels are stored (future extension).  
- **Responsive Templates** – Basic HTML/CSS templates for a clean UI (extendable with Bootstrap or Tailwind).  

---  

## Tech Stack  

| Layer | Technology |
|-------|------------|
| Backend | Python 3.9+, Django 4.x |
| Database | SQLite (default) – can be swapped for PostgreSQL/MySQL |
| Front‑end | HTML5, CSS3 (static files) |
| Version Control | Git |
| Deployment | Any WSGI‑compatible server (e.g., Gunicorn + Nginx) |
| Optional | Docker (add a `Dockerfile` if you need containerised deployment) |

---  

## Installation  

> **Prerequisites**  
> - Python 3.9 or newer  
> - `pip` (Python package manager)  
> - (Optional) Virtual environment tool (`venv` or `virtualenv`)

```bash
# 1️⃣ Clone the repository
git clone https://github.com/YOUR_USERNAME/cake_baker_final-django.git
cd cake_baker_final-django

# 2️⃣ Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate

# 3️⃣ Install dependencies
pip install -r requirements.txt   # If the file is missing, run:
# pip install Django==4.*   # adjust version as needed

# 4️⃣ Apply migrations
python manage.py migrate

# 5️⃣ Create a superuser (admin access)
python manage.py createsuperuser
# Follow the prompts – use a strong password.

# 6️⃣ Collect static files (optional for production)
python manage.py collectstatic
```

> **Note** – If you plan to use a different database (PostgreSQL, MySQL, etc.), update `myproject/settings.py` accordingly and install the appropriate DB driver.

---  

## Usage  

### Development Server  

```bash
python manage.py runserver
```

Open a browser and navigate to `http://127.0.0.1:8000/`.  

- **Admin panel:** `http://127.0.0.1:8000/admin/` (log in with the superuser created above).  
- **User flow:** Register → create