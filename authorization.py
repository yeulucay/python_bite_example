"""
Authorization layer of the application
"""
from bite.auth import AuthBase


class Authorization(AuthBase):

    def __init__(self):
        print('Authorization initialized')
        super(self.__class__, self).__init__()
    
    def user_credentials(self, username, password):
        """
        username and password inputs 
        from token request post body
        """

        self.valid_user = True # currently it grants the user

    def client_credentials(self, client_id, client_secret):
        """
        client_id and client_secret inputs 
        from token request Authorization header, Basic Authorization
        """

        self.valid_client = True # currently it grants the client