#!/usr/bin/env python3
"""Defines simple routes"""
from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def status():
    """Returns status"""
    return jsonify({"status": "OK"})


@app_views.route('/unauthorized', methods=['GET'])
def unauthorized():
    """Raises 401 error"""
    abort(401)


@app_views.route('/forbidden', methods=['GET'])
def forbidden():
    """Raises 403 error"""
    abort(403)
