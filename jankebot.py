import discord
import os
from discord.ext import commands, tasks
import logging
import json

formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

def setup_logger(name, log_file, level=logging.INFO):

    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.addHandler(streamHandler)

    return logger

logger = setup_logger('command', './logs/janke.log')
setup_logger('voice', './logs/voice.log')

def get_prefix(client, message):
    with open('prefixes.json', 'r') as prefixFile:
        prefixes = json.load(prefixFile)

    try:
        return prefixes[str(message.guild.id)]
    except:
        return '!'

with open('config.json', "r") as configFile:
    config = json.load(configFile)
    TOKEN = config.get("token")
    JAKEID = config.get("jakeId")

def is_it_jake(ctx):
    return str(ctx.author.id) == JAKEID

client = commands.Bot(command_prefix=get_prefix, intents=discord.Intents().all())

def isACounter(command, guild_id):
    with open('counters.json', 'r') as cFile:
        counterJson = json.load(cFile)

    if command.endswith('l') or command.endswith('leaders') or command.endswith('leaderboard'):
        if (command.endswith('l')):
            command = command[:-1]
        elif command.endswith('leaders'):
            command = command[:-7]
        elif command.endswith('leaderboard'):
            command = command[:-11]
    elif command.endswith('c') or command.endswith('chart') or command.endswith('g') or command.endswith('graph'):
        if (command.endswith('c') or command.endswith('g')):
            command = command[:-1]
        else:
            command = command[:-5]

    if guild_id in list(counterJson.keys()) and command in list(counterJson[guild_id].keys()):
        return True

    return False

def isAMediaFolder(command, guild_id):
    with open('media.json', 'r') as mFile:
        mediaJson = json.load(mFile)

    if mediaJson[guild_id] and command in list(mediaJson[guild_id].keys()):
        return True

    return False    

def message_contains_command(message):
    guild_id = str(message.guild.id)
    prefix = get_prefix(client, message)

    if message.content.lower().startswith(prefix):
        full_command = message.content.lower()[len(prefix):]
        command = full_command.split()[0].lower()

        if isACounter(command, guild_id) or isAMediaFolder(command, guild_id):
            return True

    return False

# Log all normal commands
@client.listen(name='on_command')
async def log_commands(ctx):
    guild = ctx.guild.name
    user = ctx.author.name
    user_discriminator = ctx.author.discriminator
    command = ctx.message.content
    logger.info(f'{guild} - {user}#{user_discriminator} - {command}')

# Log modular commands
@client.listen(name='on_message')
async def log_modular_commands(message):
    if message_contains_command(message):
        guild = message.guild.name
        user = message.author.name
        user_discriminator = message.author.discriminator
        command = message.content
        logger.info(f'{guild} - {user}#{user_discriminator} - {command}')

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
    logger.info(f'Reloaded {extension}')
    await ctx.send(f':gear: Reloaded {extension}')

# Load extension
@client.command()
@commands.check(is_it_jake)
async def load(ctx, extension):
    extension = extension.lower()
    client.load_extension(f'cogs.{extension}')
    logger.info(f'Loaded {extension}')
    await ctx.send(f':gear: Loaded {extension}')

# Unload extension
@client.command()
@commands.check(is_it_jake)
async def unload(ctx, extension):
    extension = extension.lower()
    client.unload_extension(f'cogs.{extension}')
    logger.info(f'Unloaded {extension}')
    await ctx.send(f':gear: Unloaded {extension}')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.ExtensionNotLoaded):
        logger.error(':no_entry: Extension not loaded')
    elif isinstance(error, commands.ExtensionAlreadyLoaded):
        logger.error(':no_entry: Extension already loaded')

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
    logger.info(f'{client.user} has connected to Discord')

logger.info('Loading cogs =-=-=-=-=-=-=-=-=-=-=-=-=-=')
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        logger.info(f'{filename[:-3].capitalize()} loaded...')

logger.info('Finished loading cogs =-=-=-=-=-=-=-=-=-')

client.run(TOKEN)
