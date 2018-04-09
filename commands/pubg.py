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

def setup(bot):
    bot.add_cog(Battlegrounds(bot))