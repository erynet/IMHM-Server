# -*- coding:utf-8 -*-
import re
import json
import random
import time
import datetime
import hashlib
import base64

from flask import abort, Blueprint, request, jsonify, session

process_blueprint = Blueprint(__name__, "process")

from sqlalchemy import and_, or_

from imhm import db_session as db, login_required
from imhm.models import Groups, Elements, Hardwares, Sensors


@process_blueprint.before_request
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


@process_blueprint.route("/process/", methods=["POST"])
# @login_required
def process(fingerprint):
    # 1. 받은 데이터의 키가 모두 존재하나 검사한다.
    # 2. ElementFingerprint 와 일치하는 존재가 있나 확인한다.
    # 3. LocalIPAddress, GlobalIPAddress, MachineName,
    #   HardwareReport 업데이트
    # 4. 결과물은 ElementFingerprint 와 GroupFingerprint 이다.
    results = {}
    data = json.loads(request.data)
    arguments = ["General"]
    data_keys = data.keys()
    for argument in arguments:
        if argument not in data_keys:
            raise abort(400)

    print data


    return "", 200