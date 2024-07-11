#!/usr/bin/env python3
"""SessionExpAuth Class Module"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """provides sessionexp auth"""
    def __init__(self) -> None:
        """initialiazes an instance of the class"""
        super().__init__()
        session_duration = os.getenv('SESSION_DURATION', None)
        try:
            self.session_duration = int(session_duration)
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """creates a session id for a user_id"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {'user_id': user_id, 'created_at': datetime.now()}
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ returns a User ID based on a Session ID"""
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        if self.session_duration <= 0:
            return self.user_id_by_session_id[session_id]['user_id']
        if 'created_at' not in self.user_id_by_session_id[session_id]:
            return None
        created_at = self.user_id_by_session_id[session_id]['created_at']
        expiration_time = timedelta(seconds=self.session_duration) + created_at
        current_time = datetime.now()
        if current_time > expiration_time:
            return None
        return self.user_id_by_session_id[session_id]['user_id']
