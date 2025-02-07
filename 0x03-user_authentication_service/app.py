#!/usr/bin/env python3
"""Flask app module"""
from flask import Flask, jsonify, request, abort, redirect
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


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def user_logout():
    """logs out a user"""
    session_id = request.cookies.get('session_id')
    if session_id is None:
        raise abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    raise abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """finds and returns a user"""
    session_id = request.cookies.get('session_id')
    if session_id is None:
        raise abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": f"{user.email}"})
    raise abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def reset_password():
    """generates a reset token for an email if it exists"""
    payload = dict(request.form)
    e = payload['email']
    try:
        tok = AUTH.get_reset_password_token(e)
        return jsonify({"email": f"{e}", "reset_token": f"{tok}"}), 200
    except ValueError:
        raise abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """generates a reset token for an email if it exists"""
    payload = dict(request.form)
    e = payload['email']
    tok = payload['reset_token']
    new_pw = payload['new_password']
    try:
        tok = AUTH.update_password(reset_token=tok, password=new_pw)
        return jsonify({"email": f"{e}", "message": "Password updated"}), 200
    except ValueError:
        raise abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
