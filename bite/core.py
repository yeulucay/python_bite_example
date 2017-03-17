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

from wsgiref.simple_server import make_server
from .routing import RouteMap, RouteManager
from .auth import AuthBase, AuthManager
import uuid

class Bite():
    """
    Main class of Python Bite Restful Service Framework
    """

    def __call__(self, env, start_response):
        """
        For each request, __call__ method is called
        It is fired in self.listen method's make_server call. (second parameter: self)
        """        

        # token request
        if self.token_endpoint and env["PATH_INFO"] == self.token_endpoint and self.auth_cls:
            auth_manager = AuthManager(self.auth_cls, self.auth_secret)
            auth_manager.expire_time = self.auth_expire
            auth_header = env['HTTP_AUTHORIZATION'] if 'HTTP_AUTHORIZATION' in env else ''
            status_code, res_type, result = auth_manager.token_endpoint(env['REQUEST_METHOD'], auth_header, env['wsgi.input'], env['CONTENT_LENGTH']) 
        else:
            status_code, res_type, result = self.rm.call_action(self.rm.match(env["PATH_INFO"],env['REQUEST_METHOD']),env)

        response_headers = [('Content-type', res_type)]
        start_response(status_code, response_headers)
        response_body = result

        return [response_body.encode('utf-8')]

    def listen(self, host, port):
        """
        Initialize server and starts to listen

        Keyword arguments:
        host -- application host information
        port -- application port information
        """
        self.rm = RouteManager(self.config.PROJECT_DIR, self.auth_secret)
        self.rm.prepare_routes(self.route_map.route_list)

        httpd = make_server(host, port, self)
        httpd.serve_forever()

    def config(self, config):
        """
        Sets the application configuration.

        Keyword arguments:
        config -- config module including PROJECT_DIR variable
        """
        self.config = config
        self.auth_secret = config.AUTH_SECRET if hasattr(config,'AUTH_SECRET') else str(uuid.uuid4())
        

    def route_config(self, route_map):
        """
        Sets the route configuration.

        Keyword arguments:
        route_map -- RouteMap object instance
        """
        self.route_map = route_map
        
    def use_auth(self, auth_cls):
        """
        Sets the authorization middleware

        Keyword arguments:
        auth_obj -- AuthBase subclass instance
        """
        if issubclass(auth_cls, AuthBase):
            self.auth_cls = auth_cls
        else:
            #TODO: throw exception: not AuthBase subclass
            pass

        self.token_endpoint = self.config.TOKEN_ENDPOINT if hasattr(self.config, 'TOKEN_ENDPOINT') else '/auth/token'
        # auth expire time in minutes. if TOKEN_EXPIRE not set in config file then 20 min is default
        self.auth_expire = self.config.TOKEN_EXPIRE if hasattr(self.config,'TOKEN_EXPIRE') else 20


        