#!/usr/bin/env python3
"""Session Auth Class Module"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User
from uuid import uuid4


class SessionAuth(Auth):
    """provides session auth"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a session id for a user_id"""
        if user_id is None or type(user_id) != str:
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id
