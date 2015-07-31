# -*- coding:utf-8 -*-
from flask import Blueprint, current_app

base_blueprint = Blueprint(__name__, 'terms')


@base_blueprint.route("/", methods=["GET"])
def hello():
    return "hello"


@base_blueprint.route('/ktclub/', methods=['GET'])
def get_terms_kt():
    return current_app.send_static_file('terms/ktclub.txt')
