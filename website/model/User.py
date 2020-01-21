from datetime import datetime, timedelta

import jwt


class User(object):
    def __init__(self, email, password, username):
        self.email = email
        self.password = password
        self.username = username

    def encode_auth_token(self):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=0, seconds=5),
                'iat': datetime.utcnow(),
                'sub': self.email,  # the user-id
                'usr': self.username
            }
            return jwt.encode(
                payload,
                "SUPER_SECRET_KEY",
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, "SUPER_SECRET_KEY")
            return payload['sub']  # sub==email
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
