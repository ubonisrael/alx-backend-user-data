#!/usr/bin/env python3
""" Module of Index views
"""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'],
                 strict_slashes=False)
def session_login() -> str:
    """ logs in a user using session auth
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None:
        return jsonify({"error": "email missing"}), 400
    if password is None:
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({'email': email})
    except Exception as e:
        return jsonify({"error": "no user found for this email"}), 404
    if len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            response = jsonify(user.to_json())
            response.set_cookie(os.getenv('SESSION_NAME'), session_id)
            return response
    return jsonify({"error": "wrong password"}), 401
