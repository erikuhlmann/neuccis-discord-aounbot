#!/usr/bin/env python3

import os
import sys

import discord
import asyncio

args = sys.argv
user_id = args[0]
server_id = args[1]
channel_id = args[2]

client = discord.Client()

config = {
    'intro_channel': 'introductions'
    'groups': {
        '\'first': '1st Year',
        '\'second': '2nd Year',
        '\'third': '3rd Year',
        '\'fourth': '4th Year',
        '\'fifth': '5th Year',
        '\'grad': 'Grad Student',
        '\'alum': 'Alum'
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

@client.event
async def on_ready():
    print('Username:', client.user.name)
    print('UID:', client.user.id)
    print('READY TO ROCK AND ROLL BABY')

@client.event
async def on_member_join(member):
    print('New user', client.user.name)
    serv = client.get_server(server_id)
    chan = server.get_channel(channel_id)
    client.send_message(chan, get_join_message(member))

@client.event
async def on_message(message):
    if message.channel.id != channel_id:
        return
    for k, v in config.groups.items():
        if message.content.contains(k):
            print('Trying to assign role', v, 'to', message.user.name, '...')
            role = find_role(v)
            client.add_roles(message.user, role)
            print('OK!')

client.run(user_id)
