from datetime import datetime, timezone
from typing import  List
from common.model import Base,id_key
from sqlalchemy import DateTime,String,Boolean,Integer,Text,Boolean, DateTime,ForeignKey, Numeric, BigInteger
from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy.sql import func

class Individual(Base):
    __tablename__ = "kply_individuals"

    ind_id :Mapped[id_key] = mapped_column(init=False)
    ind_unique_no = mapped_column(BigInteger, unique=True, nullable=False)
    ind_code = mapped_column(String(50), unique=True)
    ind_full_name = mapped_column(String(255), nullable=False)
    ind_phone_number = mapped_column(String(20))
    ind_email = mapped_column(String(255))
    ind_address = mapped_column(Text)
    ind_total_contribution_amount = mapped_column(Numeric(12, 2), default=0)
    ind_is_deleted = mapped_column(Boolean, default=False)
    ind_created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    ind_created_by = mapped_column(Integer, ForeignKey("kply_system_users.usr_id"))
    ind_updated_at = mapped_column(DateTime(timezone=True), onupdate=func.now())
    ind_updated_by = mapped_column(Integer, ForeignKey("kply_system_users.usr_id"))

    contributions = relationship("IndividualContribution", back_populates="individual")