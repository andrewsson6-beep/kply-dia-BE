#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import ssl
from pathlib import Path
from typing import Annotated, AsyncGenerator
from uuid import uuid4
from fastapi import Depends
from sqlalchemy import URL, make_url
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from common.model import MappedBase
from core.config import settings
try:
    import certifi
except Exception:  # certifi is in requirements
    certifi = None
def create_database_url(unittest: bool = False) -> URL:
    """
    Create a database connection URL.

    :param unittest: Indicates if the URL is for unit testing.
    :return: SQLAlchemy-compatible URL object.
    """
    # If DATABASE_URL is provided in .env, use it directly
    if settings.DATABASE_URL:
        # Use make_url() to parse a complete URL string
        base_url = make_url(settings.DATABASE_URL)
        
        # Ensure we're using the async driver
        if base_url.drivername == 'postgresql':
            base_url = base_url.set(drivername='postgresql+asyncpg')
        elif base_url.drivername == 'mysql':
            base_url = base_url.set(drivername='mysql+asyncmy')
        
        # For unit tests, modify the database name to append '_test'
        if unittest:
            # Extract the database name and append '_test'
            original_db = base_url.database or settings.DATABASE_NAME
            test_db = f'{original_db}_test'
            # Create a new URL with the test database name
            return base_url.set(database=test_db)
        
        return base_url
    
    # Fallback to individual database parameters
    url = URL.create(
       drivername='mysql+asyncmy' if settings.DATABASE_TYPE == 'mysql' else 'postgresql+asyncpg',
        username=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT,
        database=settings.DATABASE_NAME if not unittest else f'{settings.DATABASE_NAME}_test',
    )
    if settings.DATABASE_TYPE == 'mysql':
        url.update_query_dict({'charset': settings.DATABASE_CHARSET})
    return url


def _build_ssl_context() -> ssl.SSLContext | None:
    """
    Build an SSL context according to settings.DATABASE_SSL_MODE and optional CA file.

    Returns None when SSL is disabled. For PostgreSQL providers like Supabase, SSL is usually required.
    """
    mode = getattr(settings, 'DATABASE_SSL_MODE', 'verify-full')
    if mode == 'disable':
        return None
    cafile = settings.DATABASE_SSL_CERT_FILE
    # Prefer OS trust store by default; allow overriding with a provided CA bundle
    if cafile:
        ctx = ssl.create_default_context(cafile=cafile)
    else:
        ctx = ssl.create_default_context()
    if mode == 'require':
        # Don't verify cert/hostname (encryption only)
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
    elif mode == 'verify-ca':
        # Verify CA but not hostname
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_REQUIRED
    else:
        # verify-full (default): verify CA and hostname
        ctx.check_hostname = True
        ctx.verify_mode = ssl.CERT_REQUIRED
    return ctx


def get_connect_args() -> dict:
    """Return connect_args for SQLAlchemy create_async_engine based on SSL settings."""
    if settings.DATABASE_TYPE == 'mysql':
        return {}
    args: dict = {
        'statement_cache_size': getattr(settings, 'DATABASE_STATEMENT_CACHE_SIZE', 0),
        # asyncpg 0.29+ supports prepared_statement_cache_size to avoid server-side prepared statements
        'prepared_statement_cache_size': 0,
    }
    if getattr(settings, 'DATABASE_SSL_MODE', 'disable') == 'disable':
        return args
    ssl_ctx = _build_ssl_context()
    if ssl_ctx is not None:
        args['ssl'] = ssl_ctx
    return args

def create_async_engine_and_session(url: str | URL) -> tuple[AsyncEngine, async_sessionmaker[AsyncSession]]:
    """
    Create an asynchronous SQLAlchemy engine and session factory.

    :param url: The database connection URL.
    :return: A tuple containing the engine and sessionmaker.
    """
    try:

        engine = create_async_engine(
            url,
            echo=settings.DATABASE_ECHO,
            echo_pool=settings.DATABASE_POOL_ECHO,
            future=True,
            # Moderate concurrency settings
            pool_size=10,  
            max_overflow=20, 
            pool_timeout=30,  
            pool_recycle=3600,  
            pool_pre_ping=True,  
            pool_use_lifo=False,  
            connect_args=get_connect_args(),
        )
    except Exception as e:
        print(f"❌Database connection failed: {e}")
        # log.error('❌ Database connection failed: {}', e)
        sys.exit()
    else:
        db_session = async_sessionmaker(
            bind=engine,
            class_=AsyncSession,
            autoflush=False,   # Disable auto flush
            expire_on_commit=False,   # Prevent expiration on commit
        )
        return engine, db_session


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides a database session generator for request lifecycle.

    :yield: An asynchronous SQLAlchemy session.
    """
    async with async_db_session() as session:
        yield session


async def create_table() -> None:
    """
    Create all database tables defined in SQLAlchemy models.
    """
    async with async_engine.begin() as coon:
        await coon.run_sync(MappedBase.metadata.create_all)


def uuid4_str() -> str:
    """
    Generate a UUID string (compatible with database UUID column types).
    
    :return: UUID string.
    """
    return str(uuid4())


SQLALCHEMY_DATABASE_URL = create_database_url()
async_engine, async_db_session = create_async_engine_and_session(SQLALCHEMY_DATABASE_URL)
# Session Annotated
CurrentSession = Annotated[AsyncSession, Depends(get_db)]