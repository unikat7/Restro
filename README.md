# TastyHub — Django Restaurant Project

A complete, dynamic Django restaurant web app: browsable menu, session-based
cart, checkout/order tracking, table reservations, contact form, and simple
email/password authentication (**no social login, no `.env` file** — all
settings are hardcoded in `restaurant_site/settings.py` for simplicity).

## Features

- **Menu** — categories, items with images/prices, search, category filter, item detail pages
- **Cart** — session-based (add / update quantity / remove), login required to add items to cart
- **Checkout & Orders** — guest or logged-in checkout, delivery or pickup, order history & status tracking for logged-in users
- **Table Reservations** — date/time/guest count booking form
- **Contact Form** — stored in DB, visible in admin
- **Accounts** — register, login, logout, edit profile, change password (Django's built-in auth, no OAuth/social)
- **Admin Panel** — manage categories, menu items, orders, reservations, and contact messages
- **Styling** — Bootstrap 5 + custom warm restaurant theme (no build step, CDN-based)
- **Database** — SQLite (`db.sqlite3`), created automatically on first migrate

## Project Structure

```
restaurant_project/
├── manage.py
├── requirements.txt
├── restaurant_site/      # project settings & root urls
├── core/                 # home, about, contact
├── menu/                 # categories & menu items
├── cart/                 # session cart logic
├── orders/                # checkout, order + order items, order history
├── reservation/           # table reservation form
├── accounts/               # register/login/logout/profile (Profile model)
├── templates/             # all HTML templates (base.html + app subfolders)
└── static/css/style.css   # custom theme
```

## Setup Instructions

1. **Create & activate a virtual environment** (recommended)

   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` file** in the project root:

   ```env
   DJANGO_SECRET_KEY=replace-with-a-long-random-secret
   DJANGO_DEBUG=True
   DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
   ```

4. **Run migrations** (creates `db.sqlite3` automatically)

   ```bash
   python manage.py migrate
   ```

5. **Create an admin user**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the dev server**
   ```bash
   python manage.py runserver
   ```
   Visit **http://127.0.0.1:8000/** for the site and
   **http://127.0.0.1:8000/admin/** for the admin panel.

## Deploying on PythonAnywhere

1. Create a PythonAnywhere account and open a **Bash console**.
2. Upload or clone this project into `/home/<username>/restaurantProject`.
3. Create a virtual environment and install dependencies:

   ```bash
   mkvirtualenv --python=/usr/bin/python3.13 restaurant-env
   pip install -r /home/<username>/restaurantProject/requirements.txt
   ```

4. In the **Web** tab, create a manual configuration. Set the source code
   and working directory to `/home/<username>/restaurantProject`, and set the
   virtualenv to `/home/<username>/.virtualenvs/restaurant-env`.
5. Edit the generated WSGI file and add:

   ```python
   import os
   import sys

   project_home = '/home/<username>/restaurantProject'
   if project_home not in sys.path:
       sys.path.insert(0, project_home)

   os.environ['DJANGO_SETTINGS_MODULE'] = 'restaurant_site.settings'
   from restaurant_site.wsgi import application
   ```

6. Set these environment variables in the WSGI file before going live:
   `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`,
   `DJANGO_ALLOWED_HOSTS=<username>.pythonanywhere.com`, and
   `DJANGO_CSRF_TRUSTED_ORIGINS=https://<username>.pythonanywhere.com`.
7. Run these commands in the Bash console:

   ```bash
   cd /home/<username>/restaurantProject
   python manage.py migrate
   python manage.py collectstatic --noinput
   python manage.py createsuperuser
   ```

8. Add these static mappings in the **Web** tab:
   - URL `/static/` -> `/home/<username>/restaurantProject/staticfiles/`
   - URL `/media/` -> `/home/<username>/restaurantProject/media/`
9. Reload the web app and visit `https://<username>.pythonanywhere.com/`.

Replace `<username>` with your PythonAnywhere username. SQLite is suitable for
a small deployment; back up `db.sqlite3` regularly from the Files tab.

## Adding Menu Items

Easiest way: log into `/admin/`, add a **Category**, then add **Menu Items**
under it (name, price, description, image, mark "Chef's Special" to feature
on the homepage).

## Notes

- `DEBUG = True` and `SECRET_KEY` are hardcoded in `settings.py` — **change
  both before deploying to production**, and set `DEBUG = False` with a
  proper `ALLOWED_HOSTS` list.
- Email is sent to the console (no SMTP config needed) via
  `django.core.mail.backends.console.EmailBackend`.
- Media (uploaded images) are stored under `/media/`; static files under `/static/`.
  The included `media/menu/` folder already has menu photos, which can be
  replaced anytime by uploading a real photo to a Menu Item in the admin panel.
- No social auth / OAuth is included — only Django's standard username+password auth.

## Default URLs

| Path                                      | Purpose                                   |
| ----------------------------------------- | ----------------------------------------- |
| `/`                                       | Home                                      |
| `/menu/`                                  | Menu list (with search & category filter) |
| `/menu/item/<slug>/`                      | Item detail                               |
| `/cart/`                                  | Cart                                      |
| `/orders/checkout/`                       | Checkout                                  |
| `/orders/history/`                        | My orders (login required)                |
| `/reservation/`                           | Table reservation                         |
| `/contact/`                               | Contact form                              |
| `/accounts/register/`, `/accounts/login/` | Auth                                      |
| `/admin/`                                 | Django admin                              |
