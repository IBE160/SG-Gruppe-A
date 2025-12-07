# Full-Stack Web App With Next.js, FastAPI, Supabase (Remote) And Alembic

Architecture and implementation guide as a single reference.

---

## 1. High-Level Architecture

* **Frontend:** Next.js (TypeScript) in `/frontend`
* **Backend:** FastAPI (Python) in `/backend`
* **Database & Auth:** Supabase (hosted Postgres + Supabase Auth) – remote only
* **Migrations:** Alembic (running from `backend/` against Supabase Postgres)
* **Backend → DB:** `supabase-py` client using **service role key** (option 7.2)

**Data and auth flow (simplified):**

```mermaid
sequenceDiagram
    User->>Frontend: Open app
    Frontend->>Auth: Sign in request
    Auth-->>Frontend: Return JWT token
    User->>Frontend: Request data
    Frontend->>Backend: Send request with JWT
    Backend->>Auth: Verify JWT
    Auth-->>Backend: Token valid
    Backend->>Database: Query data
    Database-->>Backend: Return data
    Backend-->>Frontend: JSON response
    Frontend-->>User: Display data
```

---

## 2. Repository Structure (Option 1A)

Root layout:

```text
my-app/
  frontend/        # Next.js app (TypeScript recommended)
  backend/         # FastAPI app + Alembic migrations
  .gitignore
  README.md
```

You will:

1. Configure **Supabase** (remote project + auth).
2. Configure **backend** (FastAPI, Alembic, supabase-py).
3. Configure **frontend** (Next.js + Supabase client + calls to backend).
4. Use **Alembic** to manage Supabase schema (no manual SQL in dashboard).

---

## 3. Supabase Project Setup (Remote Only)

1. Go to `https://app.supabase.com` and create a new project.
2. Choose:

   * Region close to your users.
   * Strong DB password.
3. After project creation, note these values from **Project settings → API**:

   * `SUPABASE_URL` (Project URL), for example:

     * `https://xyzcompany.supabase.co`
   * `SUPABASE_ANON_KEY` (public anon key – frontend only).
   * `SUPABASE_SERVICE_ROLE_KEY` (secret – backend only).
4. From **Project settings → Database** get the **connection string** for Postgres.

   * Use the non-pooling `postgres://...` URL for Alembic.
5. In **Authentication → Settings**:

   * Choose sign-in methods (Email/password, etc.).
   * Set redirect URL: e.g. `http://localhost:3000` for development.

We will rely on Alembic for schema management instead of the Supabase SQL editor.

---

## 4. Backend Setup (FastAPI + Alembic + Supabase-Py)

All steps in `backend/`.

### 4.1. Create And Activate Virtual Environment

```bash
cd backend
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows (PowerShell)
# .venv\Scripts\Activate.ps1
```

### 4.2. Install Dependencies

```bash
pip install fastapi uvicorn[standard] python-dotenv python-jose[cryptography] requests
pip install alembic SQLAlchemy psycopg2-binary
pip install supabase
```

### 4.3. Minimal FastAPI App

`backend/app/main.py`:

```py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",  # Next.js dev
    # Add production frontend URL later
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok"}
```

Run dev server:

```bash
uvicorn app.main:app --reload --port 8000
```

### 4.4. Environment Variables (.env)

Create `backend/.env` (never commit this):

```env
SUPABASE_URL=https://YOUR_PROJECT_ID.supabase.co
SUPABASE_ANON_KEY=YOUR_ANON_KEY
SUPABASE_SERVICE_ROLE_KEY=YOUR_SERVICE_ROLE_KEY

# Supabase Postgres connection string (from settings → Database)
DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/postgres

# Auth/JWT configuration
SUPABASE_JWKS_URL=https://YOUR_PROJECT_ID.auth.supabase.co/.well-known/jwks.json
SUPABASE_JWT_AUDIENCE=authenticated
```

Load `.env` in your Python code using `python-dotenv` (if needed), or configure Uvicorn to load env.

---

## 5. Alembic Setup To Manage Supabase Schema

### 5.1. Initialize Alembic

From `backend/` (with venv activated):

```bash
alembic init alembic
```

This creates:

```text
backend/
  alembic.ini
  alembic/
    env.py
    script.py.mako
    versions/
```

### 5.2. Configure `alembic.ini`

In `alembic.ini`, set the sqlalchemy URL to use the `DATABASE_URL` env variable instead of a hardcoded string.

Find:

```ini
sqlalchemy.url = driver://user:pass@localhost/dbname
```

Replace with:

```ini
sqlalchemy.url = %(DATABASE_URL)s
```

This tells Alembic to read `DATABASE_URL` from the environment.

### 5.3. Define SQLAlchemy Models For Your Schema

Create `backend/app/models.py` with SQLAlchemy models that describe your tables.

Example: `auth`-linked `profiles` table.

```py
from sqlalchemy import Column, String, DateTime, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(UUID(as_uuid=True), primary_key=True)
    full_name = Column(String, nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        server_default=text("now()")
    )
```

> Note: The `id` will correspond to `auth.users.id` (UUID) in Supabase.

### 5.4. Wire Models Into Alembic `env.py`

Edit `backend/alembic/env.py` to import your `Base` and use it for autogeneration.

Basic pattern (offline and online modes condensed):

```py
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

from app.models import Base  # Import your models

# This is the Alembic Config object, which provides access to the values in alembic.ini.
config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### 5.5. Create Initial Migration

Autogenerate a migration from your models:

```bash
alembic revision --autogenerate -m "create profiles table"
```

This will create a script in `alembic/versions/xxxx_create_profiles_table.py`.

Review it and adjust if necessary (e.g. adding extensions or RLS policies if you want to manage them via SQL migrations).

Example migration (simplified):

```py
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0001_create_profiles"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "profiles",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("full_name", sa.String(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
        ),
    )


def downgrade() -> None:
    op.drop_table("profiles")
```

### 5.6. Apply Migrations To Supabase

Ensure `DATABASE_URL` is exported in your shell or loaded from `.env` when running Alembic.

Example (shell):

```bash
export DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/postgres
alembic upgrade head
```

This will create the `profiles` table directly in your **remote** Supabase Postgres instance.

**Alembic migration flow:**

```mermaid
sequenceDiagram
    Developer->>Alembic: Create revision
    Alembic-->>Developer: Migration script created
    Developer->>Alembic: Review script
    Developer->>Alembic: Run upgrade
    Alembic->>Postgres: Execute SQL
    Postgres-->>Alembic: Success
    Alembic-->>Developer: Migration complete
```

You can now keep all schema changes version-controlled via Alembic.

---

## 6. Backend: Using Supabase-Py (Option 7.2)

Now configure the backend to use `supabase-py` and JWT verification.

### 6.1. Supabase Client (Service Role)

`backend/app/supabase_client.py`:

```py
import os
from supabase import create_client

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_SERVICE_ROLE_KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]

supabase_client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
```

> Because you use the **service role key**, RLS can be bypassed. Enforce access control in your application code by always filtering queries by the authenticated user.

### 6.2. JWT Verification Dependency

`backend/app/auth.py`:

```py
import os
import requests

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt

security = HTTPBearer()

JWKS_URL = os.environ["SUPABASE_JWKS_URL"]
AUDIENCE = os.environ.get("SUPABASE_JWT_AUDIENCE", "authenticated")

_jwks_cache = None


def _get_jwks():
    global _jwks_cache
    if _jwks_cache is None:
        resp = requests.get(JWKS_URL)
        resp.raise_for_status()
        _jwks_cache = resp.json()
    return _jwks_cache


def _get_public_key(token: str):
    from jose.utils import base64url_decode
    from jose.backends.cryptography_backend import CryptographyRSAKey

    jwks = _get_jwks()
    header = jwt.get_unverified_header(token)
    kid = header.get("kid")

    for key in jwks["keys"]:
        if key["kid"] == kid:
            return CryptographyRSAKey(key)

    raise HTTPException(status_code=401, detail="Invalid token kid")


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials

    try:
        public_key = _get_public_key(token)
        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            audience=AUDIENCE,
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="User id not found in token")

    return {"id": user_id, "claims": payload}
```

### 6.3. Secure Route That Reads User Profile

`backend/app/routes.py`:

```py
from fastapi import APIRouter, Depends

from app.auth import get_current_user
from app.supabase_client import supabase_client

router = APIRouter()


@router.get("/me")
async def get_me(current_user = Depends(get_current_user)):
    user_id = current_user["id"]

    resp = (
        supabase_client
        .table("profiles")
        .select("id, full_name, created_at")
        .eq("id", user_id)
        .single()
        .execute()
    )

    return resp.data
```

Include these routes in `app.main`:

```py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import router as api_router

app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
```

**Secure call flow (frontend → backend → DB):**

```mermaid
sequenceDiagram
    User->>Frontend: Open protected page
    Frontend->>Auth: Get session
    Auth-->>Frontend: Return access token
    Frontend->>Backend: Request with Bearer token
    Backend->>Auth: Fetch JWKS
    Auth-->>Backend: Return keys
    Backend->>Backend: Validate token
    Backend->>Database: Query user profile
    Database-->>Backend: Profile data
    Backend-->>Frontend: JSON response
    Frontend-->>User: Render profile
```

---

## 7. Frontend Setup (Next.js + Supabase Auth + API Calls)

All steps in `frontend/`.

### 7.1. Initialize Next.js App

```bash
cd frontend
npx create-next-app@latest .
# Choose TypeScript: Yes
# App Router: Yes (recommended)
```

### 7.2. Install Supabase Client

```bash
npm install @supabase/supabase-js
```

### 7.3. Environment Variables

Create `frontend/.env.local`:

```env
NEXT_PUBLIC_SUPABASE_URL=https://YOUR_PROJECT_ID.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=YOUR_ANON_KEY
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

### 7.4. Supabase Client In Frontend

`frontend/lib/supabaseClient.ts`:

```ts
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;

export const supabase = createClient(supabaseUrl, supabaseAnonKey);
```

### 7.5. Simple Login Page

`frontend/app/login/page.tsx`:

```tsx
'use client';

import { useState } from 'react';
import { supabase } from '@/lib/supabaseClient';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);

  const handleSignUp = async () => {
    const { error } = await supabase.auth.signUp({ email, password });
    setError(error?.message ?? null);
  };

  const handleSignIn = async () => {
    const { error } = await supabase.auth.signInWithPassword({ email, password });
    setError(error?.message ?? null);
  };

  return (
    <div>
      <h1>Login</h1>
      <input
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        placeholder="Password"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button onClick={handleSignIn}>Sign in</button>
      <button onClick={handleSignUp}>Sign up</button>
      {error && <p>{error}</p>}
    </div>
  );
}
```

### 7.6. Call Backend With Supabase JWT

Example protected page `frontend/app/me/page.tsx`:

```tsx
'use client';

import { useEffect, useState } from 'react';
import { supabase } from '@/lib/supabaseClient';

interface Profile {
  id: string;
  full_name: string | null;
  created_at: string;
}

export default function MePage() {
  const [profile, setProfile] = useState<Profile | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProfile = async () => {
      setLoading(true);
      const { data: { session } } = await supabase.auth.getSession();

      if (!session) {
        setError('Not authenticated');
        setLoading(false);
        return;
      }

      try {
        const res = await fetch(
          `${process.env.NEXT_PUBLIC_API_BASE_URL}/me`,
          {
            headers: {
              Authorization: `Bearer ${session.access_token}`,
            },
          }
        );

        if (!res.ok) {
          throw new Error(`Backend error: ${res.status}`);
        }

        const data = await res.json();
        setProfile(data);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, []);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;
  if (!profile) return <p>No profile found.</p>;

  return (
    <div>
      <h1>My Profile</h1>
      <p>ID: {profile.id}</p>
      <p>Full Name: {profile.full_name}</p>
      <p>Created At: {new Date(profile.created_at).toLocaleString()}</p>
    </div>
  );
}
```

**Frontend auth + API flow:**

```mermaid
sequenceDiagram
    User->>Frontend: Open profile page
    Frontend->>Auth: Get session
    Auth-->>Frontend: Access token
    Frontend->>Backend: GET with auth header
    Backend-->>Frontend: Profile JSON
    Frontend-->>User: Render UI
```

---

## 8. Running The Stack In Development

1. **Start backend (FastAPI + Alembic migrations already applied):**

   ```bash
   cd backend
   source .venv/bin/activate  # or Windows equivalent
   uvicorn app.main:app --reload --port 8000
   ```
2. **Start frontend (Next.js):**

   ```bash
   cd frontend
   npm run dev -- --port 3000
   ```
3. **User flow in dev:**

   * Go to `http://localhost:3000/login` to sign up or sign in.
   * Navigate to `/me` to trigger a call to FastAPI.
   * FastAPI verifies the JWT and uses `supabase-py` + service role key to fetch data from the `profiles` table.

---

## 9. Summary Of What You Have Achieved

* **Monorepo (Option 1A)** with clear separation: `/frontend` (Next.js) and `/backend` (FastAPI).
* **Supabase (remote):** Used for both authentication and Postgres database; no local DB.
* **Alembic-managed schema:** All tables (e.g. `profiles`) are created and evolved by Alembic migrations against Supabase.
* **Backend (FastAPI):**

  * Verifies Supabase JWTs via JWKS.
  * Uses `supabase-py` with the **service role key** to query Supabase DB (Option 7.2).
* **Frontend (Next.js):**

  * Uses `@supabase/supabase-js` for auth and session management.
  * Sends the Supabase access token as `Authorization: Bearer <token>` to FastAPI.
* **Mermaid sequence diagrams** document the key flows:

  * Auth and data retrieval (`User → Next.js → Supabase Auth → FastAPI → Supabase DB`).
  * Alembic migration lifecycle (`Developer → Alembic → Supabase Postgres`).

From here you can extend:

* More tables and relationships via Alembic.
* More API routes in FastAPI.
* Better UI and routing in Next.js (layout, protected routes, etc.).
* Deployment to Vercel (frontend) and a cloud provider (backend) while keeping Supabase as the central remote backend for auth and data.
