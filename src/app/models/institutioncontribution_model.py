from datetime import datetime, timezone
from typing import  List
from common.model import Base,id_key
from sqlalchemy import DateTime,String,Boolean,Integer,Text,Boolean, DateTime,ForeignKey, Numeric, BigInteger
from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy.sql import func
class InstitutionContribution(Base):
    __tablename__ = "kply_institution_contributions"

    incon_id :Mapped[id_key] = mapped_column(init=False)
    incon_ins_id = mapped_column(Integer, ForeignKey("kply_institutions.ins_id"), nullable=False)
    incon_amount = mapped_column(Numeric(12, 2), nullable=False)
    incon_date = mapped_column(DateTime(timezone=True), server_default=func.now())
    incon_purpose = mapped_column(String(255))
    incon_is_deleted = mapped_column(Boolean, default=False)
    incon_created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    incon_created_by = mapped_column(Integer, ForeignKey("kply_system_users.usr_id"))
    incon_updated_at = mapped_column(DateTime(timezone=True), onupdate=func.now())
    incon_updated_by = mapped_column(Integer, ForeignKey("kply_system_users.usr_id"))

    institution = relationship("Institution", back_populates="contributions")