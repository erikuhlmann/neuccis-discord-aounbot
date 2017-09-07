#!/usr/bin/python3

import os
import sys

import discord
import asyncio

# Pull params from CLI options.
args = sys.argv
user_id = args[1]
server_id = args[2]
channel_name = args[3]
invite = args[4]

# Set up the Discord client.
client = discord.Client()

# Shouldn't have hardcoded this.
config = {
    'groups': [
        ('first', '1st year'),
        ('second', '2nd year'),
        ('third', '3rd year'),
        ('fourth', '4th year'),
        ('fifth', '5th year'),
        ('grad', 'grad-student'),
        ('alum', 'alum')
    ]
}

# Generates the join message given a username.
def gen_join_message(user):
    message = 'Hi there, {}!  Welcome to the NEU CCIS Discord server!  Please state your year to be assigned a group!'.format(user.mention)
    for entry in config['groups']:
        message += ('\n➤ `' + entry[0] + '` ⇒ ' + entry[1])
    return message

# Finds the role by name.
def find_role(name):
    serv = client.get_server(server_id)
    for r in serv.roles:
        if r.name == name:
            return r

# Finds a channel by name.
def get_channel(name):
    serv = client.get_server(server_id)
    if serv is None:
        client.accept_invite(invite)
        client.get_server(server_id)
    for c in serv.channels:
        if c.name == name:
            return c
    return None

@client.event
async def on_ready():
    print('Username:', client.user.name)
    print('UID:', client.user.id)
    print('Invite: https://discordapp.com/oauth2/authorize?client_id={}&scope=bot'.format(client.user.id))
    print('READY TO ROCK AND ROLL BABY')
    print('--------')
    # Announce to the server that we're here.
    for s in client.servers:
        for c in s.channels:
            if c.name == channel_name:
                await client.send_message(c, 'Hello, World!')

# Hacky thing to actually broadcast the announcement message.
async def __broadcast_announce_message(member):
    chan = get_channel(channel_name)
    await client.send_message(chan, gen_join_message(member))

# Just blindly announce the join message.
@client.event
async def on_member_join(member):
    print('New user', member.name)
    await __broadcast_announce_message(member)

@client.event
async def on_message(message):

    # Check if the message is in the right channel.
    if message.channel.name != channel_name:
        return

    # Lol I'm not stupid.
    if message.author == client.user:
        return # Let's not mess with ourselves.

    # Debugger to check if the bot goes down.
    if message.content == '\'joinmessage':
        await __broadcast_announce_message(message.author)

    # Check to see if they already have a correct role before trying to add one on.
    ok = True
    for r in message.author.roles:
        for entry in config['groups']:
            if entry[1] == r.name:
                ok = False # They already have a role.
                break
    if ok:
        for entry in config['groups']:
            # Find the role by name.
            role = find_role(entry[1])
            if entry[0] in message.content:
                print('Trying to assign role', entry[1], 'to', message.author.name, '...')
                await client.add_roles(message.author, role)
                print('OK!\n')

# Actually kick everything off.
print('Got user ID', user_id)
client.run(user_id)
