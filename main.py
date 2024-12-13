import websockets
import requests
import servers
import asyncio
import random
import string
import bots
tasks = []
def GetServers():
    _servers = servers.GetServerList()
    _str = ''
    for i in range(len(_servers)):
        server = _servers[i]
        _str += f'[{i}] {server.region} {server.game_mode} players: {server.players}/{server.max_players} distance: {server.distance}km\n'
    return {'_servers': _servers, '_str': _str}

async def main():
    print('Get server list...')
    _servers = GetServers()
    print(_servers['_str'])
    choosed_server = int(input('Select server: '))
    bots_count = int(input('Bots count: '))
    bots_nickname = input('Bots nickname: ')
    BotManager = bots.BotManager(_servers['_servers'][choosed_server].id)
    print('Create bots')
    for i in range(bots_count):
        await BotManager.CreateBot(bots_nickname)
    task = asyncio.create_task(BotManager.Update())
    bots.tasks.append(task)
#start
async def run_program():
    await main() 
    await asyncio.gather(*bots.tasks) 

asyncio.get_event_loop().run_until_complete(run_program())