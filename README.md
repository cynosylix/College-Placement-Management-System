# College Placement Management System (CPMS)

This repo currently includes the starter **authentication module** (professional UI) for:

- Login
- Registration
- Logout

## Run locally

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py migrate
```

Start server:

```bash
python manage.py runserver
```

## URLs

- Login: `/accounts/login/`
- Register: `/register/`
- Home (requires login): `/`
- Admin: `/admin/`
Web-Based College Placement Management System
