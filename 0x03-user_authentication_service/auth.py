#!/usr/bin/env python3
"""Auth class and helper functions module"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid
from typing import Union


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """searches for a user and returns one if any"""
        user = self._db._session.query(User).filter_by(email=email).first()
        if user is not None:
            raise ValueError(f"User {email} already exists")
        hashed_passwd = _hash_password(password)
        user = self._db.add_user(email=email, hashed_password=hashed_passwd)
        return user

    def valid_login(self, email: str, password: str) -> bool:
        """validates a login attempt"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
            return True
        return False

    def create_session(self, email: str) -> str:
        """returns the session ID as a string"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            setattr(user, 'session_id', session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        takes a single session_id string argument and
        returns the corresponding User or None
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None


def _hash_password(password: str) -> bytes:
    """takes in a password and returns bytes"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """returns a uuid"""
    return str(uuid.uuid4())
