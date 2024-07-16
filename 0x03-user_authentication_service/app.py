#!/usr/bin/env python3
"""Flask app module"""
from flask import Flask, jsonify, request
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def home():
    """returns homepage"""
    return jsonify({"message":"Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def user_signup():
    """signs up a user"""
    payload = dict(request.form)
    try:
        AUTH.register_user(payload['email'], payload['password'])
        return jsonify({"email": f"{payload['email']}", "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
