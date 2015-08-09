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
    #fingerprint = Column(String(128), unique=True, nullable=False)

    # 하드웨어에 속한 센서들
    # 0 : Core Load         /   value
    # 1 : Core Temperature  /   value
    # 2 : Core Power        /   value
    # 3 : Core FanRPM       /   value
    # 4 : Core TempPerLoad  /   regression
    # 5 : Core PowerPerLoad /   regression
    # 6 : Core FanRPMPerLoad/   regression
    # 7 : System DPC        /   parameter
    # 8 : System Throttling /   parameter
    # 9 : SSD/HHD Smart     /   Smart
    type = Column(Integer, nullable=False)

    sensor_name = Column(String(512), nullable=False)

    processed_at = Column(DateTime, default=functions.now(), nullable=False)
    created_at = Column(DateTime, default=functions.now(), nullable=False)
    updated_at = Column(DateTime, default=functions.now(),
                        onupdate=functions.now(), nullable=False)

    hardware_id_idx = Index("hardware_id_idx", hardware_id)
    processed_at_idx = Index("processed_at_idx", processed_at)
