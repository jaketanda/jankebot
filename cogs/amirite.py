import discord
from discord.ext import commands

class Amirite(commands.Cog):
    """Hell yeah, brother"""
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def amirite(self, ctx):
        """hell yeah, brother"""
        await ctx.reply('hell yeah, brother')

def setup(client):
    client.add_cog(Amirite(client))