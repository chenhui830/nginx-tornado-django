#coding:utf8
from config.paramiko_base import Paramiko
from config.config_base import webserver
import config
import paramiko
import os

def django_deploy():
    for host in webserver:
        client = Paramiko()
        client.connect(host=host[0],user=host[1])
        # 创建虚拟环境
        client.cmd('virtualenv /root/pythonenv/django1.8')

        #上传项目解压
        client.upload(os.path.join(os.path.dirname(__file__),'polls.zip'),'/projects/polls.zip')
        client.cmd('unzip -d /projects -o /projects/polls.zip')

        #安装项目依赖
        client.cmd('yum -y install mysql-devel')
        client.cmd('/root/pythonenv/django1.8/bin/pip install -r /projects/polls/requirements')

        # supervisor安装启动
        supervisor_install(client)
        nginx_server(client)

def supervisor_install(p):
    p.cmd(r'rpm -Uvh https://mirrors.tuna.tsinghua.edu.cn/epel//7/x86_64/e/epel-release-7-10.noarch.rpm')
    p.cmd('rm -rf /var/run/yum.pid')
    p.cmd('yum -y install supervisor')
    p.upload(os.path.join(os.path.dirname(__file__),'polls.ini'),'/etc/supervisord.d/polls.ini')
    p.cmd('systemctl start supervisord.service')
    p.cmd('supervisorctl reload') #如果启动重新加载配置文件

def nginx_server(p):
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)),'config','servertpl.conf'),'r') as f:
        content = f.read().replace('{{server_name}}',p.host)
        with open('polls.conf','w') as poll_f:
            poll_f.write(content)
    p.upload(os.path.join(os.path.dirname(__file__),'polls.conf'),'/usr/local/nginx1.10.2/conf/vhosts.d/polls.conf')
    p.cmd('chown -R nginx:nginx /projects')
    p.cmd('nginx -s reload')

if __name__ == '__main__':
    django_deploy()