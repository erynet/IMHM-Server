# -*- coding:utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding = "utf-8"

from sqlalchemy import Column, Integer, DateTime, String, Index, ForeignKey
from sqlalchemy.sql import functions

from imhm import Base
from imhm.serializer import SerializerMixin


# 모든 레포트는 여기서 번호를 따고 나서야 접근된다.
class ReportSession(SerializerMixin, Base):
    __tablename__ = "report_session"
    __table_args__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8"}

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 각 컴퓨터의 element_id(sha1)
    element_id = Column(Integer,
                        ForeignKey("elements.id", onupdate="CASCADE", ondelete="CASCADE"),
                        nullable=False)

    notify_level = Column(Integer, default=0, nullable=False)

    created_at = Column(DateTime, default=functions.now(), nullable=False)

    element_id_created_at_idx = Index("element_id_created_at_idx", element_id, created_at)
