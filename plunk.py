#!/usr/bin/env python3
from discord.ext import commands
import discord
import re
import asyncio
import configparser
import requests

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

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    bot.run(token)