#!/usr/bin/env python
# coding=utf-8

import sys
import signal
import asyncio
from dataclasses import dataclass
from asyncio.unix_events import _UnixSelectorEventLoop as LOOP

import Javise

import nest_asyncio
nest_asyncio.apply()

@dataclass(init=True)
class Tony():
    enemise: list#[str]
    old_pwd: str
    new_pwd: str
    change: bool
    output: str = None
    recorded: bool = False
    loop: LOOP = asyncio.get_event_loop()

    def attack(self):
        self.loop.add_signal_handler(signal.SIGTERM, self.signal_handler)
        self.alived_enemise = self.loop.run_until_complete(self.search_alive(self.enemise, self.loop))
        self.loop.run_until_complete(Javise.record(self.alived_enemise))
        if self.change:
            self.loop.run_until_complete(self.try2change_enemy())

    async def try2change_enemy(self):
        pass

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
