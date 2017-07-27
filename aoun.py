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
    'groups': {
        '\'first': '1st year',
        '\'second': '2nd year',
        '\'third': '3rd year',
        '\'fourth': '4th year',
        '\'fifth': '5th year',
        '\'grad': 'grad-student',
        '\'alum': 'alum'
    }
}

def gen_join_message(user):
    message = 'Hi there, {}!  Welcome to the NEU CCIS Discord server!  Please state your year to be assigned a group!' % user.mention
    for k, v in config.groups.items():
        message.append('\n')
        message.append('* `' + k + '`: ' + v)
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

@client.event
async def on_ready():
    print('Username:', client.user.name)
    print('UID:', client.user.id)
    print('Invite: https://discordapp.com/oauth2/authorize?client_id={}&scope=bot'.format(client.user.id))
    print('READY TO ROCK AND ROLL BABY')
    chan = get_channel(channel_name)
    client.send_message(chan, 'Hello, World!')

@client.event
async def on_member_join(member):
    print('New user', client.user.name)
    chan = get_channel(channel_name)
    client.send_message(chan, get_join_message(member))

@client.event
async def on_message(message):
    if message.channel.name != channel_name:
        return
    for k, v in config.groups.items():
        role = find_role(v)
        if role in message.user.roles:
            return
        if message.content.contains(k):
            print('Trying to assign role', v, 'to', message.user.name, '...')
            client.add_roles(message.user, role)
            print('OK!')

print('Got user ID', user_id)
client.run(user_id)
