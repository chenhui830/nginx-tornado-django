#coding:utf8
#实现在windows下也能切换路径

import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #相当于linux下的known_hosts,添加连接记录
try:
    client.connect('10.0.138.175',22,'root','123')
    dirs = ''
    while True:
        cmd = raw_input('>>>')
        if cmd.startswith('cd'):   #如果命令以cd开头
            dirs = cmd + ';'   #dirs将上面的命令存起来
        elif cmd.startswith('exit'):   #如果命令为exit，则退出循环
            break
        else:
            stdin,stdout,stderr = client.exec_command(dirs + cmd)  #执行命令，获取输入 输出和错误值
            for line in stdout:
                print line,

except Exception,e:
    print str(e)