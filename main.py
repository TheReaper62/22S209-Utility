from typing import Union
import os
import discord

from datetime import datetime

import config as CONF

# Fucntions
def match(raw,words):
    return any([i in raw.lower() for i in words])

client = discord.Bot()

@client.event
async def on_ready():
    print("Bot Online")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if match(message.content,['hi','hello']):
        await message.channel.send(f'Hi {message.author.mention}!!!')
    elif match(message.content,['attire']):
        today = datetime.today().weekday()
        tmr = today+1 if (today+1)<=6 else 0
        embed = discord.Embed(
            title = 'Attire',
            description = f"**Today's Attire**:\n{CONF.attire[today]}\n\n**Tomorrow's Attire**\n:{CONF.attire[tmr]}",
            colour = discord.Colour(0xE66E6B)
        )
        await message.channel.send(embed=embed)
        
client.run(os.environ['token'])
