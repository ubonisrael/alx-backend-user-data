#!/usr/bin/env python3
"""Auth Class Module"""
from flask import request
from typing import List, TypeVar


class Auth:
    """A class to manage API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """checks if a path requires auth"""
        return False

    def authorization_header(self, request=None) -> str:
        """checks authorization header"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """checks the current user"""
        return None
