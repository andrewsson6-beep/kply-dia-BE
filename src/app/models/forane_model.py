from datetime import datetime, timezone
from typing import  List
from common.model import Base,id_key
from sqlalchemy import DateTime,String,Boolean,Integer,Text,Boolean, DateTime,ForeignKey, Numeric, BigInteger
from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy.sql import func

class Forane(Base):
    __tablename__ = "kply_foranes"

    for_id :Mapped[id_key] = mapped_column(init=False)
    for_unique_no = mapped_column(BigInteger, unique=True, nullable=False)
    for_code = mapped_column(String(50), unique=True)
    for_name = mapped_column(String(255), nullable=False) # Forane Church Name
    for_location = mapped_column(String(255))
    for_vicar_name = mapped_column(String(255))
    for_total_contribution_amount = mapped_column(Numeric(12, 2), default=0)
    for_contact_number=mapped_column(String(255))
    for_is_deleted = mapped_column(Boolean, default=False)
    for_created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    for_created_by = mapped_column(Integer, ForeignKey("kply_system_users.usr_id"))
    for_updated_at = mapped_column(DateTime(timezone=True), onupdate=func.now())
    for_updated_by = mapped_column(Integer, ForeignKey("kply_system_users.usr_id"))

    parishes = relationship("Parish", back_populates="forane")
    communities = relationship("Community", back_populates="forane")
    institutions = relationship("Institution", back_populates="forane")