# -*- coding:utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding = "utf-8"

from sqlalchemy import Column, Integer, DateTime, String, BLOB, Index
from sqlalchemy.sql import functions

from imhm import Base
from imhm.serializer import SerializerMixin


class Groups(SerializerMixin, Base):
    # 컴퓨터들 종류에 의한 분류
    __tablename__ = "groups"
    __table_args__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8"}

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 자신이 속한 하드웨어 그룹
    # SHA1 / sha1(CPU model + Maniboard model + GPU Model)
    identifier = Column(String(64), unique=True, nullable=False)

    cpu = Column(String(256), nullable=False)
    mainboard = Column(String(256), nullable=False)
    gpu = Column(String(256), nullable=False)

    #count = Column(Integer, default=1, nullable=False)

    comment = Column(BLOB, nullable=True)

    created_at = Column(DateTime, default=functions.now(), nullable=False)
    updated_at = Column(DateTime, default=functions.now(),
                        onupdate=functions.now(), nullable=False)

    identifier_idx = Index("identifier_idx", identifier)

