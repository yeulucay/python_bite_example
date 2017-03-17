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

import os, sys, inspect, glob, re, types
import importlib
import controllers
from bite.mvc import Controller
from .mvc import Request


class RouteMap():

    def __init__(self):
        self.route_list = []

    def add(self, route):
        self.route_list.append(route)


class RouteManager():

    def __init__(self, project_dir):
        self.proj_dir = project_dir
        self.route_list = []

    def prepare_routes(self, route_map):
        """
        Initialize routing list.
        Requires RouteMap instance as parameter
        """

        module = None
        controllers = []

        for f in glob.glob(os.path.join(self.proj_dir,"controllers/*.py")):

            name = os.path.splitext(os.path.basename(f))[0] # file_name
            module = importlib.import_module("." + name,package="controllers")

            for member in dir(module):
                attr = getattr(module,member)
                if attr and inspect.isclass(attr) and attr is Controller:
                    # here, attr is Controller base class
                    for sub in attr.__subclasses__():

                        if "controller" not in sub.__name__.lower():
                            # TODO: here throw exception
                            continue

                        if sub not in controllers:
                            controllers.append(sub)

        for route in route_map:

            if route["template"] is None:
                # TODO: here throw exception
                continue

            template = route["template"]
            template_name = route["name"]
            #template parameters
            tmp_p = re.findall(r'\{[a-zA-Z0-9]+\}', template)

            query_p = []# query parameters will be added to route_list

            for p in tmp_p:
                if not (p == '{controller}' or p == '{action}'):
                    query_p.append(p) # query params added to query_p list

            # For each controller, template will repeat
            if '{controller}' in tmp_p:

                for ctrl in controllers:

                    c_init = ctrl()

                    ctrl_prefix = ctrl.__name__.lower().replace("controller","")

                    if '{action}' in tmp_p:
                        # For each action, template will repeat
                        for action in dir(ctrl):
                            if not action.startswith("__"):

                                a_init = getattr(c_init, action)
                                if not type(a_init) == types.MethodType \
                                    or hasattr(Controller, action):
                                    continue

                                #overload action with route decorator
                                o_action = str(a_init.route) if hasattr(a_init,'route') else action

                                formatted_template = template.format(controller=ctrl_prefix
                                            ,action=o_action.lower())
                                self.route_list.append(
                                    {
                                        "path": formatted_template,
                                        "path_parts":formatted_template.split("/"),
                                        "controller":ctrl,
                                        "action":action,
                                        "query_params":query_p,
                                        'method':str(a_init.method) if hasattr(a_init,'method') else 'GET'
                                    }
                                )
                    else:
                        # There is {controller} but no {action}
                        # Use default action for each controller
                        if route["default"] and route["default"]["action"]:
                            # default action
                            d_action = route["default"]["action"].lower()

                            for action in dir(ctrl):
                                if not action.startswith("__") and d_action == action.lower():

                                    a_init = getattr(c_init, action)
                                    if not type(a_init) == types.MethodType \
                                        or hasattr(Controller, action):
                                        continue

                                    o_action = str(a_init.route) if hasattr(a_init,'route') else action

                                    formatted_template = template.format(controller=ctrl_prefix
                                            ,action=o_action.lower())
                                    self.route_list.append(
                                        {
                                            "path":formatted_template,
                                            "path_parts":formatted_template.split("/"),
                                            "controller":ctrl,
                                            "action":action,
                                            "query_params":query_p,
                                            'method':str(a_init.method) if hasattr(a_init,'method') else 'GET'
                                        }
                                    )
                        else:
                            #TODO: Here throw exception => No default action
                            pass

            elif '{action}' in tmp_p:
                #There is no {controller} but {action} in template
                # Use default controller, repeat for each action in the controller.
                if route["default"] and route["default"]["controller"]:
                    # default controller
                    d_ctrl = route["default"]["controller"].lower()

                    for ctrl in controllers:

                        c_init = ctrl()

                        ctrl_prefix = ctrl.__name__.lower().replace("controller","")

                        if ctrl_prefix == d_ctrl:
                            for action in dir(ctrl):
                                if not action.startswith("__"):

                                    a_init = getattr(c_init, action)
                                    if not type(a_init) == types.MethodType \
                                        or hasattr(Controller, action):
                                        continue

                                    o_action = str(a_init.route) if hasattr(a_init,'route') else action

                                    formatted_template = template.format(controller=ctrl_prefix
                                            ,action=o_action.lower())
                                    self.route_list.append(
                                        {
                                            "path":formatted_template,
                                            "path_parts":formatted_template.split("/"),
                                            "controller":ctrl,
                                            "action":action,
                                            "query_params":query_p,
                                            'method':str(a_init.method) if hasattr(a_init,'method') else 'GET'
                                        }
                                    )
                else:
                    #TODO: here throw Exception => No default controller
                    pass

            else:
                #There is neither {controller} nor {action}
                if route["default"] and route["default"]["controller"] and route["default"]["action"]:
                    #default controller
                    d_ctrl = route["default"]["controller"].lower()
                    #default action
                    d_action = route["default"]["action"].lower()

                    for ctrl in controllers:

                        c_init = ctrl()

                        ctrl_prefix = ctrl.__name__.lower().replace("controller","")

                        if ctrl_prefix == d_ctrl:
                            for action in dir(ctrl):
                                if not action.startswith("__") and d_action == action.lower():

                                    a_init = getattr(c_init, action)
                                    if not type(a_init) == types.MethodType \
                                        or hasattr(Controller, action):
                                        continue

                                    self.route_list.append(
                                        {
                                            "path":template,
                                            "path_parts":template.split("/"),
                                            "controller":ctrl,
                                            "action":action,
                                            "query_params":query_p,
                                            'method':str(a_init.method) if hasattr(a_init,'method') else 'GET'
                                        }
                                    )
                else:
                    #TODO: here throw Exception => No default controller and action
                    pass


        for rl in self.route_list:
            # print all the created route_list
            print(rl)


    def match(self, uri, method):
        """
        Compares the uri with path in the routing list items.
        Initialize the first matched route's controller and calls it's related action.
        """

        uri_parts = uri.split("/")

        for rl in self.route_list:
            if not rl['method'] == method:
                continue

            if len(rl["path_parts"]) == len(uri_parts):
                fitted = True

                for i in range(len(uri_parts)):
                    #i.th path part
                    ithpp = rl["path_parts"][i]
                    if ithpp == uri_parts[i].lower() or \
                        (ithpp is not uri_parts[i] and re.match(r'\{[a-zA-Z0-9]+\}', ithpp)):
                        pass
                    else:
                        fitted = False
                        break
                if fitted:
                    return rl

        return None
        #(x for x in )

    def call_action(self, route, env):
        """
        In case of match, call_action is called.
        Related controller is initialized and the action is called.
        """
        ctrl = route["controller"]

        #initialize controller
        c_init = ctrl()

        #if 'HTTP_AUTHORIZATION'

        action = getattr(c_init, route["action"])
        method = env['REQUEST_METHOD']

        request = Request()
        request.path = env['PATH_INFO']
        request.host = env['HTTP_HOST']

        p = {}

        if method == 'GET' or method == 'DELETE':
            action_params = inspect.getargspec(action).args

            for a in action_params:
                if a is not 'self':
                    p[str(a)] = None

            uri_parts = env["PATH_INFO"].split("/")

            # place route params into method params
            for i in range(len(uri_parts)):
                if re.match(r'\{[a-zA-Z0-9]+\}', route["path_parts"][i]):
                    p_name = route["path_parts"][i].replace("{","").replace("}","")

                    if p_name in p:
                        p[p_name]=uri_parts[i]

            #query string
            qs = env["QUERY_STRING"]

            for key,value in self.parse_params(qs):
                if key in p:
                    p[key] = value

            # set Controller.request
            c_init.request = request
            # call action with GET params
            return action(**p)

        elif method == 'POST' or method == 'PUT':
            body_length = int(env['CONTENT_LENGTH'])
            body_raw = env['wsgi.input'].read(body_length)
            body = body_raw.decode('UTF-8')

            for key, value in self.parse_params(body):
                p[key] = value

            # set Controller.request
            c_init.request = request
            # call action with POST params as object
            return action(p)

        else:
            #TODO: throw 405 method not allowed
            pass

    def parse_params(self, param):
        # param list
        pl = param.split("&")

        if len(pl) > 0:
            for pli in pl: # param list item
                # param pair
                pp = pli.split("=")

                if len(pp) == 2:
                    yield pp[0], pp[1]


def route(r):
    def decorator(action):
        action.route = r
        return action
    return decorator

def GET(action):
    action.method = 'GET'
    return action

def POST(action):
    action.method = 'POST'
    return action

def PUT(action):
    action.method = 'PUT'
    return action

def DELETE(action):
    action.method = 'DELETE'
    return action
