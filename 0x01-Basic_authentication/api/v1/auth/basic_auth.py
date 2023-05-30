#!/usr/bin/env python3
""" Basic Authentication Module """
import base64
from api.v1.auth.auth import Auth
from typing import TypeVar

from models.user import User


class BasicAuth(Auth):
    """ Manage Basic Authentication """
    def extract_base64_authorization_header(self, authorization_header: str)\
            -> str:
        """ Extracts Authentication details for Basic Authentication
        Return:
            - client encoded Basic Auth details
        """
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.split(' ')[-1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """ Decodes base64 auth """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            auth_str = base64_authorization_header.encode('utf-8')
            auth_str = base64.b64decode(auth_str)
            return auth_str.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """ Extract user credentials from decoded header """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        email = decoded_base64_authorization_header.split(':')[0]
        pwd = decoded_base64_authorization_header[
                decoded_base64_authorization_header.index(':') + 1:]
        return (email, pwd)

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """ Returns User instance but validate user first """
        if not isinstance(user_email, str) or user_email is None:
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
            if not users or users == []:
                return None
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user

            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns User instance
        """
        auth_header = self.authorization_header(request)
        if auth_header is not None:
            base64_auth = self.extract_base64_authorization_header(auth_header)
            if base64_auth is not None:
                decoded = self.decode_base64_authorization_header(base64_auth)
                if decoded is not None:
                    email, pwd = self.extract_user_credentials(decoded)
                    if email is not None:
                        return self.user_object_from_credentials(email, pwd)
        return
