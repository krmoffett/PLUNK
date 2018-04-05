import discord
import os
import json
from discord.ext import commands

class Members():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def addme(self, ctx, game_name : str):
        """Adds the discord user that called the command to the player list"""
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
        discord_name = ctx.message.author.name
        pubg_name = game_name
        player_dict[discord_name] = pubg_name
        with open('playerNames.dat', 'w') as player_data:
            json.dump(player_dict, player_data)
        await self.bot.say("Added {} as {}".format(discord_name, pubg_name))
        
    @commands.command()
    async def add(self, discord_name : str, pubg_name : str):
        """Adds the specified user to the player list"""
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
        player_dict[discord_name] = pubg_name
        with open('playerNames.dat', 'w') as player_data:
            json.dump(player_dict, player_data)
        await self.bot.say("Added {} as {}".format(discord_name, pubg_name))

    @commands.command(pass_context=True)
    async def deleteme(self, ctx):
        """Deletes the user that sent command from player list"""
        if os.path.isfile('playerNames.dat'):
            player_dict = {}
            with open('playerNames.dat', 'r') as player_data:
                player_dict = json.load(player_data)
            discord_name = ctx.message.author.name
            if discord_name in player_dict:
                del player_dict[discord_name]
                with open('playerNames.dat', 'w') as player_data:
                    json.dump(player_dict, player_data)
                await self.bot.say("Removed {} from list".format(discord_name))
            else:
                await self.bot.say("Could not find {} in list".format(discord_name))
        else:
            await self.bot.say("Data file does not exist")
    
    @commands.command()
    async def delete(self, p_name : str):
        """Removes specified player name from list"""
        if os.path.isfile('playerNames.dat'):
            player_dict = {}
            with open('playerNames.dat', 'r') as player_data:
                player_dict = json.load(player_data)
            discord_name = p_name
            if discord_name in player_dict:
                del player_dict[discord_name]
                with open('playerNames.dat', 'w') as player_data:
                    json.dump(player_dict, player_data)
                await self.bot.say("Removed {} from list".format(discord_name))
            else:
                await self.bot.say("Could not find {} in list".format(discord_name))
        else:
            await self.bot.say("Data file does not exist")

    @commands.command(pass_context=True)
    async def list(self, ctx):
        """List currently registered players"""
        if os.path.isfile('playerNames.dat'):
            if os.stat('playerNames.dat').st_size == 0:
                await self.bot.say("Data file is empty")
            else:
                player_dict = {}
                with open('playerNames.dat', 'r') as player_data:
                    player_dict = json.load(player_data)
                if player_dict:
                    em = discord.Embed(title="Registered PUBG Usernames:")
                    for key in player_dict:
                        em.add_field(name=key,value=player_dict[key], inline=True)
                    await self.bot.send_message(ctx.message.channel, embed=em)
                else:
                    await self.bot.say("Nobody here :(")
        else:
            await self.bot.say("Data file does not exits")

def setup(bot):
    bot.add_cog(Members(bot))