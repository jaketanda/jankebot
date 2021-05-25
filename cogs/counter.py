import discord
import json
import matplotlib.pyplot as plt
import os
from discord.ext import commands
from discord import File

def getPrefix(guild_id):
    with open('././prefixes.json', 'r') as f:
        prefixes = json.load(f)

    if guild_id in prefixes:
        return str(prefixes.get(guild_id))
    else:
        return '!'

def getMappedUser(guild_id, user):
    with open('././mappings.json', 'r') as f:
        mappings = json.load(f)

    for user_id in mappings[guild_id].keys():
        if mappings[guild_id][user_id] == user:
            return user_id

    return '-1'

def getCounterNames(guild_id):
    with open('././counters.json', 'r') as f:
        counters = json.load(f)
    if guild_id in counters:
        return list(counters[guild_id].keys())
    return []

def addCounter(guild_id, counter_name, title):
    with open('././counters.json', 'r') as f:
        counters = json.load(f)

    if guild_id not in counters:
        counters[guild_id] = {}
    
    new_counter = {}
    new_counter['title'] = title
    new_counter['censored'] = False
    counters[guild_id][counter_name] = new_counter

    with open ('././counters.json', 'w') as f:
        json.dump(counters, f, indent=4)

def removeCounter(guild_id, counter_name):
    with open('././counters.json', 'r') as f:
        counters = json.load(f)

    counters[guild_id].pop(counter_name, None)

    with open ('././counters.json', 'w') as f:
        json.dump(counters, f, indent=4)

def counterExists(guild_id, counter_name):
    return counter_name in getCounterNames(guild_id)

def setEmoji(guild_id, counter_name, emoji_string):
    with open('././counters.json', 'r') as f:
        counters = json.load(f)
    
    counters[guild_id][counter_name]['emoji'] = emoji_string

    with open ('././counters.json', 'w') as f:
        json.dump(counters, f, indent=4)

def getEmoji(guild_id, counter_name):
    with open('././counters.json', 'r') as f:
        counters = json.load(f)
    
    return counters[guild_id][counter_name]['emoji']

def setFooter(guild_id, counter_name, new_footer):
    with open('././counters.json', 'r') as f:
        counters = json.load(f)
    
    counters[guild_id][counter_name]['footer'] = new_footer

    with open ('././counters.json', 'w') as f:
        json.dump(counters, f, indent=4)

def getFooter(guild_id, counter_name):
    with open('././counters.json', 'r') as f:
        counters = json.load(f)
    
    return counters[guild_id][counter_name]['footer']

def isCensored(guild_id, counter_name):
    with open('././counters.json', 'r') as f:
        counters = json.load(f)
    
    return counters[guild_id][counter_name]['censored']

def toggleCensorship(guild_id, counter_name):
    with open('././counters.json', 'r') as f:
        counters = json.load(f)
    
    counters[guild_id][counter_name]['censored'] = not counters[guild_id][counter_name]['censored']

    with open ('././counters.json', 'w') as f:
        json.dump(counters, f, indent=4)

def getTitle(guild_id, counter_name):
    with open('././counters.json', 'r') as f:
        counters = json.load(f)
    
    return counters[guild_id][counter_name]['title']

def setTitle(guild_id, counter_name, new_title):
    with open('././counters.json', 'r') as f:
        counters = json.load(f)
    
    counters[guild_id][counter_name]['title'] = new_title

    with open ('././counters.json', 'w') as f:
        json.dump(counters, f, indent=4)

def setCounterName(guild_id, old_counter_name, new_counter_name):
    with open('././counters.json', 'r') as f:
        counters = json.load(f)

    counters[guild_id][new_counter_name] = counters[guild_id].pop(old_counter_name)

    with open ('././counters.json', 'w') as f:
        json.dump(counters, f, indent=4)

def incrementCount(guild_id, counter_name, user_id, incrementAmount):
    with open('././counters.json', 'r') as f:
        counters = json.load(f)

    if user_id not in counters[guild_id][counter_name].keys():
        counters[guild_id][counter_name][user_id] = 0

    counters[guild_id][counter_name][user_id] += incrementAmount

    with open ('././counters.json', 'w') as f:
        json.dump(counters, f, indent=4)

def decrementCount(guild_id, counter_name, user_id, decrementAmount):
    with open('././counters.json', 'r') as f:
        counters = json.load(f)

    if user_id not in counters[guild_id][counter_name].keys():
        return -1
    
    if counters[guild_id][counter_name][user_id] > 0:
        counters[guild_id][counter_name][user_id] -= decrementAmount
        
        if counters[guild_id][counter_name][user_id] <= 0:
            counters[guild_id][counter_name].pop(user_id, None)
    else:
        return -1

    with open ('././counters.json', 'w') as f:
        json.dump(counters, f, indent=4)

def displayLeaders(guild_id, counter_name, number_to_display):
    with open('././counters.json', 'r') as f:
        counters = json.load(f)

    counter = counters[guild_id][counter_name]
    title = counter['title']
    censored = counter['censored']
    if 'emoji' in counter.keys():
        emoji = counter['emoji']
    else:
        emoji = ':loudspeaker: '
    if 'footer' in counter.keys():
        footer = counter['footer']
    else:
        footer = ''

    counter.pop('title', None)
    counter.pop('emoji', None)
    counter.pop('censored', None)
    counter.pop('footer', None)

    description = ""

    counter = sorted(counter.items(), key=lambda item: item[1], reverse=True)
    i = 1
    for user_id, count in counter:
        description += f'{i}. <@!{user_id}>'
        if not censored:
            description += f': {count}'
        description += '\n'
        i += 1

        if i == number_to_display + 1:
            break

    embed = discord.Embed(
        title = f'{emoji} {title} {emoji}',
        description = description,
        color = discord.Color.green()
    )

    if footer != '':
        embed.set_footer(text=footer)

    return embed

async def getChart(guild, guild_id, counter_name, num_to_display):
    with open('././counters.json', 'r') as f:
        counters = json.load(f)

    counter = counters[guild_id][counter_name]
    title = counter['title']
    censored = counter['censored']

    if censored:
        return None

    counter.pop('title', None)
    counter.pop('emoji', None)
    counter.pop('censored', None)
    counter.pop('footer', None)

    counter = sorted(counter.items(), key=lambda item: item[1], reverse=True)

    if len(counter) > num_to_display:
        left = list(range(1, num_to_display+1))
        counter = counter[:num_to_display]
    else:
        left = list(range(1, len(counter)+1))

    print(counter)

    users = []
    user_scores = []
    for user_id, user_score in counter:
        try:
            user = await guild.fetch_member(int(user_id))
            users.append(user.display_name)
        except :
            print('user not found')

        user_scores.append(user_score)

    print('generating')
    print(left)
    print(user_scores)
    print(users)
    plt.bar(left, user_scores, tick_label=users, color = ['green', 'blue', 'red', 'purple'])

    plt.xlabel('Users')
    plt.ylabel('Totals')

    plt.title(title)

    plt.savefig('chart.png',dpi=400)


def getUserTotalCount(guild_id, counter_name, user_id):
    with open('././counters.json', 'r') as f:
        counters = json.load(f)

    if user_id not in counters[guild_id][counter_name].keys():
        return 0
    
    return counters[guild_id][counter_name][user_id]
    
class Counter(commands.Cog):
    """Counters - for all of your additive needs!"""
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Counter loaded...')

    @commands.command(aliases=['counterl', 'counterlist', 'listcounters'])
    async def counters(self, ctx):
        """Displays the active counters in the guild
        
        Usage: `counters`
        """
        guild_id = str(ctx.guild.id)
        description = ""
        for counter in getCounterNames(guild_id):
            description += f'- {counter}\n'

        embed = discord.Embed(
            title = 'Counters',
            description = description
        )

        await ctx.send(embed = embed)

    @commands.command(aliases=['addcounter'])
    @commands.has_permissions(manage_channels=True)
    async def newcounter(self, ctx, commandname, *, title : str = "Leaderboard"):
        """Creates a counter
        
        Usage: `newcounter [counter command name] [leaderboard title]`
        """
        guild_id = str(ctx.guild.id)
        lower_command_name = commandname.lower()
        
        if not counterExists(guild_id, lower_command_name):
            addCounter(guild_id, lower_command_name, title)
            await ctx.send(f':ballot_box_with_check: Counter {lower_command_name.capitalize()} has been created!')
        else:
            await ctx.send(f':no_entry: Counter {lower_command_name.capitalize()} already exists!')

    @commands.command(aliases=['deletecounter'])
    @commands.has_permissions(manage_channels=True)
    async def removecounter(self, ctx, counter_name):
        """Removes a counter from existence
        
        Usage: `removecounter [counter name]`
        """
        guild_id = str(ctx.guild.id)
        lower_counter_name = counter_name.lower()

        if counterExists(guild_id, lower_counter_name):
            removeCounter(guild_id, lower_counter_name)
            await ctx.send(f':ballot_box_with_check: Counter {lower_counter_name.capitalize()} has been deleted!')
        else:
            await ctx.send(f':no_entry: Counter {lower_counter_name.capitalize()} does not exist!')

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def censor(self, ctx, counter_name):
        """Censors the counter's values - still displays rankings'
        
        Usage: `censor [counter name]`
        """
        guild_id = str(ctx.guild.id)
        lower_counter_name = counter_name.lower()

        if counterExists(guild_id, lower_counter_name):
            if not isCensored(guild_id, lower_counter_name):
                toggleCensorship(guild_id, lower_counter_name)

            await ctx.send(f':ballot_box_with_check: {counter_name.capitalize()} has been censored')
        
        else:
            await ctx.send(f':no_entry: Counter {counter_name.capitalize()} does not exist! Try `{getPrefix(guild_id)}newcounter [counter name] [title]`')

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def uncensor(self, ctx, counter_name):
        """Uncensors the counter (displays totals)
        
        Usage: `uncensor [counter name]`
        """
        guild_id = str(ctx.guild.id)
        lower_counter_name = counter_name.lower()

        if counterExists(guild_id, lower_counter_name):
            if isCensored(guild_id, lower_counter_name):
                toggleCensorship(guild_id, lower_counter_name)

            await ctx.send(f':ballot_box_with_check: {counter_name.capitalize()} has been uncensored')
        
        else:
            await ctx.send(f':no_entry: Counter {counter_name.capitalize()} does not exist! Try `{getPrefix(guild_id)}newcounter [counter name] [title]`')

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def setemoji(self, ctx, counter_name, emoji):
        """Sets the emoji associated with a counter
        
        Usage: `setemoji [counter name] [emoji]`
        """
        guild_id = str(ctx.guild.id)
        lower_counter_name = counter_name.lower()

        if counterExists(guild_id, lower_counter_name):
            setEmoji(guild_id, lower_counter_name, emoji)
            await ctx.send(f':ballot_box_with_check: Emoji for {counter_name.capitalize()} has been set to {emoji}!')
        else:
            await ctx.send(f':no_entry: Counter {counter_name.capitalize()} does not exist! Try `{getPrefix(guild_id)}newcounter [counter name] [title]`')
            
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def settitle(self, ctx, counter_name, *, title):
        """Sets the title for a counter's leaderboard
        
        Usage: `settitle [counter name] [title]`
        """
        guild_id = str(ctx.guild.id)
        lower_counter_name = counter_name.lower()

        if counterExists(guild_id, lower_counter_name):
            setTitle(guild_id, lower_counter_name, title)
            await ctx.send(f':ballot_box_with_check: Title for {counter_name.capitalize()} has been set to `{title}`!')

        else:
            await ctx.send(f':no_entry: Counter {counter_name.capitalize()} does not exist! Try `{getPrefix(guild_id)}newcounter [counter name] [title]`')

    @commands.command(aliases=['setfoot'])
    @commands.has_permissions(manage_channels=True)
    async def setfooter(self, ctx, counter_name, *, footer = ""):
        """Sets the footer for a counter's leaderboard
        
        Usage: `setfooter [counter name] [footer]`
        """
        guild_id = str(ctx.guild.id)
        lower_counter_name = counter_name.lower()

        if counterExists(guild_id, lower_counter_name):
            setFooter(guild_id, lower_counter_name, footer)
            await ctx.send(f':ballot_box_with_check: Title for {counter_name.capitalize()} has been set to `{footer}`!')

        else:
            await ctx.send(f':no_entry: Counter {counter_name.capitalize()} does not exist! Try `{getPrefix(guild_id)}newcounter [counter name] [title]`')

    @commands.command(aliases=['setcn', 'setcommand', 'setcommandname'])
    @commands.has_permissions(manage_channels=True)
    async def setcountername(self, ctx, counter_name, new_counter_name):
        """Sets the name of a counter's associated command
        
        Usage: `setcountername [current counter name] [new counter name]`
        """
        guild_id = str(ctx.guild.id)
        lower_counter_name = counter_name.lower()
        lower_new_counter_name = new_counter_name.lower()

        if counterExists(guild_id, lower_counter_name):
            setCounterName(guild_id, lower_counter_name, lower_new_counter_name)
            await ctx.send(f':ballot_box_with_check: Name of counter {counter_name.capitalize()} has been set to `{new_counter_name}`!')
        else:
            await ctx.send(f':no_entry: Counter {counter_name.capitalize()} does not exist! Try `{getPrefix(guild_id)}newcounter [counter name] [title]`')

    @commands.command()
    async def counterhelp(self, ctx):
        """Help command for the manipulation of counter stuff

        Usage:
        `counterhelp` - displays this stuff, but fancier
        `[Counter name]+ [user @]` - increments the specified counter for a specific user by 1
        `[Counter name]- [user @]` - decrements the specified counter for a specific user by 1
        `[Counter name]leaderboard` - Displays the leaderboard for the specified counter
        `[Counter name]` - Displays your total for the specified counter
        """
        description="Usage:\n"
        description+="`[Counter name]+ [user @]` - increments the specified counter for a specific user by 1\n\n"
        description+="`[Counter name]- [user @]` - decrements the specified counter for a specific user by 1\n\n"
        description+="`[Counter name]leaderboard` - Displays the leaderboard for the specified counter\n\n"
        description+="`[Counter name]` - Displays your total for the specified counter\n\n"

        embed = discord.Embed(
            title='Commands for a Discord guild\'s counters',
            description=description,
            color = discord.Color.gold()
        )

        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild:
            return

        ctx = await self.client.get_context(message)
        if not ctx.valid:

            guild_id = str(message.guild.id)  
            prefix = getPrefix(guild_id)

            if message.content.lower().startswith(prefix):
                line = message.content.lower()[len(prefix):]
                print(line)
                command = line.split()[0]


                counter_names = tuple(getCounterNames(guild_id))
                if command.startswith(counter_names):
                    if len(line.split()) > 1:
                        arg = line.split()[1]

                        if arg.startswith('<@!'):
                            user_id = arg[3:-1]
                        else:
                            user_id = getMappedUser(guild_id, arg)

                        if user_id != '-1':
                            if command.endswith('+'):
                                incrementCount(guild_id, command[:-1], user_id, 1)
                                await message.channel.send(f':ballot_box_with_check: Incremented {command[:-1]} counter for <@!{user_id}>!')
                            elif command.endswith('-') and message.channel.permissions_for(message.author).manage_messages:
                                if decrementCount(guild_id, command[:-1], user_id, 1) == -1:
                                    await message.channel.send(f':no_entry: <@!{user_id}> is already at 0!')
                                else:
                                    await message.channel.send(f':ballot_box_with_check: Decremented {command[:-1]} counter for <@!{user_id}>!')
                        else:
                            await message.channel.send(f':no_entry: User {arg} not found!')

                    elif command.endswith('l') or command.endswith('leaders') or command.endswith('leaderboard'):
                        if (command.endswith('l')):
                            command = command[:-1]
                        elif command.endswith('leaders'):
                            command = command[:-7]
                        elif command.endswith('leaderboard'):
                            command = command[:-11]
                        await message.channel.send(embed = displayLeaders(guild_id, command, 10))

                    elif command.endswith('c') or command.endswith('chart') or command.endswith('g') or command.endswith('graph'):
                        if (command.endswith('c') or command.endswith('g')):
                            command = command[:-1]
                        else:
                            command = command[:-5]
                        await getChart(message.guild, guild_id, command, 10)
                        await message.channel.send(file = discord.File("chart.png", "chart.png"))
                        os.remove("chart.png")
                    
                    elif command.endswith(counter_names):
                        if isCensored(guild_id, command):
                            await message.author.send(f'Your total count for {command.capitalize()}: `{getUserTotalCount(guild_id, command, str(message.author.id))}`')
                            await message.add_reaction('✉️')
                        else:
                            await message.channel.send(f'<@!{message.author.id}> Your total count for {command.capitalize()}: `{getUserTotalCount(guild_id, command, str(message.author.id))}`')

def setup(client):
    client.add_cog(Counter(client))