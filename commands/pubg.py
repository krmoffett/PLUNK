from misc.helper import getGameName
from discord.ext import commands
from pubg_python import PUBG, Shard
import discord
import re
import requests
import configparser

class Battlegrounds():
    def __init__(self, bot):
        config = configparser.ConfigParser()
        config.read('config.ini')
        defaultConfig = config['DEFAULT']
        self.api_key = defaultConfig['api_key']
        self.api = PUBG(self.api_key, Shard.PC_NA)
        self.bot = bot


    @commands.command(pass_context=True)
    async def test(self, ctx):
        shroud = self.api.players().filter(player_names=['shroud'])[0]
        shrouds_last = self.api.matches().get(shroud.matches[0].id)
        #participants = shrouds_last.rosters[0].participants 
        print (shrouds_last) 

    @commands.command(pass_context=True)
    async def last(self, ctx): 
        """Retrieves the stats of the last game played"""
        if getGameName(ctx.message.author.name)[0] == 0:
            pubg_name = getGameName(ctx.message.author.name)[1]
            print ("Searching for {}'s last game".format(pubg_name))
            player = self.api.players().filter(player_names=[pubg_name])[0]
            last_match = self.api.matches().get(player.matches[0].id)
            player_found = False
            for roster in last_match.rosters:
                for participant in roster.participants:
                    if participant.name == pubg_name:
                        player_found = True
                        print (participant.name + "Game Found")
                        em = discord.Embed(colour = discord.Colour.orange())
                        em.title = "Stat's for {}'s last game".format(pubg_name)
                        em.add_field(name='Match Time', value=last_match.created_at, inline=True)
                        em.add_field(name='Match Duration', value=last_match.duration, inline=True)
                        em.add_field(name='Finishing Place', value=participant.win_place, inline=True)
                        em.add_field(name='Kills', value=participant.kills, inline=True)
                        em.add_field(name='Assists', value=participant.assists, inline=True)
                        em.add_field(name='Headshot Kills', value=participant.headshot_kills, inline=True)
                        em.add_field(name='Walk Distance', value=str(participant.walk_distance) + "m", inline=True)
                        em.add_field(name='Ride Distance', value=str(participant.ride_distance) + "m", inline=True)
                        em.add_field(name='Team Kills', value=participant.team_kills, inline=True)
                        await self.bot.send_message(ctx.message.channel, embed=em)
                        break
            if player_found == False:
                print ("Player not found")
        else:
            await self.bot.say("Name not found. Please use the addme command")

#        for p in participants:
#            if p.name == 'shroud':
#                print(p.name)
#                break

    """ @commands.command(pass_context=True)
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
                        em.add_field(name=field_name,value=field_value,inline=True) """
    
def setup(bot):
    bot.add_cog(Battlegrounds(bot))