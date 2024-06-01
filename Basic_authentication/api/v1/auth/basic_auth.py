#!/usr/bin/env python3
"""
Basic auth class
"""

from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """ BasicAuth class
    """

    def extract_base64_authorization_header(
            self,
            authorization_header: str
            ) -> str:
        """extract base64 auth header"""
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str
            ) -> str:
        """decode base64 auth header"""
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            return base64.b64decode(
                base64_authorization_header).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
            ) -> (str, str):
        """extract user credentials"""
        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) is not str:
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        return tuple(decoded_base64_authorization_header.split(':', 1))


    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """user object from credentials"""
        if user_email is None or not isinstance(user_email, str):
            print("Invalid email: None or not a string")
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            print("Invalid password: None or not a string")
            return None

        users = User.search({'email': user_email})

        if not users:
            print(f"No users found with email: {user_email}")
            return None
        if users is None or len(users) == 0:
            print(f"No users found with email (empty list): {user_email}")
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                print(f"User found: {user}")
                return user
        
        print("No valid user found")
        return None


    def current_user(self, request=None) -> TypeVar('User'):
        """current user"""
        header = self.authorization_header(request)
        if header is None:
            return None
        b64 = self.extract_base64_authorization_header(header)
        if b64 is None:
            return None
        decoded = self.decode_base64_authorization_header(
            b64)
        if decoded is None:
            return None
        user_info = self.extract_user_credentials(
            decoded)
        if user_info is None:
            return None
        email, pwd = user_info
        user = self.user_object_from_credentials(email, pwd)
        return user
