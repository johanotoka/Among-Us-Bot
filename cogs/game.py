import discord
from discord.ext import commands

players=[]
started= False
class Game(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role('MOD')
    async def game_init(self, ctx):
        started = True
        crewmate_channel = await ctx.guild.create_text_channel('crewmate')
        
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True)
        }
        
        imposter_channel = await ctx.guild.create_text_channel('imposters', overwrites=overwrites)

        # TODO: Create common crewmate voice channel 
    
    @commands.command()
    async def lmin(self,ctx):
        if(ctx.channel.name=='crewmate'):
            players.append("hOLA")
    
    @commands.command()
    async def print(self,ctx):
        print(players)

def setup(bot):
    bot.add_cog(Game(bot))
    print('Init loaded')
    