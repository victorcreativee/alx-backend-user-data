#!/usr/bin/env python3
"""API entry point with error handlers and request filter"""

from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from api.v1.views import app_views
from os import getenv
from models import storage

# Dynamically import the correct Auth class
auth = None
auth_type = getenv("AUTH_TYPE")

if auth_type == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif auth_type == "session_auth":
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()
else:
    from api.v1.auth.auth import Auth
    auth = Auth()

app = Flask(__name__)
CORS(app)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """ Remove SQLAlchemy session """
    storage.close()


@app.before_request
def before_request():
    """ Filter each request before processing """
    if auth is None:
        return

    excluded_paths = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/',
        '/api/v1/auth_session/login/'
    ]

    if not auth.require_auth(request.path, excluded_paths):
        return

    if (auth.authorization_header(request) is None and
            auth.session_cookie(request) is None):
        abort(401)

    request.current_user = auth.current_user(request)
    if request.current_user is None:
        abort(403)


@app.errorhandler(401)
def unauthorized(error):
    """Return JSON for 401 Unauthorized"""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error):
    """Return JSON for 403 Forbidden"""
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(404)
def not_found(error):
    """Return JSON for 404 Not Found"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = int(getenv("API_PORT", "5000"))
    app.run(host=host, port=port, threaded=True)
