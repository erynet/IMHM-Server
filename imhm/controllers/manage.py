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
#@event_blueprint.route("/event/", methods=["GET"])
#@login_required

