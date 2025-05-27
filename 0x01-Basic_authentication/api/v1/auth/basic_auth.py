#!/usr/bin/env python3
"""Basic Authentication"""
import base64
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """Basic Auth class"""

    def extract_base64_authorization_header
    (self, authorization_header: str) -> str:
        """Extracts base64 part from header"""
        if not authorization_header or not isinstance
        (authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header
    (self, base64_authorization_header: str) -> str:
        """Decodes base64 string"""
        if not base64_authorization_header or not isinstance
        (base64_authorization_header, str):
            return None
        try:
            decoded = base64.b64decode(base64_authorization_header)
            return decoded.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials
    (self, decoded_base64_authorization_header: str) -> (str, str):
        """Extract user credentials"""
        if not decoded_base64_authorization_header or not isinstance
        (decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials
    (self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Finds user instance based on credentials"""
        if not user_email or not isinstance(user_email, str):
            return None
        if not user_pwd or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({"email": user_email})
            if not users:
                return None
            user = users[0]
            if not user.is_valid_password(user_pwd):
                return None
            return user
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves user from request"""
        auth_header = self.authorization_header(request)
        if not auth_header:
            return None
        base64_part = self.extract_base64_authorization_header(auth_header)
        decoded = self.decode_base64_authorization_header(base64_part)
        email, pwd = self.extract_user_credentials(decoded)
        return self.user_object_from_credentials(email, pwd)
