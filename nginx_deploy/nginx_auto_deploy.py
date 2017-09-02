from config.paramiko_base import Paramiko
from config.config_base import webserver

def nginx_deploy(hosts):
    for host in hosts:
        client = Paramiko()
        client.connect(host=host[0],user=host[1],port=22,pwd='123')
        client.upload('nginx.zip','/opt/nginx.zip')
        client.cmd('unzip -o -d /opt /opt/nginx.zip')
        client.cmd('rm -rf /opt/nginx.zip')
        client.cmd('python /opt/nginx_deploy.py')
        client.cmd(r"sed -i '116 s%^%    include /usr/local/nginx1.10.2/conf/vhosts.d/*.conf;\n%' /usr/local/nginx1.10.2/conf/nginx.conf")
        client.cmd('mkdir vhosts.d')
        client.cmd('mv /root/vhosts.d /usr/local/nginx1.10.2/conf')

if __name__=="__main__":
    nginx_deploy(webserver)


