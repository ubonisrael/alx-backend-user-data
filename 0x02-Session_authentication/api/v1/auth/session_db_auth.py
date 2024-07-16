#!/usr/bin/env python3
"""SessionDBAuth Class Module"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta
import os


class SessionDBAuth(SessionExpAuth):
    """provides sessiondb auth"""
    def create_session(self, user_id: str = None) -> str:
        """creates a session id for a user_id"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        user_session = UserSession(session_id=session_id, user_id=user_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ returns a User ID based on a Session ID"""
        if session_id is None:
            return None
        user_sessions = UserSession.search({'session_id': session_id})
        if len(user_sessions) == 0:
            return None
        user_session_obj = user_sessions[0]
        user_session = user_sessions[0].to_json()
        if self.session_duration <= 0:
            return user_session['user_id']
        if 'created_at' not in user_session:
            return None
        created_at = user_session_obj.created_at
        expiration_time = timedelta(seconds=self.session_duration) + created_at
        current_time = datetime.now()
        print(created_at)
        print(expiration_time)
        print(current_time)
        if current_time > expiration_time:
            return None
        return user_session['user_id']

    def destroy_session(self, request=None):
        """deletes the user session / logout"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_sessions = UserSession.search({'session_id': session_id})
        if len(user_sessions) == 0:
            return None
        user_session = user_sessions[0]
        user_session.remove()
        return True
