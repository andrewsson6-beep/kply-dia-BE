#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from typing import Annotated, AsyncGenerator
from uuid import uuid4
from fastapi import Depends
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from common.model import MappedBase
from core.config import settings
def create_database_url(unittest: bool = False) -> URL:
    """
    Create a database connection URL.

    :param unittest: Indicates if the URL is for unit testing.
    :return: SQLAlchemy-compatible URL object.
    """

    url = URL.create(
       drivername='mysql+asyncmy' if settings.DATABASE_TYPE == 'mysql' else 'postgresql+asyncpg',
        username=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT,
        database=settings.DATABASE_SCHEMA if not unittest else f'{settings.DATABASE_SCHEMA}_test',
    )
    if settings.DATABASE_TYPE == 'mysql':
        url.update_query_dict({'charset': settings.DATABASE_CHARSET})
    return url


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
        )
    except Exception as e:
        print("❌Database connection failed: {}",e)
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