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
        print('test')
        await asyncio.sleep(10)
    async def Error(self, bot_id: int):
        self.bots.pop(bot_id)
        for i in range(len(self.bots)):
            self.bots[i].id = i

    #api

    async def OnTeamName(self,data, bot_id: int):
        print('OnTeamName')
        print(data)
    async def OnAlert(self,data, bot_id: int):
        print('OnAlert')
        print(data)
    async def OnNicknamesToken(self,data, bot_id: int):
        print('OnNicknamesToken')
        print(data)
    async def OnNewPlayer(self,data, bot_id: int):
        print('OnNewPlayer')
        player_id = data[1]
        player_token_id = data[2]
        player_nickname = data[3]
        player_skin = data[4]
        player_ghoul = data[5]

    async def OnChatMessage(self,data, bot_id: int):
        print('OnChatMessage')
        player_id = data[1]
        text = data[2]

    async def OnPlayerDeath(self,data: bytes, bot_id: int):
        print(f'{bot_id} OnPlayerDeath')
    async def OnHandshake(self, data: bytes, ui8: bytearray, bot_id: int):
        print(f'{bot_id} OnHandshake')
        ui16 = struct.unpack(f'{len(data)//2}H', data)
        my_player_id = ui8[1]
        time_duration = ui16[3] << 5
        units_per_player = ui16[1]
        player_number = ui8[4]
        gamemode = ui8[5]
        len = (len(data) - 8) / 10
        i = 0
        info = 8
        add_info = 4
        while (i < len):
            player_id = ui8[info]
            player_ghoul = ui8[info + 4]
            player_token_id = ui16[add_info + 3]
            player_score = ui16[add_info + 4]
            info += 10,
            add_info += 5
            i += 1
    async def OnUnits(data: bytes, ui8: bytearray, bot_id: int):
        print(f'{bot_id} OnUnits')
        ui16 = struct.unpack(f'{len(data)//2}H', data)
        len = (len(ui8) - 2) // 18
        isRef8 = 2
        isRef16 = 1
        i = 0
        while (i < len):
            pid = ui8[isRef8] #like player id
            uid = ui8[isRef8 + 1] #like entity id (ghoul and etc)
            type = ui8[isRef8 + 3]
            state = ui16[isRef16 + 2]
            id = ui16[isRef16 + 3]
            extra = ui16[isRef16 + 8]
            #create entity
            pos_x = ui16[isRef16 + 4] #world pos
            pos_y = ui16[isRef16 + 5] #world pos
            unk_pos_x = ui16[isRef16 + 6] #map pos maybe?
            unk_pos_y = ui16[isRef16 + 7] #map pos maybe?
            rotation = ui8[isRef8 + 2]
            #make update entity pos here!

            isRef8  += 18
            isRef16 += 9
            i += 1
       
    async def OnAreas(self, ui8: bytearray, bot_id: int):
        print(f'{bot_id} OnAreas')
    async def OnTeamCreated(self,data, bot_id: int):
        print(f'OnTeamCreated {data}')
        if data[3] == 'BOT':
            self.bots[bot_id].wantcommand = f'[30,{data[1]}]'
    async def OnOldVersion(data: bytes, bot_id: int):
        print(f'OnOldVersion {data}')
        ui16 = struct.unpack(f'{len(data)//2}H', data)
        error_id = ui16[1]
    async def OnServerFull(bot_id: int):
        print(f'OnServerFull')
    async def OnPlayerDie(self, ui8: bytearray, bot_id: int):
        print('OnPlayerDie')
        killer = (ui8[1] << 8) + ui8[2]
    async def OnOtherDie(self, ui8: bytearray, bot_id: int):
        print('OnOtherDie')
        player_id = ui8[1]
    async def OnFailRestoreSession(self, bot_id: int):
        print('OnFailRestoreSession')
    async def OnStoleYourSession(self, bot_id: int):
        print('OnStoleYourSession')
    async def OnMute(self, ui8: bytearray, bot_id: int):
        print('OnMute')
        delay = ui8[1]
    async def OnLeaderboard(self, data: bytes, ui8: bytearray, bot_id: int):
        print('OnLeaderboard')
        ui16 = struct.unpack(f'{len(data)//2}H', data)
        for i in range(10):
            player_id = ui8[2 + (i * 4)]
            player_score = ui16[2 + (i * 2)]
            player_karma = ui8[3 + (i * 4)]
    async def OnKickInactivity(self, bot_id: int):
        print('OnKickInactivity')
    async def OnNotification(self, ui8: bytearray, bot_id: int):
        print('OnNotification')
        player_id = ui8[1]
        notification = ui8[2] >> 2
        notification_level = ui8[2] & 3
    async def OnGauges(self, ui8: bytearray, bot_id: int): #like hud info!
        print('OnGauges')
        life  = ui8[1]
        food = ui8[2]
        cold = ui8[3]
        stamina = ui8[4]
        radiation = ui8[5]
    async def OnScore(self, data: bytes, bot_id: int):
        print('OnScore')
        ui16 = struct.unpack(f'{len(data)//2}H', data)
        experience = (ui16[1] << 16) + ui16[2] 
    async def OnPlayerHit(self, ui8: bytearray, bot_id: int): #like hud info!
        print('OnPlayerHit')
        player_id = ui8[1]
        angle = ui8[2] #hurt angle like ((angle * 2) * pi) / 255
    async def OnFullInventory(self, ui8: bytearray, bot_id: int): #like hud info!
        print('OnFullInventory')
        i = 1
        j = 0
        while (i < len(ui8)): #inventory items
            item_id = ui8[i]
            #inventory[1] = ui8[i + 1] #unknow
            #inventory[2] = ui8[i + 2] #unknow
            #inventory[3] = ui8[i + 3] #unknow
            #inventory[0] = item_id #unknow
            i += 4
            j += 1
    async def OnDeleteItem(self, ui8: bytearray, bot_id: int): #like hud info!
        print('OnDeleteItem')
        #for inventory
        #if inventory[i][0] == ui8[1] and ... and ... and ...:
        #inventory[i][0] = 0 #unknow
        #inventory[i][1] = 0 #unknow
        #inventory[i][2] = 0 #unknow
        #inventory[i][3] = 0 #unknow
    #api end
    async def Callbacks(self, data: bytes, bot_id: int):
        # print(f'callback from {bot_id}')
        ui8 = bytearray(data)
        if data[0] in caseMap:
            case_number = caseMap[data[0]]
            if case_number == newCaseNumbers[0]:
                await self.OnUnits(data, ui8, bot_id)
            elif case_number == newCaseNumbers[1]:
                await self.OnOldVersion(data, bot_id)
            elif case_number == newCaseNumbers[2]:
                await self.OnServerFull(bot_id)
            elif case_number == newCaseNumbers[3]:
                await self.OnPlayerDie(ui8, bot_id)
            elif case_number == newCaseNumbers[4]:
                await self.OnOtherDie(ui8, bot_id)
            elif case_number == newCaseNumbers[5]:
                await self.OnFailRestoreSession(bot_id)
            elif case_number == newCaseNumbers[6]:
                await self.OnStoleYourSession(bot_id)
            elif case_number == newCaseNumbers[7]:
                await self.OnMute(ui8, bot_id)
            elif case_number == newCaseNumbers[8]:
                await self.OnLeaderboard(data, ui8, bot_id)
            elif case_number == newCaseNumbers[9]:
                await self.OnHandshake(data, ui8, bot_id)
            elif case_number == newCaseNumbers[10]:
                await self.OnKickInactivity(bot_id)
            elif case_number == newCaseNumbers[11]:
                await self.OnNotification(ui8, bot_id)
            elif case_number == newCaseNumbers[12]:
                await self.OnGauges(ui8, bot_id)
            elif case_number == newCaseNumbers[13]:
                await self.OnScore(data, bot_id)
            elif case_number == newCaseNumbers[14]:
                await self.OnPlayerHit(ui8, bot_id)
            elif case_number == newCaseNumbers[15]:
                await self.OnFullInventory(ui8, bot_id)
            elif case_number == newCaseNumbers[16]:
                await self.OnDeleteItem(ui8, bot_id)
            elif case_number == newCaseNumbers[17]:
                await self.OnNewItem(ui8, bot_id)
            elif case_number == newCaseNumbers[18]:
                await self.OnPlayerLife(ui8[1], bot_id)
            elif case_number == newCaseNumbers[19]:
                await self.OnLifeDecreas(bot_id)
            elif case_number == newCaseNumbers[20]:
                await self.OnSelectedItem(ui8, bot_id)
            elif case_number == newCaseNumbers[21]:
                await self.OnLifeStop(bot_id)
            elif case_number == newCaseNumbers[22]:
                await self.OnPlayerHeal(ui8[1], bot_id)
            elif case_number == newCaseNumbers[23]:
                await self.OnStaminaIncrease(bot_id)
            elif case_number == newCaseNumbers[24]:
                await self.OnStaminaStop(bot_id)
            elif case_number == newCaseNumbers[25]:
                await self.OnStaminaDecrease(bot_id)
            elif case_number == newCaseNumbers[26]:
                await self.OnColdIncrease(bot_id)
            elif case_number == newCaseNumbers[27]:
                await self.OnColdStop(bot_id)
            elif case_number == newCaseNumbers[28]:
                await self.OnColdDecrease(bot_id)
            elif case_number == newCaseNumbers[29]:
                await self.OnPlayerStamina(ui8[1], bot_id)
            elif case_number == newCaseNumbers[30]:
                await self.OnLifeIncrease(bot_id)
            elif case_number == newCaseNumbers[31]:
                await self.OnReplaceItem(ui8, bot_id)
            elif case_number == newCaseNumbers[32]:
                await self.OnStackItem(ui8, bot_id)
            elif case_number == newCaseNumbers[33]:
                await self.OnSplitItem(ui8, bot_id)
            elif case_number == newCaseNumbers[34]:
                await self.OnReplaceAmmo(ui8, bot_id)
            elif case_number == newCaseNumbers[35]:
                await self.OnStartInteraction(ui8[1], bot_id)
            elif case_number == newCaseNumbers[36]:
                await self.OnInterruptInteraction(bot_id)
            elif case_number == newCaseNumbers[37]:
                await self.OnReplaceItemAndAmmo(ui8, bot_id)
            elif case_number == newCaseNumbers[38]:
                await self.OnBlueprint(ui8[1], bot_id)
            elif case_number == newCaseNumbers[39]:
                await self.OnDay(bot_id)
            elif case_number == newCaseNumbers[40]:
                await self.OnNight(bot_id)
            elif case_number == newCaseNumbers[41]:
                await self.OnPlayerXp((ui8[1] << 8) + ui8[2], bot_id)
            elif case_number == newCaseNumbers[42]:
                await self.OnPlayerXpSkill(ui8, bot_id)
            elif case_number == newCaseNumbers[43]:
                await self.OnBoughtSkill(ui8[1], bot_id)
            elif case_number == newCaseNumbers[44]:
                await self.OnStartCraft(ui8[1], bot_id)
            elif case_number == newCaseNumbers[45]:
                await self.OnLostBuilding(bot_id)
            elif case_number == newCaseNumbers[46]:
                await self.OnOpenBuilding(ui8, bot_id)
            elif case_number == newCaseNumbers[47]:
                await self.OnNewFuelValue(ui8, bot_id)
            elif case_number == newCaseNumbers[48]:
                await self.OnRadOn(bot_id)
            elif case_number == newCaseNumbers[49]:
                await self.OnRadOff(bot_id)
            elif case_number == newCaseNumbers[50]:
                await self.OnWarmOn(bot_id)
            elif case_number == newCaseNumbers[51]:
                await self.OnWarmOff(bot_id)
            elif case_number == newCaseNumbers[52]:
                await self.OnWrongTool(ui8[1], bot_id)
            elif case_number == newCaseNumbers[53]:
                await self.OnFullChest(ui8, bot_id)
            elif case_number == newCaseNumbers[54]:
                await self.OnAcceptedTeam(ui8[1], ui8[2], bot_id)
            elif case_number == newCaseNumbers[55]:
                await self.OnKickedTeam(ui8[1], bot_id)
            elif case_number == newCaseNumbers[56]:
                await self.OnDeleteTeam(ui8[1], bot_id)
            elif case_number == newCaseNumbers[57]:
                await self.OnJoinTeam(ui8[1], bot_id)
            elif case_number == newCaseNumbers[58]:
                await self.OnTeamPosition(ui8, bot_id)
            elif case_number == newCaseNumbers[59]:
                await self.OnKarma(ui8[1], bot_id)
            elif case_number == newCaseNumbers[60]:
                await self.OnBadKarma(ui8, bot_id)
            elif case_number == newCaseNumbers[61]:
                await self.OnAreas(ui8, bot_id)
            elif case_number == newCaseNumbers[62]:
                await self.OnWrongPassword(bot_id)
            elif case_number == newCaseNumbers[63]:
                await self.OnModdedGaugesValues(data, bot_id)
            elif case_number == newCaseNumbers[64]:
                await self.OnShakeExplosionState(ui8[1], bot_id)
            elif case_number == newCaseNumbers[65]:
                await self.OnPlayerEat(ui8[1], bot_id)
            elif case_number == newCaseNumbers[66]:
                await self.OnCitiesLocation(ui8, bot_id)
            elif case_number == newCaseNumbers[67]:
                await self.OnPoisened(ui8[1], bot_id)
            elif case_number == newCaseNumbers[68]:
                await self.OnRepellent(ui8[1], ui8[2], bot_id)
            elif case_number == newCaseNumbers[69]:
                await self.OnLapadoine(ui8[1], ui8[2], bot_id)
            elif case_number == newCaseNumbers[70]:
                await self.OnResetDrug(ui8[1], ui8[2], bot_id)
            elif case_number == newCaseNumbers[71]:
                await self.OnDramaticChrono(ui8[1], bot_id)
            elif case_number == newCaseNumbers[72]:
                await self.FeederonWarmOn(bot_id)
            elif case_number == newCaseNumbers[73]:
                await self.FeederonWarmOff(bot_id)
        

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
                        if response[0] == 0:
                            await self.controller.OnChatMessage(response, self.id)
                        elif response[0] == 1:
                            await self.controller.OnNewPlayer(response, self.id)
                        elif response[0] == 2:
                            await self.controller.OnNicknamesToken(response, self.id)
                        elif response[0] == 3:
                            await self.controller.OnAlert(response, self.id)
                        elif response[0] == 4:
                            await self.controller.OnTeamCreated(response, self.id)
                        elif response[0] == 5:
                            await self.controller.OnTeamName(response, self.id)
                        
                except Exception as e:
                    if not self.died:
                        print(f'{self.nickname} {self.id} died! Reconnecting...')
                        await self.controller.Error(self.id)
                        await self.controller.CreateBot(self.nickname)
                        break
                    print(f"[{self.id}] Error in Handle: {e}")
                    break