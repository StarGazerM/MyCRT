import asyncio
import sys
import functools
from concurrent.futures import ThreadPoolExecutor

import asyncssh
import motor.motor_asyncio
import pymongo
import zmq
import zmq.asyncio

loop = zmq.asyncio.ZMQEventLoop()
asyncio.set_event_loop(loop)

client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
# lient = pymongo.MongoClient('mongodb://localhost:27017/')
db = client.MyCRT

executor = ThreadPoolExecutor(10)


async def handle_session(stdin, stdout, stderr):
    print('start to handle session')
    username = await stdin.read()
    zmq_context = zmq.asyncio.Context()
    zmq_socket = zmq_context.socket(zmq.PAIR)
    zmq_socket.bind('ipc://' + username.decode())
    loop.create_task(exchange_from_zmq_to_ssh(zmq_socket, stdout))
    loop.create_task(exchange_from_ssh_to_zmq(stdin, zmq_socket))


# class MySSHSession(asyncssh.SSHServerSession):
#     def __int__(self):
#         self._input = ''

#     def connection_made(self):
#         return True

#     def data_received(self):
#         self._


async def exchange_from_zmq_to_ssh(sock, ssh_writer):
    while True:
        data = await sock.recv_unicode()
        if len(data) != 0:
            await ssh_writer.write(data)


async def exchange_from_ssh_to_zmq(ssh_reader, sock):
    while True:
        data = await ssh_reader.read()
        if len(data) != 0:
            await sock.send(data)


class AsyncSSHServer(asyncssh.SSHServer):

    def session_requested(self):
        print('session request')
        return handle_session

    def connection_lost(self, exc):
        if exc:
            print('SSH connection error: ' + str(exc), file=sys.stderr)
        else:
            print('SSH connection closed.')

    def begin_auth(self, username):
        # user = asyncio.run_coroutine_threadsafe(
        #     find(username, password), loop)
        # print(user.result())
        # return user.result() is not None
        return True

    def password_auth_supported(self):
        return True

    async def validate_password(self, username, password):
        print('start valid password')
        user = await find_db(username, password)
        if user is not None:
            return True
        else:
            return False


async def find_db(username, password):
    user = await db.user.find_one({'username': username, 'password': password})
    return user


async def run_server():
    with open('id_rsa') as file:
        key = file.read()
        host_key = asyncssh.import_private_key(key, '123456')
    await asyncssh.create_server(AsyncSSHServer, 'localhost', 2200,
                                 server_host_keys=[host_key], gss_host=None)


if __name__ == '__main__':
    try:
        loop.run_until_complete(run_server())
    except (OSError, asyncssh.Error) as exc:
        sys.exit('Error starting server: ' + str(exc))
    loop.run_forever()
