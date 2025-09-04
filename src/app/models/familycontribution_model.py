from datetime import datetime, timezone
from typing import  List
from common.model import Base,id_key
from sqlalchemy import DateTime,String,Boolean,Integer,Text,Boolean, DateTime,ForeignKey, Numeric, BigInteger
from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy.sql import func
class FamilyContribution(Base):
    __tablename__ = "kply_family_contributions"

    fcon_id :Mapped[id_key] = mapped_column(init=False)
    fcon_fam_id = mapped_column(Integer, ForeignKey("kply_families.fam_id"), nullable=False)
    fcon_amount = mapped_column(Numeric(12, 2), nullable=False)
    fcon_date = mapped_column(DateTime(timezone=True), server_default=func.now())
    fcon_purpose = mapped_column(String(255))
    fcon_is_deleted = mapped_column(Boolean, default=False)
    fcon_created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    fcon_created_by = mapped_column(Integer, ForeignKey("kply_system_users.usr_id"))
    fcon_updated_at = mapped_column(DateTime(timezone=True), onupdate=func.now())
    fcon_updated_by = mapped_column(Integer, ForeignKey("kply_system_users.usr_id"))

    family = relationship("Family", back_populates="contributions")