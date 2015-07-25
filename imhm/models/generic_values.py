# -*- coding:utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding = "utf-8"

from sqlalchemy import Column, Integer, Float, DateTime, String, BLOB, ForeignKey, Index
from sqlalchemy.sql import functions

from imhm import Base
from imhm.serializer import SerializerMixin


class GenericValues(SerializerMixin, Base):
    # 센서에서 오는 정보중 실수값에 해당하는 것
    __tablename__ = "generic_values"
    __table_args__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8"}

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 자신이 속한 센서
    sensor_id = Column(Integer, ForeignKey("sensors.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    value = Column(Float, nullable=False)

    timestamp = Column(DateTime, default=functions.now(), nullable=False)

    sensor_id_idx = Index("sensor_id_idx", sensor_id)