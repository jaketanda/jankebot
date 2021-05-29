import discord
from discord.ext import commands

class Zoop(commands.Cog):
    """Finger guns"""
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['z00p'])
    async def zoop(self, ctx):
        """z00p"""
        await ctx.send(':point_right: :sunglasses: :point_right:')
        
    @commands.command(aliases=['p00z'])
    async def pooz(self, ctx):
        """p00z"""
        await ctx.send(':point_left: :sunglasses: :point_left:')

def setup(client):
    client.add_cog(Zoop(client))