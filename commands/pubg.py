from lib.helper import *
from discord.ext import commands
import discord
import re
import requests
import configparser

class PUBG():
    def __init__(self, bot):
        config = configparser.ConfigParser()
        config.read('config.ini')
        defaultConfig = config['DEFAULT']
        self.api_key = defaultConfig['api_key']
        self.bot = bot

    @commands.command(pass_context=True)
    async def last(self, ctx):
        discord_name = ctx.message.author.name
        name_fetch = getGameName(discord_name)
        name_found = False
        pubg_name = ""
        if name_fetch[0] == 0:
            name_found = True
            pubg_name = name_fetch[1] 
        else:
            self.bot.say(name_fetch[1])

        if name_found:
            url = 'https://api.playbattlegrounds.com/shards/pc-na/players?filter[playerNames]=' + pubg_name
            header = {
                    "Authorization": self.api_key,
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
                em = discord.Embed(colour = discord.Colour.orange())
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
    
def setup(bot):
    bot.add_cog(PUBG(bot))