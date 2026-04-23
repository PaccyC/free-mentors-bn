# FreeMentors — Backend

Django 3.2 + GraphQL API for the FreeMentors platform, backed by MongoDB Atlas.

## Tech Stack

| Tool | Version |
|------|---------|
| Python | 3.9 |
| Django | 3.2 |
| graphene-django | 3.2.3 |
| Djongo | 1.3.7 |
| PyMongo | 3.11.4 |
| PyJWT | 2.12.1 |
| django-cors-headers | 3.14.0 |

## Prerequisites

- Python 3.9
- MongoDB Atlas account (or local MongoDB instance)

## Setup

```bash
cd free-mentors-bn
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install --use-deprecated=legacy-resolver -r requirements.txt
```

> **Note:** `--use-deprecated=legacy-resolver` is required because Djongo 1.3.7 incorrectly declares `django<=3.1.12` in its metadata, but is compatible with Django 3.2. The strict pip resolver rejects the installation without this flag.

Create a `.env` file:

```env
MONGODB_URI=mongodb+srv://<user>:<password>@<cluster>.mongodb.net/
MONGODB_DB_NAME=free_mentors_db
SECRET_KEY=your-django-secret-key
JWT_SECRET=your-jwt-secret          # optional — falls back to SECRET_KEY
```

Apply migrations and start the server:

```bash
python manage.py migrate
python manage.py runserver
```

## Commands

```bash
python manage.py runserver        # Dev server on http://localhost:8000
python manage.py migrate          # Apply migrations
python manage.py makemigrations   # Generate migration files
python manage.py check            # Validate configuration
```

> **MongoDB schema changes:** Djongo does not support `ALTER TABLE`. When adding fields to existing models, set the migration's `operations = []` (no-op). MongoDB is schemaless, so new fields work without an SQL migration.

## GraphQL API

**Endpoint:** `POST http://localhost:8000/graphql`

GraphiQL interactive UI is available at `http://localhost:8000/graphql` in a browser (GET request).

**Authentication:** Pass a JWT in the `Authorization` header:

```
Authorization: Bearer <token>
```

### Queries

| Query | Auth | Description |
|-------|------|-------------|
| `mentors` | No | List all users with MENTOR role |
| `mentor(id)` | No | Get a single mentor's profile |
| `me` | Yes | Get the authenticated user's profile |
| `allUsers` | ADMIN | List all users |
| `mySessions` | Yes | Sessions created by the authenticated mentee |
| `mentorSessions` | MENTOR | Sessions assigned to the authenticated mentor |
| `mentorReviews(mentorId)` | No | Reviews for a mentor |
| `allReviews` | ADMIN | All reviews in the system |

### Mutations

| Mutation | Auth | Description |
|----------|------|-------------|
| `signup(...)` | No | Create a new USER account |
| `login(email, password)` | No | Authenticate; returns `token` + `user` |
| `changeUserToMentor(userId)` | ADMIN | Promote a USER to MENTOR |
| `createSession(mentorId, questions)` | Yes | Request a mentorship session |
| `acceptSession(sessionId)` | MENTOR | Accept a pending session |
| `declineSession(sessionId)` | MENTOR | Decline a pending session |
| `reviewMentor(mentorId, score, comment)` | Yes | Leave a review (requires accepted session) |
| `hideReview(reviewId)` | ADMIN | Hide a review from public view |

## User Roles

| Role | Description |
|------|-------------|
| `USER` | Default role after signup. Can browse mentors and request sessions. |
| `MENTOR` | Can accept/decline session requests. Promoted by an admin. |
| `ADMIN` | Full access — promote users, view all data, hide reviews. |

## Creating an Admin User

Django admin is not wired to the custom `User` model. Create an admin via the Django shell:

```bash
python manage.py shell
```

```python
from users.models import User
from django.contrib.auth.hashers import make_password

User.objects.create(
    first_name='Admin',
    last_name='User',
    email='admin@example.com',
    password=make_password('yourpassword'),
    role='ADMIN',
    bio='',
    address='',
    occupation='',
    expertise='',
)
```

## Project Structure

```
free-mentors-bn/
├── free_mentors_bn/
│   ├── settings.py
│   ├── urls.py              # /graphql endpoint
│   ├── schema.py            # Root schema (combines users + sessions)
│   └── utils/
│       └── auth.py          # create_token() / get_user_from_info()
├── users/
│   ├── models.py            # User model (roles: USER / MENTOR / ADMIN)
│   └── schema.py            # User queries + mutations
├── mentorship_sessions/
│   ├── models.py            # MentorshipSession + Review models
│   └── schema.py            # Session queries + mutations
└── requirements.txt
```

## Version Constraints

Do not upgrade these packages — the pinned versions are intentional:

| Package | Pinned version | Reason |
|---------|---------------|--------|
| Django | 3.2 | Djongo 1.3.7 is incompatible with Django 4.x SQL parameter style |
| django-cors-headers | 3.14.0 | v4+ requires Django 4.2+ |
| pymongo | 3.11.4 | Djongo 1.3.7 is incompatible with pymongo 4.x |

## Docker

Build the image:

```bash
docker build -t free-mentors-bn:latest .
```

The container runs `python manage.py runserver 0.0.0.0:8000` and exposes port 8000. Supply environment variables via `.env` or `--env-file`:

```bash
docker run --env-file .env -p 8000:8000 free-mentors-bn:latest
```

## docker-compose

Run the full stack from the repo root:

```bash
docker compose up -d
```

The backend is health-checked via a TCP connection to port 8000. The frontend container starts only after this check passes.
