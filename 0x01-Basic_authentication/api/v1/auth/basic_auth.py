#!/usr/bin/env python3
"""Auth Class Module"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """provides basic auth"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        returns the Base64 part of the Authorization
        header for a Basic Authentication
        """
        if authorization_header is None or type(authorization_header) != str:
            return None
        if authorization_header.startswith('Basic ') is False:
            return None
        return authorization_header.split(' ')[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        returns the decoded value of a Base64
        string base64_authorization_header
        """
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) != str:
            return None
        try:
            decoded_value = base64.b64decode(base64_authorization_header)
            return decoded_value.decode('utf-8')
        except Exception as e:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        returns the user email and password
        from the Base64 decoded value.
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) != str:
            return None, None
        if decoded_base64_authorization_header.find(':') == -1:
            return None, None
        user_email = decoded_base64_authorization_header.split(':')[0]
        user_passwd = decoded_base64_authorization_header.split(':')[1]
        return user_email, user_passwd

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """returns the User instance based on his email and password."""
        if user_email is None or type(user_email) != str:
            return None
        if user_pwd is None or type(user_pwd) != str:
            return None
        users = User.search({'email': user_email})
        if len(users) == 0:
            return None
        user = users[0]
        if user is None:
            return None
        if user.is_valid_password(user_pwd) is False:
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """overloads Auth and retrieves the User instance for a request"""
        auth_h = self.authorization_header(request)
        b64_auth_h = self.extract_base64_authorization_header(auth_h)
        decoded_header = self.decode_base64_authorization_header(b64_auth_h)
        user_cred = self.extract_user_credentials(decoded_header)
        return self.user_object_from_credentials(user_cred[0], user_cred[1])
