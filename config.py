# -*- coding:utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "3177eafc7c29543170f776b2b0813f0e1fa065a90c54c26e89f11297c7895512"
    SSL_DISABLE = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    FLASKY_SLOW_DB_QUERY_TIME = 0.5

    @staticmethod
    def init_app(app):
        pass


class TestingConfig(Config):
    DEBUG = True
    DEBUG_TB_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SESSION_TYPE = "file"
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL") or \
                              "sqlite:///" + os.path.join(basedir, "data-test.sqlite")


class DevelopmentConfig(Config):
    DEBUG = True
    DEBUG_TB_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SESSION_TYPE = "redis"
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://" \
                              "imhm:3F4868C0E88995CBE3D47DC990BE0C16@localhost:33006/imhm"


class ProductionConfig(Config):
    DEBUG = False
    SESSION_TYPE = "redis"
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://" \
                              "imhm:3F4868C0E88995CBE3D47DC990BE0C16@localhost:33006/imhm"


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}
