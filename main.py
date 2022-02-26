from typing import Union
import os
import discord

from datetime import datetime, timedelta

import config as CONF

# Fucntions
def match(raw,words):
    return any([i in raw.lower() for i in words])

client = discord.Bot(intents=discord.Intents.all())

@client.event
async def on_ready():
    print("Bot Online")

@client.event
async def on_member_join(member):
    await member.send(f'Welcome {member.mention}!\nPlease Identify yourself in #introductions before you get access to the rest of the server')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('|clear') and message.author.id in CONF.ADMIN_IDs:
        limit = int(message.content.split(' ')[1]) if len(message.content.split(' ')) > 1 else 10
        await message.channel.purge(limit=limit)
        await message.channel.send(f"Cleared {limit} messages", delete_after=3)
    if message.content.startswith('|reverify') and message.author.id in CONF.ADMIN_IDs:
        for member in message.guild.members:
            if 946341272015237150 not in [r.id for r in member.roles]:
                await member.send(f'Welcome {member.mention}!\nPlease Identify yourself in #introductions before you get access to the rest of the server')
    if match(message.content,['hi','hello']):
        await message.channel.send(f'Hi {message.author.mention}!!!')
    elif match(message.content,['attire']):
        today = datetime.today().weekday()
        tmr = today+1 if (today+1)<=6 else 0
        embed = discord.Embed(
            title = 'Attire',
            description = f"**Today's Attire**:\n{CONF.attire[today]}\n\n**Tomorrow's Attire**:\n{CONF.attire[tmr]}",
            colour = discord.Colour(0xE66E6B)
        )
        await message.channel.send(embed=embed)
        
@client.event
async def on_raw_reaction_add(payload):
    emoji = payload.emoji.name
    member = payload.member
    channel_ = await member.guild.fetch_channel(payload.channel_id)
    message = await channel_.fetch_message(payload.message_id)
    if len(message.embeds) > 0:
        cache = message.embeds[0]
        if "Managed by 22S209 Utility" in cache.footer.text and len(cache.fields) == 1:
            opt_in = cache.fields[0].value.split("\n")
            if emoji == "✅" and str(member) not in opt_in:
                opt_in.append(str(member))
                if len(opt_in) > 1 and 'None' in opt_in:
                    opt_in.remove('None')
                
                cache.remove_field(0)
                cache.add_field(name="Opt In", value="\n".join(opt_in))
                await message.edit(embed=cache)

            elif emoji == "❌" and str(member) in opt_in:
                opt_in.remove(str(member))
                if len(opt_in) ==0 :
                    opt_in = ['None']

                cache.remove_field(0)
                cache.add_field(name="Opt In", value="\n".join(opt_in))
                await message.edit(embed=cache)

def timestamps(key=None):
    stamps = {
        '10 Minutes': datetime.now()+timedelta(minutes=10),
        '30 Minutes' : datetime.now()+timedelta(minutes=30),
        '1 Hour' : datetime.now()+timedelta(hours=1),
        '3 Hours' : datetime.now()+timedelta(hours=3),
        '6 Hours' : datetime.now()+timedelta(hours=6),
        '24 Hours' : datetime.now()+timedelta(days=1),
        'Tomorrow Morning (8:00)': (datetime.now()+timedelta(days=1)).replace(hour=8),
    }
    if key is None:
        return stamps
    return int(stamps[key].timestamp()+28800)

@client.slash_command(
    guild_ids=[946223026238783599],
    name='purchase',
    description='Create Purchase Menu',
)
async def purchase(
    ctx: discord.ApplicationContext,
    item_name: discord.commands.Option(str, 'Name of Item', required=True),
    item_desc: discord.commands.Option(str, 'Description of Item', required=True),
    item_cost: discord.commands.Option(float, 'Cost of Item', required=True),
    expiry: discord.commands.Option(str, 'Expiry of this Menu', choices=timestamps().keys(), required=True)
):
    item_cost = "{:.2f}".format(item_cost)
    embed = discord.Embed(
        title = f'Purchase of {item_name}',
        description = f"**Item Description**: {item_desc}\n**Item Cost**: **${item_cost}**\n**Expiry**: <t:{timestamps(expiry)}>\n\nDo React Below so that the representative can help you purchase this material on your behalf. Collection and Payment will be settled later.",
        colour = discord.Colour(0xE66E6B)
    ).set_footer(text = f'Managed by 22S209 Utility | Created by {ctx.author}')
    embed.add_field(name="Opt In", value='None')
    message = await ctx.send(embed=embed)
    await ctx.respond('Completed Without Errors\n*Only you can see this*',ephemeral=True)
    await message.add_reaction('✅')
    await message.add_reaction('❌')

client.run(os.environ['token'])
