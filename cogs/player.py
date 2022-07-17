import discord
from discord.ext import commands

class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

  
    

def setup(bot):
    bot.add_cog(Player(bot))
    print('player loaded')
    