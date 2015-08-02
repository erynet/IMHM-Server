# -*- coding:utf-8 -*-
from flask import Blueprint, current_app, jsonify

base_blueprint = Blueprint(__name__, 'terms')


@base_blueprint.route("/hello/", methods=["GET"])
def hello():
    results = {}
    results["reply"] = "Hello, World!"
    return jsonify(results), 200


@base_blueprint.route('/ktclub/', methods=['GET'])
def get_terms_kt():
    return current_app.send_static_file('terms/ktclub.txt')
