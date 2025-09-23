import asyncio
import sys
from pathlib import Path

# Ensure project 'src' is on sys.path when running from repo root
SRC = Path(__file__).resolve().parents[1]
if str(SRC) not in sys.path:
    sys.path.append(str(SRC))

from core.config import settings
from database.db import create_database_url, create_table, async_engine
from sqlalchemy.engine.url import make_url
from sqlalchemy import text

# Import all models so metadata is populated
from app.models import (
    community_model,
    familycontribution_model,
    family_model,
    forane_model,
    individualcontribution_model,
    individual_model,
    institutioncontribution_model,
    institution_model,
    parish_model,
    photo_model,
    role_model,
    systemuser_model,
)


async def main():
    url = create_database_url()
    sanitized = make_url(str(url)).set(password="***")
    print(
        f"[create_tables] Target {sanitized.username}@{sanitized.host}:{sanitized.port}/{sanitized.database}"
    )
    print(
        f"[create_tables] SSL mode: {getattr(settings, 'DATABASE_SSL_MODE', 'disable')}, "
        f"stmt_cache: {getattr(settings, 'DATABASE_STATEMENT_CACHE_SIZE', 0)}"
    )

    # Optionally ensure schema exists if configured and not public
    schema = getattr(settings, 'DATABASE_SCHEMA', None)
    if schema and schema.lower() != 'public':
        print(f"[create_tables] Ensuring schema exists: {schema}")
        try:
            async with async_engine.begin() as conn:
                await conn.run_sync(
                    lambda c: c.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{schema}"'))
                )
        except Exception as e:
            print(f"[create_tables] Warning: could not create schema '{schema}': {e}")

    print("[create_tables] Creating tables via SQLAlchemy metadata...")
    await create_table()
    print("[create_tables] Done.")


if __name__ == "__main__":
    asyncio.run(main())
