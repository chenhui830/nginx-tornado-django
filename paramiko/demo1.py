#coding:utf8

import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #相当于linux下的known_hosts,添加连接记录
try:
    client.connect('10.0.138.52',22,'root','123')
    while True:
        cmd = raw_input('>>>')
        stdin,stdout,stderr = client.exec_command(cmd)  #执行ls命令，获取输入 输出和错误值
        print stdout.read(),
except Exception as e:
    print(e)