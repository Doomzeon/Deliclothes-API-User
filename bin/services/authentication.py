import jwt
import datetime
from bin.utils.data_classes import Customer

class Jwt:
    def __init__(self):
        pass
    
    def encode_auth_token(self, customer:Customer):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'email': customer.email
            }
            return jwt.encode(
                payload,
                'doomzeon',
                #app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e
    
    
    def decode_auth_token(self, auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, 'doomzeon')
            return payload['email']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'