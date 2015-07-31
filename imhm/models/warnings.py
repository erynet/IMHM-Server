# -*- coding:utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding = "utf-8"

from sqlalchemy import Column, Integer, Float, DateTime, String, BLOB, ForeignKey, Boolean, Index
from sqlalchemy.sql import functions

from imhm import Base
from imhm.serializer import SerializerMixin


class Warnings(SerializerMixin, Base):
    # 시스템에서 오는 이벤트들, ISR, DPC, Throttling
    __tablename__ = "warnings"
    __table_args__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8"}

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 자신이 속한 하드웨어
    hardware_id = Column(Integer, \
                         ForeignKey("hardwares.id", onupdate="CASCADE", ondelete="CASCADE"), \
                         nullable=False)
    event_code = Column(Integer, nullable=False)
    event_code_description = Column(String(1024), nullable=True)
    value = Column(Integer, nullable=False)

    level = Column(Integer, default=0, nullable=False)
    warned = Column(Boolean, default=False, nullable=False)
    timestamp = Column(DateTime, default=functions.now(), nullable=False)

    hardware_id_idx = Index("hardware_id_idx", hardware_id)
    hardware_id_event_code_warned_idx = \
        Index("hardware_id_smart_code_warned_idx", hardware_id, event_code, warned)