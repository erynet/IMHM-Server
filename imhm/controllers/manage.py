# -*- coding:utf-8 -*-
import re
import json
import random
import time
import datetime
import hashlib

from flask import abort, Blueprint, request, jsonify, session

manage_blueprint = Blueprint(__name__, "manage")

from sqlalchemy import and_, or_

from imhm import db_session as db, login_required
from imhm.models import Groups, Elements


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
    #1. 받은 데이터의 키가 모두 존재하나 검사한다.
    data = json.loads(request.data)
    arguments = ["MachineName", "LocalIpAddress", "GlobalIPAddress",
                 "GroupFingerprint", "HardwareList",
                 "CoreComponent_CPU", "CoreComponent_Mainboard", "CoreComponent_GPU"]
    data_keys = data.keys()
    for argument in arguments:
        if argument not in data_keys:
            raise abort(400)
    #2. 일단 받아온 그룹이 존재하나 확인한다.
    element_md5 = "%032x" % random.getrandbits(128)
    group = db.query(Groups).filter_by(identifier=data["GroupFingerprint"])
    if not group:
        #3. 그룹이 존재하지 않는다면 그룹을 등록한다.
        #   그다음 엘리먼트를 추가한다.
        try:
            with db.begin_nested():
                g = Groups(identifier=data["GroupFingerprint"],
                           cpu=data["CoreComponent_CPU"],
                           mainboard=data["CoreComponent_Mainboard"],
                           gpu=data["CoreComponent_GPU"])
                db.add(g)
                db.flush()

                e = Elements(group_id=g.id, fingerprint=element_md5,
                             machine_name=data["MachineName"],
                             ip_address_local=data["LocalIpAddress"],
                             ip_address_global=data["GlobalIPAddress"])
                db.add(e)

        except Exception, e:
            print str(e)
            raise abort(500)
    else:
        #이미 그룹이 존재한다.
        e = Elements(group_id=group.id, fingerprint=element_md5,
                     machine_name=data["MachineName"],
                     ip_address_local=data["LocalIpAddress"],
                     ip_address_global=data["GlobalIPAddress"])
        db.add(e)
    db.flush()
    #5. 해당 엘리먼트의 하위에 하드웨어들을 등록하면서 랜덤 SHA1 을 등록한다.
    hws = data["HardwareList"]
    for hw_name in hws.keys():
        if hws[hw_name] == "CPU":
            #CPU 부하
            #CPU 온도
            #CPU 전력사용량
            pass
        elif hws[hw_name] == "Mainboard":
            pass
        elif hws[hw_name] == "Nvidia GPU":
            pass
        elif hws[hw_name] == "AMD GPU":
            pass
        elif hws[hw_name] == "SSD":
            pass
        elif hws[hw_name] == "HDD":
            pass





    return jsonify(results), 200