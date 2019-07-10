from flask import request
from functools import wraps
import jwt
import datetime
from app import app


def token_required(f):
    """
    Decorator function to ensure that a resource is access by only authenticated users`
    provided their auth tokens are valid
    :param f:
    :return:
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return {
                    'status': 'failed',
                    'message': 'Provide a valid auth token'
                }, 403

        if not token:
            return {
                'status': 'failed',
                'message': 'Token is missing'
            }, 401

        try:
            decode_response = decode_auth_token(token)
        except:
            message = 'Invalid token'
            if isinstance(decode_response, str):
                message = decode_response
            return {
                'status': 'failed',
                'message': message
            }, 401

        return f(decode_response, *args, **kwargs)
        #return f(current_user, *args, **kwargs)

    return decorated_function


def create_token(name):
    """
    Encode the Auth token
    :param name: name
    :return:
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=app.config.get('AUTH_TOKEN_EXPIRY_DAYS'),
                                                                    seconds=app.config.get(
                                                                        'AUTH_TOKEN_EXPIRY_SECONDS')),
            'iat': datetime.datetime.utcnow(),
            'sub': name
        }
        return jwt.encode(
            payload,
            app.config['SECRET_KEY'],
            algorithm='HS256'
        )
    except Exception as e:
        return e

def decode_auth_token(token):
    """
    Decoding the token to get the payload and then return the user Id in 'sub'
    :param token: Auth Token
    :return:
    """
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired, Please sign in again'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please sign in again'

def response(status, message, status_code):
    """
    Helper method to make an Http response
    :param status: Status
    :param message: Message
    :param status_code: Http status code
    :return:
    """
    #print('STATUS', status)
    #print('MESSAGE', message)
    return {'status': status, 
        'message': message
        }, status_code


def response_auth(status, message, token, status_code):
    """
    Make a Http response to send the auth token
    :param status: Status
    :param message: Message
    :param token: Authorization Token
    :param status_code: Http status code
    :return: Http Json response
    """
    return {'status': status, 
        'message': message, 
        'auth_token': token.decode("utf-8")
        }, status_code

def check_key(key):
    if key == app.config['MASTER_KEY']:
        return True
    return False