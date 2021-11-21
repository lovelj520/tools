# -*- coding: utf-8 -*-
"""
@Time ： 2021/11/21 11:32
@Auth ： feige-xu
@File ：getip.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)

"""
import yaml

def parseYaml(yamlfile, parse_list=None):
    if parse_list is None:
        parse_list = []
    with open(yamlfile, 'r', encoding='utf-8') as fr:
        yaml_to_dict = yaml.safe_load(fr)
        global_user = yaml_to_dict['global']['user']
        global_passwd = yaml_to_dict['global']['passwd']
        global_port = int(yaml_to_dict['global']['port'])
        for detail in yaml_to_dict['jumpserver']:
            tag = detail['name']
            get_hostList = detail['hostList']
            if isinstance(get_hostList[0], dict):
                for ssh in get_hostList:
                    sshDetail = {
                        'tag': tag,
                        'host': ssh['host'],
                        'user': ssh['user'] if 'user' in ssh else global_user,
                        'port': int(ssh['port']) if 'port' in ssh else global_port,
                        'passwd': ssh['passwd'] if 'passwd' in ssh else global_passwd
                    }
                    parse_list.append(sshDetail)
            elif isinstance(get_hostList[0], str):
                for h in get_hostList:
                    sshDetail = {
                        'tag': tag,
                        'host': h,
                        'user': global_user,
                        'port': global_port,
                        'passwd': global_passwd
                    }
                    parse_list.append(sshDetail)
        return parse_list

if __name__ == '__main__':
    print(parseYaml('ip.yaml'))