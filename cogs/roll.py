import discord
from discord.ext import commands
import random

class Roll(commands.Cog):
    """Rolling of the die"""
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Roll loaded...')

    @commands.command()
    async def roll(self, ctx, amount=6):
        """Rolling of the die

        Usage: `roll [Size of die (optional - defaults to 6)]`
        """
        print(f'roll {amount}')
        if amount > 0:
            await ctx.send(f':game_die: Rolled a {random.randint(1, amount)}')
        else:
            await ctx.send(f':no_entry: Integer must be greater than 0')

    @roll.error
    async def roll_error(self, ctx, error):
        await ctx.send('Command format: `roll [integer > 0]`')

def setup(client):
    client.add_cog(Roll(client))