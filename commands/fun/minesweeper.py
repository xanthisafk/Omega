import discord
from discord.ext import commands
import random

class InvalidDifficultyError(Exception):
    def __init__(self):
        super().__init__("Invalid difficulty.\nDifficulty should be between **EASY**, **MEDIUM**, or **HARD**.")

class Minesweeper(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    async def generate_board(self,n,k):
        """
        Creates a minesweeper grid. Copied directly off https://medium.com/swlh/this-is-how-to-create-a-simple-minesweeper-game-in-python-af02077a8de

        args:
            n: int -> Number of rows
            k: int -> Number of trees
        """

        arr = [[0 for row in range(n)] for column in range(n)]
        
        for num in range(k):
            x = random.randint(0,n-1)
            y = random.randint(0,n-1)
            arr[y][x] = 'X'

            if (x >=0 and x <= 3) and (y >= 0 and y <= 4):
                if arr[y][x+1] != 'X':
                    arr[y][x+1] += 1 # center right

            if (x >=1 and x <= 4) and (y >= 0 and y <= 4):
                if arr[y][x-1] != 'X':
                    arr[y][x-1] += 1 # center left

            if (x >= 1 and x <= n-1) and (y >= 1 and y <= n-1):
                if arr[y-1][x-1] != 'X':
                    arr[y-1][x-1] += 1 # top left
    
            if (x >= 0 and x <= n-2) and (y >= 1 and y <= n-1):
                if arr[y-1][x+1] != 'X':
                    arr[y-1][x+1] += 1 # top right

            if (x >= 0 and x <= n-1) and (y >= 1 and y <= n-1):
                if arr[y-1][x] != 'X':
                    arr[y-1][x] += 1 # top center
    
            if (x >=0 and x <= n-2) and (y >= 0 and y <= n-2):
                if arr[y+1][x+1] != 'X':
                    arr[y+1][x+1] += 1 # bottom right

            if (x >= 1 and x <= n-1) and (y >= 0 and y <= n-2):
                if arr[y+1][x-1] != 'X':
                    arr[y+1][x-1] += 1 # bottom left

            if (x >= 0 and x <= n-1) and (y >= 0 and y <= n-2):
                if arr[y+1][x] != 'X':
                    arr[y+1][x] += 1 # bottom center
            
            for row in arr:
                m = "\t".join(str(cell) for cell in row)

        print("after arr:\n", m)

        emotes = {
            0: '0️⃣',
            1: '1️⃣',
            2: '2️⃣',
            3: '3️⃣',
            4: '4️⃣',
            5: '5️⃣',
            6: '6️⃣',
            7: '7️⃣',
            8: '8️⃣',
            9: '9️⃣',
            'X': '💥'

        }

        for i in range(10):
            m = m.replace(str(i), f'||{emotes[i]}||')

        print("after replace:\n", m)

        m = m.replace("X", f'||{emotes["X"]}||')
        m = m.replace(" ", "")
        print(m)

        print("after final\n", m)

        return m

    @commands.command(name = "Minesweeper")
    async def play(self, ctx, difficulty: str = 'easy'):
        """
        Minesweeper game.
        """

        if difficulty == 'easy':
            n = 9
            k = 10
        elif difficulty == 'medium':
            n = 16
            k = 40
        elif difficulty == 'hard':
            n = 30
            k = 99
        else:
            raise InvalidDifficultyError()
        m = await self.generate_board(n,k)
        #print(m)
        embed = discord.Embed(title = "Minesweeper", description = m, color = 0x00ff00)
        await ctx.send(embed = embed)

    @play.error
    async def play_error(self, ctx, error):
        if isinstance(error, InvalidDifficultyError):
            await ctx.send(error)
        else:
            await ctx.send(error)
            raise error


def setup(bot):
    bot.add_cog(Minesweeper(bot))