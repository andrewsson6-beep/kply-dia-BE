#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Annotated

from sqlalchemy import DateTime
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, declared_attr, mapped_column

from utils.timezone import timezone

# Common mapped primary key type annotation. Use manually in models like:
# MappedBase -> id: Mapped[id_key]
# DataClassBase or Base -> id: Mapped[id_key] = mapped_column(init=False)
id_key = Annotated[
    int, mapped_column(primary_key=True, index=True, autoincrement=True, sort_order=-999, comment='Primary Key ID')
]




class MappedBase(AsyncAttrs, DeclarativeBase):
    """
    Declarative base class used as the parent for all ORM models.

    - AsyncAttrs: Adds async ORM support.
    - DeclarativeBase: Standard SQLAlchemy base class.
    """

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """Generate table name based on class name"""
        return cls.__name__.lower()

    @declared_attr.directive
    def __table_args__(cls) -> dict:
        """Table configuration with optional comment"""
        return {'comment': cls.__doc__ or ''}


class DataClassBase(MappedAsDataclass, MappedBase):
    """
    Declarative data class base, enabling dataclass integration.
    Offers advanced configuration but be mindful when used with DeclarativeBase.
    """

    __abstract__ = True

# Currentlt DateTimeMixin is excluded from the Base(DataClassBase):
class Base(DataClassBase):
    """
    Full-featured declarative base class combining data class functionality
    and default datetime mixins.
    """

    __abstract__ = True