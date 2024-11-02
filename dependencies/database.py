from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.ext.asyncio import AsyncSession

import logging
import os
from typing import Any, Dict, Generator
from fastapi.responses import JSONResponse
from fastapi import Depends, HTTPException, status

from .config import settings


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, pool_pre_ping=True, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

async def get_async_session() -> Generator[AsyncSession, Any, None]:
    async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
    async_session = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=async_engine,
        class_=AsyncSession,
    )
    async with async_session() as session:
        yield session

async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            session.close()