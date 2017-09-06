#!/usr/bin/python3

import os
import sys
import time

import discord
import asyncio

import praw

args = sys.argv

rclientid = os.environ['rclientid']
rclientsecret = os.environ['rclientsecret']
rusername = 'AounBot' # I shouldn't hardcode this, but whatever.
rpassword = os.environ['rpassword']
ruseragent = 'AounBot by /u/Treyzania for /r/NEU'
rsubreddit = 'NEU' # Probably shouldn't hardcode this either.
rsleep = 60 # Ever 60 seconds.  Also shouldn't hardcode this.
dclientid = os.environ['dclientid']
dserverid = os.environ['dserverid']
dchannelname = os.environ['dchannelname']
dinvite = os.environ['dinvite']

dc = discord.Client()
dchannel = None

@dc.event
async def on_ready():
    print('Discord Username:', dc.user.name)
    print('Discord UID:', dc.user.id)
    print('Discord Invite: https://discordapp.com/oauth2/authorize?client_id={}&scope=bot'.format(dc.user.id))
    for s in dc.servers:
        for c in s.channels:
            if c.name == dchannelname:
                dchannel = c
                await dc.send_message(c, 'i read it on reddit')

reddit = praw.Reddit( \
    client_id=rclientid, \
    client_secret=rclientsecret, \
    username=rusername, \
    password1=rpassword, \
    user_agent=ruseragent)

#print('Reddit username:', reddit.user.me())
#print('Reddit auth code:', reddit.auth.authorize())

async def reddit_loop():
    dc.wait_until_ready()
    time.sleep(10)
    neusub = reddit.subreddit(rsubreddit)
    seen = []
    while True:
        print('Checking', rsubreddit, '...')
        recent = neusub.new(limit=5)
        for p in recent:
            if p in seen:
                break
            seen.append(p)
            if dc is not None:
                print('found new post', str(p))
                await dc.send_message(dchannel, '>>> New reddit post: ' + p.shortlink)
            else:
                print('found new post,', str(p), 'but we can\'t post it yet')
        time.sleep(rsleep)

print('Got user ID:', dclientid)
dc.loop.create_task(reddit_loop())
dc.run(dclientid)
