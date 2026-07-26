# Bayong — Grocery Price Comparison API

A FastAPI + PostgreSQL backend for comparing grocery prices across stores, built with a layered,
class-based (OOP) architecture.

## Architecture

```
app/
  core/           Cross-cutting building blocks
    config.py         Settings (DATABASE_URL, SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES via pydantic-settings)
    database.py       SQLAlchemy engine, session factory, get_db() FastAPI dependency
    security.py       Password hashing (bcrypt) and JWT encode/decode (PyJWT)
    base_repository.py  Generic BaseRepository[ModelT] with shared CRUD (get/list/create/update/delete)
    dependencies.py   FastAPI Depends() providers wiring db -> repository -> service, plus
                      get_current_user / require_admin auth dependencies
    exceptions.py     NotFoundError, InvalidCredentialsError — translated to HTTP 404/401 in routers

  models/         SQLAlchemy ORM classes (one per table) + models/enums.py for SizeUnit/PriceSource/UserRole
    Relationships (Product.prices, Store.prices, Product.images, Product.price_history, ...) are
    declared on the models. Model-level helper methods that belong on the entity itself also live
    here, e.g. Product.price_per_unit(price) and Price.effective_price().

  repositories/   One class per entity (CategoryRepository, StoreRepository, ProductRepository,
    PriceRepository, PriceHistoryRepository, ProductImageRepository, UserRepository), each
    subclassing BaseRepository and adding entity-specific queries (e.g.
    ProductRepository.get_cheapest_price, ProductRepository.list_with_filters,
    PriceRepository.list_by_product, UserRepository.get_by_username). Routers and services never
    touch the SQLAlchemy Session directly — only through repositories.

  services/       Business logic on top of repositories. Calculated/derived logic lives here, not
    in routes or models:
      - PriceComparisonService: get_prices_for_product, get_cheapest_across_stores,
        calculate_price_per_unit, get_price_history (accounts for active promos via
        Price.effective_price(), not just the raw stored price)
      - PriceService: create/update/delete prices; updating the `price` field automatically writes
        a PriceHistory row (old_price -> new_price)
      - ProductService, StoreService, CategoryService: thin CRUD + filtering wrappers
      - UserService: creates users with hashed passwords
      - AuthService: authenticates username/password and issues JWTs

  schemas/        Pydantic request/response models, separate from the ORM models
    (ProductCreate/Update/Read, PriceCreate/Update/Read, CheapestPriceRead, Token, etc.)
    validators.py defines NonPlaceholderStr, a reusable type rejecting FastAPI/Swagger's
    auto-generated example text (e.g. "string") on free-text fields.

  routers/        FastAPI routers per resource (auth, categories, stores, products, prices). Each
    router only calls into its service layer and translates NotFoundError -> HTTP 404. Write
    endpoints (POST/PATCH/DELETE) additionally depend on require_admin — see Authorization below.

  main.py         FastAPI app instance, router registration, /health endpoint

alembic/          Migrations (env.py loads DATABASE_URL from app.core.config and app.models.Base.metadata)
seed/             Seeder class (seed/seeder.py, also creates the default admin user) + seed/seed.py
                  CLI entrypoint
conftest.py       Root pytest fixtures: db_session (isolated in-memory SQLite), client (TestClient
                  wired to db_session via dependency override), admin_user/auth_headers (a seeded
                  admin + ready-to-use Bearer token for testing protected write endpoints)
```

## Authorization

Write endpoints (`POST`/`PATCH`/`DELETE` on every resource) require a valid JWT for a user with the
`admin` role, obtained via `POST /auth/login`. All `GET` endpoints stay public/unauthenticated,
since this is a price-comparison app meant for public reads.

There's no public self-registration endpoint — the only way to get an admin account today is the
one the `Seeder` creates (see Setup below). This is a deliberate v1 scope: a single `admin` role
gates all writes, rather than modeling finer-grained roles (e.g. a `contributor` role limited to
submitting prices) — straightforward to add later if needed.

```bash
# Get a token
curl -X POST http://127.0.0.1:8000/auth/login -d "username=admin&password=ChangeMe123!"
# -> {"access_token": "...", "token_type": "bearer"}

# Use it on a write endpoint
curl -X POST http://127.0.0.1:8000/categories \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"category_name": "Frozen Foods"}'
```

In Swagger UI (`/docs`), use the padlock "Authorize" button and log in with the seeded admin
credentials — it will attach the Bearer token to subsequent requests automatically.

### Why SQLite for tests but Postgres in production

`Product.tags` is declared as `JSONB().with_variant(SQLiteJSON(), "sqlite")` and enum columns use
SQLAlchemy's cross-dialect `Enum` type, so the exact same model classes run against an in-memory
SQLite database in tests and against real PostgreSQL in dev/prod — no test-only model duplication.

## Testing

Every source file has a matching `<same_filename>_test.py` next to it (not a separate mirrored
`tests/` tree), e.g.:

- `app/repositories/product_repository.py` -> `app/repositories/product_repository_test.py`
- `app/services/price_comparison_service.py` -> `app/services/price_comparison_service_test.py`
- `app/routers/products.py` -> `app/routers/products_test.py`

Repository, service, and router tests run against an isolated **in-memory SQLite** database (see
`conftest.py`'s `db_session`/`client` fixtures) — they never touch real data, and each test gets a
fresh schema. Coverage includes, at minimum:

- CRUD success paths for every entity
- Not-found cases (404 at the router layer, `NotFoundError` at the service/repository layer)
- Price-comparison logic: cheapest price across stores (including promo/sale-price handling via
  `Price.effective_price()`), price-per-unit calculation, and price-history logging on updates
- Auth: password hashing/verification, JWT issuance/expiry/tamper rejection, login success/failure,
  and that write endpoints reject missing/invalid/non-admin tokens (`core/security_test.py`,
  `core/dependencies_test.py`, `services/auth_service_test.py`, `routers/auth_test.py`)
- Placeholder-value rejection: Swagger's auto-filled `"string"` example text is rejected on every
  free-text field (`schemas/validators_test.py` and per-schema tests)
- `Seeder` correctness and idempotency, including the seeded admin user (`seed/seeder_test.py`)

Run the whole suite:

```bash
pip install -r requirements-dev.txt
pytest
```

(150 tests, all passing against SQLite — no database server required.)

## Setup

### 1. Start PostgreSQL

```bash
docker-compose up -d
```

This starts Postgres 17 on `localhost:5432` with database `bayong`, user `bayong`, password
`bayong_dev_pw` (see `docker-compose.yml`). If you already run Postgres locally instead of Docker,
create a matching database/role yourself and skip this step.

### 2. Configure environment

```bash
cp .env.example .env
```

`.env` / `.env.example` hold `DATABASE_URL`, `SECRET_KEY` (JWT signing key — generate your own, e.g.
`python -c "import secrets; print(secrets.token_hex(32))"`), and `ACCESS_TOKEN_EXPIRE_MINUTES`:

```
DATABASE_URL=postgresql+psycopg2://bayong:bayong_dev_pw@localhost:5432/bayong
SECRET_KEY=change-me-to-a-long-random-string
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 3. Install dependencies

```bash
python -m venv .venv
.venv/Scripts/activate      # Windows
# source .venv/bin/activate # macOS/Linux
pip install -r requirements-dev.txt
```

### 4. Run migrations

```bash
alembic upgrade head
```

### 5. Seed sample data

```bash
python -m seed.seed
```

Loads 3 categories, 4 stores, and 10 products (Beverages/Snacks/Household) with 3-4 prices each
across stores, including some active promos — plus a default admin user (username `admin`,
password `ChangeMe123!`). Both are printed to the console; rotate the password before any real
deployment.

### 6. Run the API

```bash
uvicorn app.main:app --reload
```

Visit `http://127.0.0.1:8000/docs` for interactive Swagger docs.

## API Endpoints

- `POST /auth/login` — form-encoded `username`/`password`, returns a Bearer JWT

Full CRUD (`GET`/`POST /`, `GET`/`PATCH`/`DELETE /{id}`) for:

- `/categories`
- `/stores`
- `/products` — supports `?category=`, `?brand=`, and arbitrary tag filters via query params that
  match keys in `Product.tags`, e.g. `?vegan=true&gluten_free=false`
- `/prices`

`POST`/`PATCH`/`DELETE` on all four resources require an admin Bearer token (see Authorization).
`GET` endpoints are public.

Plus:

- `GET /products/{id}/prices` — all current prices for a product across stores, cheapest first
  (accounting for active promo/sale prices)
- `GET /products/{id}/cheapest` — cheapest current price + the store it's at
- `GET /health` — liveness check

Price-per-unit is always computed on the fly via `PriceComparisonService.calculate_price_per_unit()`
/ `Product.price_per_unit()` — it is never stored.

## Verified end-to-end

Migrations, seed data, and endpoints have all been exercised against a real local PostgreSQL 17
instance (not just the SQLite test suite): `alembic upgrade head` applied cleanly, `python -m
seed.seed` populated 10 products / 4 stores / 3 categories / 38 prices / 1 admin user, and manual
requests against a running `uvicorn` server confirmed tag filtering (`?vegan=true`),
cheapest-price-with-promo logic, and price-history logging on `PATCH /prices/{id}`.

Authorization was verified the same way: an unauthenticated `POST /categories` returns 401, a
login with the wrong password returns 401, `POST /auth/login` with the seeded admin credentials
returns a working JWT, and that token successfully authorizes a write that a plain `GET` never
required in the first place.
