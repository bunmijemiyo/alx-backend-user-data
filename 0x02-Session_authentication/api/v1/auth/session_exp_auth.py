#!/usr/bin/env python3
""" SessionExpAuth class. """
from os import getenv
from datetime import datetime, timedelta
from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """
    Adds an expiration time to a session ID
    """
    def __init__(self):
        """ Initialize SessionExpAuth class """
        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id):
        """
        Create Session for a user
        params:
            - user_id (str): user's ID
        return:
            - session_id (str): session ID for the user.
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Returns a user ID based on Session ID """
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id.keys():
            return None
        user_info = self.user_id_by_session_id.get(session_id)
        if self.session_duration <= 0:
            return user_info.get('user_id')
        if 'created_at' not in user_info.keys():
            return None
        if user_info.get('created_at') + \
                timedelta(seconds=self.session_duration) < datetime.now():
            return None
        return user_info.get('user_id')
