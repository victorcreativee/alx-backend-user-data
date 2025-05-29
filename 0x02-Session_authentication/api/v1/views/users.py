#!/usr/bin/env python3
"""Users view"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users():
    """ GET /api/v1/users """
    users = [user.to_json() for user in User.all()]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def user_by_id(user_id):
    """ GET /api/v1/users/<user_id> or /users/me """
    if user_id == "me":
        if request.current_user is None:
            abort(404)
        return jsonify(request.current_user.to_json())

    user = User.get(user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_json())
