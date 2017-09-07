#!/usr/bin/python3

import os
import sys
import time
import datetime

import discord
import asyncio

import praw

args = sys.argv

# Pull a bunch of setting from envvars.
rclientid = os.environ['rclientid']
rclientsecret = os.environ['rclientsecret']
rusername = 'AounBot' # I shouldn't hardcode this, but whatever.
rpassword = os.environ['rpassword']
ruseragent = 'AounBot by /u/Treyzania for /r/NEU'
rsubreddit = 'NEU+CCIS+Racket'
rsleep = 60 # Ever 60 seconds.  Also shouldn't hardcode this.
dclientid = os.environ['dclientid']
dserverid = os.environ['dserverid']
dchannelname = os.environ['dchannelname']
dinvite = os.environ['dinvite']

# Set up the Discord client.
dc = discord.Client()

# Set up the reddit wrapper.
reddit = praw.Reddit( \
    client_id = rclientid, \
    client_secret = rclientsecret, \
    username = rusername, \
    password = rpassword, \
    user_agent = ruseragent)

@asyncio.coroutine
async def reddit_loop(chan):
    # We have to set the last time we checked to the current time so that we don't check stuff all the way in the past.
    lastcheck = datetime.datetime.utcnow()
    # Also wait until Discord is set up, if it isn't already.
    await dc.wait_until_ready()
    # Pull the subreddit handles.
    neusub = reddit.subreddit(rsubreddit)
    while True:
        print('Checking subreddits...')
        recent = neusub.new(limit = 5) # Limit 5 to be nice.
        for p in recent:
            # If we already passed it then don't announce it.
            if datetime.datetime.utcfromtimestamp(p.created_utc) > lastcheck: # Ugly but works.
                print('posting', str(p))
                await dc.send_message(chan, '➤ **New reddit post:** ' + p.shortlink)
            else:
                print('ignoring', str(p))
        lastcheck = datetime.datetime.utcnow()
        await asyncio.sleep(rsleep)

@dc.event
async def on_ready():
    print('Discord Username:', dc.user.name)
    print('Discord UID:', dc.user.id)
    print('Discord Invite: https://discordapp.com/oauth2/authorize?client_id={}&scope=bot'.format(dc.user.id))
    # Ugly way to look up channel by name.
    for s in dc.servers:
        for c in s.channels:
            if c.name == dchannelname:
                dc.loop.create_task(reddit_loop(c))

# Get it all going.
print('Got user ID:', dclientid)
dc.run(dclientid)
