# -*- coding:utf-8 -*-

from functools import wraps

from flask import Flask, session, escape, jsonify
from flask.ext.session import Session

from flask_debugtoolbar import DebugToolbarExtension

from sqlalchemy import create_engine, event
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import DisconnectionError
from sqlalchemy.pool import QueuePool

from config import config

config_name = "default"

flask_session_obj = Session()

app = Flask(__name__)
toolbar = DebugToolbarExtension(app)

if config_name == "production":
    engine = create_engine(config[config_name].SQLALCHEMY_DATABASE_URI,
                           convert_unicode=True, pool_recycle=30, poolclass=QueuePool, \
                           echo_pool=True, pool_size=20)
else:
    engine = create_engine(config[config_name].SQLALCHEMY_DATABASE_URI,
                           convert_unicode=True, pool_recycle=30, poolclass=QueuePool, \
                           echo_pool=True, pool_size=20, echo=True)


@event.listens_for(QueuePool, "checkout")
def mysql_checkout_listener(dbapi_con, con_record, con_proxy):
    try:
        print "DEBUG / Check Connection"
        if not dbapi_con.is_connected():
            print "DEBUG / Attempt Reconnect"
            dbapi_con.reconnect(attempts=1, delay=0)
            print "DEBUG / Reconnect Success"
    except Exception, e:
        print str(Exception)
        print str(e)

    # except dbapi_con.OperationalError as exc:
    #	if exc.args[0] in (2006, 2013, 2014, 2045, 2055):
    #		raise DisconnectionError()


# event.listen(engine, 'checkout', mysql_checkout_listener)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         expire_on_commit=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session_token = session.get("t")
        if session_token is None:
            # raise abort(401)
            return "", 401
        escape(session)

        return f(*args, **kwargs)

    return decorated_function

def create_app():
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    toolbar.init_app(app)

    app.config["SESSION_TYPE"] = config[config_name].SESSION_TYPE
    flask_session_obj.init_app(app)

    from imhm.controllers import (base_blueprint, manage_blueprint,
                                  report_blueprint, process_blueprint,
                                  ps_blueprint)

    # register blueprints.
    blueprints = [v for k, v in locals().items()
                  if str(k).endswith("blueprint")]
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    return app
