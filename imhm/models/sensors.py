# -*- coding:utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding = "utf-8"

from sqlalchemy import Column, Integer, DateTime, String, BLOB, ForeignKey, Index
from sqlalchemy.sql import functions

from imhm import Base
from imhm.serializer import SerializerMixin


class Sensors(SerializerMixin, Base):
    # 하드웨어마다 달려있는 센서들
    __tablename__ = "sensors"
    __table_args__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8"}

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 자신이 속한 하드웨어
    hardware_id = Column(Integer, ForeignKey("hardwares.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    # 랜덤 sha256
    fingerprint = Column(String(128), unique=True, nullable=False)

    # 하드웨어에 속한 센서들
    # 0 : Core Temperature
    # 1 : Core Voltage
    # 2 : Core Frequency
    # 3 : Core Load
    # 4 :
    # 5 :
    # 6 :
    # 7 :
    type = Column(Integer, nullabled=False)

    sensor_name = Column(String(512), nullable=False)

    created_at = Column(DateTime, default=functions.now(), nullable=False)
    updated_at = Column(DateTime, default=functions.now(),
                        onupdate=functions.now(), nullable=False)

    hardware_id_idx = Index("harware_id_idx", hardware_id)
    fingerprint_idx = Index("fingerprint_idx", fingerprint)
