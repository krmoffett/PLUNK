from datetime import datetime 
import os
import json

def getGameName(discord_name):
    player_dict = {}

    if os.path.isfile('playerNames.dat'):
        if os.stat('playerNames.dat').st_size == 0:
            return None
        else:
            with open('playerNames.dat', 'r') as player_data:
                player_dict = json.load(player_data)
            if discord_name in player_dict:
                return player_dict[discord_name]
            else:
                return None
def parseDate(date_string):
    months = dict([(1,'Jan'), (2,'Feb'), (3,'Mar'), (4,'Apr'), (5,'May'), (6,'Jun'), (7,'Jul'),\
    (8,'Aug'), (9,'Sep'), (10,'Oct'), (11,'Nov'), (12,'Dec')])
    date_string = date_string.split('T')
    date = date_string[0].split('-')
    year = date[0]
    month = date[1]
    day = date[2]
    date = day + " " + months[int(month)] + " " + year
    time = date_string[1].split('Z')[0]
    return (date, time)

def getTimeSince(match_time):
    currentTime = datetime.now()
    diff = currentTime - match_time
    return diff