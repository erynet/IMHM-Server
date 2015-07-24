# -*- coding:utf-8 -*-
import sys
import json

reload(sys)
sys.setdefaultencoding("utf-8")

import os

basedir = os.path.abspath(os.path.dirname(__file__))

sys.path.append(os.path.join(basedir, "../../../"))

from celery import Task

from sadari import db_session as db
from sadari.utils.async import celery_app


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
