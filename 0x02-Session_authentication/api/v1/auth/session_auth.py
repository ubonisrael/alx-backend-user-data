#!/usr/bin/env python3
"""Session Auth Class Module"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class SessionAuth(Auth):
    """provides session auth"""
    pass
