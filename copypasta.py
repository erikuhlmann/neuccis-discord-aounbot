#!/usr/bin/env python

import discord
import asyncio
import random
import os

userid = os.environ['clientid']
serverid = os.environ['serverid']
invite = os.environ['invite']

text = open('copypasta.txt').read()
text = text.split("\n\n")

client = discord.Client()

@asyncio.coroutine
async def copypasta(server):
	while(True):
		textChannels = [i for i in list(server.channels) if i.type == discord.ChannelType.text]
		channel = random.choice(textChannels)
		#select random post from list of copypastas
		post = random.choice(text)

		await client.send_message(channel, post)
		await asyncio.sleep(random.randint(14400, 86400)) #wait for a random time between 4 and 24 hrs

@client.event
async def on_ready():
    print('Discord Username:', client.user.name)
    print('Discord UID:', client.user.id)
    print('Discord Invite: https://discordapp.com/oauth2/authorize?client_id={}&scope=bot'.format(client.user.id))
    for s in client.servers:
    	if s.id == serverid:
	    	client.loop.create_task(copypasta(s))

@client.event
async def on_message(message):
    if ("lonely" in message.content.lower()) and ("hackathon" in message.content.lower()):
    	await asyncio.sleep(random.randint(30, 90))
    	await client.send_message(message.channel, random.choice(text))

print('Got user ID:', userid)
client.run(userid)
