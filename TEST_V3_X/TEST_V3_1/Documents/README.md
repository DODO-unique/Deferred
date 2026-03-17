# `TEST_V3_1`
**Project:** `DEFERRED`
**Codename:** `touch-engine-dock`

---

## What This Is

A flow-driven backend API. It receives tasks from a frontend, validates them, and persists them for deferred execution.

This is not a product surface. This is the spine.

---

## What Changed From 2.x

- **Users and sessions introduced.** Every request to `/tasks` requires a valid session token.
- **`uid` handshake removed.** Session token in the `Authorization` header replaces it entirely.
- **Auth pipeline added.** `/auth/register` and `/auth/login` are separate from the task pipeline.
- **Operation manager removed.** Brought back when scheduling needs it.
- **Async foundation.** DB calls are async throughout. Endpoints are `async def`.
- **Email validation moved to `master_validator`.** Fires at the endpoint via Pydantic before anything goes deeper.

---

## Endpoints

| Method | Endpoint | Auth Required | Purpose |
|--------|----------|---------------|---------|
| GET | `/home` | No | Health check / placeholder |
| POST | `/auth/register` | No | Create new user |
| POST | `/auth/login` | No | Verify user, return session token |
| POST | `/tasks` | Yes | CRUD operations |

Session token travels in the `Authorization` header:
```
Authorization: Bearer <session_token>
```

---

## System Flow

```
POST /auth/register or /auth/login
        ↓
   auth_moderator
        ↓
   common/ (username check, password hash)
        ↓
   registration.py → store user
   verification.py → compare hash → session_manager.create() → return token

────────────────────────────────────────────

POST /tasks
        ↓
   session_manager.verify(token)
        ↓ (green)
   prompt validation
        ↓
   async DB write (Touch/ORM)
        ↓
   Database
```

---

## Session Rules

- Sessions expire after **1 hour** (10 minutes in test config).
- `session_manager.verify()` checks `current_time < expires_at`. If expired — session row is killed, specific error returned.
- Sessions are created **only** through the verification (login) pipe.
- `force_kill()` triggered by logout destroys the session immediately.

---

## Database

Single Postgres instance. Three tables.

```sql
users
  id           UUID        PK
  email        TEXT        UNIQUE NOT NULL
  password_hash TEXT       NOT NULL
  created_at   TIMESTAMPTZ NOT NULL DEFAULT now()

sessions
  id           UUID        PK
  user_id      UUID        FK → users.id
  token        TEXT        UNIQUE NOT NULL
  created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
  expires_at   TIMESTAMPTZ NOT NULL

scheduled_messages
  id           UUID        PK
  user_id      UUID        FK → users.id
  prompt       TEXT        NOT NULL
  execute_at   TIMESTAMPTZ NOT NULL
  created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
  job_status   enum_status NOT NULL DEFAULT 'pending'
```

---

## File Structure

```
TEST_V3_1/
│
├── Dock/
│   └── endpoints.py              # /home, /auth/*, /tasks
│
├── Auth/
│   ├── auth_moderator/
│   │   ├── registration.py       # new user logic
│   │   └── verification.py       # login logic
│   │
│   └── common/
│       ├── username_check.py     # await DB → does user exist?
│       └── hasher.py             # password hashing + comparing
│
├── Session/
│   ├── session_manager.py        # create, verify, force_kill
│   └── session_store.py          # DB interface for sessions table
│
├── Tasks/
│   └── crud.py                   # task operations, async DB
│
├── Touch/
│   ├── ORM.py                    # async CRUD
│   ├── orm_schema.py             # table definitions
│   └── boundary_validator.py     # strict validation before DB
│
├── schema/
│   ├── schema.sql                # canonical DB schema
│   └── migrations/               # schema evolution
│
└── Utility/
    ├── pypolice/
    │   ├── master_validator.py   # ISODateTime, EmailStr, Flag, etc.
    │   └── payload_validator.py  # endpoint-level payload schemas
    ├── ErrorHandler.py           # error codes, raise to FastAPI
    └── logger.py                 # shared singleton (Hebu)
```

---

## Error Code Ranges

| Range | Layer |
|-------|-------|
| 1000s | Dock |
| 2000s | Auth |
| 3000s | ORM / DB |
| 4000s | User / Session |
| 9000s | Validators |

---

## Ambient Services

**Logger** (`Utility/logger.py`) and **Error Handler** (`Utility/ErrorHandler.py`) run parallel to the entire flow. Every layer logs. Every error propagates up to FastAPI's exception handler.

---

## What This Version Does Not Include

- EMAIL verification with OTP
- Task scheduling / execution (Celery / pg_cron — future version)
- Operation state / operation manager (returns when scheduling needs it)
- Frontend (API only)
- Refresh tokens (hard expiry only)

---

## Deployment

Railway. One FastAPI service, one Postgres instance.

---

## Version Intent

**3.1 is the identity release.**

Users exist. Sessions are real. Every task is owned by someone.

Everything after this builds on top of a system that knows who it's talking to.
