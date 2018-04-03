#!/usr/bin/env python3
import discord
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

        elif command == 'addMe':      # Adds authors supplied PUBG name to a dictionary with
            if len(usrIn) != 2:     # the discord name as the key and writes to playerNames.dat
                em.description = "use: {}addMe *<in-game-name>*".format(prefix)
            else:
                player_dict = {}
                with open('playerNames.dat', 'w+') as player_data:
                    if os.stat('playerNames.dat').st_size == 0:
                        pass
                    else:
                        player_dict = json.load(player_data)
                discord_name = message.author.name
                pubg_name = usrIn[1]
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
                        em.description = "__**{0:<30}{1:>30}**__\n".format('Discord Name', 'PUBG Name')
                        player_dict = {}
                        with open('playerNames.dat', 'r') as player_data:
                            player_dict = json.load(player_data)
                        if player_dict:
                            for key in player_dict:
                                em.description += "{0:<30}{1:>30}\n".format(key, player_dict[key])
                        else:
                            em.description = "Nobody here :("
            
        elif command == 'help':
            em.description = "Available commands:\n\t{}hello".format(prefix)

        else:
            em.description = "Command not recognized.\nPlease use " + prefix + "help for a list of commands"

        await client.send_message(message.channel, embed=em)

client.run(token)
