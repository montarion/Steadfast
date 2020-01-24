import json

import bcrypt

from model.User import User
from repositories.UserRepository import UserRepository


class UserService(object):
    def __init__(self):
        self.__userRepository = UserRepository()

    def register(self, email, password, username):
        """
        Register the user
        :param email:
        :param password:
        :param username:
        :return string:
        """
        user = self.__userRepository.get_by_id(email)
        if not user:
            try:
                new_user = User(email, username, bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode("utf-8"))
                added_user = self.__userRepository.add(new_user)
                auth_token = added_user.encode_auth_token()
                response_object = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token.decode()
                }
                return json.dumps(response_object)
            except Exception as e:
                response_object = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return json.dumps(response_object)
        else:
            response_object = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return json.dumps(response_object)

    def login(self, email, password):
        try:
            user = self.__userRepository.get_by_id(email)
            user = User(user['email'], user['username'], user['password'])
            if user and bcrypt.checkpw(password.encode(), user.password.encode()):
                auth_token = user.encode_auth_token()
                response_object = {
                    'status': 'success',
                    'message': 'Successfully logged in.',
                    'auth_token': auth_token.decode()
                }
                return json.dumps(response_object)
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'User does not exist.'
                }
                return json.dumps(response_object)
        except Exception as e:
            print(e)
            response_object = {
                'status': 'fail',
                'message': 'Try again'
            }
            return json.dumps(response_object)

    def get_user_details(self, auth_header):
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = self.__userRepository.get_by_id(resp)  # resp==email==id
                response_object = {  # the user-object details go in here
                    'status': 'success',
                    'data': {
                        'email': user.email,
                        'username': user.username
                    }
                }
                return json.dumps(response_object)
            response_object = {
                'status': 'fail',
                'message': resp
            }
            return json.dumps(response_object)
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return json.dumps(response_object)
