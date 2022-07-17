import discord
from discord.ext import commands

class Basics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=discord.Game(name='Among Us'))
        print('Logged in as')
        print(self.bot.user.name)
        print(self.bot.user.id)
        print('------')

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms')

def setup(bot):
    bot.add_cog(Basics(bot))
    print('Basics loaded')