from datetime import datetime, timezone
from typing import  List
from common.model import Base,id_key
from sqlalchemy import Date, DateTime,String,Boolean,Integer,Text,Boolean, DateTime,ForeignKey, Numeric, BigInteger
from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy.sql import func

class IndividualContribution(Base):
    __tablename__ = "kply_individual_contributions"

    icon_id :Mapped[id_key] = mapped_column(init=False)
    icon_ind_id = mapped_column(Integer, ForeignKey("kply_individuals.ind_id"), nullable=False)
    icon_amount = mapped_column(Numeric(12, 2), nullable=False)
    icon_date = mapped_column(Date,nullable=True)
    icon_purpose = mapped_column(String(255))
    icon_is_deleted = mapped_column(Boolean, default=False)
    icon_created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    icon_created_by = mapped_column(Integer, ForeignKey("kply_system_users.usr_id"))
    icon_updated_at = mapped_column(DateTime(timezone=True), onupdate=func.now())
    icon_updated_by = mapped_column(Integer, ForeignKey("kply_system_users.usr_id"))

    individual = relationship("Individual", back_populates="contributions")