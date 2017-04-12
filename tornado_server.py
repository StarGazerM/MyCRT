import os
import socket
import json
import bson.json_util
from concurrent.futures import ThreadPoolExecutor

import motor.motor_tornado
import zmq
from zmq.eventloop import ioloop, zmqstream

ioloop.install()

import tornado
import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.concurrent import run_on_executor

from pycket.session import SessionMixin
from pycket.session import SessionManager


client = motor.motor_tornado.MotorClient('localhost', 27017)
db = client['MyCRT']


class AuthencatedRequiredHandler(tornado.web.RequestHandler, SessionMixin):
    '''
        the base handler for the handler which need session to authencate user
    '''

    def get_current_user(self):
        user = self.session.get('user')
        return user


class MainHandler(AuthencatedRequiredHandler):
    '''
        the home page of the website
    '''

    @tornado.web.authenticated
    def get(self):
        self.write("hello world!")


class RegisterHandler(tornado.web.RequestHandler):
    '''
        the handler used for register
    '''

    def get(self):
        self.render('register.html')

    async def post(self):
        _db = self.settings['db']
        username = self.get_argument('username')
        password = self.get_argument('password')
        user = await _db.user.find_one({'username': username})
        if user is not None:
            self.render('register.html')
        else:
            await db.user.insert_one({'username': username, 'password': password,
                                      'machines': [], 'isOnline': False})
            self.redirect('/login')


class LoginHandler(tornado.web.RequestHandler, SessionMixin):
    '''
        login handler
    '''

    def get(self):
        self.render('login.html', msg='')

    async def post(self):
        _db = self.settings['db']
        username = self.get_argument('username')
        password = self.get_argument('password')
        user = await _db.user.find_one({'username': username, 'password': password})
        if username is not None:
            self.session.set('user', user)
            self.set_secure_cookie('shell_user', username)
            self.redirect('/dashboard')
        else:
            self.render('login.html')


class LogoutHandler(AuthencatedRequiredHandler):
    '''
        logout handler
    '''

    @tornado.web.authenticated
    def get(self):
        self.session.set('user', None)
        self.redirect('/login')


class DashboardHandler(AuthencatedRequiredHandler):
    '''
        the page render for the app's dashboard
    '''

    @tornado.web.authenticated
    def get(self):
        print(self.get_secure_cookie("shell_user"))
        self.render('dashboard.html')


class XtermPageHandler(AuthencatedRequiredHandler):
    '''
        the page render for the web shell app
    '''

    @tornado.web.authenticated
    def get(self):
        self.render('cmd.html')


class ShellHandler(tornado.websocket.WebSocketHandler, SessionMixin):
    '''
        the handler for the websocket request from xterm.js in the front end
    '''

    executor = ThreadPoolExecutor(4)

    def __init__(self, application, request, **kwargs):
        print('init')
        super(ShellHandler, self).__init__(application, request, **kwargs)
        context = zmq.Context()
        self.socket = context.socket(zmq.PAIR)
        self.zstream = None

    def get_current_user(self):
        user = self.session.get("user")
        return user

    def open(self):
        self.current_user = self.get_current_user()
        if not self.current_user:
            self.write_message('please login')
            self.close()
            return
        # default_name = self.get_secure_cookie("shell_user")
        # print(default_name)
        # if not default_name:
        #     self.close()
        #     return
        username = self.get_argument(
            'username', default=self.current_user["username"])
        self.socket.connect('ipc://' + username)
        self.zstream = zmqstream.ZMQStream(self.socket)
        self.zstream.on_recv(self.handle_recv)
        print("ssh opened connected to " + username)

    def on_message(self, message):
        # self.socket.send_string(message)
        self.zstream.send_string(message)

    def on_close(self):
        if self.zstream:
            self.zstream.close()
        print("WebSocket closed")

    def check_origin(self, origin):
        return True

    def handle_recv(self, msgs):
        '''
            handle the message recieved by zmq
        '''
        for m in msgs:
            self.write_message(m)


class ListMachineHandler(AuthencatedRequiredHandler):
    '''
        list the machine can be connect
    '''

    @tornado.web.authenticated
    async def get(self):
        machines = []
        machines.append(self.current_user)
        for m_id in self.current_user['machines']:
            user = await db.user.find_one(m_id)
            # machines.append({'_id': user['_id'], 'username': user['username'],
            #                  'isOnline': user['isOnline']})
            machines.append(user)

        print(bson.json_util.dumps(machines))
        self.write(bson.json_util.dumps(machines))
        print("write")


class AddMachineHandler(AuthencatedRequiredHandler):
    '''
        add a machine to machine list
    '''

    @tornado.web.authenticated
    async def post(self):
        machine_list = self.current_user['machines']
        _db = self.settings['db']
        username = self.get_argument('username')
        password = self.get_argument('password')
        u = await _db.user.find_one({'username': username, 'password': password})
        if u is not None:
            machine_list.append(u['_id'])
            _db.user.update_one({'_id': self.current_user['_id']},
                                {'$set': {'machines': machine_list}})
            self.write(json.dumps(
                {'ok': True, 'message': 'Successfully added!'}))
        self.write(json.dumps(
            {'ok': False, 'message': 'There is no such user!'}))


def make_app():
    '''
        tornado setting and routing
    '''
    settings = {
        'pycket': {
            'engine': 'redis',
            'storage': {
                'host': 'localhost',
                'port': 6379,
                'db_sessions': 10,
                'db_notifications': 11,
                'max_connections': 2 ** 31,
            },
            'cookies': {
                'expires_days': 20,
            },
        },
        'template_path': os.path.join(os.path.dirname(__file__), "templates"),
        'static_path': os.path.join(os.path.dirname(__file__), "statics"),
        'login_url': '/login',
        'cookie_secret': 'bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=',
    }
    return tornado.web.Application([
        (r"/", DashboardHandler),
        (r"/xterm", XtermPageHandler),
        (r"/shell", ShellHandler),
        (r"/register", RegisterHandler),
        (r"/login", LoginHandler),
        (r"/u/machine_list", ListMachineHandler),
        (r"/u/add_machine", AddMachineHandler),
        (r"/dashboard", DashboardHandler),
        (r"/logout", LogoutHandler),
    ], db=db, debug=True, **settings)


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    ioloop.IOLoop.instance().start()
