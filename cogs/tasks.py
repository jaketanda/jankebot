import discord
from discord.ext import commands, tasks
from itertools import cycle
import json
import random
import datetime

with open('././config.json', "r") as configFile:
    config = json.load(configFile)
    status = cycle(config.get("statuses"))

class Tasks(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.change_status.start()

    def cog_unload(self):
        self.change_status.cancel()

    @tasks.loop(seconds=1800)
    async def change_status(self):
        print('Changing status...')
        await self.client.change_presence(activity=discord.Game(next(status)))


def setup(client):
    client.add_cog(Tasks(client))