import select
import sys
import getopt
import traceback

import config
import interactive

import paramiko


def connect_ssh(host, port, username, password):
    '''
    连接到ssh
    '''
    client = paramiko.SSHClient()
    # client.load_host_keys(paramiko.AutoAddPolicy())
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, port=port, username=username, password=password)
    return client


def passive():
    '''
    待连接的主机执行的函数
    '''
    client_local = connect_ssh(
        '127.0.0.1', 22, config.LOCAL_USERNAME, config.LOCAL_PASSWORD)
    # client_remote = connect_ssh('121.42.157.113', 2200, 'foo', 'bar')
    client_remote = connect_ssh(
        '127.0.0.1', 2200, config.REMOTE_USERNAME, config.REMOTE_PASSWORD)
    chan_local = client_local.invoke_shell()
    chan_remote = client_remote.get_transport().open_session()
    chan_remote.send(config.REMOTE_USERNAME)

    while True:
        r, w, x = select.select([chan_local, chan_remote], [], [])
        if chan_remote in r:
            data = chan_remote.recv(1024)
            if len(data) == 0:
                break
            chan_local.send(data)
        if chan_local in r:
            data = chan_local.recv(1024)
            if len(data) == 0:
                break
            chan_remote.send(data)
    chan_local.close()
    chan_remote.close()
    print('closed')


def active():
    '''
    控制端主机执行的方法
    '''

    client_remote = connect_ssh(
        '127.0.0.1', 2201, config.REMOTE_USERNAME, config.REMOTE_PASSWORD)
    chan_remote = client_remote.get_transport().open_session()
    chan_remote.send(config.REMOTE_USERNAME)
    interactive.interactive_shell(chan_remote)
    chan_remote.close()
    client_remote.close()


if __name__ == '__main__':
    try:
        MODE = str(sys.argv[-1])
        if MODE != 'active' and MODE != 'passive':
            raise getopt.GetoptError('参数不存在！')
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(1)

    if MODE == 'active':
        active()
    if MODE == 'passive':
        passive()
