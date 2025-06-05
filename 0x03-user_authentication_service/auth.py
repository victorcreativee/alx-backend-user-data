#!/usr/bin/env python3
"""
Auth module for authentication service
"""
import bcrypt
from db import DB
from user import User
from uuid import uuid4
from typing import Union


def _hash_password(password: str) -> bytes:
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generate a new UUID string"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except Exception:
            hashed_pwd = _hash_password(password)
            return self._db.add_user(email, hashed_pwd.decode('utf-8'))

    def valid_login(self, email: str, password: str) -> bool:
        """Check if provided login credentials are valid"""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8'))
        except Exception:
            return False

    def create_session(self, email: str) -> Union[str, None]:
        """Create a new session ID for the user"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Find a user by session ID"""
        if session_id is None:
            return None
        try:
            return self._db.find_user_by(session_id=session_id)
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroy a user session"""
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Generate a reset password token"""
        user = self._db.find_user_by(email=email)
        token = _generate_uuid()
        self._db.update_user(user.id, reset_token=token)
        return token

    def update_password(self, reset_token: str, password: str) -> None:
        """Update password using reset token"""
        user = self._db.find_user_by(reset_token=reset_token)
        hashed = _hash_password(password).decode('utf-8')
        self._db.update_user(user.id, hashed_password=hashed, reset_token=None)
