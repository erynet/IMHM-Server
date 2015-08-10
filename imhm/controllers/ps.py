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


@ps_blueprint.route("/ps/", methods=["post"])
# @login_required
def hw_report():
    # 1. 받은 데이터의 키가 모두 존재하나 검사한다.
    # 2. ElementFingerprint 와 일치하는 존재가 있나 확인한다.
    # 3. LocalIPAddress, GlobalIPAddress, MachineName,
    #   HardwareReport 업데이트
    # 4. 결과물은 ElementFingerprint 와 GroupFingerprint 이다.
    element = db.query(Elements). \
        filter_by(fingerprint=fingerprint).first()

    if not element:
        raise abort(404)

    # print "DEBUG"
    # base64 디코드 필수임

    response = make_response(base64.b64decode(element.report))
    response.headers["Content-Disposition"] = "attachment; filename=%s.txt" % \
            (element.machine_name + "-" + fingerprint,)

    return response, 200