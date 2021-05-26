import discord
import json
from discord.ext import commands

def dadIsEnabled(guild_id):
    with open('././dad.json', 'r', encoding='utf8') as f:
        dadStatuses = json.load(f)
    
    if guild_id in dadStatuses:
        return dadStatuses[guild_id]
    else:
        return False

def toggleDadStatus(guild_id):
    with open('././dad.json', 'r', encoding='utf8') as f:
        dadStatuses = json.load(f)

    if guild_id in dadStatuses:
        dadStatuses[guild_id] = not dadStatuses[guild_id]
    else:
        dadStatuses[guild_id] = True

    with open ('././dad.json', 'w') as f:
        json.dump(dadStatuses, f, indent=4)

class Dad(commands.Cog):
    """I am your father"""
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Dad loaded...')

    @commands.command(aliases=['dad'])
    @commands.has_permissions(manage_channels=True)
    async def dadbot(self, ctx, status='toggle'):
        """Toggles Dad-Bot mode
        
        Usage: `dadbot [on/off/toggle(optional)]`"""

        updatedStatus = status.lower()
        guild_id = str(ctx.guild.id)

        if updatedStatus == 'on':
            newStatus = "enabled"
            if not dadIsEnabled(guild_id):
                toggleDadStatus(guild_id)

        elif updatedStatus == 'off':
            newStatus = "disabled"
            if not dadIsEnabled(guild_id):
                toggleDadStatus(guild_id)

        elif updatedStatus == 'toggle':
            if dadIsEnabled(guild_id):
                newStatus = "disabled"
            else:
                newStatus = "enabled"

            toggleDadStatus(guild_id)

        else:
            ctx.send(':no_entry: Invalid syntax! Proper syntax: `dadbot [on/off/toggle(optional)]`')
            return

        await ctx.send(f':man: Dad-mode {newStatus}!')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild:
            dadStrings = ['i am ', 'i\'m ', 'i’m ', ' im ']
            userMessage = message.content
            guild_id = str(message.guild.id)
            found = False

            if dadIsEnabled(guild_id) and not message.author.bot:
                for dadString in dadStrings:
                    if dadString in userMessage.lower():
                        index = userMessage.lower().find(dadString) + len(dadString)
                        if index < len(userMessage):
                            botMessage = userMessage[index:]
                            found = True
                            break

                if userMessage.lower().startswith('im '):
                    botMessage = userMessage[3:]
                    found = True

                if found:
                    await message.channel.send(f'Hello, {botMessage}, I\'m Janke!')


def setup(client):
    client.add_cog(Dad(client))