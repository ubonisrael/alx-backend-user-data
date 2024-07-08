#!/usr/bin/env python3
"""Auth Class Module"""
from api.v1.auth.auth import Auth
import base64


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
