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


MVC module
"""

import json

class Request():
    host = None
    path = None
    headers = {}

    def __init__(self):
        pass


class Controller():
    """
    Controller base class
    """
    request = None
    auth_secret = ''

    def __init__(self):
        pass

    def ok(self, result = None):
        return '200 OK', 'application/json', json.dumps(result)

    def created(self, result = None):
        return "201 Created", 'application/json', json.dumps(result)

    def bad_request(self, message = None):
        return "400 Bad Request",'text/plain', message

    def unauthorized(self, message = None):
        return "401 Unauthorized", 'text/plain', message

    def not_found(self, message = None):
        return "404 Not Found", 'text/plain', message

    def internal_server_error(self, message = None):
        return "500 Internal Server Error",'text/plain' , message

    def json(self, code, result = None):
        return str(code), 'application/json', json.dumps(result)
