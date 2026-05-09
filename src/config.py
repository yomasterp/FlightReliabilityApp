import os
from urllib.parse import quote_plus, urlparse

from dotenv import load_dotenv

load_dotenv()

AVIATIONSTACK_API_KEY = os.getenv("AVIATIONSTACK_API_KEY")
BASE_URL = os.getenv("AVIATIONSTACK_BASE_URL", "https://api.aviationstack.com/v1")

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "flight_reliability")

# Optional full URI (e.g. paste from Supabase "Connection string" → URI). Overrides DB_* when set.
_RAW_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL", "").strip()


def _normalize_sqlalchemy_database_url(url: str) -> str:
    """Use psycopg2 driver and accept Heroku/Supabase ``postgres://`` aliases."""
    u = url.strip()
    if u.startswith("postgres://"):
        rest = u[len("postgres://") :]
        return f"postgresql+psycopg2://{rest}"
    if u.startswith("postgresql://") and "+" not in u.split("://", 1)[0]:
        rest = u[len("postgresql://") :]
        return f"postgresql+psycopg2://{rest}"
    return u


def _is_local_host(host: str) -> bool:
    h = (host or "").lower().strip()
    return h in ("localhost", "127.0.0.1", "::1")


def _append_query_param(url: str, key: str, value: str) -> str:
    sep = "&" if "?" in url else "?"
    return f"{url}{sep}{key}={value}"


def _url_has_param(url: str, key: str) -> bool:
    try:
        q = urlparse(url).query
        return f"{key}=" in q or q.startswith(f"{key}=")
    except Exception:
        return False


def _build_url_from_parts() -> str:
    user = quote_plus(DB_USER)
    password = quote_plus(DB_PASSWORD)
    url = f"postgresql+psycopg2://{user}:{password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    ssl = os.getenv("DB_SSLMODE", "").strip().lower()
    if ssl:
        if not _url_has_param(url, "sslmode"):
            url = _append_query_param(url, "sslmode", ssl)
    elif not _is_local_host(DB_HOST):
        if not _url_has_param(url, "sslmode"):
            url = _append_query_param(url, "sslmode", "require")

    return url


if _RAW_DATABASE_URL:
    SQLALCHEMY_DATABASE_URL = _normalize_sqlalchemy_database_url(_RAW_DATABASE_URL)
    ssl = os.getenv("DB_SSLMODE", "").strip()
    if ssl and not _url_has_param(SQLALCHEMY_DATABASE_URL, "sslmode"):
        SQLALCHEMY_DATABASE_URL = _append_query_param(
            SQLALCHEMY_DATABASE_URL, "sslmode", ssl
        )
elif os.getenv("DATABASE_URL", "").strip():
    # Common PaaS convention (e.g. some hosts set only DATABASE_URL)
    SQLALCHEMY_DATABASE_URL = _normalize_sqlalchemy_database_url(
        os.getenv("DATABASE_URL", "").strip()
    )
    ssl = os.getenv("DB_SSLMODE", "").strip()
    if ssl and not _url_has_param(SQLALCHEMY_DATABASE_URL, "sslmode"):
        SQLALCHEMY_DATABASE_URL = _append_query_param(
            SQLALCHEMY_DATABASE_URL, "sslmode", ssl
        )
else:
    SQLALCHEMY_DATABASE_URL = _build_url_from_parts()
