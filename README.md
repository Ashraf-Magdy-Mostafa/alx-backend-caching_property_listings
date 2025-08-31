# ALX Backend Caching: Property Listings

## Quick Start

```bash
# 1) Start PostgreSQL and Redis
docker compose -f docker-compose.yml up -d

# 2) Create virtual env and install deps (optional but recommended)
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt

# 3) Run migrations and create a superuser
python manage.py migrate
python manage.py createsuperuser

# 4) Run the dev server
python manage.py runserver 0.0.0.0:8000
```

- Properties API: `GET /properties/`
- Admin: `/admin/`

### Notes
- View-level cache: 15 minutes on `/properties/`
- Low-level cache: Redis key `all_properties` (TTL: 3600s)
- Signals: automatic invalidation on create/update/delete `Property`
- Metrics: call `properties.utils.get_redis_cache_metrics()` from shell or wire it to a view if needed.
