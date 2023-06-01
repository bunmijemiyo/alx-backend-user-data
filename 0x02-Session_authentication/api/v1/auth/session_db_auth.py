#!/usr/bin/env python3
"""
SessionDBAuth class
"""
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """ Session Authentication, Expirable and storage support. """
    def create_session(self, user_id=None):
        """
        Creates and stores Authentication Session for User
        Return:
            - session_id (str): User's generated session ID
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        kwargs = {
            'user_id': user_id,
            'session_id': session_id
        }
        user_session = UserSession(**kwargs)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieves `user_id` by requesting UserSession
        in the database based on `session_id`
        """
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(sessions) <= 0:
            return None
        if sessions[0].created_at + \
                timedelta(seconds=self.session_duration) < datetime.utcnow():
            return None
        return sessions[0].user_id

    def destroy_session(self, request=None):
        """ Destroys Authentication session. """
        session_id = self.session_cookie(request)
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False
        if len(sessions) <= 0:
            return False
        sessions[0].remove()
        return True
