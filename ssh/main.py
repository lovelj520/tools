# -*- coding: utf-8 -*-
"""
@Time ： 2021/11/21 11:34
@Auth ： feige-xu
@File ：main.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)

"""
import os
import ssh
import getip

def login(yamlfile):
    try:
        print("\033[1;30;47m{:^50}\033[0m\n".format("简易跳板机"))
        outer_flag = False
        while not outer_flag:
            print("\033[5;35;46m{:<}\033[0m\n".format("请选择"))
            print("\033[0;32m输入 'p/P' 打印所有主机信息\033[0m")
            print("\033[0;31m输入 'q/quit' 退出\033[0m\n")
            input_x = input(">>>>>: ").strip().lower()
            if input_x == 'p':
                os.system("clear")
                ip_info = ssh.list_info(yamlfile)
                print("\n")
                print("\033[0;32m输入 '编号' 进入对应的服务器\033[0m")
                print("\033[0;32m输入 'q' 退出\033[0m")
                print("\033[0;32m输入 'b' 返回\033[0m")
                inner_flag = False
                while not inner_flag:
                    act = input("\033[0;32m>>>>>: \033[0m").strip().lower()
                    if act.isdigit():
                        ip_id = int(act)
                        if ip_id in ip_info.keys():
                            host = ip_info[ip_id][0]
                            user = ip_info[ip_id][1]
                            passwd = str(ip_info[ip_id][2])
                            port = int(ip_info[ip_id][3])
                            ssh.sshclient(
                                host=host,
                                user=user,
                                port=port,
                                passwd=passwd
                            )
                            inner_flag = True
                        else:
                            print("\033[0;31m编号不存在，请重新输入，退出请输入任意字符\033[0m")
                            continue
                    else:
                        if act == 'q' or act == 'quit':
                            print("\033[0;31m告辞 !!!\033[0m")
                            inner_flag = True
                            outer_flag = True
                        elif act == 'b' or act == 'back':
                            inner_flag = True
            elif input_x == 'q' or input_x == 'quit':
                print("\033[0;31m告辞 !!!\033[0m")
                outer_flag = True
            else:
                print("\033[0;31m请输入指定的内容 !!!\033[0m")
                continue
    except Exception as e:
        raise e




if __name__ == '__main__':
    login(ssh.list_info(getip.parseYaml('ip.yaml')))