import discord
from discord.ext import commands

class Zoop(commands.Cog):
    """Finger guns"""
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Zoop loaded...')

    @commands.command(aliases=['z00p'])
    async def zoop(self, ctx):
        """z00p"""
        print('zoop')
        await ctx.send(':point_right: :sunglasses: :point_right:')
        
    @commands.command(aliases=['p00z'])
    async def pooz(self, ctx):
        """p00z"""
        print('pooz')
        await ctx.send(':point_left: :sunglasses: :point_left:')

def setup(client):
    client.add_cog(Zoop(client))