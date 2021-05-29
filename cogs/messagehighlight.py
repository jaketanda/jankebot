import discord
from discord.ext import commands, tasks
import json
import random
import datetime
import time
from .media import is_it_jake

async def getom(channel, daysAgo):
    async with channel.typing():
        while True:
            try:
                messages = list(await channel.history(limit=10, around=datetime.datetime.now() - datetime.timedelta(days=daysAgo)).flatten())
            except:
                await channel.send(':no_entry: Too old! Try a smaller amount of days!')
                return

            message = random.choice(messages)
               
            if message.content and len(message.content) < 1900:
                break
    await channel.send(f'**{message.author.display_name}** (*{message.created_at.strftime("%A, %B %d, %Y")}*) - {message.content}')

class MessageHighlight(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['gom'])
    async def getoldmessage(self, ctx, days_ago=0):
        if days_ago < 0:
            await ctx.send(':no_entry: Days must be greater than 0')
            return
        
        await getom(ctx.channel, days_ago)

def setup(client):
    client.add_cog(MessageHighlight(client))