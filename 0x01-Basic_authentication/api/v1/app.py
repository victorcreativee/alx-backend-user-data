#!/usr/bin/env python3
"""API entry point with error handlers and request filter"""
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from api.v1.views import app_views  # 👈 Make sure this line is at the top
import os

app = Flask(__name__)
CORS(app)
app.register_blueprint(app_views)  # 👈 This line is often forgotten


# Error handlers
@app.errorhandler(401)
def unauthorized(error):
    """Return JSON for 401 Unauthorized"""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error):
    """Return JSON for 403 Forbidden"""
    return jsonify({"error": "Forbidden"}), 403


# before_request logic (you can keep this part if needed)
@app.before_request
def before_request():
    """Filter each request before processing"""
    if auth is None:
        return
    excluded =
    ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']
    if not auth.require_auth(request.path, excluded):
        return
    if auth.authorization_header(request) is None:
        abort(401)
    if auth.current_user(request) is None:
        abort(403)


# Auth handling
auth = None
if os.getenv("AUTH_TYPE") == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif os.getenv("AUTH_TYPE") == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()

# Run app
if __name__ == "__main__":
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "5000"))
    app.run(host=host, port=port)
