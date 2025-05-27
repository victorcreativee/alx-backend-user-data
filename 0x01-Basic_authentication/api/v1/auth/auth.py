#!/usr/bin/env python3
"""Template for all authentication systems"""
from flask import request
from typing import List, TypeVar

User = TypeVar('User')


class Auth:
    """Authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if path requires auth"""
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if path[-1] != '/':
            path += '/'
        for ep in excluded_paths:
            if path == ep:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Returns Authorization header"""
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> User:
        """Get current user (stub)"""
        return None
