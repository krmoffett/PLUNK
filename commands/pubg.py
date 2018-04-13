from misc.helper import getGameName, parseDate, getTimeSince
from discord.ext import commands
from pubg_python import PUBG, Shard
import discord
import configparser

class Battlegrounds():
    def __init__(self, bot):
        config = configparser.ConfigParser()
        config.read('config.ini')
        defaultConfig = config['DEFAULT']
        self.api_key = defaultConfig['api_key']
        self.api = PUBG(self.api_key, Shard.PC_NA)
        self.bot = bot

    def embedStats(self, match, participant, killer):
        """Take in player and match objects to be embedded for message"""
        em = discord.Embed(colour = discord.Colour.orange())
        match_datetime = parseDate(match.created_at)
        em.description = "Created At: {}, {} UTC".format(match_datetime[0], match_datetime[1])
        em.description += "\nMatch ID: {}".format(match.id)
        em.add_field(name='Match Type', value=match.game_mode, inline=True)
        em.add_field(name='Finishing Place', value=participant.win_place, inline=True)
        em.add_field(name='Kills', value=participant.kills, inline=True)
        em.add_field(name='Assists', value=participant.assists, inline=True)
        em.add_field(name='Headshot Kills', value=participant.headshot_kills, inline=True)
        em.add_field(name='Walk Distance', value=str(participant.walk_distance) + "m", inline=True)
        em.add_field(name='Ride Distance', value=str(participant.ride_distance) + "m", inline=True)
        em.add_field(name='Team Kills', value=participant.team_kills, inline=True)
        em.add_field(name='Killed by', value=killer, inline=True)
        return em    

    @commands.command(pass_context=True)
    async def last(self, ctx, supplied_name=None): 
        """Retrieves the stats of the last game played
        
        If no name is provided, the data file will be searched for the user's discord name.
        Parameters:
        supplied_name -- the PUBG in game name to search for
        """
        if not supplied_name and not getGameName(ctx.message.author.name):
            await self.bot.say("No name found. Please use: `{}help last` for usage instructions".format(self.bot.command_prefix))
            return
        pubg_name = getGameName(ctx.message.author.name)
        if supplied_name:
            pubg_name = supplied_name
        print ("Searching for {}'s last game".format(pubg_name))
        search_message = await self.bot.send_message(ctx.message.channel, "Searching...")
        player = None
        try:
            player = self.api.players().filter(player_names=[pubg_name])[0]
        except Exception:
            await self.bot.edit_message(search_message, "{} not found".format(pubg_name))
            return
        try:
            last_match = self.api.matches().get(player.matches[0].id)
        except Exception:
            await self.bot.edit_message(search_message, "No recent matches for {}".format(pubg_name))
        asset = last_match.assets[0]
        telemetry = self.api.telemetry(asset.url)
        player_kill_events = telemetry.events_from_type('LogPlayerKill')
        killer = "#unkown"
        for event in player_kill_events:
            if event.victim.name == pubg_name:
                killer = event.killer.name
        player_found = False
        for roster in last_match.rosters:
            for participant in roster.participants:
                if participant.name == pubg_name:
                    player_found = True
                    print (participant.name + "Game Found")
                    em = self.embedStats(last_match, participant, killer)
                    em.title = "Stat's for {}'s last game".format(participant.name)
                    await self.bot.edit_message(search_message, new_content="Game Found", embed=em)
                    break
        if player_found == False:
            print ("Player not found")

    @commands.command(pass_context=True)
    async def matches(self, ctx, supplied_name=None): 
        """NEED HIGHER RATE LIMIT FOR THIS
        Returns a list of the last 5 matches for a player to choose from.

        Requires a response from the user. The bot will then find the stats of the selected game.
        Parameters:
        supplied-name -- the PUBG in game name to search for
        """
        if not supplied_name and not getGameName(ctx.message.author.name):
            await self.bot.say("No name found. Please use: `{}help matches` for usage instructions".format(self.bot.command_prefix))
            return
        pubg_name = getGameName(ctx.message.author.name)
        if supplied_name:
            pubg_name = supplied_name
        print ("Searching for {}'s last game".format(pubg_name))
        search_message = await self.bot.send_message(ctx.message.channel, "Searching...")
        player = None
        try:
            player = self.api.players().filter(player_names=[pubg_name])[0]
        except Exception:
            await self.bot.edit_message(search_message, "{} not found".format(pubg_name))
            return
        
        matches = []
        try:
            for m in player.matches[0:5]:
                matches.append(self.api.matches().get(m))
        except Exception as e:
            print(type(e).__name__, e)
            await self.bot.edit_message(search_message, "No recent matches for {}".format(pubg_name))
            return
        words = "***Most recent matches for {}***".format(pubg_name)
        for idx,m in enumerate(matches):
            for roster in m.rosters:
                for participant in roster.participants:
                    if participant.name == pubg_name:
                        words += "\n{}. *Date:* {}\t*Mode:*{}\t*Rank:*{}".format((idx-1), parseDate(m.created_at)[0], \
                        m.game_mode, participant.win_place)
        await self.bot.edit_message(search_message, words)

def setup(bot):
    bot.add_cog(Battlegrounds(bot))