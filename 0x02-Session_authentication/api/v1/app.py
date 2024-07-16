#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
auth = os.getenv('AUTH_TYPE')
if auth:
    from api.v1.auth.auth import Auth
    from api.v1.auth.basic_auth import BasicAuth
    from api.v1.auth.session_auth import SessionAuth
    from api.v1.auth.session_exp_auth import SessionExpAuth
    from api.v1.auth.session_db_auth import SessionDBAuth
    if auth == 'basic_auth':
        auth = BasicAuth()
    elif auth == 'session_auth':
        auth = SessionAuth()
    elif auth == 'session_exp_auth':
        auth = SessionExpAuth()
    elif auth == 'session_db_auth':
        auth = SessionDBAuth()
    else:
        auth = Auth()

auth_list = ['/api/v1/status/', '/api/v1/unauthorized/',
             '/api/v1/forbidden/', '/api/v1/auth_session/login/']


@app.before_request
def before_request():
    """filters requests"""
    if auth:
        if auth.require_auth(request.path, auth_list):
            user = auth.current_user(request)
            if auth.authorization_header(request) is None:
                if auth.session_cookie(request) is None:
                    return None, abort(401)
            if user is None:
                raise abort(403)
            request.current_user = user


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=True)
