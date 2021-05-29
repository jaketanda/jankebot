import discord
from discord.ext import commands
import requests
import json

def set_default_ip(guild_id, ip):
    with open('././minecraft.json', 'r') as f:
        ips = json.load(f)

    ips[guild_id] = ip

    with open('././minecraft.json', 'w') as f:
        json.dump(ips, f, indent=4)

def get_default_ip(ctx):
    with open('././minecraft.json', 'r') as f:
        ips = json.load(f)

    if (str(ctx.guild.id)) in ips.keys():
        return str(ips[str(ctx.guild.id)])
    return '-1'

class Minecraft(commands.Cog):
    """Commands for getting information about Minecraft Servers"""
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['minecraft'])
    async def mc(self, ctx, ip : str='-1'):
        """Information retrieval of Minecraft servers

        Usage: `mc [IP Address (optional)]`
        """
        api_ip = ip
        if api_ip == '-1':
            api_ip = get_default_ip(ctx)
        if api_ip != '-1':
            response = requests.get(f'https://api.mcsrvstat.us/2/{api_ip}')
            
            if response.json()["online"] == True:
                players = ""
                if ("list" in response.json()["players"].keys()):
                    for player in list(response.json()["players"]["list"]):
                        players += f'- {str(player)}\n'

                embed = discord.Embed(
                    title = response.json()["motd"]["clean"][0],
                    description = f'Server online? :white_check_mark:\nIP: {response.json()["ip"]}\n\nPlayers [{response.json()["players"]["online"]}/{response.json()["players"]["max"]}]:\n{players}',
                    color = discord.Color.green()
                )
                embed.set_thumbnail(url='https://i.pinimg.com/originals/7a/a3/0c/7aa30c0658b18c60becc10a3563360b9.png')
                
            else:
                embed = discord.Embed(
                    title = "A Minecraft Server",
                    description = f'Server online? :x:\nIP: {api_ip}',
                    color = discord.Color.red()
                )
                embed.set_thumbnail(url='https://i.pinimg.com/originals/47/ce/a6/47cea671e0b4baac64a08bd148c0f5da.png')
                
            await ctx.channel.send(embed=embed)
        else:
            await ctx.send(':no_entry: No default IP set... set one by running `setmcip [IP]`')
    
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def setmcip(self, ctx, ip):
        """Sets the default Minecraft IP address for the guild

        Usage: `setmcip [IP address]`
        """
        set_default_ip(str(ctx.guild.id), str(ip))
        await ctx.send(f'Updated new default ip to {ip}')

def setup(client):
    client.add_cog(Minecraft(client))