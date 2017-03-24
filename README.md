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

