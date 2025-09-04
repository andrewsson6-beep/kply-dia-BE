from datetime import datetime, timezone
from typing import  List
from common.model import Base,id_key
from sqlalchemy import DateTime,String,Boolean,Integer,Text,Boolean, DateTime,ForeignKey, Numeric, BigInteger
from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy.sql import func


class Community(Base):
    __tablename__ = "kply_communities"

    com_id :Mapped[id_key] = mapped_column(init=False)
    com_for_id = mapped_column(Integer, ForeignKey("kply_foranes.for_id"), nullable=True)
    com_par_id = mapped_column(Integer, ForeignKey("kply_parishes.par_id"), nullable=True)
    com_unique_no = mapped_column(BigInteger, unique=True, nullable=False)
    com_code = mapped_column(String(50), unique=True)
    com_name = mapped_column(String(255), nullable=False)
    com_total_contribution_amount = mapped_column(Numeric(12, 2), default=0)
    com_is_deleted = mapped_column(Boolean, default=False)
    com_created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    com_created_by = mapped_column(Integer, ForeignKey("kply_system_users.usr_id"))
    com_updated_at = mapped_column(DateTime(timezone=True), onupdate=func.now())
    com_updated_by = mapped_column(Integer, ForeignKey("kply_system_users.usr_id"))

    forane = relationship("Forane", back_populates="communities")
    parish = relationship("Parish", back_populates="communities")
    families = relationship("Family", back_populates="community")