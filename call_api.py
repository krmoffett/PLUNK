#!/usr/bin/env python3
import requests
import configparser
import json

config = configparser.ConfigParser()
config.read('config.ini')
defaultConfig = config['DEFAULT']
api_key = str(defaultConfig['api_key'])
url = "https://api.playbattlegrounds.com/shards/pc-na/matches/276f5bcb-a831-4e8c-a610-d2073692069e"

header = {
        "Authorization": api_key,
        "Accept": "application/vnd.api+json"
}

r = requests.get(url, headers=header)
print (r)
