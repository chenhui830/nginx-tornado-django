#coding:utf8
from config.paramiko_base import Paramiko
from config.config_base import webserver
import config
import paramiko
import os

def django_deploy():
    for host in webserver:
        client = Paramiko()
        client.connect(host=host[0],user=host[1],pwd='123')
        # 创建虚拟环境
        client.cmd('virtualenv /root/pythonenv/django1.8')

        #上传项目解压
        client.upload('polls.zip','/projects/polls.zip')
        client.cmd('unzip -d /projects -o /projects/polls.zip')

        #安装项目依赖
        client.cmd('yum -y install mysql-devel')
        client.cmd('/root/pythonenv/django1.8/bin/pip install -r /projects/polls/requirements')

        # supervisor安装启动
        supervisor_install(client)
        nginx_server(client)

def supervisor_install(client):
    client.cmd(r'rpm -Uvh https://mirrors.tuna.tsinghua.edu.cn/epel//7/x86_64/e/epel-release-7-10.noarch.rpm')
    client.cmd('rm -rf /var/run/yum.pid')
    client.cmd('yum -y install supervisor')
    client.upload('polls.ini','/etc/supervisord.d/polls.ini')
    client.cmd('systemctl start supervisord.service')
    client.cmd('supervisorctl reload') #如果启动重新加载配置文件

def nginx_server(client):
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'config','servertpl.conf')
    try:
        with open(path,'r') as f:
            content = f.read().replace('{{server_name}}',client.host)
            with open('polls.conf','w') as poll_f:
                poll_f.write(content)
        client.upload('polls.conf','/usr/local/nginx1.10.2/conf/vhosts.d/polls.conf')
        client.cmd('chown -R nginx:nginx /projects')
        client.cmd('nginx -s reload')
    except Exception,e:
        print str(e)

if __name__ == '__main__':
    django_deploy()