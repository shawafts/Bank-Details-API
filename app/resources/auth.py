#from app.models import db, User, BlackListToken
from app.resources.helper import response, response_auth, token_required, create_token, check_key
from sqlalchemy import exc
import re
from flask_restful import Resource
from flask import request

class NewToken(Resource):
    """
    Resource to register a user via the api
    """

    def post(self):
        """
        Register a user, generate their token and add them to the database
        :return: Json Response with the user`s token
        """
        if request.content_type == 'application/json':
            post_data = request.get_json()
            name = post_data.get('name')
            key = post_data.get('key')
            if not name or len(name) < 4:
                return response('failed', 'Missing name or name is less than 4 characters', 400)
            if not key:
                return response('failed', 'Missing key: Key is required to generate new token', 400)
            if not check_key(key):
                return response('failed', 'Key provided is invalid', 400)
            token = create_token(name)
            print("Token Type:", type(token))
            print("Token:", token)
            return response_auth('success', 'Successfully created token', token, 201)
        return response('failed', 'Content-type must be json', 400)

