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


class HomeController(Controller):

    def __init__(self):
        print("Home Controller Initialized")
        super(self.__class__, self).__init__()

    def index(self):
        print("Home.Index Method called")
        return self.ok({"message":"hello world!"})
