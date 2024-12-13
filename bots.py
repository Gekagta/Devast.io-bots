import ssl
import requests
import asyncio
import websockets
import string
import random
import struct
import json

letters = string.ascii_letters 
digits = string.digits
tasks = []
newCaseNumbers = [42, 0, 35, 31, 27, 1, 32, 22, 34, 19, 28, 17, 15, 4, 30, 29, 23, 12, 33, 37, 54, 3, 56, 38, 14, 48, 64, 52, 46, 6, 11, 61, 10, 71, 41, 5, 59, 73, 58, 16, 60, 53, 20, 49, 40, 8, 62, 67, 25, 26, 2, 36, 18, 44, 9, 21, 7, 13, 24, 57, 69, 68, 55, 51, 39, 45, 65, 72, 70, 43, 47, 50, 66, 63]
caseMap = {
        52: newCaseNumbers[0], 0: newCaseNumbers[1], 34: newCaseNumbers[2], 46: newCaseNumbers[3], 51: newCaseNumbers[4],
        63: newCaseNumbers[5], 6: newCaseNumbers[6], 65: newCaseNumbers[7], 56: newCaseNumbers[8], 72: newCaseNumbers[9],
        71: newCaseNumbers[10], 55: newCaseNumbers[11], 17: newCaseNumbers[12], 1: newCaseNumbers[13], 40: newCaseNumbers[14],
        58: newCaseNumbers[15], 64: newCaseNumbers[16], 30: newCaseNumbers[17], 48: newCaseNumbers[18], 35: newCaseNumbers[19],
        29: newCaseNumbers[20], 54: newCaseNumbers[21], 9: newCaseNumbers[22], 69: newCaseNumbers[23], 39: newCaseNumbers[24],
        3: newCaseNumbers[25], 38: newCaseNumbers[26], 21: newCaseNumbers[27], 43: newCaseNumbers[28], 20: newCaseNumbers[29],
        44: newCaseNumbers[30], 42: newCaseNumbers[31], 12: newCaseNumbers[32], 18: newCaseNumbers[33], 47: newCaseNumbers[34],
        73: newCaseNumbers[35], 61: newCaseNumbers[36], 25: newCaseNumbers[37], 66: newCaseNumbers[38], 59: newCaseNumbers[39],
        24: newCaseNumbers[40], 41: newCaseNumbers[41], 19: newCaseNumbers[42], 57: newCaseNumbers[43], 67: newCaseNumbers[44],
        37: newCaseNumbers[45], 32: newCaseNumbers[46], 22: newCaseNumbers[47], 4: newCaseNumbers[48], 60: newCaseNumbers[49],
        53: newCaseNumbers[50], 8: newCaseNumbers[51], 13: newCaseNumbers[52], 16: newCaseNumbers[53], 7: newCaseNumbers[54],
        31: newCaseNumbers[55], 68: newCaseNumbers[56], 50: newCaseNumbers[57], 45: newCaseNumbers[58], 28: newCaseNumbers[59],
        49: newCaseNumbers[60], 10: newCaseNumbers[61], 62: newCaseNumbers[62], 27: newCaseNumbers[63], 26: newCaseNumbers[64],
        5: newCaseNumbers[65], 15: newCaseNumbers[66], 23: newCaseNumbers[67], 70: newCaseNumbers[68], 14: newCaseNumbers[69],
        33: newCaseNumbers[70], 2: newCaseNumbers[71], 36: newCaseNumbers[72], 11: newCaseNumbers[73]
}
class BotManager:
    def __init__(self, server: str) -> None:
        self.bots = []
        self.server = server

    async def CreateBot(self, nickname: str) -> None:
        bot_id = len(self.bots) + 1
        print(f'[{bot_id}] Create bot {nickname} {bot_id}...')
        bot = Bot(nickname + str(bot_id), self)

        print(f'[{bot_id}] Connect to server')
        try:
            data = {'lobby_id': self.server}
            response = requests.post('https://matechmaker-o2y3.vercel.app/join', json=data)
            if response.status_code == 200:
                print(f'[{bot_id}] Connected')
            else:
                print(f'[{bot_id}] Bot creation failed due to unknown error (HTTP CODE {response.status_code})')
            response = response.json()
        except:
            print(f'[{bot_id}] Unknown error (maybe due to limit)')
            await self.CreateBot(nickname)
            return

        if response:
            print(f'[{bot_id}] Create url to connect...')
            url = 'ws'
            if response['lobby']['ports']['default']['is_tls']:
                url += 's'
            ip = response['lobby']['ports']['default']['hostname']
            port = response['lobby']['ports']['default']['port']
            token = response['lobby']['player']['token']
            url += f'://{ip}:{port}/?token={token}'

            print(f'[{bot_id}] Connect to {ip}')
            if (await bot.Init(url, bot_id)):
                self.bots.append(bot)
                print(f'[{bot_id}] Created')
        else:
            await self.CreateBot(nickname)
    async def Update(self):
        await asyncio.sleep(10)
    async def Error(self, bot_id: int):
        self.bots.pop(bot_id)
        for i in range(len(self.bots)):
            self.bots[i].id = i
    async def OnPlayerDeath(self,data: bytes, bot_id: int):
        print(f'{bot_id} OnPlayerDeath')
        pass
    async def OnHandshake(self, data: bytes, ui8: bytearray, bot_id: int):
        print(f'{bot_id} OnHandshake')
        ui16 = struct.unpack(f'{len(data)//2}H', data)
        duration = ui16[3] << 5
        print(f'WORLD.Player.id = {ui8[1]}')
        print(f'World.playerNumber = {ui8[4]}')
        print(f'World.gameMode = {ui8[5]}')
        print(f'Duration = {duration}')
    async def OnUnits(data: bytes, ui8: bytearray, bot_id: int):
        print(f'{bot_id} OnUnits')
        ui16 = struct.unpack(f'{len(data)//2}H', data)
        len_objects = (len(ui8) - 2) // 18
        for i in range(len_objects):
            isRef8 = 2 + i * 18
            isRef16 = 1 + i * 9
            pid = ui8[isRef8]
            uid = ui8[isRef8 + 1]
            type_ = ui8[isRef8 + 3] 
            state = ui16[isRef16 + 2]  
            id_ = ui16[isRef16 + 3] 
            extra = ui16[isRef16 + 8]
            x_position = ui16[isRef16 + 4]  
            y_position = ui16[isRef16 + 5]  
            x_position2 = ui16[isRef16 + 6]  
            y_position2 = ui16[isRef16 + 7]  
            print(f'x1,y1: {x_position},{y_position}')
            print(f'x2,y2: {x_position2},{y_position2}')
            print(f'pid, uid: {pid}, {uid}')
    async def OnAreas(self, ui8: bytearray, bot_id: int):
        print(f'{bot_id} OnAreas')
    async def OnTeamCreated(self,data, bot_id: int):
        print(f'OnTeamCreated {data}')
        if data[3] == 'BOT':
            self.bots[bot_id].wantcommand = f'[30,{data[1]}]'
    async def Callbacks(self, data: bytes, bot_id: int):
       # print(f'callback from {bot_id}')
        ui8 = bytearray(data)
        if data[0] in caseMap:
            case_number = caseMap[data[0]]
            if case_number == newCaseNumbers[3]:
                await self.OnPlayerDeath(data,bot_id)
            elif case_number == newCaseNumbers[9]:
                await self.OnHandshake(data,ui8,bot_id)
            elif case_number == newCaseNumbers[0]:
                await self.OnUnits(data,ui8,bot_id)
            elif case_number == newCaseNumbers[61]:
                await self.OnAreas(ui8,bot_id)
        

class Bot:
    def __init__(self, nickname: str, controller: BotManager):
        self.nickname = nickname
        self.ws = None
        self.id = -1
        self.controller = controller
        self.died = None
        self.want = None
        self.wantcommand = None
    async def GenerateRandomData(self, bot_id: int) -> str:
        template = 'xIxxxxxxxx?IIxxIxxI'
        token = '' #universal token for ind. player
        for char in template:
            if char == 'x': 
                token += random.choice(letters)
            elif char == 'I': 
                token += str(random.choice(digits))
            elif char == '?': 
                token += '?'
            else:
                token += char
        token_id = random.randint(10000,30000) #token id :)
        user_id = random.randint(50,200) #user id =)
        return f'[30, "{token}", "{token_id}", {user_id}, 0, "{self.nickname} {bot_id}", 0, 0, 0]'
    async def Init(self, server: str, bot_id: int):
        self.id = bot_id - 1
        try:
            data = await self.GenerateRandomData(bot_id)
            task = asyncio.create_task(self.Handle(server, data))
            tasks.append(task)
            return True
        except Exception as e:
            print(f'Error in Init: {e}')
            return False
    async def Handle(self, server: str, data: str):
        print('start handle')
        async with websockets.connect(server) as ws:
            try:
                await ws.send(data)
                response = await ws.recv()
                self.died = False
            except Exception as e:
                print(f'Error on spawn bot! {e}')
                self.controller.Error(self.id)
                return
            while True:
                try:
                    if self.wantcommand:
                        await ws.send(self.wantcommand)
                        self.wantcommand = None
                    await ws.send(f'[1]') #antikick if bot is stuck and afk ([1,"msg"] - chat)
                    await ws.send(f'[2,5]') #move left-down
                    response = await ws.recv()
                    if isinstance(response, bytes):
                        await self.controller.Callbacks(response, self.id)
                    else:
                        response = json.loads(response)
                        if response[0] == 4:
                            await self.controller.OnTeamCreated(response, self.id)
                except Exception as e:
                    if not self.died:
                        print(f'{self.nickname} {self.id} died! Reconnecting...')
                        await self.controller.Error(self.id)
                        await self.controller.CreateBot(self.nickname)
                        break
                    print(f"[{self.id}] Error in Handle: {e}")
                    break