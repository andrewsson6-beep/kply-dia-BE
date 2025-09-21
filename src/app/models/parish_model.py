from datetime import datetime, timezone
from typing import  List
from common.model import Base,id_key
from sqlalchemy import DateTime,String,Boolean,Integer,Text,Boolean, DateTime,ForeignKey, Numeric, BigInteger
from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy.sql import func
class Parish(Base):
    __tablename__ = "kply_parishes"

    par_id :Mapped[id_key] = mapped_column(init=False)
    par_for_id = mapped_column(Integer, ForeignKey("kply_foranes.for_id"), nullable=False)
    par_unique_no = mapped_column(BigInteger, unique=True, nullable=False)
    par_code = mapped_column(String(50), unique=True)
    par_name = mapped_column(String(255), nullable=False)
    par_location = mapped_column(String(255))
    par_vicar_name = mapped_column(String(255))
    par_total_contribution_amount = mapped_column(Numeric(12, 2), default=0)
    par_is_deleted = mapped_column(Boolean, default=False)
    par_created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    par_created_by = mapped_column(Integer, ForeignKey("kply_system_users.usr_id"))
    par_updated_at = mapped_column(DateTime(timezone=True), onupdate=func.now())
    par_updated_by = mapped_column(Integer, ForeignKey("kply_system_users.usr_id"))

    forane = relationship("Forane", back_populates="parishes")
    communities = relationship("Community", back_populates="parish")
    # institutions = relationship("Institution", back_populates="parish")