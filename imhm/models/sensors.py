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
    # 2 : Core Frequency    /   value
    # 3 : Core FanRPM       /   value
    # 4 : Core PowerConsume /   value
    # 5 : System DPC        /   parameter
    # 6 : SMART,5,Reallocated Sector    /   parameter
    # 7 : SMART,9,Power-On Hours        /   parameter
    # 8 : SMART,187,Reported Uncorrectable Errors   /   parameter
    # 9 : SMART,190,Airflow Temperature    /   parameter
    # 10 : SMART,191,Mechanical Shock       /   parameter
    # 11 : SMART,194,Temperature        /   parameter
    # 12 : SMART,196,Reallocation Event Count   /   parameter
    # 13 : SMART,197,Current Pending Sector Count   /   parameter
    # 14 : SMART,198,Uncorrectable Sector Count     /   parameter
    # 15 : SMART,199,UltraDMA CRC Error Count       /   parameter
    # 16 : SMART,201,Soft Read Error Rate           /   parameter
    # 17 : SMART,231,Temperature        /   parameter
    type = Column(Integer, nullable=False)

    sensor_name = Column(String(512), nullable=False)

    created_at = Column(DateTime, default=functions.now(), nullable=False)
    updated_at = Column(DateTime, default=functions.now(),
                        onupdate=functions.now(), nullable=False)

    hardware_id_idx = Index("harware_id_idx", hardware_id)
