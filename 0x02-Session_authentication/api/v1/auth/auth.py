#!/usr/bin/env python3
"""Auth Class Module"""
from flask import request
from typing import List, TypeVar
import re


class Auth:
    """A class to manage API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """checks if a path requires auth"""
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path[-1] != '/':
            path = path + '/'
        for excluded_path in excluded_paths:
            if excluded_path[-1] == '*':
                excluded_path = re.escape(excluded_path[:-1]) + ".*"
                match = re.match(excluded_path, path)
                if match is not None:
                    return False
            if path == excluded_path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """checks authorization header"""
        if request is None:
            return None
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return None
        return auth_header

    def current_user(self, request=None) -> TypeVar('User'):
        """checks the current user"""
        return None
