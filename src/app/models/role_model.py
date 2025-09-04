from datetime import datetime, timezone
from typing import  List
from common.model import Base,id_key
from sqlalchemy import DateTime,String,Boolean,Integer,Text,Boolean, DateTime,ForeignKey, Numeric, BigInteger
from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy.sql import func


class Role(Base):
    __tablename__ = "kply_roles"

    rol_id :Mapped[id_key] = mapped_column(init=False)
    rol_name = mapped_column(String(100), unique=True, nullable=False)
    rol_description = mapped_column(String(500))
    rol_is_deleted = mapped_column(Boolean, default=False)
    rol_created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    rol_created_by = mapped_column(Integer)
    rol_updated_at = mapped_column(DateTime(timezone=True), onupdate=func.now())
    rol_updated_by = mapped_column(Integer)

    users = relationship("SystemUser", back_populates="role")