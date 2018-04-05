import os
import json

def getGameName(discord_name):
    player_dict = {}

    if os.path.isfile('playerNames.dat'):
        if os.stat('playerNames.dat').st_size == 0:
            return (1, "Data file is empty")
        else:
            with open('playerNames.dat', 'r') as player_data:
                player_dict = json.load(player_data)
            if discord_name in player_dict:
                return (0, player_dict[discord_name])
            else:
                return (1, "Player name not found")
