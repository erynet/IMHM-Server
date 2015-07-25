# -*- coding:utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding = "utf-8"

from sqlalchemy import Column, Integer, DateTime, String, Index
from sqlalchemy.sql import functions

from imhm import Base
from imhm.serializer import SerializerMixin


class Admin(SerializerMixin, Base):
    __tablename__ = "admin"
    __table_args__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8"}

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    name = Column(String(128), nullable=False)
    uuid = Column(String(256), nullable=False)
    email = Column(String(256), nullable=False)

    # 경고 레벨
    # 0 : INFO 이상 모두 수신
    # 1 : WARNING 이상 모두 수신
    # 2 : ALERT 만 수신
    notify_level = Column(Integer, default=0, nullable=False)

    created_at = Column(DateTime, default=functions.now(), nullable=False)
    updated_at = Column(DateTime, default=functions.now(),
                        onupdate=functions.now(), nullable=False)

    notify_level_uuid_idx = Index("notify_level_uuid_idx", notify_level, uuid)
