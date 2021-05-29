import discord
import json
from discord.ext import commands

def getIdFromNick(guildId, nick):
    """
    Gets the mapped ID from the inputted nickname

    If no nickname is stored, returns -1
    """

    with open('././mappings.json', 'r') as f:
        mappings = json.load(f)

    if str(guildId) in list(mappings.keys()):
        for user_id in mappings[guildId].keys():
            if mappings[guildId][user_id] == nick:
                return int(user_id)

    return -1

def getNickFromId(guildId, id):
    """
    Gets the mapped nickname from the inputted user id

    If no id is stored, returns \'-1\'
    """

    with open('././mappings.json', 'r') as f:
        mappings = json.load(f)
    
    if str(guildId) in list(mappings.keys()) and str(id) in list(mappings[guildId].keys()):
        return mappings[guildId][id]
            
    return '-1'

class Mapping(commands.Cog):
    """Mappings stuff for user IDs to nicknames

    Used for tracking stuff
    """
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['maps'])
    async def mappings(self, ctx):
        """List mappings of user IDs to nicknames
        
        Usage: `mappings`
        """
        with open('././mappings.json', 'r') as f:
            media = json.load(f)

        if str(ctx.guild.id) in media:
            keys = list(media[str(ctx.guild.id)].keys())
            message = ""

            for key in keys:
                message += f'<@!{key}>: {media[str(ctx.guild.id)][key].capitalize()}\n'

            embed = discord.Embed(
                title = ':gear: Mappings (Nerd Stuff) :gear:',
                description = message,
                color = discord.Color.green(),
            )
            await ctx.send(embed = embed)

    @commands.command(aliases=['addmap'])
    @commands.has_permissions(manage_channels=True)
    async def addmapping(self, ctx, arg1 : str, arg2 : str):
        """Add mapping of user IDs to nicknames
        
        Usage: `addmapping [user @] [nickname]`
        """
        if arg1.startswith('<@!'):
            id = arg1[3:-1]
            nick = arg2.lower()
        elif arg2.startswith('<@!'):
            id = arg2[3:-1]
            nick = arg1.lower()
        else:
            await ctx.send(':no_entry: One of the arguments must be a user `@`!')
            return

        guild_id = str(ctx.guild.id)
        
        with open('././mappings.json', 'r') as f:
            mapping_json = json.load(f)

        if id in mapping_json[guild_id].keys():
            await ctx.send(f'<@!{id}> is already mapped!')

        elif nick in mapping_json[guild_id].values():
            await ctx.send(f'{nick} is already mapped!')

        else:
            mapping_json[guild_id][id] = nick

            with open ('././mappings.json', 'w') as f:
                json.dump(mapping_json, f, indent=4)

            await ctx.message.purge(limit=1)
            await ctx.send(f'{nick} has been mapped!')

    @commands.command(aliases=['removemap', 'deletemapping', 'deletemap'])
    @commands.has_permissions(manage_channels=True)
    async def removemapping(self, ctx, arg1 : str):
        """Remove mapping of user IDs to nicknames
        
        Usage: `removemapping [user @/nickname]`
        """

        with open('././mappings.json', 'r') as f:
            mapping_json = json.load(f)
        
        guild_id = str(ctx.guild.id)

        if arg1.startswith('<@!'):
            id = arg1[3:-1]

            if id in mapping_json[guild_id].keys():
                mapping_json[guild_id].pop(id)
                #await ctx.message.purge(limit=1)
                await ctx.send(f'Removed ID `{id}` from mappings!')

            else:
                await ctx.send(f':no_entry: ID `{id}` not found in mappings!')
                return

        else:
            nick = arg1.lower()

            if nick in mapping_json[guild_id].values():
                for storedID in mapping_json[guild_id].keys():

                    if str(mapping_json[guild_id][storedID]) == nick:
                        mapping_json[guild_id].pop(storedID)
                        break

                await ctx.send(f'Removed {nick} from mappings!')

            else:
                await ctx.send(f':no_entry: {nick.capitalize()} not found in mappings!')
                return

        with open ('././mappings.json', 'w') as f:
                json.dump(mapping_json, f, indent=4)

def setup(client):
    client.add_cog(Mapping(client))