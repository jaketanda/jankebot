import discord
from discord.ext import commands

class Echo(commands.Cog):
    """ECHO ECHo ECho Echo echo"""
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Echo loaded...')

    @commands.command()
    async def echo(self, ctx, *, message : str):
        """ECHO ECHo ECho Echo echo
        Echoes your message for a little anonymity 
        
        Usage: `echo [message]`
        """
        print(f'<@!{ctx.message.author.id}> - echo {message}')
        await ctx.channel.purge(limit=1)
        await ctx.send(message)

def setup(client):
    client.add_cog(Echo(client))