#!/usr/bin/env python3
from helper import *
import discord
import re
import asyncio
import configparser
import requests
import json
import os

client = discord.Client()
config = configparser.ConfigParser()
config.read('config.ini')
defaultConfig = config['DEFAULT']
token = defaultConfig['token']
prefix = defaultConfig['prefix']
preflen = len(prefix)
api_key = defaultConfig['api_key']
#url = "url_here"
#
#header = {
#        "Authorization": api_key,
#        "Accept": "application/vnd.api+json"
#}
#
#r = requests.get(url, headers=header)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
# Receive message
async def on_message(message):
    if message.content[0:preflen] == prefix:
        usrIn = message.content.split()
        if len(usrIn) < 2:
            usrIn.append('blank')
        em = discord.Embed(colour = discord.Colour.orange())

        command = usrIn[0][preflen:]
        if usrIn[1] == 'blank':
            usrIn.remove('blank')
        print ("User: " + message.author.name)
        print ("Message: " + message.content)
        print ("Command: " + command + "\n")
        #List commands here
        if command == 'hello':      # Test command
            em.description = "hello there!"

        elif command == 'addMe' or command == 'add':      # Adds authors supplied PUBG name to a dictionary with
            if len(usrIn) < 2:     # the discord name as the key and writes to playerNames.dat
                em.description = "use: {}addMe *<in-game-name>*".format(prefix)
            else:
                player_dict = {}
                if os.path.isfile('playerNames.dat'):
                    with open('playerNames.dat', 'r') as player_data:
                        if os.stat('playerNames.dat').st_size == 0:
                            pass
                        else:
                            player_dict = json.load(player_data)
                else:
                    with open('playerNames.dat','w+'):
                        pass
                discord_name = ""
                pubg_name = ""
                if len(usrIn) == 2:
                    pubg_name = usrIn[1]
                    discord_name = message.author.name
                else:
                    pubg_name = usrIn[2]
                    discord_name = usrIn[1]
                player_dict[discord_name] = pubg_name
                with open('playerNames.dat', 'w') as player_data:
                    json.dump(player_dict, player_data)
                em.description = "Added {} as {}".format(discord_name, pubg_name)

        elif command == 'deleteMe':
            if len(usrIn) != 1:
                em.description = "use: {}deleteMe".format(prefix)
            else:
                if os.path.isfile('playerNames.dat'):
                    player_dict = {}
                    with open('playerNames.dat', 'r') as player_data:
                        player_dict = json.load(player_data)
                    discord_name = message.author.name
                    if discord_name in player_dict:
                        del player_dict[discord_name]
                        with open('playerNames.dat', 'w') as player_data:
                            json.dump(player_dict, player_data)
                        em.description = "Removed {} from list".format(discord_name)
                    else:
                        em.description = "Could not find {} in list".format(discord_name)
                else:
                    em.description = "Data file does not exist"

        elif command == 'list' or command == 'listPlayers':
            if len(usrIn) != 1:
                em.description = "Unexpected argument detected."
            else:
                if os.path.isfile('playerNames.dat'):
                    if os.stat('playerNames.dat').st_size == 0:
                        em.description = "Data file is empty"
                    else:
                        em.title = ('Registered PUBG Usernames:')
                        player_dict = {}
                        with open('playerNames.dat', 'r') as player_data:
                            player_dict = json.load(player_data)
                        if player_dict:
                            for key in player_dict:
                                em.add_field(name=key,value=player_dict[key], inline=True)
                        else:
                            em.description = "Nobody here :("
            
        elif command == 'lastGame' or command == 'last':
            discord_name = message.author.name
            name_fetch = getGameName(discord_name)
            name_found = False
            pubg_name = ""
            if name_fetch[0] == 0:
                name_found = True
                pubg_name = name_fetch[1] 
            else:
                em.description = name_fetch[1]

            if name_found:
                url = 'https://api.playbattlegrounds.com/shards/pc-na/players?filter[playerNames]=' + pubg_name
                header = {
                        "Authorization": api_key,
                        "Accept": "application/vnd.api+json"
                }
                r = requests.get(url, headers=header)
                json_player = r.json()

                last_match_id = 0

                if len(json_player['data'][0]['relationships']['matches']['data']) > 0:                 # Determine if there
                    last_match_id = json_player['data'][0]['relationships']['matches']['data'][0]['id'] # is match data saved
                                                                                                        # for player
                if last_match_id != 0:
                    url = 'https://api.playbattlegrounds.com/shards/pc-na/matches/' + last_match_id     # Retrieve data from
                    r = requests.get(url, headers=header)                                               # last match
                    json_match = r.json()
                    participant_list = []
                    match_time = json_match['data']['attributes']['createdAt'] 
                    match_length = json_match['data']['attributes']['duration']
                    for i in json_match['included']:
                        if i['type'] == 'participant':
                            participant_list.append(i)

                    player_stats = {}
                    for p in participant_list:
                        if p['attributes']['stats']['name'] == pubg_name:
                            player_stats = p['attributes']['stats']
                    em.title = "Stats for {}'s last game:".format(pubg_name)
                    em.add_field(name='Match Date',value=match_time,inline=True)
                    em.add_field(name='Match Duration',value=match_length,inline=True)
                    em.add_field(name='Finishing Place',value=player_stats['winPlace'],inline=True)
                    excluded = ['name','killPointsDelta','winPlace','lastWinPoints','killPoints','playerId','winPoints',\
                            'winPointsDelta','lastKillPoints','mostDamage']
                    for key in player_stats:
                        if key not in excluded:
                            field_name = key
                            field_value = player_stats[key]
                            field_name = re.sub("([A-Z])"," \g<0>",field_name)
                            em.add_field(name=field_name,value=field_value,inline=True)



        elif command == 'help':
            em.description = "Available commands:\n\t```{0}hello\n".format(prefix) + \
                "{0}addMe <in-game-name>\n".format(prefix) + \
                "{0}deleteMe\n".format(prefix)+ \
                "{0}listPlayers```".format(prefix)

        else:
            em.description = "Command not recognized.\nPlease use " + prefix + "help for a list of commands"

        await client.send_message(message.channel, embed=em)

client.run(token)
