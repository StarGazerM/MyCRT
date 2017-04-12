# MyCRT

-------------------------------------------
MyCRT是一个Linux下的能够穿透NAT的远程管理软件,是我的毕业设计,虽然很low,也没有什么技术含量,但是在写的过程中起码还是学到了一点点东西的在这里感谢
毕设的老师和翔哥出这个题目.也许是个很水的项目但是真心还是有收获的

##测试开发环境
- Python3.5.3
- Mint Linux16
- redis3.2
- zeromq4.2.1
- mongodb3.4
- tornado4.4.2

## 依赖

# v1
## 目标

系统只需要考虑支撑linux操作系统

系统主要分成三部分
1. 客户端·
2. vps服务端
3. web前端

实现类似teamview的**不同局域网多台主机能够互相相互访问**


## 原理和实现要点
客户端通过paramiko链接到本机的sshd上,再通过paramiko来实现一个反向链接到远程的自己写的ssh server上面, ssh server使用zeromq和前面的tornado服务器进行通信交换数据,最后前端用xterm.js实现一个webshell和服务器之间使用websocket通信



ssh -fNg -R port:localhost:22 username@121.42.157.113

## 交互部分设计

> 客户端

使用xterm.js编写的web shell

> 服务端

1. tornado的http server提供基本的登录验证等功能
2. websocket 和前端xterm.js通信
3. mongodb存放用户数据
4. pycket + redis 来做session管理



# v2

## 目标功能
把paramiko换成c的底层,想办法封装一个异步的paramiko chanel(好吧封装好了````结果有现成的asyncssh)
支撑docker集群的管理
修复用vim打开中文较多文件的时候出现的tornado send_message 失效问题

## 实现
c语言实现服务端尝试实用libssh和openssl来重写sshd服务来实现一个端口复用多个ssh隧道。
zeromq部分可以独立展开支撑更多的功能
把session的管理做到mongodb里面


# 安装部署

-----------------------
## 服务器开发环境

### 配置python环境
1. 安装pyenv
```bash

    curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash  
```
2. 在~/.bashrc末尾加入，配置pyenv环境变量，之后source ~/.bashrc
```
    export PATH="/home/stargazer/.pyenv/bin:$PATH"
    eval "$(pyenv init -)"
    eval "$(pyenv virtualenv-init -)"
```

3.安装必要依赖(根据自己的系统决定)
```bash
    sudo apt-get install build-essential
    sudo apt-get install libreadline-dev
    sudo apt-get install libssl-dev
```

4. 安装python
```bash
    pyenv install -v 3.5.3
```

5. 设定全局python版本
```bash
    pyenv global 3.5.3
```

6.安装python依赖库,在项目根目录下执行
```bash
    pip install -r requirements.txt
```

### 安装 zeromq
在项目的other目录下解压zeromq然后执行
```bash
    ./configure
    sudo make install
```
### 安装启动redis（只使用命令行版本无需设置）
1. 解压到~/目录下

```bash
    sudo make install
```

2. 启动redis
```bash
    nohup redis-server&
``` 

如果出现redis在小内存机器上的持久化问题可以google解决

### 安装启动mongodb

```bash
    echo "deb [ arch=amd64 ] http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list

    sudo apt-get update
    sudo apt-get install -y mongodb-org
    sudo service mongod start

```

### 配置前端开发环境（只使用命令行版本无需设置）

1. 安装nvm
```bash
    curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.1/install.sh | bash
```
2. 配置环境变量,之后source
```bash
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh" 
```

2. 安装node
```bash
    nvm intsall v6.10.2
```

3. 安装模块在static/myxterm下
```bash
    npm install
```

4. 打包
修改config.js中的域名为自己的域名，然后build
```
    npm run build
```

### 启动
运行tornado_server.py和sshserver.py

------------------------------------
## 客户端

把client.py放过去,安装python(>=3.5)和库,修改里面的变量

## 命令行版本

0. 在mongodb数据库的MyCRT.user中插入一条用户数据 {'username': , 'password': , isOnline: false}, 并且配置config.py

1. 脚本在cmd文件夹下，服务器端运行

```
    python mycrtd.py backend
    python mycetd.py frontend
```

2. 被控制端

```
    python mycrtc.py passive
```

3. 控制端运行

```
    python mycrtc.py active
```
