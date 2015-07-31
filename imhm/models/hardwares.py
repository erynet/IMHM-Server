# -*- coding:utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding = "utf-8"

from sqlalchemy import Column, Integer, DateTime, String, BLOB, ForeignKey, Index
from sqlalchemy.sql import functions

from imhm import Base
from imhm.serializer import SerializerMixin


class Hardwares(SerializerMixin, Base):
    # 개벌 컴퓨터(Element) 에 달려있는 하드웨어들의 일람
    __tablename__ = "hardwares"
    __table_args__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8"}

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 자신이 속한 컴퓨터
    element_id = Column(Integer, ForeignKey("elements.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    # 랜덤 sha1
    fingerprint = Column(String(64), unique=True, nullable=False)

    # 컴퓨터에 속한 하드웨어들
    # 0 : CPU
    # 1 : Mainboard
    # 2 : Nvidia GPU
    # 3 : AMD GPU
    # 4 : HDD
    # 5 : SSD
    # 6 : System
    type = Column(Integer, nullable=False)
    hardware_name = Column(String(512), nullable=False)

    created_at = Column(DateTime, default=functions.now(), nullable=False)
    updated_at = Column(DateTime, default=functions.now(),
                        onupdate=functions.now(), nullable=False)

    element_id_idx = Index("element_id_idx", element_id)
    #fingerprint_idx = Index("fingerprint_idx", fingerprint)
