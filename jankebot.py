import discord
import os
from discord.ext import commands, tasks
import json

def get_prefix(client, message):
    with open('prefixes.json', 'r') as prefixFile:
        prefixes = json.load(prefixFile)

    if message.guild:
        return prefixes[str(message.guild.id)]
    else:
        return '!'

with open('config.json', "r") as configFile:
    config = json.load(configFile)
    TOKEN = config.get("token")
    JAKEID = config.get("jakeId")

def is_it_jake(ctx):
    return str(ctx.author.id) == JAKEID

client = commands.Bot(command_prefix = get_prefix)

# Reload config
@client.command()
@commands.check(is_it_jake)
async def reloadconfig(ctx):
    with open('config.json', "r") as configFile:
        config = json.load(configFile)
        PREFIX = config.get("prefix")
    client.command_prefix = PREFIX
    await ctx.send(':gear: Updated config')

# Reload extension
@client.command()
@commands.check(is_it_jake)
async def reload(ctx, extension):
    extension = extension.lower()
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    print(f'Reloaded {extension}')
    await ctx.send(f':gear: Reloaded {extension}')

# Load extension
@client.command()
@commands.check(is_it_jake)
async def load(ctx, extension):
    extension = extension.lower()
    client.load_extension(f'cogs.{extension}')
    print(f'Loaded {extension}')
    await ctx.send(f':gear: Loaded {extension}')

# Unload extension
@client.command()
@commands.check(is_it_jake)
async def unload(ctx, extension):
    extension = extension.lower()
    client.unload_extension(f'cogs.{extension}')
    print(f'Unloaded {extension}')
    await ctx.send(f':gear: Unloaded {extension}')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.ExtensionNotLoaded):
        print(':no_entry: Extension not loaded')
    elif isinstance(error, commands.ExtensionAlreadyLoaded):
        print(':no_entry: Extension already loaded')

@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '!'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    with open('media.json', 'r') as f:
        media = json.load(f)

    if str(guild.id) not in media:
        media[str(guild.id)] = {}
        with open ('media.json', 'w') as f:
            json.dump(media, f, indent=4)

    with open('mappings.json', 'r') as f:
        mappings = json.load(f)

    mappings[str(guild.id)] = {}

    with open('mappings.json', 'w') as f:
        json.dump(mappings, f, indent=4)

    with open('counters.json', 'r') as f:
        counters = json.load(f)

    counters[str(guild.id)] = {}

    with open('counters.json', 'w') as f:
        json.dump(counters, f, indent=4)

@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
        
    with open('media.json', 'r') as f:
        media = json.load(f)

    media.pop(str(guild.id))
    
    with open ('media.json', 'w') as f:
        json.dump(media, f, indent=4)

    with open('mappings.json', 'r') as f:
        mappings = json.load(f)

    mappings.pop(str(guild.id))

    with open('mappings.json', 'w') as f:
        json.dump(mappings, f, indent=4)

    with open('counters.json', 'r') as f:
        counters = json.load(f)

    counters.pop(str(guild.id))

    with open('counters.json', 'w') as f:
        json.dump(counters, f, indent=4)

@client.command()
@commands.is_owner()
async def changeprefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix 

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    await ctx.send(f':gear: Changed prefix to `{prefix}`')

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(TOKEN)
