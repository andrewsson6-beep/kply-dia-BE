from datetime import datetime, timezone
from typing import  List
from common.model import Base,id_key
from sqlalchemy import DateTime,String,Boolean,Integer,Text,Boolean, DateTime,ForeignKey, Numeric, BigInteger
from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy.sql import func

class Photo(Base):
    __tablename__ = "kply_photos"

    pho_id :Mapped[id_key] = mapped_column(init=False)
    pho_for_id = mapped_column(Integer, ForeignKey("kply_foranes.for_id"))
    pho_par_id = mapped_column(Integer, ForeignKey("kply_parishes.par_id"))
    pho_com_id = mapped_column(Integer, ForeignKey("kply_communities.com_id"))
    pho_fam_id = mapped_column(Integer, ForeignKey("kply_families.fam_id"))
    pho_ins_id = mapped_column(Integer, ForeignKey("kply_institutions.ins_id"))
    pho_url = mapped_column(Text, nullable=False)
    pho_caption = mapped_column(String(255))
    pho_is_primary = mapped_column(Boolean, default=False)
    pho_is_deleted = mapped_column(Boolean, default=False)
    pho_created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    pho_created_by = mapped_column(Integer, ForeignKey("kply_system_users.usr_id"))
    pho_updated_at = mapped_column(DateTime(timezone=True), onupdate=func.now())
    pho_updated_by = mapped_column(Integer, ForeignKey("kply_system_users.usr_id"))