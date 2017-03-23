import os
import re
import redis
import pexpect


def get_ssh_port_status():
    """
    获取ssh端口状态
    """
    ports = []
    os.system('netstat -tnpl | grep ssh > port_status')
    with open('./port_status', 'r') as status_file:
        for line in status_file.readlines():
            pattern = re.compile(r'\S+')
            ports.append(pattern.findall(line)[3].split(':')[1])
    return ports


def query_busy_port():
    '''
        查看6000~7000所有的占用端口号
    '''
    busy_ports = []
    with open('/proc/net/tcp', 'r') as tcp:
        for line in tcp.readlines():
            pattern = re.compile(r'\S+')
            port = pattern.findall(line)[1].split(':')[1]
            busy_ports.append(str(int(port, 16)))
    return busy_ports


def regist_machine(name):
    '''
       在服务器上开放端口为反向端口
    '''
    database = redis.Redis(host='localhost', port=6379, db=0)
    count = 6000
    if database.exists(name):
        return -1
    else:
        busy_ports = query_busy_port()
        while count in busy_ports:
            count += 1
            if count > 7000:
                return False
        database.set(name, count)
        # child = pexpect.spawn('ssh -fNg -R %d:localhost:22 root@121.42.157.113'% count)
        # i = child.expect(["root@121.42.157.113.*", 'The authen.*'])
        # if i == 0:
        #     child.sendline('yes')
        #     print('save auth')
        # child.expect("root@121.42.157.113.*")
        # child.sendline('Apple2011')
        return count
