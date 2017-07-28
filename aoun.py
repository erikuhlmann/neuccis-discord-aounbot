#!/usr/bin/python3

import os
import sys

import discord
import asyncio

args = sys.argv
user_id = args[1]
server_id = args[2]
channel_name = args[3]
invite = args[4]

client = discord.Client()

config = {
    'groups': [
        ('\'first', '1st year'),
        ('\'second', '2nd year'),
        ('\'third', '3rd year'),
        ('\'fourth', '4th year'),
        ('\'fifth', '5th year'),
        ('\'grad', 'grad-student'),
        ('\'alum', 'alum')
    ]
}

def gen_join_message(user):
    message = 'Hi there, {}!  Welcome to the NEU CCIS Discord server!  Please state your year to be assigned a group!'.format(user.mention)
    for entry in config['groups']:
        message += ('\n➤ `' + entry[0] + '` ⇒ ' + entry[1])
    return message

def find_role(name):
    serv = client.get_server(server_id)
    for r in serv.roles:
        if r.name == name:
            return r

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
    for s in client.servers:
        for c in s.channels:
            if c.name == channel_name:
                await client.send_message(c, 'Hello, World!')

async def __broadcast_announce_message(member):
    chan = get_channel(channel_name)
    await client.send_message(chan, gen_join_message(member))

@client.event
async def on_member_join(member):
    print('New user', member.name)
    await __broadcast_announce_message(member)

@client.event
async def on_message(message):

    if message.channel.name != channel_name:
        return

    if message.author == client.user:
        return # Let's not mess with ourselves.

    if message.content == '\'joinmessage':
        await __broadcast_announce_message(message.author)

    ok = True
    for r in message.author.roles:
        for entry in config['groups']:
            if entry[1] == r.name:
                ok = False # They already have a role.
                break
    if ok:
        for entry in config['groups']:
            role = find_role(entry[1])
            if entry[0] in message.content:
                print('Trying to assign role', entry[1], 'to', message.author.name, '...')
                await client.add_roles(message.author, role)
                print('OK!\n')


print('Got user ID', user_id)
client.run(user_id)
