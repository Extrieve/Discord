# Make a discord bot application with music functionality
import discord
import asyncio
import youtube_dl
import os
from discord.ext import commands
from discord.ext.commands import Bot
import random
import time
import datetime
import json
import requests
import urllib.request
import urllib.parse
import urllib.error
import re
import sys
import os


# Create discord bot class
class MyClient(discord.Client):
    # Create discord bot on_ready function
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        await self.change_presence(game=discord.Game(name='!help'))
    
    # Create on_member_join method
    async def on_member_join(self, member):
        # Send message to server
        await self.send_message(member, "Welcome to the server, {}".format(member.mention))
        # Send message to channel
        await self.send_message(member.server.get_channel('channel_id'), "{} joined the server!".format(member.mention))

    # Create discord bot on_message function
    async def on_message(self, message):
        # check if message is from ourselves
        if message.author == self.user:
            return
        # check if message is from a bot
        if message.author.bot:
            return

        # reply with a joke if users ask for a joke
        if message.content.startswith('!joke'):
            # get a random joke
            joke = requests.get('https://icanhazdadjoke.com/', headers={"Accept": "application/json"})
            # send the joke
            await message.channel.send(message.channel, joke.json()['joke'])

        # reply with an anime fact if users ask for one
        if message.content.startswith('!anime'):
            # get a random anime fact
            anime = requests.get('https://anime-fact.herokuapp.com/random')
            # send the fact
            await message.channel.send(message.channel, anime.json()['fact'])

# initialize intents with admin settings
intents = discord.Intents.default()
intents.members = True

# start client object
client = MyClient()
# run client
client.run('token')

        
