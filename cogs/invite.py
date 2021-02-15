import discord
from discord.ext import commands

class Invite(commands.Cog):
    """Get an invite link to the discord"""
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Invite loaded...')

    @commands.command(aliases=['getinv', 'invite', 'inv'])
    @commands.has_permissions(attach_files=True)
    async def getinvite(self, ctx, guildId = '0'):
        """Get invite for the specified guild
        
        Usage: `getinvite [guild ID : leave blank for current guild]`
        """
        if guildId == '0':
            guildId = str(ctx.guild.id)

        try:
            guild = self.client.get_guild(int(guildId))
            inviteLink = await guild.text_channels[0].create_invite()
            await ctx.send(inviteLink)
        except:
            await ctx.send(':no_entry: Either invalid guild ID or insufficient bot permissions')

def setup(client):
    client.add_cog(Invite(client))