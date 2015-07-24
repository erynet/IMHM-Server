# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding = "utf-8"

from sqlalchemy import Column, Integer, DateTime, String, Index
from sqlalchemy.sql import functions

#from sqlalchemy_fulltext import FullText, FullTextSearch
#from sqlalchemy_fulltext.modes import FullTextMode

from imhm import Base
from imhm.serializer import SerializerMixin


#class Address(SerializerMixin, FullText, Base):
class Address(SerializerMixin, Base):
	__tablename__ = "address"
	__table_args__ = {"mysql_engine":"InnoDB", "mysql_charset":"utf8"}
	#__fulltext_columns__ = ('address')
	
	id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

	address = Column(String(128), nullable=False)

	price_code = Column(String(4), nullable=False)

	created_at = Column(DateTime, default=functions.now(), nullable=False)
	updated_at = Column(DateTime, default=functions.now(),
						onupdate=functions.now(), nullable=False)
	
	# address_ft_idx = Index("address_ft_idx", mysql_using="fulltext")
	# MariaDB 5.5 는 FT 를 지원하지 않는다.
