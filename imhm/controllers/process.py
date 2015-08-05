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
from imhm.models import Groups, Elements, Hardwares, Sensors, ReportSession, GenericValues, GenericParameters, \
    GenericRegression, GenericSmart


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
def process():
    # 1. 받은 데이터의 키가 모두 존재하나 검사한다.
    # 2. ElementFingerprint 와 일치하는 존재가 있나 확인한다.
    # 3. 각 fingerprint 를 사용해 해당 장치의 종류를 식별한다.
    # 4. 세션을 하나 딴다.
    # 5. 각 장치에 따라 그 장치에 해당된 정보를 추출하고 입력한다.
    results = {}
    # 1. 받은 데이터의 키가 모두 존재하나 검사한다.
    data = json.loads(request.data)
    arguments = ["General"]
    data_keys = data.keys()
    for argument in arguments:
        if argument not in data_keys:
            raise abort(400)
    ef = data["General"]["ElementFingerprint"]

    # 2. ElementFingerprint 와 일치하는 존재가 있나 확인한다.
    element = db.query(Elements).filter_by(fingerprint=ef).first()
    if not element:
        raise abort(404)

    hws = db.query(Hardwares).filter_by(element_id=element.id).all()
    if not hws:
        raise abort(404)

    # 3. 각 fingerprint 를 사용해 해당 장치의 종류를 식별한다.
    hw_dict = {}
    for key in data_keys:
        if key == "General":
            continue
        for hw in hws:
            if hw.fingerprint == key:
                hw_dict[key] = {}
                hw_dict[key]["id"] = hw.id
                hw_dict[key]["type"] = hw.type

    # 4. 세션을 하나 딴다.
    try:
        with db.begin_nested():
            rss = ReportSession(element_id=element.id)
            db.add(rss)
            db.flush()
    except Exception, e:
        print str(e)
        raise abort(500)

    # 5. 각 장치에 따라 그 장치에 해당된 정보를 추출하고 입력한다.
    for fp in hw_dict.keys():
        if hw_dict[fp]["type"] == 0:
            #CPU
            try:
                with db.begin_nested():
                    hw = db.query(Hardwares).filter_by(fingerprint=fp).first()

                    d = data[fp]["Load"]
                    snsr = db.query(Sensors).filter_by(hardware_id=hw.id, type=0).first()
                    s1 = GenericValues(sensor_id=snsr.id, rss_id =rss.id, min=d[0], max=d[1], avg=d[2], dev=d[3])
                    db.add(s1)

                    if data[fp].has_key("Temp"):
                        d = data[fp]["Temp"]
                        snsr = db.query(Sensors).filter_by(hardware_id=hw.id, type=1).first()
                        s2 = GenericValues(sensor_id=snsr.id, rss_id =rss.id, min=d[0], max=d[1], avg=d[2], dev=d[3])
                        db.add(s2)

                    if data[fp].has_key("Power"):
                        d = data[fp]["Power"]
                        snsr = db.query(Sensors).filter_by(hardware_id=hw.id, type=2).first()
                        s3 = GenericValues(sensor_id=snsr.id, rss_id =rss.id, min=d[0], max=d[1], avg=d[2], dev=d[3])
                        db.add(s3)

                    if data[fp].has_key("TempPerLoad"):
                        d = data[fp]["TempPerLoad"]
                        snsr = db.query(Sensors).filter_by(hardware_id=hw.id, type=4).first()
                        for l in d:
                            s = GenericRegression(sensor_id=snsr.id, rss_id =rss.id, criterion=l["Key"],
                                                  min=l["Value"][0], max=l["Value"][1],
                                                  avg=l["Value"][2], dev=l["Value"][3])
                            db.add(s)

                    if data[fp].has_key("PowerPerLoad"):
                        d = data[fp]["PowerPerLoad"]
                        snsr = db.query(Sensors).filter_by(hardware_id=hw.id, type=5).first()
                        for l in d:
                            s = GenericRegression(sensor_id=snsr.id, rss_id =rss.id, criterion=l["Key"],
                                                  min=l["Value"][0], max=l["Value"][1],
                                                  avg=l["Value"][2], dev=l["Value"][3])
                            db.add(s)
            except Exception, e:
                print str(e)
                raise abort(500)
        elif hw_dict[fp]["type"] == 2:
            #Nvidia GPU
            try:
                with db.begin_nested():
                    hw = db.query(Hardwares).filter_by(fingerprint=fp).first()

                    d = data[fp]["Load"]
                    snsr = db.query(Sensors).filter_by(hardware_id=hw.id, type=0).first()
                    s1 = GenericValues(sensor_id=snsr.id, rss_id =rss.id, min=d[0], max=d[1], avg=d[2], dev=d[3])
                    db.add(s1)

                    d = data[fp]["Temp"]
                    snsr = db.query(Sensors).filter_by(hardware_id=hw.id, type=1).first()
                    s2 = GenericValues(sensor_id=snsr.id, rss_id =rss.id, min=d[0], max=d[1], avg=d[2], dev=d[3])
                    db.add(s2)

                    if data[fp].has_key("FanRPM"):
                        d = data[fp]["FanRPM"]
                        snsr = db.query(Sensors).filter_by(hardware_id=hw.id, type=3).first()
                        s3 = GenericValues(sensor_id=snsr.id, rss_id =rss.id, min=d[0], max=d[1], avg=d[2], dev=d[3])
                        db.add(s3)

                    d = data[fp]["TempPerLoad"]
                    snsr = db.query(Sensors).filter_by(hardware_id=hw.id, type=4).first()
                    for l in d:
                        s = GenericRegression(sensor_id=snsr.id, rss_id =rss.id, criterion=l["Key"],
                                              min=l["Value"][0], max=l["Value"][1],
                                              avg=l["Value"][2], dev=l["Value"][3])
                        db.add(s)

                    if data[fp].has_key("FanrpmPerLoad"):
                        d = data[fp]["FanrpmPerLoad"]
                        snsr = db.query(Sensors).filter_by(hardware_id=hw.id, type=6).first()
                        for l in d:
                            s = GenericRegression(sensor_id=snsr.id, rss_id =rss.id, criterion=l["Key"],
                                                  min=l["Value"][0], max=l["Value"][1],
                                                  avg=l["Value"][2], dev=l["Value"][3])
                            db.add(s)
            except Exception, e:
                print str(e)
                raise abort(500)
        elif hw_dict[fp]["type"] == 3:
            #AMD GPU
            try:
                with db.begin_nested():
                    hw = db.query(Hardwares).filter_by(fingerprint=fp).first()

                    d = data[fp]["Load"]
                    snsr = db.query(Sensors).filter_by(hardware_id=hw.id, type=0).first()
                    s1 = GenericValues(sensor_id=snsr.id, rss_id =rss.id, min=d[0], max=d[1], avg=d[2], dev=d[3])
                    db.add(s1)

                    d = data[fp]["Temp"]
                    snsr = db.query(Sensors).filter_by(hardware_id=hw.id, type=1).first()
                    s2 = GenericValues(sensor_id=snsr.id, rss_id =rss.id, min=d[0], max=d[1], avg=d[2], dev=d[3])
                    db.add(s2)

                    d = data[fp]["FanRPM"]
                    snsr = db.query(Sensors).filter_by(hardware_id=hw.id, type=3).first()
                    s3 = GenericValues(sensor_id=snsr.id, rss_id =rss.id, min=d[0], max=d[1], avg=d[2], dev=d[3])
                    db.add(s3)

                    d = data[fp]["TempPerLoad"]
                    snsr = db.query(Sensors).filter_by(hardware_id=hw.id, type=4).first()
                    for l in d:
                        s = GenericRegression(sensor_id=snsr.id, rss_id =rss.id, criterion=l["Key"],
                                              min=l["Value"][0], max=l["Value"][1],
                                              avg=l["Value"][2], dev=l["Value"][3])
                        db.add(s)

                    d = data[fp]["FanrpmPerLoad"]
                    snsr = db.query(Sensors).filter_by(hardware_id=hw.id, type=6).first()
                    for l in d:
                        s = GenericRegression(sensor_id=snsr.id, rss_id =rss.id, criterion=l["Key"],
                                              min=l["Value"][0], max=l["Value"][1],
                                              avg=l["Value"][2], dev=l["Value"][3])
                        db.add(s)
            except Exception, e:
                print str(e)
                raise abort(500)
        elif hw_dict[fp]["type"] == 4:
            #HDD
            try:
                with db.begin_nested():
                    hw = db.query(Hardwares).filter_by(fingerprint=fp).first()
                    snsr = db.query(Sensors).filter_by(hardware_id=hw.id, type=9).first()
                    d = data[fp]
                    for l in d:
                        s = GenericSmart(sensor_id=snsr.id, rss_id =rss.id,
                                         code=l["Value"]["Code"], description=l["Value"]["Description"],
                                         threshold=l["Value"]["Thres"], physical=l["Value"]["Physical"])
                        db.add(s)
            except Exception, e:
                print str(e)
                raise abort(500)
        elif hw_dict[fp]["type"] == 5:
            #SSD
            try:
                with db.begin_nested():
                    hw = db.query(Hardwares).filter_by(fingerprint=fp).first()
                    snsr = db.query(Sensors).filter_by(hardware_id=hw.id, type=9).first()
                    d = data[fp]
                    for l in d:
                        s = GenericSmart(sensor_id=snsr.id, rss_id =rss.id,
                                         code=l["Value"]["Code"], description=l["Value"]["Description"],
                                         threshold=l["Value"]["Thres"], physical=l["Value"]["Physical"])
                        db.add(s)
            except Exception, e:
                print str(e)
                raise abort(500)
        elif hw_dict[fp]["type"] == 6:
            #System
            try:
                with db.begin_nested():
                    hw = db.query(Hardwares).filter_by(fingerprint=fp).first()
                    snsr = db.query(Sensors).filter_by(hardware_id=hw.id, type=7).first()
                    d = data[fp]

                    s = GenericParameters(sensor_id=snsr.id, rss_id =rss.id,
                                          value=d["DPC"]["Stat"][1], additional=d["DPC"]["Driver"])
                    db.add(s)

                    for l in d["Throttling"]:
                        s = GenericParameters(sensor_id=snsr.id, rss_id =rss.id, value=l)
                        db.add(s)
            except Exception, e:
                print str(e)
                raise abort(500)
    db.commit()
    return jsonify(results), 200