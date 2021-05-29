import discord
from discord.ext import commands

class PingPong(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        """pong

        Usage: `ping`
        """
        await ctx.send(f'Pong! :ping_pong: - `{round(self.client.latency * 1000)}ms`')

    @commands.command()
    async def pong(self, ctx):
        """ping

        Usage: `pong`
        """
        await ctx.send(f':ping_pong: Ping! - `{round(self.client.latency * 1000)}ms`')

def setup(client):
    client.add_cog(PingPong(client))