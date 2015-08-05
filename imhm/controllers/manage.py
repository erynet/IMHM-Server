# -*- coding:utf-8 -*-
import re
import json
import random
import time
import datetime
import hashlib
import base64

from flask import abort, Blueprint, request, jsonify, session

manage_blueprint = Blueprint(__name__, "manage")

from sqlalchemy import and_, or_

from imhm import db_session as db, login_required
from imhm.models import Groups, Elements, Hardwares, Sensors


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

@manage_blueprint.route("/signin/", methods=["POST"])
#@login_required
def signin():
    #1. 받은 데이터의 키가 모두 존재하나 검사한다.
    #2. ElementFingerprint 와 일치하는 존재가 있나 확인한다.
    #3. LocalIPAddress, GlobalIPAddress, MachineName,
    #   HardwareReport 업데이트
    #4. 결과물은 ElementFingerprint 와 GroupFingerprint 이다.
    results = {}
    data = json.loads(request.data)
    arguments = ["ElementFingerprint", "MachineName",
                 "LocalIPAddress", "GlobalIPAddress", "GatewayIPAddress",
                 "HardwareReport"]
    data_keys = data.keys()
    for argument in arguments:
        if argument not in data_keys:
            raise abort(400)

    element = db.query(Elements).\
        filter_by(fingerprint=data["ElementFingerprint"]).first()
    if not element:
        raise abort(404)

    try:
        with db.begin_nested():
            db.query(Elements).filter_by(id=element.id).\
                update({Elements.machine_name:data["MachineName"],
                        Elements.ip_address_local:data["LocalIPAddress"],
                        Elements.ip_address_global:data["GlobalIPAddress"],
                        Elements.ip_address_gateway:data["GatewayIPAddress"],
                        Elements.report:data["HardwareReport"]})
    except Exception, e:
        print str(e)
        raise abort(500)

    results["element_id"] = element.fingerprint

    db.commit()
    return jsonify(results), 200


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
    arguments = ["MachineName", "LocalIPAddress", "GlobalIPAddress", "GatewayIPAddress",
                 "GroupFingerprint", "HardwareList",
                 "CoreComponent_CPU", "CoreComponent_Mainboard", "CoreComponent_GPU"]
    data_keys = data.keys()
    for argument in arguments:
        if argument not in data_keys:
            raise abort(400)
    #2. 일단 받아온 그룹이 존재하나 확인한다.
    element_md5 = "%032x" % random.getrandbits(128)
    group = db.query(Groups).filter_by(identifier=data["GroupFingerprint"]).first()
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
                             ip_address_local=data["LocalIPAddress"],
                             ip_address_global=data["GlobalIPAddress"],
                             ip_address_gateway=data["GatewayIPAddress"])
                db.add(e)

        except Exception, e:
            print str(e)
            raise abort(500)
    else:
        try:
            with db.begin_nested():
                # 이미 그룹이 존재한다.
                e = Elements(group_id=group.id, fingerprint=element_md5,
                             machine_name=data["MachineName"],
                             ip_address_local=data["LocalIPAddress"],
                             ip_address_global=data["GlobalIPAddress"],
                             ip_address_gateway=data["GatewayIPAddress"])
                db.add(e)
        except Exception, e:
            print str(e)
            raise abort(500)

    #5. 해당 엘리먼트의 하위에 하드웨어들을 등록하면서 랜덤 SHA1 을 등록한다.
    hws = data["HardwareList"]
    hws_sha1_dict = {}
    for hw_name in hws.keys():
        rsha1 = hashlib.sha1(str(random.random())).hexdigest()
        if hws[hw_name] == "CPU":
            #CPU 부하
            #CPU 온도
            #CPU 전력사용량
            try:
                with db.begin_nested():
                    h = Hardwares(element_id=e.id, fingerprint=rsha1, \
                                  type=0, hardware_name=hw_name)
                    db.add(h)
                    db.flush()
                    hws_sha1_dict[hw_name] = rsha1
                    s1 = Sensors(hardware_id=h.id, type=0, \
                                 sensor_name="Core Load")
                    db.add(s1)
                    s2 = Sensors(hardware_id=h.id, type=1, \
                                 sensor_name="Core Temperature")
                    db.add(s2)
                    s3 = Sensors(hardware_id=h.id, type=2, \
                                 sensor_name="Core Power")
                    db.add(s3)
                    s4 = Sensors(hardware_id=h.id, type=4, \
                                 sensor_name="Core TempPerLoad")
                    db.add(s4)
                    s5 = Sensors(hardware_id=h.id, type=5, \
                                 sensor_name="Core PowerPerLoad")
                    db.add(s5)
            except Exception, e:
                print str(e)
                raise abort(500)
        elif hws[hw_name] == "Mainboard":
            try:
                with db.begin_nested():
                    h = Hardwares(element_id=e.id, fingerprint=rsha1, \
                                  type=1, hardware_name=hw_name)
                    db.add(h)
                    db.flush()
                    hws_sha1_dict[hw_name] = rsha1
                    #여기에 추가되는 센서는 ... 없다.
            except Exception, e:
                print str(e)
                raise abort(500)

        elif hws[hw_name] == "Nvidia GPU":
            try:
                with db.begin_nested():
                    h = Hardwares(element_id=e.id, fingerprint=rsha1, \
                                  type=2, hardware_name=hw_name)
                    db.add(h)
                    db.flush()
                    hws_sha1_dict[hw_name] = rsha1
                    s1 = Sensors(hardware_id=h.id, type=0, \
                                 sensor_name="Core Load")
                    db.add(s1)
                    s2 = Sensors(hardware_id=h.id, type=1, \
                                 sensor_name="Core Temperature")
                    db.add(s2)
                    s3 = Sensors(hardware_id=h.id, type=3, \
                                 sensor_name="Core FanRPM")
                    db.add(s3)
                    s4 = Sensors(hardware_id=h.id, type=4, \
                                 sensor_name="Core TempPerLoad")
                    db.add(s4)
                    s5 = Sensors(hardware_id=h.id, type=6, \
                                 sensor_name="Core FanRPMPerLoad")
                    db.add(s5)
            except Exception, e:
                print str(e)
                raise abort(500)
        elif hws[hw_name] == "AMD GPU":
            try:
                with db.begin_nested():
                    h = Hardwares(element_id=e.id, fingerprint=rsha1, \
                                  type=3, hardware_name=hw_name)
                    db.add(h)
                    db.flush()
                    hws_sha1_dict[hw_name] = rsha1
                    s1 = Sensors(hardware_id=h.id, type=0, \
                                 sensor_name="Core Load")
                    db.add(s1)
                    s2 = Sensors(hardware_id=h.id, type=1, \
                                 sensor_name="Core Temperature")
                    db.add(s2)
                    s3 = Sensors(hardware_id=h.id, type=3, \
                                 sensor_name="Core FanRPM")
                    db.add(s3)
                    s4 = Sensors(hardware_id=h.id, type=4, \
                                 sensor_name="Core TempPerLoad")
                    db.add(s4)
                    s5 = Sensors(hardware_id=h.id, type=6, \
                                 sensor_name="Core FanRPMPerLoad")
                    db.add(s5)
            except Exception, e:
                print str(e)
                raise abort(500)
        elif hws[hw_name] == "SSD":
            try:
                with db.begin_nested():
                    h = Hardwares(element_id=e.id, fingerprint=rsha1, \
                                  type=5, hardware_name=hw_name)
                    db.add(h)
                    db.flush()
                    hws_sha1_dict[hw_name] = rsha1
                    #여기에 추가되는 센서는 ... 없다.
                    #대신 SMART 가 있다.
            except Exception, e:
                print str(e)
                raise abort(500)
        elif hws[hw_name] == "HDD":
            try:
                with db.begin_nested():
                    h = Hardwares(element_id=e.id, fingerprint=rsha1, \
                                  type=4, hardware_name=hw_name)
                    db.add(h)
                    db.flush()
                    hws_sha1_dict[hw_name] = rsha1
                    #여기에 추가되는 센서는 ... 없다.
                    #대신 SMART 가 있다.
            except Exception, e:
                print str(e)
                raise abort(500)
    try:
        rsha1 = hashlib.sha1(str(random.random())).hexdigest()
        with db.begin_nested():
            h = Hardwares(element_id=e.id, fingerprint=rsha1, \
                          type=6, hardware_name="System")
            db.add(h)
            db.flush()
            hws_sha1_dict["System"] = rsha1
            s1 = Sensors(hardware_id=h.id, type=7, \
                         sensor_name="DPC")
            db.add(s1)
            s1 = Sensors(hardware_id=h.id, type=8, \
                         sensor_name="Throttling")
            db.add(s1)
    except Exception, e:
        print str(e)
        raise abort(500)

    results["element_id"] = element_md5
    results["hardware_sha1"] = hws_sha1_dict
    db.commit()

    return jsonify(results), 200
