import discord
import json
import time
import os
import matplotlib.pyplot as plt
from discord.ext import commands

current_milli_time = lambda: int(round(time.time() * 1000))

def getTotalTimeMilli(guild_id, user_id):
    with open('././voicetime.json', 'r') as f:
        vtjson = json.load(f)

    if guild_id in vtjson and user_id in vtjson[guild_id]:
        if vtjson[guild_id][user_id]['timeJoinedVoice'] == -1:
            return vtjson[guild_id][user_id]['totalVoiceTime']
        else:
            return (current_milli_time() - vtjson[guild_id][user_id]['timeJoinedVoice']) + vtjson[guild_id][user_id]['totalVoiceTime']

    return 0

def getFormattedTime(millis):
    seconds=(millis/1000)%60
    seconds = int(seconds)
    minutes=(millis/(1000*60))%60
    minutes = int(minutes)
    hours=(millis/(1000*60*60))

    formatted_time = "%02d:%02d:%02d" % (hours, minutes, seconds)
    return formatted_time

def updateUserJoinsVoice(guild_id, user_id):
    with open('././voicetime.json', 'r') as f:
        vtjson = json.load(f)

    if guild_id not in vtjson:
        vtjson[guild_id] = {}

    if user_id not in vtjson[guild_id]:
        vtjson[guild_id][user_id] = {}
        vtjson[guild_id][user_id]['totalVoiceTime'] = 0
    
    vtjson[guild_id][user_id]['timeJoinedVoice'] = current_milli_time()

    with open ('././voicetime.json', 'w') as f:
        json.dump(vtjson, f, indent=4)
    
def updateUserLeavesVoice(guild_id, user_id):
    with open('././voicetime.json', 'r') as f:
        vtjson = json.load(f)

    if guild_id not in vtjson:
        vtjson[guild_id] = {}

    if user_id not in vtjson[guild_id]:
        vtjson[guild_id][user_id] = {}
        vtjson[guild_id][user_id]['timeJoinedVoice'] = current_milli_time()
        vtjson[guild_id][user_id]['totalVoiceTime'] = 0
    
    vtjson[guild_id][user_id]['totalVoiceTime'] =  current_milli_time() - vtjson[guild_id][user_id]['timeJoinedVoice'] + vtjson[guild_id][user_id]['totalVoiceTime']
    vtjson[guild_id][user_id]['timeJoinedVoice'] = -1

    with open ('././voicetime.json', 'w') as f:
        json.dump(vtjson, f, indent=4)

def timeIsVisible(guild_id):
    with open('././voicetime.json', 'r') as f:
        vtjson = json.load(f)

    if guild_id in vtjson and 'visible' in vtjson[guild_id]:
        return vtjson[guild_id]['visible']
        
    return False

def timeIsCensored(guild_id):
    with open('././voicetime.json', 'r') as f:
        vtjson = json.load(f)

    if guild_id in vtjson and 'censored' in vtjson[guild_id]:
        return vtjson[guild_id]['censored']

    return True

def toggleVoiceTimeVisibility(guild_id):
    with open('././voicetime.json', 'r') as f:
        vtjson = json.load(f)

    if not guild_id in vtjson:
        vtjson[guild_id] = {}

    if not 'visible' in vtjson[guild_id]:
        vtjson[guild_id]['visible'] = False

    vtjson[guild_id]['visible'] = not vtjson[guild_id]['visible']

    with open ('././voicetime.json', 'w') as f:
        json.dump(vtjson, f, indent=4)

def toggleVoiceTimeCensorship(guild_id):
    with open('././voicetime.json', 'r') as f:
        vtjson = json.load(f)

    if not guild_id in vtjson:
        vtjson[guild_id] = {}

    if not 'censored' in vtjson[guild_id]:
        vtjson[guild_id]['censored'] = True

    vtjson[guild_id]['censored'] = not vtjson[guild_id]['censored']

    with open ('././voicetime.json', 'w') as f:
        json.dump(vtjson, f, indent=4)

def displayVoiceTimeLeaders(guild_id, is_censored, number_to_display):
    with open('././voicetime.json', 'r') as f:
        vtjson = json.load(f)

    title = ':alarm_clock: Time in Voice Chat Leaderboard :alarm_clock:'

    if guild_id in vtjson:
        vtjson[guild_id].pop('censored', None)
        vtjson[guild_id].pop('visible', None)

    if guild_id not in vtjson or len(vtjson[guild_id].keys()) == 0:
        description = 'No users to display!'
        embed = discord.Embed(
            title=title,
            color=discord.Color.orange(),
            description=description
        )
    else:
        user_dict = {}
        description = ""
        for key in vtjson[guild_id].keys():
            user_dict[key] = getTotalTimeMilli(guild_id, key)
        
        user_dict = sorted(user_dict.items(), key=lambda item: item[1], reverse=True)
        
        counter = 1
        for key, value in user_dict:
            if counter >= number_to_display + 1:
                break

            description += f'{counter}. <@!{key}>'

            if not is_censored:
                description += f': {getFormattedTime(value)}'

            description += '\n'

            counter += 1

        embed = discord.Embed(
            title=title,
            color=discord.Color.orange(),
            description=description
        )
            
    return embed

async def getChart(guild, num_to_display):
    with open('././voicetime.json', 'r') as f:
        vtjson = json.load(f)

    guild_id = str(guild.id)
    title = f'Voice time for {guild.name}'

    if guild_id in vtjson:
        vtjson[guild_id].pop('censored', None)
        vtjson[guild_id].pop('visible', None)
    else:
        return None

    user_dict = {}
    for key in vtjson[guild_id].keys():
        user_dict[key] = getTotalTimeMilli(guild_id, key)
    
    # format: [('109060566210859008', 6193)]
    user_dict = sorted(user_dict.items(), key=lambda item: item[1], reverse=True)

    if len(user_dict) > num_to_display:
        left = list(range(1, num_to_display+1))
        user_dict = user_dict[:num_to_display]
    else:
        left = list(range(1, len(user_dict)+1))

    users = []
    user_times = []
    for user_id, user_time in user_dict:
        try:
            user = await guild.fetch_member(int(user_id))
            users.append(user.name)
        except :
            print('user not found')
            users.append(f'id:{user_id}')

        user_times.append(float(user_time)/1000/60/60)

    plt.xlabel('Users')
    plt.xticks(left, users, rotation="vertical")
    plt.ylabel('Total Time (Hours)')

    plt.subplots_adjust(bottom=0.3)

    plt.title(title)

    plt.bar(left, user_times, tick_label=users, color = ['green', 'blue', 'red', 'purple'])

    plt.savefig(f'{guild_id}.png')
    plt.close()

class VoiceTime(commands.Cog):
    """Commands for viewing the amount of time spent in voice chat"""
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('VoiceTime loaded...')

    @commands.command(aliases=['vt'])
    async def voicetime(self, ctx):
        """Check how much time you've spent in voice chat
        
        Usage: `voicetime`"""

        guild_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)

        millis = getTotalTimeMilli(guild_id, user_id)

        formatted_time = getFormattedTime(millis)

        embed = discord.Embed(
            title = f'Your time in {ctx.guild.name} voice!',
            description = f'Time in voice: **{formatted_time}**',
            color = discord.Color.dark_blue()
        )

        embed.set_thumbnail(url=ctx.guild.icon_url)
        
        await ctx.author.send(embed = embed)
        await ctx.message.add_reaction('✉️')

    @commands.command(aliases=['vtl', 'voicetimeleaders'])
    @commands.has_permissions(attach_files=True)
    async def voicetimeleaderboard(self, ctx, total=10):
        """Displays the leaders for time spent in voice chat
        
        Usage: `voicetimeleaderboard`
        """

        guild_id = str(ctx.guild.id)

        if timeIsVisible(guild_id):
            print(f'voicetime leaders {total}')
            if timeIsCensored(guild_id):
                await ctx.send(embed=displayVoiceTimeLeaders(guild_id, True, total))
            else:
                await ctx.send(embed=displayVoiceTimeLeaders(guild_id, False, total))

        elif ctx.channel.permissions_for(ctx.author).administrator:
            await ctx.author.send(embed=displayVoiceTimeLeaders(guild_id, False, total))

    @commands.command(aliases=['vtg', 'vtc', 'voicetimegraph'])
    @commands.has_permissions(attach_files=True)
    async def voicetimechart(self, ctx, total=10):
        """Displays the leaders for time spent in voice chat in barchart form
        
        Usage: `voicetimechart`
        """

        guild_id = str(ctx.guild.id)

        if timeIsVisible(guild_id) and not timeIsCensored(guild_id):
            await getChart(ctx.guild, total)
            await ctx.reply(file = discord.File(f'{guild_id}.png', f'{guild_id}.png'))
            os.remove(f'{guild_id}.png')

        elif ctx.channel.permissions_for(ctx.author).administrator:
            await getChart(ctx.guild, total)
            await ctx.author.send(file = discord.File(f'{guild_id}.png', f'{guild_id}.png'))
            os.remove(f'{guild_id}.png')


    @commands.command(aliases=['vtvisible', 'vtvis', 'makevtvisible', 'vtv'])
    @commands.has_permissions(administrator=True)
    async def makevoicetimevisible(self, ctx):
        """Enables the voicetimeleaderboard command
        
        Usage: `makevoicetimevisible`
        """

        guild_id = str(ctx.guild.id)
        
        if not timeIsVisible(guild_id):
            print('voicetime visible')
            toggleVoiceTimeVisibility(guild_id)
        
        await ctx.send(f':white_check_mark: Voice time leaderboards are now visible! - Type `voicetimeleaderboard` to check the leaderboard!')

    @commands.command(aliases=['vtinvisible', 'vtinvis', 'makevtinvisible', 'vti'])
    @commands.has_permissions(administrator=True)
    async def makevoicetimeinvisible(self, ctx):
        """Disables the voicetimeleaderboard command for all but admins
        
        Usage: `makevoicetimeinvisible`
        """

        guild_id = str(ctx.guild.id)

        if timeIsVisible(guild_id):
            print('voicetime invisible')
            toggleVoiceTimeVisibility(guild_id)
        
        await ctx.send(f':white_check_mark: Voice time leaderboards are now invisible! - Type `makevoicetimevisible` to make these visible again!')

    @commands.command(aliases=['censorvt', 'cvt'])
    @commands.has_permissions(manage_channels=True)
    async def censorvoicetime(self, ctx):
        """Censors the total time spent in discord
        
        Usage: `cesnsorvoicetime`
        """
        guild_id = str(ctx.guild.id)

        if not timeIsCensored(guild_id):
            print('voicetime censored')
            toggleVoiceTimeCensorship(guild_id)

        await ctx.send(f':white_check_mark: Voice time leaderboard times are now censored!')

    @commands.command(aliases=['uncensorvt', 'uvt'])
    @commands.has_permissions(manage_channels=True)
    async def uncensorvoicetime(self, ctx):
        """Uncensors the total time spent in discord
        
        Usage: `uncensorvoicetime`
        """
        guild_id = str(ctx.guild.id)

        if timeIsCensored(guild_id):
            print('voicetime uncensored')
            toggleVoiceTimeCensorship(guild_id)

        await ctx.send(f':white_check_mark: Voice time leaderboard times are now uncensored!')
        
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        user_id = str(member.id)
        guild_id = str(member.guild.id)

        if not before.channel and after.channel: #joined
            print(f'{member.name} joined {after.channel.name}')
            updateUserJoinsVoice(guild_id, user_id)

        elif before.channel and not after.channel: #left
            print(f'{member.name} left {before.channel.name}')
            updateUserLeavesVoice(guild_id, user_id)

def setup(client):
    client.add_cog(VoiceTime(client))