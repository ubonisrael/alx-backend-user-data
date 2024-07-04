#!/usr/bin/env python3
"""contains the encryption functions"""
from bcrypt import checkpw, gensalt, hashpw


def hash_password(password: str) -> bytes:
    """hashes a password and returns the result"""
    return hashpw(password.encode('utf-8'), gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """checks if a password is valid"""
    return checkpw(password.encode('utf-8'), hashed_password)
