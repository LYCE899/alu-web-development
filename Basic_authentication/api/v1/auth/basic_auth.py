#!/usr/bin/env python3
"""
Classe d'authentification basique
"""

from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User
import logging

# Configurer la journalisation
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("BasicAuth")

class BasicAuth(Auth):
    """ Classe BasicAuth
    """

    def extract_base64_authorization_header(
            self,
            authorization_header: str
            ) -> str:
        """extraire l'en-tête d'autorisation base64"""
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
        """décoder l'en-tête d'autorisation base64"""
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            return base64.b64decode(
                base64_authorization_header).decode('utf-8')
        except Exception as e:
            logger.error(f"Erreur lors du décodage : {e}")
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
            ) -> (str, str):
        """extraire les identifiants de l'utilisateur"""
        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) is not str:
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str
            ) -> TypeVar('User'):
        """objet utilisateur à partir des identifiants"""
        # Vérifie si l'email de l'utilisateur est None ou n'est pas une chaîne
        if user_email is None or type(user_email) is not str:
            return None
        # Vérifie si le mot de passe de l'utilisateur est None ou n'est pas une chaîne
        if user_pwd is None or type(user_pwd) is not str:
            return None

        logger.debug(f"Recherche d'utilisateur avec l'email : {user_email}")
        # Recherche des utilisateurs avec l'email donné
        users = User.search({'email': user_email})
        
        logger.debug(f"Utilisateurs trouvés : {users}")

        # Si aucun utilisateur n'est trouvé, retourne None
        if not users or len(users) == 0:
            return None

        # Vérifie le mot de passe pour chaque utilisateur trouvé
        for user in users:
            logger.debug(f"Vérification du mot de passe pour l'utilisateur : {user}")
            if user.is_valid_password(user_pwd):
                return user
        # Si aucun utilisateur n'a un mot de passe valide, retourne None
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """utilisateur actuel"""
        header = self.authorization_header(request)
        if header is None:
            return None
        b64 = self.extract_base64_authorization_header(header)
        if b64 is None:
            return None
        decoded = self.decode_base64_authorization_header(b64)
        if decoded is None:
            return None
        user_info = self.extract_user_credentials(decoded)
        if user_info is None:
            return None
        email, pwd = user_info
        user = self.user_object_from_credentials(email, pwd)
        return user
