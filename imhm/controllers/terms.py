# -*- coding:utf-8 -*-
from flask import Blueprint, current_app

terms_blueprint = Blueprint(__name__, 'terms', url_prefix='/terms')

@terms_blueprint.route("/", methods=["GET"])
def hello():
	return "hello"

@terms_blueprint.route('/ktclub/', methods=['GET'])
def get_terms_kt():
	return current_app.send_static_file('terms/ktclub.txt')