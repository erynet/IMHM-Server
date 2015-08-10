# -*- coding:utf-8 -*-
import sys
import json
import time
import datetime

reload(sys)
sys.setdefaultencoding("utf-8")

import os

basedir = os.path.abspath(os.path.dirname(__file__))

sys.path.append(os.path.join(basedir, "../../../"))

from celery import Task
from sqlalchemy import func

from imhm import db_session as db
from imhm.models import Sensors, Hardwares, Elements, Groups, \
    GenericParameters, GenericRegression, GenericSmart, GenericValues, \
    ReportSession, Warnings, Admin
from imhm.utils.async import celery_app


class DefaultPushTask(Task):
    abstract = True


@celery_app.task(base=DefaultPushTask,
                 name="imhm.utils.async.functions.android_push")
def android_push(uuids, message):
    if not uuids:
        raise Exception("Registration_id is required.")

    # GCM Configuration
    from gcm import GCM

    api_key = "AIzaSyAheYj04o3dgHhG8MrN5NGQKY4HT8NhzKc"
    gcm = GCM(api_key)

    if type(uuids) is list:
        gcm.json_request(registration_ids=uuids, data=message)
    else:
        gcm.plaintext_request(registration_id=uuids, data=message)

    return ""


# interrupt_timer
@celery_app.task(base=DefaultPushTask,
                 name="imhm.utils.async.functions.interrupt_timer")
def interrupt_timer():
    # 1. Sensors 를 돌면서 processed_at 이 10분이 지난 대상으로 큐잉.
    dt = datetime.datetime.now() + datetime.timedelta(seconds=-600)
    targets = db.query(Sensors).filter(Sensors.processed_at < dt).all()
    for t in targets:
        if t.type in [0, 1, 2, 3]:
            proc_values.apply_async(args=[t.id,])
            #pass
        elif t.type in [4, 5, 6]:
            proc_regression.apply_async(args=[t.id,])
            #pass
        elif t.type in [7, 8]:
            proc_parameters.apply_async(args=[t.id,])
        elif t.type == 9:
            proc_smart.apply_async(args=[t.id,])
            #pass
        else:
            pass
    #이 밑으로는 리그레션 프로세서를 넣어야 하는데 ..


# warning_processor
@celery_app.task(base=DefaultPushTask,
                 name="imhm.utils.async.functions.warning_processor")
def warning_processor():
    # android_push.apply_async(args=[user.uuid, message])
    admins = db.query(Admin).all()

    warns = db.query(Warnings).filter_by(warned=False).all()
    for warn in warns:
        uuids = []
        for admin in admins:
            if admin.notify_level <= warn.level:
                uuids.append(admin.uuid)
        hw = db.query(Hardwares).filter_by(id=warn.hardware_id).first()
        element = db.query(Elements).filter_by(id=hw.element_id).first()
        group = db.query(Groups).filter_by(id=element.group_id).first()
        msg = dict(id=unicode(warn.id), time_code=unicode(time.mktime(warn.timestamp.timetuple())), \
                   error_code=unicode(warn.event_code), group_fingerprint=group.identifier, \
                   element_fingerprint=element.fingerprint, machine_name=element.machine_name, \
                   ip_address_local=element.ip_address_local, ip_address_global=element.ip_address_global, \
                   hardware_name=hw.hardware_name, warning_level=unicode(warn.level), \
                   message=unicode(warn.event_code_description))
        android_push.apply_async(args=[uuids, msg])
        db.query(Warnings).filter_by(id=warn.id).update({Warnings.warned: True})
    db.commit()

# 1. 파라메터
# 사실 DPC 밖에 없다고 봐도 틀린말이 아니지.
@celery_app.task(base=DefaultPushTask,
                 name="imhm.utils.async.functions.proc_parameters")
def proc_parameters(sensor_id):
    # 처리한지 15분이 지났으니 오는것임.
    ssid = db.query(Sensors).filter_by(id=sensor_id).first()
    if not ssid:
        return
    rssid = db.query(ReportSession). \
        filter(ReportSession.created_at >= ssid.processed_at). \
        order_by(ReportSession.created_at.asc()).first()

    dpc_maxs = db.query(func.max(GenericParameters.value)). \
        filter_by(sensor_id=ssid.id). \
        filter(GenericParameters.rss_id >= rssid.id).first()

    # for dpc in dpc_maxs:
    #    dpc_max = dpc
    #    break
    dpc_max = dpc_maxs[0]
    if not dpc_max:
        return
    #print dpc_maxs;

    #row = db.query(GenericParameters).filter_by(value=dpc_max).first()
    row = db.query(GenericParameters). \
        filter_by(sensor_id=ssid.id). \
        filter_by(value=dpc_max). \
        filter(GenericParameters.rss_id >= rssid.id).first()


    if row.value > 250:
        # high dpc info
        d = u"DPC 가 25 이 넘었습니다. 오디오 재생같은 실시간 어플리케이션에 장애가 발생할 수 있습니다. "
        if row.additional == "NDIS.sys":
            d += u"값을 기록한 드라이버는 NDIS.sys 입니다. "
            d += u"DDOS 공격을 당하고 있을 가능성이 있습니다."
            w = Warnings(hardware_id=ssid.hardware_id, event_code=10,
                         event_code_description=d, value=row.value, level=0)
        elif row.additional == "USBPORT.sys":
            d += u"값을 기록한 드라이버는 USBPORT.sys 입니다. "
            d += u"USB 로 연결된 장치중 하나 이상이 올바른 드라이버가 "
            d += u"없거나 파손되었을 가능성이 있습니다."
            w = Warnings(hardware_id=ssid.hardware_id, event_code=11,
                         event_code_description=d, value=row.value, level=0)
        else:
            d += u"값을 기록한 드라이버는 %s 입니다. " % (row.additional,)
            w = Warnings(hardware_id=ssid.hardware_id, event_code=0,
                         event_code_description=d, value=row.value, level=0)
        try:
            with db.begin_nested():
                db.add(w)
        except Exception, e:
            print str(e)

    elif row.value > 500:
        # very high dpc warning
        d = u"DPC 가 500 이 넘었습니다. 오디오 재생같은 실시간 어플리케이션에 장애가 발생합니다. "
        if row.additional == "NDIS.sys":
            d += u"값을 기록한 드라이버는 NDIS.sys 입니다. "
            d += u"DDOS 공격을 당하고 있을 가능성이 있습니다."
            w = Warnings(hardware_id=ssid.hardware_id, event_code=110,
                         event_code_description=d, value=row.value, level=1)
        elif row.additional == "USBPORT.sys":
            d += u"값을 기록한 드라이버는 USBPORT.sys 입니다. "
            d += u"USB 로 연결된 장치중 하나 이상이 올바른 드라이버가 "
            d += u"없거나 파손되었을 가능성이 있습니다."
            w = Warnings(hardware_id=ssid.hardware_id, event_code=111,
                         event_code_description=d, value=row.value, level=1)
        else:
            d += u"값을 기록한 드라이버는 %s 입니다. " % (row.additional,)
            w = Warnings(hardware_id=ssid.hardware_id, event_code=100,
                         event_code_description=d, value=row.value, level=1)
        try:
            with db.begin_nested():
                db.add(w)
        except Exception, e:
            print str(e)
    db.commit()
    return ""


# 2. 선형회귀
@celery_app.task(base=DefaultPushTask,
                 name="imhm.utils.async.functions.proc_regression")
def proc_regression(sensor_id):
    # 처리한지 15분이 지났으니 오는것임.
    pass


# 3. values
@celery_app.task(base=DefaultPushTask,
                 name="imhm.utils.async.functions.proc_values")
def proc_values(sensor_id):
    ssid = db.query(Sensors).filter_by(id=sensor_id).first()
    if not ssid:
        return
    rssid = db.query(ReportSession). \
        filter(ReportSession.created_at >= ssid.processed_at). \
        order_by(ReportSession.created_at.asc()).first()
    hw = db.query(Hardwares).filter_by(id=ssid.hardware_id).first()

    if hw.type == 0:
        # cpu
        d = u"CPU 온도가 너무 높습니다.  "
        # 1 : Core Temperature  /   value
        w = None
        avg_min = db.query(func.avg(GenericValues.min)). \
            filter_by(sensor_id=ssid.id). \
            filter(GenericSmart.rss_id >= rssid.id).first()
        if avg_min[0] > 75:
            d += u"CPU 최저 온도가 %d 를 넘습니다. 쿨러를 체크하세요." % (int(avg_min[0]))
            w = Warnings(hardware_id=ssid.hardware_id, event_code=500,
                         event_code_description=d, value=(int(avg_min[0])), level=1)
        elif avg_min[0] > 65:
            d += u"CPU 최저 온도가 %d 를 넘습니다. 쿨러를 체크하세요." % (int(avg_min[0]))
            w = Warnings(hardware_id=ssid.hardware_id, event_code=501,
                         event_code_description=d, value=(int(avg_min[0])), level=0)
        if not (w == None):
            try:
                with db.begin_nested():
                    db.add(w)
            except Exception, e:
                print str(e)
        w = None
        avg_max = db.query(func.avg(GenericValues.max)). \
            filter_by(sensor_id=ssid.id). \
            filter(GenericSmart.rss_id >= rssid.id).first()
        if avg_max[0] > 90:
            d += u"CPU 최고 온도가 %d 를 넘습니다. 쿨러를 체크하세요." % (int(avg_min[0]))
            w = Warnings(hardware_id=ssid.hardware_id, event_code=502,
                         event_code_description=d, value=(int(avg_min[0])), level=2)
        elif avg_max[0] > 80:
            d += u"CPU 최고 온도가 %d 를 넘습니다. 쿨러를 체크하세요." % (int(avg_min[0]))
            w = Warnings(hardware_id=ssid.hardware_id, event_code=503,
                         event_code_description=d, value=(int(avg_min[0])), level=1)
        if not (w == None):
            try:
                with db.begin_nested():
                    db.add(w)
            except Exception, e:
                print str(e)
    elif hw.type == 2:
        # Nvidia GPU
        d = u"GPU 온도가 너무 높습니다.  "
        # 1 : Core Temperature  /   value
        w = None
        avg_min = db.query(func.avg(GenericValues.min)). \
            filter_by(sensor_id=ssid.id). \
            filter(GenericSmart.rss_id >= rssid.id).first()
        if avg_min[0] > 80:
            d += u"GPU 최저 온도가 %d 를 넘습니다. 쿨러를 체크하세요." % (int(avg_min[0]))
            w = Warnings(hardware_id=ssid.hardware_id, event_code=504,
                         event_code_description=d, value=(int(avg_min[0])), level=1)
        elif avg_min[0] > 70:
            d += u"GPU 최저 온도가 %d 를 넘습니다. 쿨러를 체크하세요." % (int(avg_min[0]))
            w = Warnings(hardware_id=ssid.hardware_id, event_code=505,
                         event_code_description=d, value=(int(avg_min[0])), level=0)
        if not (w == None):
            try:
                with db.begin_nested():
                    db.add(w)
            except Exception, e:
                print str(e)
        w = None
        avg_max = db.query(func.avg(GenericValues.max)). \
            filter_by(sensor_id=ssid.id). \
            filter(GenericSmart.rss_id >= rssid.id).first()
        if avg_max[0] > 95:
            d += u"GPU 최고 온도가 %d 를 넘습니다. 쿨러를 체크하세요." % (int(avg_min[0]))
            w = Warnings(hardware_id=ssid.hardware_id, event_code=506,
                         event_code_description=d, value=(int(avg_min[0])), level=2)
        elif avg_max[0] > 85:
            d += u"GPU 최고 온도가 %d 를 넘습니다. 쿨러를 체크하세요." % (int(avg_min[0]))
            w = Warnings(hardware_id=ssid.hardware_id, event_code=507,
                         event_code_description=d, value=(int(avg_min[0])), level=1)
        if not (w == None):
            try:
                with db.begin_nested():
                    db.add(w)
            except Exception, e:
                print str(e)
    elif hw.type == 3:
        # AMD GPU
        pass

    try:
        with db.begin_nested():
            db.query(Sensors).filter_by(id=sensor_id). \
                update({Sensors.processed_at: datetime.datetime.now()})
    except Exception, e:
        print str(e)
    db.commit()

# 4. smart
@celery_app.task(base=DefaultPushTask,
                 name="imhm.utils.async.functions.proc_smart")
def proc_smart(sensor_id):
    # 처리한지 15분이 지났으니 오는것임.
    ssid = db.query(Sensors).filter_by(id=sensor_id).first()
    if not ssid:
        return
    rssid = db.query(ReportSession). \
        filter(ReportSession.created_at >= ssid.processed_at). \
        order_by(ReportSession.created_at.asc()).first()

    rows = db.query(GenericSmart.code, \
                    func.min(GenericSmart.physical), \
                    func.max(GenericSmart.physical), \
                    GenericSmart.threshold, GenericSmart.description). \
        filter_by(sensor_id=ssid.id). \
        filter(GenericSmart.rss_id >= rssid.id). \
        group_by(GenericSmart.code).all()

    for row in rows:
        code, min, max, thres, desc = row
        w = None
        d = u"HDD/SSD 관련 정보입니다. "
        if code == 5:
            # 1. 수치 5 이하에서 증가(Info)
            if max < 5:
                if max - min > 0:
                    comment = u"Reallocated Sector 수의 증가는 하드디스크 이상의 전조일 수 있습니다."
                    d += u"S.M.A.R.T Code : %d, Description : %s, Value : %d, Comment : %s" % \
                         (code, desc, max, comment)
                    w = Warnings(hardware_id=ssid.hardware_id, event_code=200,
                                 event_code_description=d, value=max, level=0)
            # 2. 수치 5 이상에서 증가(Warning)
            elif max >= 5:
                if max - min > 0:
                    comment = u"Reallocated Sector 수의 증가는 하드디스크 이상의 전조일 수 있습니다."
                    d += u"S.M.A.R.T Code : %d, Description : %s, Value : %d, Comment : %s" % \
                         (code, desc, max, comment)
                    w = Warnings(hardware_id=ssid.hardware_id, event_code=201,
                                 event_code_description=d, value=max, level=1)
            # 3. 수치 7 이상에서 증가(Alert)
            elif max >= 7:
                if max - min > 0:
                    comment = u"Reallocated Sector 수가 임계점을 넘었습니다. 데이터를 백업하십시오."
                    d += u"S.M.A.R.T Code : %d, Description : %s, Value : %d, Comment : %s" % \
                         (code, desc, max, comment)
                    w = Warnings(hardware_id=ssid.hardware_id, event_code=202,
                                 event_code_description=d, value=max, level=2)
        elif code == 9:
            if max > 43800:
                comment = u"하드디스크 가동시간이 3년이 넘었습니다. 교체를 고려하십시오."
                d += u"S.M.A.R.T Code : %d, Description : %s, Value : %d, Comment : %s" % \
                     (code, desc, max, comment)
                w = Warnings(hardware_id=ssid.hardware_id, event_code=300,
                             event_code_description=d, value=max, level=1)
        elif code == 10:
            if max - min > 0:
                comment = u"Spin Retry Count 수의 증가는 하드디스크 구동부 문제거나 전원의 불안정을 암시합니다."
                d += u"S.M.A.R.T Code : %d, Description : %s, Value : %d, Comment : %s" % \
                     (code, desc, max, comment)
                w = Warnings(hardware_id=ssid.hardware_id, event_code=400,
                             event_code_description=d, value=max, level=1)
        elif code == 183:
            if max - min > 0:
                comment = u"SATA Downshift Error 는 SATA 케아블의 불량이나 관련 칩셋의 문제를 의미합니다."
                d += u"S.M.A.R.T Code : %d, Description : %s, Value : %d, Comment : %s" % \
                     (code, desc, max, comment)
                w = Warnings(hardware_id=ssid.hardware_id, event_code=401,
                             event_code_description=d, value=max, level=2)
        elif code == 187:
            if max - min > 0:
                comment = u"Reported Uncorrectable Error 수의 증가는 심각한 수준의 하드디스크 플래터 손상이나 기판의 문제를 의미합니다."
                d += u"S.M.A.R.T Code : %d, Description : %s, Value : %d, Comment : %s" % \
                     (code, desc, max, comment)
                w = Warnings(hardware_id=ssid.hardware_id, event_code=203,
                             event_code_description=d, value=max, level=2)
        elif code == 188:
            if max - min > 0:
                comment = u"Command Timeout 는 SATA 케아블의 불량이나 전원의 불안정을 암시합니다. 데이터 오염이 발생할 수 있습니다."
                d += u"S.M.A.R.T Code : %d, Description : %s, Value : %d, Comment : %s" % \
                     (code, desc, max, comment)
                w = Warnings(hardware_id=ssid.hardware_id, event_code=402,
                             event_code_description=d, value=max, level=2)
        elif code == 191:
            if max - min > 0:
                comment = u"Mechanical Shock 는 대상 PC 가 불안정한 위치에 있거나 충격을 받는 경우 발생합니다."
                d += u"S.M.A.R.T Code : %d, Description : %s, Value : %d, Comment : %s" % \
                     (code, desc, max, comment)
                w = Warnings(hardware_id=ssid.hardware_id, event_code=301,
                             event_code_description=d, value=max, level=1)
        elif code == 194:
            if max > 55:
                comment = u"온도가 55도 이상입니다. 하드디스크의 급격한 노화가 진행될 수 있습니다."
                d += u"S.M.A.R.T Code : %d, Description : %s, Value : %d, Comment : %s" % \
                     (code, desc, max, comment)
                w = Warnings(hardware_id=ssid.hardware_id, event_code=303,
                             event_code_description=d, value=max, level=1)
            elif max > 45:
                comment = u"온도가 45도 이상입니다."
                d += u"S.M.A.R.T Code : %d, Description : %s, Value : %d, Comment : %s" % \
                     (code, desc, max, comment)
                w = Warnings(hardware_id=ssid.hardware_id, event_code=302,
                             event_code_description=d, value=max, level=0)
        # 중간은잠시 생략, 196, 197, 198, 199, 201, 230
        elif code == 231:
            if max > 55:
                comment = u"온도가 55도 이상입니다. 하드디스크의 급격한 노화가 진행될 수 있습니다."
                d += u"S.M.A.R.T Code : %d, Description : %s, Value : %d, Comment : %s" % \
                     (code, desc, max, comment)
                w = Warnings(hardware_id=ssid.hardware_id, event_code=303,
                             event_code_description=d, value=max, level=1)
            elif max > 45:
                comment = u"온도가 45도 이상입니다."
                d += u"S.M.A.R.T Code : %d, Description : %s, Value : %d, Comment : %s" % \
                     (code, desc, max, comment)
                w = Warnings(hardware_id=ssid.hardware_id, event_code=302,
                             event_code_description=d, value=max, level=0)
        if not (w == None):
            try:
                with db.begin_nested():
                    db.add(w)
            except Exception, e:
                print str(e)
    try:
        with db.begin_nested():
            db.query(Sensors).filter_by(id=sensor_id). \
                update({Sensors.processed_at: datetime.datetime.now()})
    except Exception, e:
        print str(e)
    db.commit()

"""
@celery_app.task(base=DefaultPushTask,
                 name="imhm.utils.async.functions.expired_order")
def expired_order():
    import datetime


    from sadari.models import Order, Operator, OperatorAdminMatch, Point

    now = datetime.datetime.now()
    orders = Order.query. \
        filter(Order.status != 2,
               Order.created_at >= now - datetime.timedelta(days=2),
               Order.created_at < now - datetime.timedelta(days=1)).all()

    for order in orders:
        order.status = 2
        db.flush()

        operator_admin_match = \
            OperatorAdminMatch.query. \
                filter_by(operator=order.orderer).first()
        master = Operator.query.filter_by(is_master=True).first()

        total_commission = order.price / 10

        # 포인트 분배
        orderee_point = Point(user=order.orderee, type=1,
                              how_much=total_commission)
        db.add(orderee_point)
        order.orderee.point -= total_commission
        db.flush()

        operator_point = Point(user=operator_admin_match.operator, type=0,
                               how_much=total_commission *
                                        (order.orderer_commission / 100))
        db.add(operator_point)
        operator_admin_match.operator.point += \
            total_commission * (order.orderer_commission / 100)
        db.flush()

        admin_point = Point(user=operator_admin_match.admin, type=0,
                            how_much=total_commission *
                                     (order.admin_commission / 100))
        db.add(admin_point)
        operator_admin_match.admin.point += \
            total_commission * (order.admin_commission / 100)
        db.flush()

        master_point = Point(user=operator_admin_match.admin, type=0,
                             how_much=total_commission *
                                      (order.master_commission / 100))
        db.add(master_point)
        master.point += \
            total_commission * (order.master_commission / 100)
        db.flush()


    return ""
    """
