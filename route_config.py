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


route_config file
"""
from bite.routing import RouteMap

map = RouteMap()

map.add({
    "name":"blog",
    "template":"/blog/test/{id}",
    "default":{"controller":"Test","action":"Action1"}
})
"""
map.add({
    "name":"only_index",
    "template":"/api/{controller}/Index",
    "default":{"action":"Index"}
})

map.add({
    "name":"only_test",
    "template":"/api/test_static/{action}",
    "default":{"controller":"Test"}
})
"""
map.add({
    "name":"default",
    "template":"/api/{controller}/{action}"
})

# no need to place default controller and action if {controller} and {action} does not exist
