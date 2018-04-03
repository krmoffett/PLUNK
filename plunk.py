#!/usr/bin/env python3
import discord
import asyncio
import configparser
import request
import json

client = discord.Client()
config = configparser.ConfigParser()
config.read('config.ini')
defaultConfig = config['DEFAULT']
token = defaultConfig['token']
prefix = defaultConfig['prefix']
url = "url_here"

header = {
        "Authorization": "<api-key>",
        "Accept": "application/vnd.api+json"
}

r = requests.get(url, headers=header)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
# Receive message
async def on_message(message):
    usrIn = message.content.split()
    if len(usrIn) < 2:
        userIn.append('blank')
    preflen = len(prefix)
    response = ""
    if message.content[0:preflen] == prefix:
        command = usrIn[0][preflen:]
        print ("User: " + message.author.name)
        print ("Message: " + message.content)
        print ("Command: " + command + "\n")
        #List commands here
        if command == 'hello':      #test command
            response = "hello there!"

        elif command == 'help':
            response = "Available commands:\n\t!hello"

        else:
            response = "Command not recognized.\nPlease use " + prefix + "help for a list of commands"

        await client.send_message(message.channel, response)

client.run(token)
