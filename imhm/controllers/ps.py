# -*- coding:utf-8 -*-
import re
import json
import random
import time
import datetime
import hashlib
import base64
import HTMLParser
import base64

from flask import abort, Blueprint, request, jsonify, session, make_response

ps_blueprint = Blueprint(__name__, "ps")

from sqlalchemy import and_, or_

from imhm import db_session as db, login_required
from imhm.models import Groups, Elements, Hardwares, Sensors


@ps_blueprint.before_request
def pre_request_logging():
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    from flask import current_app
    import datetime
    current_app.logger.info("\t".join([
        datetime.datetime.today().ctime(),
        request.remote_addr,
        request.method,
        request.url,
        unicode(request.data, "utf8"),
        ", ".join([": ".join(x) for x in request.headers])])
    )


@ps_blueprint.route("/query/", methods=["post"])
# @login_required
def query():
    results = {}
    # 1. 받은 데이터의 키가 모두 존재하나 검사한다.
    data = json.loads(request.data)
    print data

    return data, 200