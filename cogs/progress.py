# Inspired by @year_progress on Twitter

import discord
import math
from discord.ext import commands
from datetime import datetime, date
from pytz import timezone
import random

timezoneString = 'US/Eastern'
tz = timezone(timezoneString)

def getPercentBar(percentage, length=32, whiteChar='▓', grayChar='░'):
    percentageStrings = []
    for i in range(length):
        percentageStrings.append(whiteChar * i + grayChar * (length - i))
    
    return percentageStrings[math.floor(percentage/100 * len(percentageStrings))]

def getDaysInThisMonth(currentMonth, year):
    daysInMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if year % 4 == 0:
        daysInMonth[1] = 29

    return daysInMonth[currentMonth-1]

def getDayProgress():
    now = datetime.now(tz)
    seconds_since_midnight = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
    seconds_in_a_day = 86400
    
    dayPercent = math.floor(seconds_since_midnight/seconds_in_a_day * 100)
    return f'{getPercentBar(dayPercent)} {dayPercent}%'

def getMonthProgress():
    day_of_month = datetime.today().day
    currentMonth = datetime.today().month
    year = date.today().year
    days_in_this_month = getDaysInThisMonth(currentMonth, year)

    monthPercent = math.floor(day_of_month/days_in_this_month * 100)
    return f'{getPercentBar(monthPercent)} {monthPercent}%'

def getYearProgress():
    year = date.today().year
    day_of_year = datetime.now().timetuple().tm_yday
    days_in_this_year = 366 if year % 4 == 0 else 365

    yearPercent = math.floor(day_of_year/days_in_this_year * 100)
    return f'{getPercentBar(yearPercent)} {yearPercent}%'

def getLifeProgress(user_id):
    day_of_year = datetime.now().timetuple().tm_yday
    seed = day_of_year + user_id
    random.seed(seed)

    lifePercent = random.randint(20, 99)
    return f'{getPercentBar(lifePercent)} {lifePercent}%'

class Progress(commands.Cog):
    """Check the progress of the year, month, and day"""
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['dayprog', 'progday', 'progressday'])
    async def dayprogress(self, ctx):
        """Get the progress of the current day in percentage form
        
        Usage: dayprogress"""
        await ctx.reply(f'Day ({timezoneString}) progress: {getDayProgress()}')

    @commands.command(aliases=['monthprog', 'progmonth', 'progressmonth'])
    async def monthprogress(self, ctx):
        """Get the progress of the current month in percentage form
        
        Usage: monthprogress"""
        await ctx.reply(f'Month progress: {getMonthProgress()}')

    @commands.command(aliases=['yearprog', 'progyear', 'progressyear'])
    async def yearprogress(self, ctx):
        """Get the progress of the current year in percentage form
        
        Usage: yearprogress"""
        await ctx.reply(f'Year progress: {getYearProgress()}')

    @commands.command(aliases=['prog'])
    async def progress(self, ctx):
        """Get the progress of the current year, day, and month in percentage form
        
        Usage: progress"""
        await ctx.reply(f'{getDayProgress()} - Day ({timezoneString})\n{getMonthProgress()} - Month\n{getYearProgress()} - Year')

    @commands.command(aliases=['lifeprog', 'progresslife', 'proglife'])
    async def lifeprogress(self, ctx):
        """Get the progress of your life - 100% accurate
        
        Usage: lifeprogress"""
        await ctx.reply(f'Your life progress: {getLifeProgress(ctx.author.id)}')


def setup(client):
    client.add_cog(Progress(client))