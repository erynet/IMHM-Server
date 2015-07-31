# -*- coding:utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding = "utf-8"

from sqlalchemy import Column, Integer, DateTime, String, BLOB, ForeignKey, Index
from sqlalchemy.sql import functions

from imhm import Base
from imhm.serializer import SerializerMixin


class Elements(SerializerMixin, Base):
    # 각각의 컴퓨터 개체
    __tablename__ = "elements"
    __table_args__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8"}

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 자신이 속한 하드웨어 그룹
    group_id = Column(Integer, ForeignKey("groups.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    # 랜덤 md5
    fingerprint = Column(String(64), unique=True, nullable=False)

    machine_name = Column(String(256),  nullable=False)
    ip_address_local = Column(String(64), nullable=False)
    ip_address_global = Column(String(64), nullable=False)
    #os = Column(String(512), nullable=False)

    # 컴퓨터가 커져서 로그인 할 시에 GetReport 로 만들어서 기록한다.
    report = Column(BLOB, nullable=True)
    comment = Column(BLOB, nullable=True)

    created_at = Column(DateTime, default=functions.now(), nullable=False)
    updated_at = Column(DateTime, default=functions.now(),
                        onupdate=functions.now(), nullable=False)

    fingerprint_idx = Index("fingerprint_idx", fingerprint)
    group_id_machine_name_idx = Index("group_id_machine_name_idx", group_id, machine_name)
