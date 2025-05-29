#!/usr/bin/env python3
""" Session authentication module """

from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """Session authentication logic"""
    user_id_by_session_id = {}


    def create_session(self, user_id: str = None) -> str:
        """Create session ID for a user_id"""
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id


    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Get user ID from session ID"""
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)


    def current_user(self, request=None):
        """Get User instance from session ID in request"""
        from models.user import User
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)


    def destroy_session(self, request=None) -> bool:
        """Destroy user session"""
        session_id = self.session_cookie(request)
        if request is None or session_id is None:
            return False
        if self.user_id_by_session_id.get(session_id) is None:
            return False
        del self.user_id_by_session_id[session_id]
        return True
