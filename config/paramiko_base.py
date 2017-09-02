#coding:utf8


import paramiko
import os
from config_base import webserver

class Paramiko:
    def __init__(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sftp = None

    #连接函数
    def connect(self,host,user,pwd=None,port=22):
        try:
            self.host = host
            if pwd is None:   #用私钥连
                key = paramiko.RSAKey.from_private_key_file(os.path.join(os.path.dirname(__file__),'id_rsa'))
                #key = paramiko.RSAKey.from_private_key_file('id_rsa')
                self.ssh.connect(host,port,user,pkey=key)
            else:             #用密码连
                self.ssh.connect(host,port,user,pwd)
        except Exception,e:
            print str(e)

    #执行命令函数
    def cmd(self,cmd):
        try:
            stdin,stdout,stderr = self.ssh.exec_command(cmd)
            for line in stdout:
                print line
        except Exception,e:
            print str(e)


    #获取获取ssh连接，然后创建sftp管道
    def __getsftp(self):
        if self.sftp is None:
            self.sftp = paramiko.SFTPClient.from_transport(self.ssh.get_transport())
        return self.sftp

    #上传文件函数
    def upload(self,local,remote):
        try:
            sftp = self.__getsftp()
            sftp.put(local,remote)
        except Exception,e:
            print(str(e))

    #下载文件函数
    def download(self,remote,local):
        try:
            sftp = self.__getsftp()
            sftp.get(remote,local)
        except Exception,e:
            print(str(e))



#测试
# for host in webserver:
#     p = Paramiko()
#     p.connect(host=host[0],user=host[1],port=22)
#     #p.cmd('mkdir abc.b')
#     p.cmd('mv /root/abc.b /usr/local/nginx1.10.2/conf')
#     #p.cmd('cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys')
#     #p.upload('loc','/root/loc.txt')
#     #p.download('/root/.ssh/id_rsa','id_rsa')
#     print("完成")