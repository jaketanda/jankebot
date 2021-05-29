import discord
from discord.ext import commands
import time

class Clear(commands.Cog):
    """Clean-up of messages kind of stuff"""
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount : int):
        """Deletes messages.
        
        Usage: `clear [# of messages to clear (max 100)]`
        """
        if amount > 100:
            amount = 100
        await ctx.channel.purge(limit=amount+1)
        
        clear_message = await ctx.send(f':white_check_mark: Cleared {amount} messages')
        time.sleep(4)

        try:
            await clear_message.delete()
        except:
            return
        
    
    @clear.error
    async def clear_error(self, ctx, error):
        await ctx.send('Command format: `clear [# of messages to clear]`')

def setup(client):
    client.add_cog(Clear(client))