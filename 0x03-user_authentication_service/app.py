#!/usr/bin/env python3
"""Flask app module"""
from flask import Flask, jsonify, request, abort
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def home():
    """returns homepage"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def user_signup():
    """signs up a user"""
    payload = dict(request.form)
    try:
        AUTH.register_user(payload['email'], payload['password'])
        return jsonify({"email": f"{payload['email']}",
                        "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def user_login():
    """authenticates a user"""
    payload = dict(request.form)
    email = payload['email']
    passwd = payload['password']
    if AUTH.valid_login(email, passwd):
        session_id = AUTH.create_session(email)
        response = jsonify({"email": f"{email}", "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response
    raise abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
