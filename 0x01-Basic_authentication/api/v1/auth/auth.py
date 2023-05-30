#!/usr/bin/env python3
""" Authentication Module."""
from flask import request
from typing import List, TypeVar


class Auth:
    """ Manage API Authentication """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Checks if a path requires authentication. """
        if path is None:
            return True
        if not excluded_paths:
            return True
        if path in excluded_paths:
            return False
        else:
            for paths in excluded_paths:
                if paths.startswith(path):
                    return False
                if path.startswith(paths):
                    return False
                if paths.endswith('*'):
                    if path.startswith(paths[:-1]):
                        return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Checks request header for Authorization. """
        if request is None:
            return None
        header = request.headers.get('Authorization')
        if header is None:
            return None
        else:
            return header

    def current_user(self, request=None) -> TypeVar('User'):
        """ checks current user """
        return None
