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


from bite.mvc import Controller
from bite.routing import POST,GET,route
from bite.auth import authorize


class TestController(Controller):

    def __init__(self):
        print("Test Controller Initialized")
        super(self.__class__, self).__init__()

    @authorize()
    def index(self):
        print("Test.Index Method called")
        return self.ok({"message":"result"})

    def action1(self, id):
        print("Test.Action1 GET Method called")
        print("ID: {0}".format(id))
        return self.bad_request('bad request message')

    @POST
    @route('another')
    def action2(self, dto):
        print("Test.Action2 POST Method called")
        print(dto)

class Test2Controller(Controller):

    def __init__(self):
        print("Test2 Controller Initialized")
        super(self.__class__, self).__init__()

    def index(self):
        print("Test2.Index Method called")
        return self.ok({"message":"test2 index called"})

    def action2(self, action_param2):
        print("Test2.Action2 Method called")
        return self.ok({"message":"test2 action 2 called"})
