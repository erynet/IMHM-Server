# -*- coding:utf-8 -*-
import re
import json
import time
import datetime
import hashlib

from flask import abort, Blueprint, request, jsonify, session

manage_blueprint = Blueprint(__name__, "manage")

from sqlalchemy import and_, or_

#from sadari import db_session as db, login_required, get_permission
#from sadari.models import Event


@manage_blueprint.before_request
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


# 구현완료
# 그냥 있는대로 다 긁는다.
@manage_blueprint.route("/signup/", methods=["POST"])
#@login_required
def signup():
    #1. 받은 데이터의 키가 모두 존재하나 검사한다.
    #2. 일단 받아온 그룹이 존재하나 확인한다.
    #3. 그룹이 존재하지 않는다면 그룹을 등록한다.
    #4. 해당 그룹 아래에 엘리먼트를 등록하면서 랜덤 md5 를 생성한다.
    #5. 해당 엘리먼트의 하위에 하드웨어들을 등록하면서 랜덤 SHA1 을 등록한다.
    #6. 해당 하드웨어의 장치에 따라서 얻어올 센서값은 정해져 있으므로
    #   해당 센서값들을 하드웨어 종류에 맟춰서 등록한다.
    #   하드디스크의 SMART 값은 통쨰로 저장하는게 옳다.
    results = {}
    data = json.loads(request.data)
    arguments = ["MachineName", "LocalIpAddress", "GlobalIPAddress", "GroupFingerprint", "HardwareList"]
    data_keys = data.keys()
    for argument in arguments:
        if argument not in data_keys:
            raise abort(400)
    #data_keys = json.lo
    #for key in
    #print request.form["MachineName"]
    #print request.form["LocalIPAddress"]
    #print request.form["GlobalIPAddress"]
    #print request.form["GroupFingerprint"]
    #print request.data
    return jsonify(results), 200