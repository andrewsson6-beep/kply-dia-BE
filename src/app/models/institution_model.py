from datetime import datetime, timezone
from typing import  List
from common.model import Base,id_key
from sqlalchemy import DateTime,String,Boolean,Integer,Text,Boolean, DateTime,ForeignKey, Numeric, BigInteger
from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy.sql import func

class Institution(Base):
    __tablename__ = "kply_institutions"

    ins_id :Mapped[id_key] = mapped_column(init=False)
    # ins_for_id = mapped_column(Integer, ForeignKey("kply_foranes.for_id"), nullable=True)
    # ins_par_id = mapped_column(Integer, ForeignKey("kply_parishes.par_id"), nullable=True)
    ins_unique_no = mapped_column(BigInteger, unique=True, nullable=False)
    ins_code = mapped_column(String(50), unique=True)
    ins_name = mapped_column(String(255), nullable=False)
    ins_type = mapped_column(String(100))
    ins_address = mapped_column(Text)
    ins_total_contribution_amount = mapped_column(Numeric(12, 2), default=0)
    ins_phone = mapped_column(String(20))
    ins_email = mapped_column(String(255))
    ins_website = mapped_column(String(255))
    ins_head_name = mapped_column(String(255))
    ins_is_deleted = mapped_column(Boolean, default=False)
    ins_created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    ins_created_by = mapped_column(Integer, ForeignKey("kply_system_users.usr_id"))
    ins_updated_at = mapped_column(DateTime(timezone=True), onupdate=func.now())
    ins_updated_by = mapped_column(Integer, ForeignKey("kply_system_users.usr_id"))

    # forane = relationship("Forane", back_populates="institutions", foreign_keys=[ins_for_id],uselist=False,)
    # parish = relationship("Parish", back_populates="institutions", foreign_keys=[ins_par_id],uselist=False,)
    contributions = relationship("InstitutionContribution", back_populates="institution")