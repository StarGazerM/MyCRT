import asyncio
import socket
import sys
import threading
import traceback
from binascii import hexlify
# from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
import functools

import paramiko
from paramiko.py3compat import b, decodebytes, u
import zmq
import zmq.asyncio
import pymongo

# setup logging
paramiko.util.log_to_file('demo_server.log')

host_key = paramiko.RSAKey(filename='test_rsa.key')
#host_key = paramiko.DSSKey(filename='test_dss.key')

print('Read key: ' + u(hexlify(host_key.get_fingerprint())))

loop = zmq.asyncio.ZMQEventLoop()
asyncio.set_event_loop(loop)

db = pymongo.MongoClient('mongodb://localhost:27017/')
# client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
# db = client['MyCRT']

executor = ThreadPoolExecutor(10)


class Server (paramiko.ServerInterface):
    # 'data' is the output of base64.b64encode(key)
    # (using the "user_rsa_key" files)
    data = (b'AAAAB3NzaC1yc2EAAAABIwAAAIEAyO4it3fHlmGZWJaGrfeHOVY7RWO3P9M7hp'
            b'fAu7jJ2d7eothvfeuoRFtJwhUmZDluRdFyhFY/hFAh76PJKGAusIqIQKlkJxMC'
            b'KDqIexkgHAfID/6mqvmnSJf0b5W8v5h2pI/stOSwTQ+pxVhwJ9ctYDhRSlF0iT'
            b'UWT10hcuO4Ks8=')
    good_pub_key = paramiko.RSAKey(data=decodebytes(data))

    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        # if (username == 'foo') and (password == 'bar'):
        #     return paramiko.AUTH_SUCCESSFUL
        # return paramiko.AUTH_FAILED
        # future = loop.create_future(check_form_mongo, username, password)
        user = db.MyCRT.user.find_one({'username': username, 'password':password})
        if user is not None:
            return paramiko.AUTH_SUCCESSFUL
        else:
            return paramiko.AUTH_FAILED

    def check_auth_publickey(self, username, key):
        print('Auth attempt with key: ' + u(hexlify(key.get_fingerprint())))
        if (username == 'robey') and (key == self.good_pub_key):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_auth_gssapi_with_mic(self, username,
                                   gss_authenticated=paramiko.AUTH_FAILED,
                                   cc_file=None):
        """
        .. note::
            We are just checking in `AuthHandler` that the given user is a
            valid krb5 principal! We don't check if the krb5 principal is
            allowed to log in on the server, because there is no way to do that
            in python. So if you develop your own SSH server with paramiko for
            a certain platform like Linux, you should call ``krb5_kuserok()`` in
            your local kerberos library to make sure that the krb5_principal
            has an account on the server and is allowed to log in as a user.
        .. seealso::
            `krb5_kuserok() man page
            <http://www.unix.com/man-page/all/3/krb5_kuserok/>`_
        """
        if gss_authenticated == paramiko.AUTH_SUCCESSFUL:
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_auth_gssapi_keyex(self, username,
                                gss_authenticated=paramiko.AUTH_FAILED,
                                cc_file=None):
        if gss_authenticated == paramiko.AUTH_SUCCESSFUL:
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def enable_auth_gssapi(self):
        UseGSSAPI = True
        GSSAPICleanupCredentials = False
        return UseGSSAPI

    def get_allowed_auths(self, username):
        return 'gssapi-keyex,gssapi-with-mic,password,publickey'

    def check_channel_shell_request(self, channel):
        print('shell request')
        self.event.set()
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth,
                                  pixelheight, modes):
        return True


DoGSSAPIKeyExchange = False

# ssh_server = Server()

async def async_ssh_handler(client):

    try:
        t = paramiko.Transport(client, gss_kex=DoGSSAPIKeyExchange)
        t.set_gss_host(socket.getfqdn(""))
        try:
            t.load_server_moduli()
        except:
            print('(Failed to load moduli -- gex will be unsupported.)')
            raise
        t.add_server_key(host_key)
        ssh_server = Server()
        try:
            t.start_server(server=ssh_server)
        except paramiko.SSHException:
            print('*** SSH negotiation failed.')
            sys.exit(1)

        # wait for auth
        chan = t.accept(20)
        if chan is None:
            print('*** No channel.')
            sys.exit(1)
        print('Authenticated!')
        # chan.setblocking(0)

        zmq_context = zmq.asyncio.Context()
        zmq_socket = zmq_context.socket(zmq.PAIR)
        # pool = ThreadPoolExecutor()
        username = await loop.run_in_executor(executor, chan.recv, 1024)
        zmq_socket.bind('ipc://' + username.decode())
        loop.create_task(read_from_ssh_to_zmq(chan, zmq_socket))
        loop.create_task(read_from_zmq_to_ssh(zmq_socket, chan))

    except Exception as e:
        print('*** Caught exception: ' + str(e.__class__) + ': ' + str(e))
        traceback.print_exc()
        try:
            t.close()
        except:
            pass
        sys.exit(1)

async def recv_ssh(chan):
    return chan.recv(1024)

async def read_from_zmq_to_ssh(sock, chan):
    while True:
        data = await sock.recv_unicode()
        if len(data) is not 0:
            await loop.run_in_executor(executor, chan.send, data)

async def read_from_ssh_to_zmq(chan, sock):
    while True:
        data = await loop.run_in_executor(executor, chan.recv, 1024)
        if len(data) != 0:
            await sock.send(data)

async def run_server():
    # now connect
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', 2200))
    except Exception as e:
        print('*** Bind failed: ' + str(e))
        traceback.print_exc()
        sys.exit(1)

    sock.listen(100)
    sock.setblocking(False)
    print('Listening for connection ...')
    # executor = ProcessPoolExecutor(10)

    while True:
        try:
            client, addr = await loop.sock_accept(sock)
        except Exception as e:
            print('*** Listen/accept failed: ' + str(e))
            traceback.print_exc()
            sys.exit(1)
        # create_ssh_transport(client) 10)
        loop.create_task(async_ssh_handler(client))
        print('accepted')

if __name__ == '__main__':
    # loop.set_debug(True)
    loop.create_task(run_server())
    loop.run_forever()
