# -*- coding:utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding = "utf-8"

from sqlalchemy import Column, Integer, Float, DateTime, String, BLOB, ForeignKey, Boolean, Index
from sqlalchemy.sql import functions

from imhm import Base
from imhm.serializer import SerializerMixin


class SmartHDDWarning(SerializerMixin, Base):
    # hdd 에서 오는 smart 값들의 모음
    __tablename__ = "smart_hdd_warning"
    __table_args__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8"}

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 자신이 속한 하드웨어
    hardware_id = Column(Integer, ForeignKey("hardwares.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    smart_code = Column(Integer, nullable=False)
    smart_code_description = Column(String(1024), nullable=True)
    value = Column(Integer, nullable=False)

    warned = Column(Boolean, default=False, nullable=False)
    timestamp = Column(DateTime, default=functions.now(), nullable=False)

    hardware_id_idx = Index("hardware_id_idx", hardware_id)
    hardware_id_smart_code_warned_idx = Index("hardware_id_smart_code_warned_idx", hardware_id, smart_code, warned)