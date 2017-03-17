"""
Authorization layer of the application
"""
from bite.auth import AuthBase


class Authorization(AuthBase):

    def __init__(self):
        print('Authorization initialized')
        super(self.__class__, self).__init__()
    
    def user_credentials(self, username, password):
        self.valid_user = True

    def client_credentials(self, client_id, client_secret):
        self.valid_client = True