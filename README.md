# Django Boilerplate Repository

A production-grade Django boilerplate designed as a scalable and reusable GitHub starter template. This project implements best practices for architecture, security, and developer experience.

## Project Overview

**Tech Stack:**
- **Language:** Python 3.12+
- **Framework:** Django 5+
- **API:** Django Rest Framework (DRF)
- **Database:** PostgreSQL
- **Authentication:** JWT via `djangorestframework-simplejwt`
- **Asynchronous Tasks:** Celery + Redis
- **Containerization:** Docker + Docker Compose

## Architecture Explanation

This application follows a clean monolith architecture standard:

- `config/`: Central project settings. Split into `base.py`, `dev.py`, and `production.py` to organize environment-specific configurations safely. Also contains ASGI/WSGI entry points and Celery setup.
- `apps/`: Contains isolated business domains. Only the `users` app is included out of the box.
- `apps/users/`: Implements custom authentication (`User`), an `OTP` model, custom Managers, and a robust `services.py` containing pure Python business logic (decoupled from views).
- `common/`: Contains shared logic, constants, and utilities usable across all apps.
- `docker/`: Contains specialized `Dockerfile` definitions for `django` and `celery`.

## Setup Instructions

### Local Development (Virtual Environment)
1. **Clone the repository:**
   ```bash
   git clone <repo-url> my-project
   cd my-project
   ```

2. **Set up the virtual environment:**
   ```bash
   python3.12 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables:**
   ```bash
   cp .env.example .env
   # Make sure to edit .env and update DB, Redis, and Email configurations
   ```

4. **Run database setup (assuming local PostgreSQL is running):**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. **Start the local server:**
   ```bash
   python manage.py runserver
   ```

### Docker Usage
We recommend using Docker Compose for an isolated environment that sets up PostgreSQL, Redis, Django, and Celery automatically.

1. **Build and start the containers:**
   ```bash
   docker-compose up --build
   ```

2. **Run migrations within Docker:**
   ```bash
   docker-compose exec django python manage.py makemigrations
   docker-compose exec django python manage.py migrate
   ```

3. **Create a superuser:**
   ```bash
   docker-compose exec django python manage.py createsuperuser
   ```

### Running the Celery Worker
If you are running outside of Docker, start the Celery worker and ensure Redis is running:
```bash
celery -A config worker -l info
```
(Docker handles this automatically using the `celery-worker` service defined in `docker-compose.yml`)

## Environment Variables
Environment variables are handled via `django-environ`. Copy `.env.example` to `.env` and configure:

**Core Settings:**
- `DJANGO_SETTINGS_MODULE` - Defaults to `config.settings.dev`. Use `config.settings.production` for production deployments.
- `DEBUG` - Set to `False` in production.
- `SECRET_KEY` - A long, random secret key. Generate a new one for each deployment.
- `ALLOWED_HOSTS` - Comma-separated list of allowed hostnames.

**Database:**
- `DATABASE_URL` - PostgreSQL connection string. Format: `postgres://user:password@host:port/database`

**Redis & Celery:**
- `REDIS_URL` - Redis connection URL for Celery task queue. Default: `redis://localhost:6379/0`

**Email (SMTP):**
- `EMAIL_HOST` - SMTP server hostname (e.g., `smtp.gmail.com`)
- `EMAIL_PORT` - SMTP port (usually 587 for TLS, 465 for SSL)
- `EMAIL_HOST_USER` - SMTP username/email
- `EMAIL_HOST_PASSWORD` - SMTP password or app-specific password
- `EMAIL_USE_TLS` - Whether to use TLS encryption
- `DEFAULT_FROM_EMAIL` - Sender email address for application emails

**JWT:**
- `JWT_SECRET_KEY` - Secret key for JWT token signing. Can default to `SECRET_KEY` if not set.

**OTP (One-Time Password):**
- `OTP_EXPIRATION_MINUTES` - OTP validity duration in minutes (default: 10)
- `MAX_OTP_ATTEMPTS` - Maximum failed OTP verification attempts before lockout (default: 5)

## Development vs Production Settings
- **`dev.py`**: Enables `DEBUG=True`, uses console email backend, and lacks cookie security enforcement.
- **`production.py`**: Forces `DEBUG=False`, reads a secure production DB URL, enforces HTTPS, sets strict HSTS headers, secure cookies, proxy headers, and sets up SMTP for real emails.

## API Endpoints
Provided endpoints currently cover the authentication flow using DRF:

- `POST /api/users/signup/` - Submits an email and password. Generates and sends a 6-digit OTP to the provided email address via standard Django email. Sets user as inactive.
- `POST /api/users/confirm-signup/` - Validates the OTP within 10 minutes. If valid, the user becomes active and verified.
- `POST /api/users/login/` - Accepts an email and password. Returns JWT `access` and `refresh` tokens for authenticated endpoints.
- `POST /api/users/token/refresh/` - Takes a refresh token and returns a new access token.

## Formatting
This project is configured to work smoothly with standard configurations of **Black** and **Ruff**.
