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

from bite.core import Bite
import config, route_config
from authorization import Authorization

# Bite instance
app = Bite()

# routing configuration 
app.route_config(route_config.map)

# application configuration
app.config(config)

# authorization 
app.use_auth(Authorization)

# listen requests
app.listen('localhost',7000)
