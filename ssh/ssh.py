# -*- coding: utf-8 -*-
"""
@Time ： 2021/11/21 11:25
@Auth ： feige-xu
@File ：ssh.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)

"""
import pexpect
import getip

def run_cmd(cmd, patterns):
    child = pexpect.spawn(cmd, encoding='utf-8')
    child.setwinsize(24, 80)
    index = child.expect(patterns, timeout=10)
    return [index, child]

def sshclient(host, user, port, passwd):
    ssh_newkey = "continue"
    ssh_passwd = "assword:"
    ssh_confirm = "yes"
    ssh_refuse = "Connection refused"
    ssh_login = "Last login:"
    ssh_repeat_passwd = "Permission denied, please try again"
    ssh_noroutetohost = "No route to host"
    ssh_conntimeout = "Connection timed out"
    # 远程ssh时的完整命令
    ssh_cmd = "ssh {u}@{h} -p {p}".format(u=user, h=host, p=port)
    # 初始化一个句柄，并获取索引号
    index, child = run_cmd(ssh_cmd, [
        ssh_newkey,
        ssh_passwd,
        ssh_refuse,
        ssh_login,
        ssh_noroutetohost,
        ssh_conntimeout,
        pexpect.EOF,
        pexpect.TIMEOUT])
    try:
        if index == 0:
            child.sendline(ssh_confirm)
            # 一般第一次ssh时，会让你输入yes/no之类的，所以匹配到这个的时候，就做一次递归
            return sshclient(host, user, port, passwd)
        elif index == 1:
            print("Begin Load Password...")
            child.sendline(passwd)
            result = child.expect([
                ssh_repeat_passwd,
                ssh_login,
            ])
            if result == 1:
                print("{} login success (-_-)".format(host))
                child.interact()
                return
            elif result == 0:
                # 说明密码错误，需要重新输入密码，并进行递归
                passwd = input('Passwd: ').strip()
                return sshclient(host, user, port, passwd)
        elif index == 2:
            print("Connect refused, Pls check ssh port.")
            return
        elif index == 3:
            print("Login success")
            child.interact()
            return
        elif index == 4:
            print("The host %s connected faild: No route to host" % host)
            return
        elif index == 5:
            print("The host %s connected faild: Connection timeout" % host)
            return
        elif index == 6:
            print("Abnormal exit")
            return
        elif index == 7:
            print("Timeout for connect host %s, pls check network" % host)
            return
        return
    except Exception as e:
        raise e

def list_info(originList):
    try:
        print("******\033[1;30;43mIP信息如下，请选择对应的编号进行登陆\033[0m******\n")
        print("\033[0;32m{:<5}\033[0m{:<19}{}".format("编号", "IP地址", "标签"))
        sshList = []
        sshDict = {}
        for info in originList:
            id = originList.index(info) + 1
            host = info['host']
            tag = info['tag']
            user = info['user']
            port = int(info['port'])
            passwd = info['passwd']
            sshDict[id] = [
                host, user, passwd, port
            ]
            print("{:<5}{:<22}{}".format(id, host, tag))
        return sshDict
    except Exception as e:
        raise e



if __name__ == "__main__":
    sshclient('127.0.0.1','ljxpf',22, '123456')


