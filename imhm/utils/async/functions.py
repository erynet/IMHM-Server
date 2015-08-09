# -*- coding:utf-8 -*-
import sys
import json

reload(sys)
sys.setdefaultencoding("utf-8")

import os

basedir = os.path.abspath(os.path.dirname(__file__))

sys.path.append(os.path.join(basedir, "../../../"))

from celery import Task
from sqlalchemy import func

from imhm import db_session as db
from imhm.models import Sensors, Hardwares, \
    GenericParameters, GenericRegression, GenericSmart, GenericValues, \
    ReportSession, Warnings
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

#interrupt_timer
#warning_processor

# 1. 파라메터
# 사실 DPC 밖에 없다고 봐도 틀린말이 아니지.
@celery_app.task(base=DefaultPushTask,
                 name="imhm.utils.async.functions.proc_parameter")
def proc_parameter(sensor_id):
    # 처리한지 15분이 지났으니 오는것임.
    ssid = db.query(Sensors).filter_by(id=sensor_id)
    if not ssid:
        return
    rssid = db.query(ReportSession).\
        filter(ReportSession.created_at >= ssid.processed_at).\
        order_by(ReportSession.created_at.asc()).first()

    dpc_maxs = db.query(func.max(GenericParameters.value)).\
        filter_by(sensor_id=ssid.id).\
        filter(GenericParameters.rss_id >= rssid.id).all()

    for dpc in dpc_maxs:
        dpc_max = dpc
        break

    row = db.query(GenericParameters).filter_by(value=dpc_max).first()

    if row.value > 250:
        #high dpc info
        d = u"DPC 가 25 이 넘었습니다. 오디오 재생같은 실시간 어플리케이션에 장애가 발생할 수 있습니다. "
        if row.additional == "NDIS.sys":
            d += u"값을 기록한 드라이버는 NDIS.sys 입니다. "
            d += u"DDOS 공격을 당하고 있을 가능성이 있습니다."
            w = Warnings(hardware_id=ssid.harware_id, event_code=10,
                         event_code_description=d, value=row.value, level=0)
        elif row.additional == "USBPORT.sys":
            d += u"값을 기록한 드라이버는 USBPORT.sys 입니다. "
            d += u"USB 로 연결된 장치중 하나 이상이 올바른 드라이버가 "
            d += u"없거나 파손되었을 가능성이 있습니다."
            w = Warnings(hardware_id=ssid.harware_id, event_code=11,
                         event_code_description=d, value=row.value, level=0)
        else:
            d += u"값을 기록한 드라이버는 %s 입니다. " % (row.additional,)
            w = Warnings(hardware_id=ssid.harware_id, event_code=0,
                         event_code_description=d, value=row.value, level=0)
        try:
            with db.begin_nested():
                db.add(w)
        except Exception, e:
            print str(e)

    elif row.value > 500:
        #very high dpc warning
        d = u"DPC 가 500 이 넘었습니다. 오디오 재생같은 실시간 어플리케이션에 장애가 발생합니다. "
        if row.additional == "NDIS.sys":
            d += u"값을 기록한 드라이버는 NDIS.sys 입니다. "
            d += u"DDOS 공격을 당하고 있을 가능성이 있습니다."
            w = Warnings(hardware_id=ssid.harware_id, event_code=110,
                         event_code_description=d, value=row.value, level=1)
        elif row.additional == "USBPORT.sys":
            d += u"값을 기록한 드라이버는 USBPORT.sys 입니다. "
            d += u"USB 로 연결된 장치중 하나 이상이 올바른 드라이버가 "
            d += u"없거나 파손되었을 가능성이 있습니다."
            w = Warnings(hardware_id=ssid.harware_id, event_code=111,
                         event_code_description=d, value=row.value, level=1)
        else:
            d += u"값을 기록한 드라이버는 %s 입니다. " % (row.additional,)
            w = Warnings(hardware_id=ssid.harware_id, event_code=100,
                         event_code_description=d, value=row.value, level=1)
        try:
            with db.begin_nested():
                db.add(w)
        except Exception, e:
            print str(e)
    return ""
# 2. 선형회귀
@celery_app.task(base=DefaultPushTask,
                 name="imhm.utils.async.functions.proc_regression")
def proc_regression(sensor_id):
    # 처리한지 15분이 지났으니 오는것임.
# 3. values
@celery_app.task(base=DefaultPushTask,
                 name="imhm.utils.async.functions.proc_values")
def proc_values(sensor_id):
    pass

# 4. smart
@celery_app.task(base=DefaultPushTask,
                 name="imhm.utils.async.functions.proc_smart")
def proc_smart(sensor_id):
    # 처리한지 15분이 지났으니 오는것임.
    ssid = db.query(Sensors).filter_by(id=sensor_id)
    if not ssid:
        return
    rssid = db.query(ReportSession).\
        filter(ReportSession.created_at >= ssid.processed_at).\
        order_by(ReportSession.created_at.asc()).first()

    rows =



@celery_app.task(base=DefaultPushTask,
                 name="imhm.utils.async.functions.expired_order")
def expired_order():
    import datetime

    """
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
    """

    return ""
