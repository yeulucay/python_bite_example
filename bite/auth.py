"""
Python Bite Rest Framework is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Python Bite Rest Framework is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Python Bite Rest Framework.  If not, see <http://www.gnu.org/licenses/>.
"""
import jwt, base64, json
from datetime import datetime, timezone, timedelta, tzinfo


class AuthManager():
    """
    Authorization Manager class 
    Manages AuthBase subclasses for token requests
    """
    def __init__(self, auth_cls, auth_secret):
        self.auth_cls = auth_cls   
        self.auth_secret = auth_secret     
    
    def token_endpoint(self, method, auth_header, content, content_length):
        """
        token end point request call manager
        """
        result = {}
        res_type = '400 Bad Request'

        if method == 'POST':
            body_raw = content.read(int(content_length))
            body = body_raw.decode('UTF-8')

            p = {}      
            client_id = ''

            for key, value in self.parse_params(body):
                p[key] = value

            if ('grant_type' in p and 'username' in p and 
                    p['grant_type'] == 'password' and p['username'] != ''):
                # AuthBase subclass initialization
                bite_auth = self.auth_cls()
                bite_auth.user_credentials(
                    p['username'] if 'username' in p else '', 
                    p['password'] if 'password' in p else '')
                
                header_parts = auth_header.strip().split()

                # authorization header exists and basic
                if len(header_parts) == 2 and header_parts[0].lower() == 'basic':
                    decoded_header = base64.b64decode(header_parts[1]).decode('UTF-8')
                    # client_id and client_secret pair
                    isp = decoded_header.split(':') 

                    if len(isp) == 2:
                        client_id = isp[0]
                        bite_auth.client_credentials(isp[0], isp[1])                
                else:
                    # client_credentials are called with empty strings
                    bite_auth.client_credentials('','')
                
                # if valid_client and valid_user
                if bite_auth.is_valid():
                    exp = datetime.utcnow() + timedelta(minutes=20)

                    token_content = {
                        'user': p['username'],
                        'client_id': client_id,
                        'exp': exp
                    }
                    # let user override token. AuthBase.edit_jwt is an overridable method.
                    token_content = bite_auth.edit_jwt(token_content)
                    
                    token = jwt.encode(token_content, self.auth_secret)                    

                    if token:
                        result['token'] = token.decode('UTF-8')
                        result['expire_in'] = exp.isoformat()
                        return '200 OK', 'application/json', json.dumps(result)
                else:
                    res_type = '401 Unauthorized'
                    result['message'] = 'User or client does not have grant.'
            else:
                result['message'] = 'grant_type POST parameter must be set correctly.'        
        else:
            #request type is not POST
            result['message'] = 'POST request must be sent.'

        return res_type, 'application/json', json.dumps(result)

    def parse_params(self, param):
        # param list
        pl = param.split("&")

        if len(pl) > 0:
            for pli in pl: # param list item
                # param pair
                pp = pli.split("=")

                if len(pp) == 2:
                    yield pp[0], pp[1]


class AuthBase():
    """
    Python Bite authorization base class
    """

    valid_user = False
    valid_client = False

    def edit_jwt(self, token):
        """
        To edit JWT before token is created, 
        this method can be overriden
        """
        return token

    def edit_result(self, result):
        """
        To edit token response before it is sent to client, 
        this method can be overriden
        """
        return result

    def user_credentials(self, username, password):
        """
        To handle username and password during token request, 
        this method must be overriden.
        Otherwise, user will never be valid
        """
        print('user_credentials called')

    def client_credentials(self, client_id, client_secret):
        """
        To handle username and password during token request, 
        this method must be overriden.
        Otherwise, user will never be valid
        """
        print('client_credentials called')

    def is_valid(self):
        return self.valid_user and self.valid_client


def authorize(roles=[]):
    """
    authorize decorator for controller actions.
    the method is protected with this way and requires a bearer token 
    bearer token must be in the Authorization header of http request
    """
    def decorator(f):
        def wrapped(self, *args, **kwargs):
            if 'Authorization' in self.request.headers:
                a_split = self.request.headers['Authorization'].strip().split()
                
                if len(a_split) == 2 and a_split[0].lower() == 'bearer':
                    token = a_split[1]                    
                    
                    is_authorized = False

                    try:
                        token_content = jwt.decode(token, self.auth_secret) 
                        is_authorized = True
                    except jwt.ExpiredSignatureError:
                        print('token expired')
                        pass  
                    except jwt.DecodeError:
                        print('token decode error')            
                        pass
                    except jwt.InvalidTokenError:
                        print('invalid token error')
                        pass
                    
                    if not is_authorized:
                        return self.unauthorized('Unauthorized request.')

            return f(self, *args, **kwargs)
        return wrapped
    return decorator