import select

import paramiko


def connect_ssh(host, port, username, password):
    client = paramiko.SSHClient()
    # client.load_host_keys(paramiko.AutoAddPolicy())
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, port=port, username=username, password=password)
    return client


def main():
    print('start')
    remote_username = 'foo'
    remote_password = 'bar'
    local_username = 'stargazer'
    local_password = 'Apple2011'
    client_local = connect_ssh('127.0.0.1', 22, local_username, local_password)
    # client_remote = connect_ssh('121.42.157.113', 2200, 'foo', 'bar')
    client_remote = connect_ssh('127.0.0.1', 2200, remote_username, remote_password)

    chan_local = client_local.invoke_shell()
    chan_remote = client_remote.get_transport().open_session()
    chan_remote.send(remote_username)

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
    print('chanel closed')


if __name__ == '__main__':
    main()
