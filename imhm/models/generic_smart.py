# -*- coding:utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding = "utf-8"

from sqlalchemy import Column, Integer, Float, DateTime, String, BLOB, ForeignKey, Index
from sqlalchemy.sql import functions

from imhm import Base
from imhm.serializer import SerializerMixin


class GenericSmart(SerializerMixin, Base):
    # 센서에서 오는 정보중 정수값에 해당하는 것
    __tablename__ = "generic_smart"
    __table_args__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8"}

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 자신이 속한 센서
    sensor_id = Column(Integer, ForeignKey("sensors.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    rss_id = Column(Integer, ForeignKey("report_session.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)

    code = Column(Integer, nullable=False)
    description = Column(String(64), nullable=True)
    threshold = Column(Integer, nullable=False)
    physical = Column(Integer, nullable=False)

    timestamp = Column(DateTime, default=functions.now(), nullable=False)

    sensor_id_rss_id_idx = Index("sensor_id_rss_id_idx", sensor_id, rss_id)
    rss_id_sensor_id_idx = Index("rss_id_sensor_id_idx", rss_id, sensor_id)