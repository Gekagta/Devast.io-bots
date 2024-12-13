import requests

class Server:
    def __init__(self, id: str, game_mode: str, max_players: int, players: int, distance: int, region: str):
        self.id = id
        self.game_mode = game_mode
        self.max_players = max_players
        self.players = players
        self.distance = distance
        self.region = region


def GetServerList():
    servers = []
    response = requests.get('https://matechmaker-o2y3.vercel.app/list')
    response = response.json()
    for lobby in response['lobbies']:
        game_mode = lobby['game_mode_id']
        id = lobby['lobby_id']
        max_players = lobby['max_players_normal']
        players = lobby['total_player_count']
        dist = None
        region_id = None
        for region in response['regions']:
            if region['region_id'] == lobby['region_id']:
                region_id = region['region_display_name']
                dist = round(region['datacenter_distance_from_client']['kilometers'])
        server = Server(id,game_mode,max_players,players,dist,region_id)
        servers.append(server)
    return servers