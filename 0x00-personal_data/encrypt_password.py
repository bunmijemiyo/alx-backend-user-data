#!/usr/bin/env python3
"""
Password Hashing and validation.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hash password string using bcrypt
    params:
        - password (str): password string to be hashed
    return:
        - (bytes): hashed password
    """
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    validate password.
    params:
        - hashed_password (bytes): bcrypt hashed password
        - password (str): plain password string
    return:
        - (bool): True if password match else False
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
