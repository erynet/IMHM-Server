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
    match = False
    z = ""
    # 1. 받은 데이터의 키가 모두 존재하나 검사한다.
    d = json.loads(request.data)
    if d[0] == "show":
        #show groups
        #show elements in group #####
        if d[1] == "groups":
            for g in db.query(Groups).all():
                z += g.identifier
                z += " : "
                z += g.cpu + " / " + g.mainboard + " / " + g.gpu + "\n"
            results["result"] = z
            return jsonify(results), 200
        elif d[1] == "elements":
            if d[2] == "in":
                if d[3] == "group":
                    g = db.query(Groups).filter_by(identifier=d[4]).first()
                    if not g:
                        raise abort(404)
                    for e in db.query(Elements).filter_by(group_id=g.id).all():
                        z += e.fingerprint + " : " + e.machine_name + " / " + e.ip_address_local + "\n"
                    results["result"] = z
                    return jsonify(results), 200
    elif d[0] == "describe":
        #3. describe element asfWasFasfA
        if d[1] == "element":
            e = db.query(Elements).filter_by(fingerprint=d[2]).first()
            if not e:
                raise abort(404)
            z += e.fingerprint + " : " + e.machine_name + " / " + e.ip_address_local + "\n"
            results["result"] = z
            return jsonify(results), 200
        #4. describe machine #####
        elif d[1] == "machine":
            e = db.query(Elements).filter_by(machine_name=d[2]).first()
            if not e:
                raise abort(404)
            z += e.fingerprint + " : " + e.machine_name + " / " + e.ip_address_local + "\n"
            results["result"] = z
            return jsonify(results), 200
    elif d[0] == "list":
        #5. list elements in group AGasfasfASFAS have warning (above 0)
        #6. list warnings in element ASavASVAsfas (above 0)
        #7. list warnings in machine WS-LDONGHOE (above 0)
        pass
    elif d[0] == "report":
        #8. report machine #####
        #9. report element #####
        pass
    raise abort(404)