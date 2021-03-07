import discord
from discord.ext import commands
import json
import random

async def confirmation(self, message, sentUser, channel, successMessage = ':white_check_mark: Operation successful', cancelledMessage = ':x: Operation cancelled'):
    new_message = await channel.send(message)

    await new_message.add_reaction('✅')
    await new_message.add_reaction('❌')

    def check(reaction, user):
        return user == sentUser

    reaction = None

    while True:
        if str(reaction) == '✅':
            await new_message.clear_reactions()
            await new_message.edit(content=successMessage)
            return True
        elif str(reaction) == '❌':
            await new_message.clear_reactions()
            await new_message.edit(content=cancelledMessage)
            return False

        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout = 30.0, check = check)
            await new_message.remove_reaction(reaction, user)
        except:
            await new_message.clear_reactions()
            await new_message.edit(content=cancelledMessage)
            return False

async def areYouSure(self, message, sentUser, channel, successMessage = ':white_check_mark: Operation successful', cancelledMessage = ':x: Operation cancelled'):
    are_you_sure_message = f'Are you sure you would like to {message}?'
    return await confirmation(self, are_you_sure_message, sentUser, channel, successMessage=successMessage, cancelledMessage=cancelledMessage)
    

async def list_media(self, message, folder_name):
    pages = []
    guild_id = str(message.guild.id)
    with open('././media.json', 'r', encoding='utf8') as f:
        media = json.load(f)
    
    counter = 1
    page = 1
    description = ""

    for item in media[guild_id][folder_name]:
        description += f'{counter}: {item.get("description")}\n'

        if counter % 20 == 0:
            
            embed = discord.Embed(
                title = f'{folder_name.capitalize()} - Page {page}',
                description = description,
                color = discord.Color.red()
            )

            pages.append(embed)
            description = ""
            page += 1

        counter += 1

    if description != "" or page == 1:
        embed = discord.Embed(
            title = f'{folder_name.capitalize()} - Page {page}',
            description = description,
            color = discord.Color.red()
        )
        pages.append(embed)

    new_message = await message.channel.send(embed = pages[0])
    if len(pages) > 1:
        await new_message.add_reaction('⏮')
        await new_message.add_reaction('◀')
        await new_message.add_reaction('▶')
        await new_message.add_reaction('⏭')

        def check(reaction, user):
            return user == message.author

        i = 0
        reaction = None

        while True:
            if str(reaction) == '⏮':
                if i != 0:
                    i = 0
                    await new_message.edit(embed = pages[i])
            elif str(reaction) == '◀':
                if i > 0:
                    i -= 1
                    await new_message.edit(embed = pages[i])
            elif str(reaction) == '▶':
                if i < len(pages)-1:
                    i += 1
                    await new_message.edit(embed = pages[i])
            elif str(reaction) == '⏭':
                if i != len(pages)-1:
                    i = len(pages)-1
                    await new_message.edit(embed = pages[i])
            
            try:
                reaction, user = await self.client.wait_for('reaction_add', timeout = 30.0, check = check)
                await new_message.remove_reaction(reaction, user)
            except:
                break

        await new_message.clear_reactions()

async def displayMedia(self, folder_name, media_number, guild_id, message):
    media_list = get_media(guild_id, folder_name)

    def getMessageToSend(current_num):
        return f'{folder_name.capitalize()} media [{current_num+1} of {len(media_list)}]: {media_list[current_num].get("content")} {media_list[current_num].get("description")}'
    
    new_message = await message.channel.send(getMessageToSend(media_number))

    if len(media_list) > 1:
        await new_message.add_reaction('⏮')
        await new_message.add_reaction('◀')
        await new_message.add_reaction('▶')
        await new_message.add_reaction('⏭')

        def check(reaction, user):
            return user == message.author

        i = media_number
        reaction = None

        while True:
            if str(reaction) == '⏮':
                if i != 0:
                    i = 0
                    await new_message.edit(content=getMessageToSend(i))
            elif str(reaction) == '◀':
                if i > 0:
                    i -= 1
                    await new_message.edit(content=getMessageToSend(i))
            elif str(reaction) == '▶':
                if i < len(media_list)-1:
                    i += 1
                    await new_message.edit(content=getMessageToSend(i))
            elif str(reaction) == '⏭':
                if i != len(media_list)-1:
                    i = len(media_list)-1
                    await new_message.edit(content=getMessageToSend(i))
            
            try:
                reaction, user = await self.client.wait_for('reaction_add', timeout = 30.0, check = check)
                await new_message.remove_reaction(reaction, user)
            except:
                break

        await new_message.clear_reactions()

def get_media_folders(guildId):
    with open('././media.json', 'r') as f:
        media = json.load(f)
    if str(guildId) in media and len(media[str(guildId)]) > 0:
        return list(media[str(guildId)].keys())
    return []

def get_media(guild_id, folder):
    with open('././media.json', 'r') as f:
        media = json.load(f)
    if str(guild_id) in media and folder in media[str(guild_id)]:
        return list(media[str(guild_id)][folder])
    return []

def add_media(guild_id, folder_name, media):
    with open('././media.json', 'r') as f:
        media_json = json.load(f)

    media_json[str(guild_id)][folder_name].append({"content": media, "description": ""})

    with open ('././media.json', 'w') as f:
        json.dump(media_json, f, indent=4)

def add_media_with_description(guild_id, folder_name, media):
    with open('././media.json', 'r') as f:
        media_json = json.load(f)

    description = ""
    counter = 0
    for arg in media:
        if counter >= 3:
            description += f'{str(arg)} '
        counter += 1

    media_json[str(guild_id)][folder_name].append({"content": media[2], "description": description})

    with open ('././media.json', 'w') as f:
        json.dump(media_json, f, indent=4)

def remove_media(guild_id, folder_name, media_number):
    with open('././media.json', 'r') as f:
        media = json.load(f)

    media[str(guild_id)][folder_name].pop(media_number-1)

    with open ('././media.json', 'w') as f:
        json.dump(media, f, indent=4)

def updatedescription(args, discord_id):
    with open('././media.json', 'r') as f:
        media_json = json.load(f)

    description = ""
    counter = 0
    for arg in args:
        if counter > 2:
            description += f'{arg} '
        counter+=1

    media_json[discord_id][args[0]][int(args[2])-1]["description"] = description

    with open ('././media.json', 'w') as f:
        json.dump(media_json, f, indent=4)

def addfolder(ctx, folder_name : str):
    with open('././media.json', 'r') as f:
        media = json.load(f)

    if str(ctx.guild.id) not in media:
        media[str(ctx.guild.id)] = {}

    if folder_name in media[str(ctx.guild.id)]:
        return -1

    else:
        media[str(ctx.guild.id)][str(folder_name)] = []

        with open ('././media.json', 'w') as f:
            json.dump(media, f, indent=4)

        return 0

def is_it_jake(ctx):
    with open('././config.json', "r") as configFile:
        config = json.load(configFile)
        JAKEID = config.get("jakeId")
    return str(ctx.author.id) == JAKEID

class Media(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Media loaded...')
    
    @commands.command()
    async def media(self, ctx):
        """Lists the media folders associated with a guild

        Usage: `media`
        """

        folders = get_media_folders(ctx.guild.id)
        folders.sort()
        folder_string = ""
        for folder in folders:
            folder_string += f'{folder}, '
        folder_string = folder_string[:-2]
        embed = discord.Embed(
            title = ':file_folder: Media Folders :file_folder:',
            description = folder_string,
            color = discord.Color.blue(),
        )
        await ctx.channel.send(embed = embed)

    @commands.command()
    @commands.has_permissions(attach_files=True)
    async def addfolder(self, ctx, folder_name):
        """Adding of a media folder associated with a guild

        Usage: `addfolder [Folder name]`
        """

        print('here')
        check = addfolder(ctx, folder_name.lower())
        if check == -1:
            await ctx.send(f'Folder {folder_name.lower().capitalize()} already exists!')
        else:
            await ctx.send(f':file_folder: Created {folder_name.lower().capitalize()}!')
        
    
    @commands.command(aliases=['deletefolder'])
    @commands.has_permissions(manage_channels=True)
    async def removefolder(self, ctx, folder_name):
        """Removal of a media folder associated with a guild

        Usage: `removefolder [Folder name]`
        """
        if await areYouSure(self, f'delete folder `{folder_name}`', ctx.author, ctx.channel, successMessage=f':file_folder: Removed `{folder_name}`!'):
            if str(folder_name) in get_media_folders(str(ctx.guild.id)):
                with open('././media.json', 'r') as f:
                    media = json.load(f)

                media[str(ctx.guild.id)].pop(str(folder_name), None)

                with open ('././media.json', 'w') as f:
                    json.dump(media, f, indent=4)

    @commands.command(aliases=['[folderhelp]'])
    async def mediahelp(self, ctx):
        """Displays commands for media manipulation
        
        Usage:
        `[Folder name]` - displays a random piece of media from the selected folder.
        `[Folder name] [Positive integer]` - displays a specific piece of media as determined by the number.
        `[Folder name] add [Media URL] [Description (Optional)]` - Add a piece of media to a specified folder
        `[Folder name] remove [Positive integer]` - Remove a piece of media from a specified folder
        `[Folder name] list` - List the media as well as the descriptions for a folder
        `[Folder name] updatedescription [Positive integer] [description]` - Update the description for a piece of media
        """

        description="Usage:\n"
        description+="`[Folder name]` - displays a random piece of media from the selected folder.\n\n"
        description+="`[Folder name] [Positive integer]` - displays a specific piece of media as determined by the number\n\n"
        description+="`[Folder name] add [Media URL] [Description (Optional)]` - Add a piece of media to a specified folder\n\n"
        description+="`[Folder name] remove [Positive integer]` - Remove a piece of media from a specified folder\n\n"
        description+="`[Folder name] list` - List the media as well as the descriptions for a folder\n\n"
        description+="`[Folder name] updatedescription [Positive integer] [description]` - Update the description for a piece of media"

        embed = discord.Embed(
            title='Commands for manipulation of a Discord guild\'s media',
            description=description,
            color = discord.Color.gold()
        )

        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(is_it_jake)
    async def transfer(self, ctx, folder_name):
        """Used for transferring images from Jankebot 2.2 to Jankebot 3.0
        
        Usage: `transfer [Folder name]`
        """

        print(f'transfer {folder_name}')
        guild_id = str(ctx.guild.id)
        with open("././jankeMedia.json", "r", encoding="utf8") as f:
            old_media = json.load(f)

        with open('././media.json', 'r') as j:
            new_media = json.load(j)
        
        if folder_name.lower() in old_media.keys():
            if folder_name not in new_media[guild_id].keys():
                await ctx.send(f'Creating {folder_name}')
                addfolder(ctx, folder_name)

            for media_item in old_media[folder_name]:
                add_media(guild_id, folder_name, media_item)
            await ctx.send(f'Successfully transferred {folder_name}!')
        else:
            await ctx.send(f':no_entry: Old folder {folder_name} not found!')

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild:
            return

        with open('././prefixes.json', 'r') as f:
            prefixes = json.load(f)

        ctx = await self.client.get_context(message)
        if not ctx.valid:
            if str(message.guild.id) in prefixes:    
                prefix = str(prefixes.get(str(message.guild.id)))
            else:
                prefix = '!'

            if message.content.lower().startswith(prefix):
                args = message.content[len(prefix):].split()
                folderName = args[0].lower()
                
                if folderName in (get_media_folders(message.guild.id)):
                    print(message.content[len(prefix):])
                    folderSize = len(get_media(message.guild.id, folderName))

                    if len(args) > 1:
                        if args[1] == "add":
                            if len(args) == 3:
                                add_media(message.guild.id, folderName, args[2])
                                await message.channel.purge(limit=1)
                                await message.channel.send(f'Added media to {folderName}!')
                            elif len(args) > 3:
                                add_media_with_description(message.guild.id, folderName, args)
                                await message.channel.purge(limit=1)
                                await message.channel.send(f'Added media to {folderName}!')
                            else:
                                await message.channel.send(f':no_entry: Proper format: `{prefix}{folderName} add [content]`')
                            return

                        elif args[1] == "remove" or args[1] == "delete":
                            if message.channel.permissions_for(message.author).manage_messages:
                                if len(args) == 3:
                                    if await areYouSure(self, f'delete {folderName} media number {args[2]}', message.author, message.channel, successMessage=f'Removed media `{args[2]}` from `{folderName}`'):
                                        remove_media(message.guild.id, folderName, int(args[2]))
                                else:
                                    await message.channel.send(f':no_entry: Proper format: `{prefix}{folderName} remove [number to remove]`')
                            return

                        elif args[1] == "list":
                            await list_media(self, message, folderName)
                            return

                        elif args[1] == 'updatedescription' or args[1] == 'updatedesc' or args[1] == 'update' and len(args) >= 3:
                            updatedescription(args, str(message.guild.id))
                            await message.channel.send(f'Updated description for `{args[0]} {args[2]}`')
                            return

                        else:
                            medianum = int(args[1])-1

                    elif len(args) == 1 and folderSize != 0:
                        medianum = random.randint(0, folderSize-1)

                    if folderSize == 0:
                        await message.channel.send(f':no_entry: The {folderName.capitalize()} folder is empty!' 
                                                + f' Do `{prefix}{folderName.capitalize()} add [media] [description]` to get started!')
                        return
                    
                    try:
                        await displayMedia(self, args[0].lower(), medianum, message.guild.id, message)
                        
                    except:
                        await message.channel.send(f':no_entry: Invalid number. Valid numbers: `1-{len(get_media(message.guild.id, args[0]))}`')

def setup(client):
    client.add_cog(Media(client))