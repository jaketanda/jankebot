import discord
from discord.ext import commands
from .mapping import getIdFromNick
from .media import confirmation

def getColorSelection(x):
    if x == 1:
        return 'red'
    elif x == 2:
        return 'yellow'
    else:
        return 'black'

def getColorGrid(x):
    if x == 1:
        return 'red'
    elif x == 2:
        return 'yellow'
    elif x == 0:
        return 'white'
    else:
        return 'blue'

def moveSelection(selection, playerNum, spotsToMove):
    for index, item in enumerate(selection):
        if item != 0:
            selection[index] = 0
            newPos = index + spotsToMove
            if newPos < 0:
                newPos = 0
            elif newPos > 6:
                newPos = 6
            selection[newPos] = playerNum
            break
    return selection

def isPlacementPossible(selection, grid):
    for pos, item in enumerate(selection):
        if item != 0:
            break

    height = 5
    while True:
        if height < 0:
            break
        if grid[height][pos] == 0:
            return True
        height -= 1
    return False

def updateGrid(selection, grid):
    symbol = 0
    for pos, item in enumerate(selection):
        if item != 0:
            symbol = item
            break

    height = 5
    while True:
        if height < 0:
            break
        if grid[height][pos] == 0:
            grid[height][pos] = symbol
            break
        height -= 1
    return grid

def changeSelectionColor(selection):
    for index, item in enumerate(selection):
        if item == 1:
            selection[index] = 0
            selection[3] = 2
            break
        elif item == 2:
            selection[index] = 0
            selection[3] = 1
            break
    return selection

def checkForWinner(selection, grid):
    foundWinner = False
    symbol = 0
    for pos, item in enumerate(selection):
        if item != 0:
            symbol = item
            break

    height = 5
    for x in range(5):
        if grid[x][pos] == symbol and (x == 0 or grid[x-1][pos] == 0):
            height = x
            break
        
    #check horizontal
    inarow = 0
    for x in range(7):
        if grid[height][x] == symbol:
            inarow += 1
            if inarow >= 4:
                grid[height][x] = 3
                grid[height][x-1] = 3
                grid[height][x-2] = 3
                grid[height][x-3] = 3
                foundWinner = True
        else:
            inarow = 0

    #check vertical
    inarow = 0
    for x in range(6):
        if grid[x][pos] == symbol or grid[x][pos] == 3:
            inarow += 1
            if inarow >= 4:
                grid[x][pos] = 3
                grid[x-1][pos] = 3
                grid[x-2][pos] = 3
                grid[x-3][pos] = 3
                foundWinner = True
        else:
            inarow = 0  

    #check diagonal negative slope
    inarow = 0
    for x in range(-5, 6):
        if height+x >= 0 and height+x <= 5 and pos+x >= 0 and pos+x <= 6 and (grid[height+x][pos+x] == symbol or grid[height+x][pos+x] == 3):
            inarow += 1
            if inarow >= 4:
                grid[height+x][pos+x] = 3
                grid[height+x-1][pos+x-1] = 3
                grid[height+x-2][pos+x-2] = 3
                grid[height+x-3][pos+x-3] = 3
                foundWinner = True
        else:
            inarow = 0  

    #check diagonal positive slope
    inarow = 0
    for x in range(-5, 6):
        if height-x >= 0 and height-x <= 5 and pos+x >= 0 and pos+x <= 6 and (grid[height-x][pos+x] == symbol or grid[height-x][pos+x] == 3):
            inarow += 1
            if inarow >= 4:
                grid[height-x][pos+x] = 3
                grid[height-x+1][pos+x-1] = 3
                grid[height-x+2][pos+x-2] = 3
                grid[height-x+3][pos+x-3] = 3
                foundWinner = True
        else:
            inarow = 0
        
    if foundWinner:
        return symbol

    #check if grid is full (tie scenario)
    gridNotFull = False
    for x in grid:
        for y in x:
            if y == 0:
                gridNotFull = True
                break
        if gridNotFull:
            break
    
    if not gridNotFull:
        return 0
    return 100

def createMessageEmbed(currentPlayer, playerOneDisplayName, playerTwoDisplayName, color, embedColor, firstLine, selection, grid):
    desc = f'{firstLine}\n\n'
    
    if len(selection) > 0:
        for item in selection:
            desc += f':{getColorSelection(item)}_circle:'
        desc+='\n'

    for row in grid:
        for item in row:
            desc += f':{getColorGrid(item)}_circle:'
        desc += '\n'

    embed = discord.Embed(
        title=f'Connect-4 : {playerOneDisplayName} vs. {playerTwoDisplayName}',
        description=desc,
        color = embedColor
    )

    return embed

async def createMessage(currentPlayer, playerOneDisplayName, playerTwoDisplayName, color, embedColor, firstLine, selection, grid, channel):
    return await channel.send(embed=createMessageEmbed(currentPlayer, playerOneDisplayName, playerTwoDisplayName, color, embedColor, firstLine, selection, grid))

async def updateMessage(currentPlayer, playerOneDisplayName, playerTwoDisplayName, color, embedColor, firstLine, selection, grid, message):
    await message.edit(embed=createMessageEmbed(currentPlayer, playerOneDisplayName, playerTwoDisplayName, color, embedColor, firstLine, selection, grid))

async def playConnectFour(self, playerOne, playerTwo, channel):
    # initialize variables

    if not await confirmation(self, f'<@!{playerTwo.id}>! Do you want to play Connect-Four with {playerOne.display_name}?', playerTwo, channel, cancelledMessage=':x: Connect-Four game cancelled!', successMessage='Starting Connect-Four match'):
        return

    turn = 1
    grid = [[0 for x in range(7)] for y in range(6)] 

    selection = [0, 0, 0, 1, 0, 0, 0]

    playerNumber = 1
    color = 'red'
    currentPlayer = playerOne
    embedColor = discord.Color.red()

    firstLine = f'<@!{str(currentPlayer.id)}>\'s turn :{color}_circle:'
    new_message = await createMessage(currentPlayer, playerOne.display_name, playerTwo.display_name, color, embedColor, firstLine, selection, grid, channel)

    reaction = None

    await new_message.add_reaction('◀')
    await new_message.add_reaction('▶')
    await new_message.add_reaction('✅')

    while True:
        def check(reaction, user):
            if turn == 1:
                return user == playerOne
            else:
                return user == playerTwo

        if str(reaction) == '◀':
            selection = moveSelection(selection, playerNumber, -1)
        elif str(reaction) == '▶':
            selection = moveSelection(selection, playerNumber, 1)
        elif str(reaction) == '✅':
            if isPlacementPossible(selection, grid):
                grid = updateGrid(selection, grid)
                winner = checkForWinner(selection, grid)

                if winner == 100: # no winner
                    selection = changeSelectionColor(selection)
                    turn = turn * -1
                    
                    if turn == 1:
                        playerNumber = 1
                        color = 'red'
                        currentPlayer = playerOne
                        embedColor = discord.Color.red()
                    else:
                        playerNumber = 2
                        color = 'yellow'
                        currentPlayer = playerTwo
                        embedColor = discord.Color.gold()
                else: # Someone won
                    break
        
        firstLine = f'<@!{str(currentPlayer.id)}>\'s turn :{color}_circle:'
        await updateMessage(currentPlayer, playerOne.display_name, playerTwo.display_name, color, embedColor, firstLine, selection, grid, new_message)
            
        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout = 60.0, check = check)
            await new_message.remove_reaction(reaction, user)
        except:
            if playerNumber == 1:
                winner = -2
            else:
                winner = -1
            break
        
    await new_message.clear_reactions()
    if winner == 1:
        firstLine = f'**<@!{str(playerOne.id)}> wins!** :red_circle:'
    elif winner == 2:
        firstLine = f'**<@!{str(playerTwo.id)}> wins!** :yellow_circle:'
    elif winner == -1:
        firstLine = f':alarm_clock: Time\'s up! **<@!{str(playerOne.id)}> wins!** :red_circle:'
    elif winner == -2:
        firstLine = f':alarm_clock: Time\'s up! **<@!{str(playerTwo.id)}> wins!** :yellow_circle:'
    elif winner == 0:
        firstLine = f'**No one** wins! We have a tie!'
    else:
        firstLine = f'Error determining winner but the game is over!'

    await updateMessage(currentPlayer, playerOne.display_name, playerTwo.display_name, color, discord.Color.blue(), firstLine, [], grid, new_message)

class ConnectFour(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Connect-Four loaded...')

    @commands.command(aliases = ['connect4', 'c4', 'cfour'])
    async def connectfour(self, ctx, player_two:str):
        """connectfour

        Usage: `connectfour [user @ to challenge]`
        """
        if player_two.startswith('<@!') and player_two.endswith('>'):
            player_two_id = int(player_two[3:-1])
        else:
            player_two_id = getIdFromNick(str(ctx.guild.id), player_two.lower())

        playerOne = ctx.author
        try:
            playerTwo = await ctx.guild.fetch_member(player_two_id)

            await playConnectFour(self, playerOne, playerTwo, ctx.channel)
        except:
            await ctx.send(':no_entry: Player not found!')

def setup(client):
    client.add_cog(ConnectFour(client))