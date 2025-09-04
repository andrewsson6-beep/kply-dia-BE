from datetime import datetime, timezone
from typing import  List
from common.model import Base,id_key
from sqlalchemy import DateTime,String,Boolean,Integer,Text,Boolean, DateTime,ForeignKey, Numeric, BigInteger
from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy.sql import func
class Family(Base):
    __tablename__ = "kply_families"

    fam_id :Mapped[id_key] = mapped_column(init=False)
    fam_com_id = mapped_column(Integer, ForeignKey("kply_communities.com_id"), nullable=False)
    fam_unique_no = mapped_column(BigInteger, unique=True, nullable=False)
    fam_code = mapped_column(String(50), unique=True)
    fam_house_name = mapped_column(String(255), nullable=False)
    fam_head_name = mapped_column(String(255), nullable=False)
    fam_phone_number = mapped_column(String(20))
    fam_total_contribution_amount = mapped_column(Numeric(12, 2), default=0)
    fam_is_deleted = mapped_column(Boolean, default=False)
    fam_created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    fam_created_by = mapped_column(Integer, ForeignKey("kply_system_users.usr_id"))
    fam_updated_at = mapped_column(DateTime(timezone=True), onupdate=func.now())
    fam_updated_by = mapped_column(Integer, ForeignKey("kply_system_users.usr_id"))

    community = relationship("Community", back_populates="families")
    contributions = relationship("FamilyContribution", back_populates="family")