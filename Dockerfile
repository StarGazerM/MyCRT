FROM hub.c.163.com/netease_comb/ubuntu:16.04
MAINTAINER StarGazer

# 更新源
RUN apt-get update    

# 安装常用软件
RUN apt-get update && apt-get install -y build-essential g++ vim tar wget curl rsync bzip2 iptables tcpdump less telnet net-tools lsof && rm -rf /var/lib/apt/lists/*    

# 安装pyenv
RUN curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
RUN pyenv install 3.5.3

#下载代码
RUN cd ~ 
RUN git clone git@git.oschina.net:cad431/MyCRT.git
RUN cd MyCRT 

#安装python 库
RUN pip install -r requirements.txt
RUN cd other

#安装redis
RUN wget http://download.redis.io/releases/redis-3.2.8.tar.gz
RUN tar xzf redis-3.2.8.tar.gz
RUN cd redis-3.2.8
RUN make
RUN nohup src/redis-server&
RUN cd ..

#编译 zeromq
RUN tar -xvf zeromq-4.2.1.tar.gz
RUN cd zeromq-4.2.1
RUN ./config
RUN make
RUN make install

#安装mongodb
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6
RUN apt-get update
RUN apt-get install -y mongodb-org
RUN service mongod start

# 设置允许root ssh远程登录
RUN sed -i s/"PermitRootLogin without-password"/"PermitRootLogin yes"/g /etc/ssh/sshd_config       


#启动服务器
RUN python tornado_server.py
RUN python sshserver.py

# 容器需要开放SSH 22端口
EXPOSE 22 2200 8888

# SSH终端服务器作为后台运行
ENTRYPOINT /usr/sbin/sshd -D