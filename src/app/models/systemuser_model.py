from datetime import datetime, timezone
from typing import  List
from common.model import Base,id_key
from sqlalchemy import DateTime,String,Boolean,Integer,Text,Boolean, DateTime,ForeignKey, Numeric, BigInteger
from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy.sql import func

class SystemUser(Base):
    __tablename__ = "kply_system_users"

    usr_id:Mapped[id_key] = mapped_column(init=False)
    usr_username = mapped_column(String(100), unique=True, nullable=False)
    usr_password_hash = mapped_column(Text, nullable=False)
    usr_email = mapped_column(String(255), unique=True, nullable=False)
    usr_full_name = mapped_column(String(255),)
    usr_rol_id = mapped_column(Integer, ForeignKey("kply_roles.rol_id"), nullable=False)
    usr_status = mapped_column(String(20), default="active")
    usr_is_deleted = mapped_column(Boolean, default=False)
    usr_created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    usr_created_by = mapped_column(Integer)
    usr_updated_at = mapped_column(DateTime(timezone=True), onupdate=func.now())
    usr_updated_by = mapped_column(Integer)

    role = relationship("Role", back_populates="users")