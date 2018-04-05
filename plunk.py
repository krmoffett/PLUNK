#!/usr/bin/env python3
from discord.ext import commands
import discord
import re
import asyncio
import configparser
import requests

#bot = discord.Client()
config = configparser.ConfigParser()
config.read('config.ini')
defaultConfig = config['DEFAULT']
token = defaultConfig['token']
prefix = defaultConfig['prefix']
preflen = len(prefix)
api_key = defaultConfig['api_key']
bot = commands.Bot(command_prefix=prefix)
startup_extensions = ['commands.members', 'commands.pubg']

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

""" @bot.event
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

        await bot.send_message(message.channel, embed=em)
 """
if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    bot.run(token)
