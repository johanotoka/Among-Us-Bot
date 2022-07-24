import discord
from discord.ext import commands

players = [153518379565711361]
started = False

CREW_CHANNEL = 'crewmate'
IMPOSTER_CHANNEL = 'imposter'
MEETING_CHANNEL = 'meeting'
LOBBY_CHANNEL = 'lobby'

class Game(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role('MOD')
    async def game_init(self, ctx):
        started = True
        crewmate_channel = await ctx.guild.create_text_channel(CREW_CHANNEL)

        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True)
        }
        imposter_channel = await ctx.guild.create_text_channel(IMPOSTER_CHANNEL,overwrites=overwrites)

        voice_channel = await ctx.guild.create_voice_channel(MEETING_CHANNEL)

        lobby_channel = await ctx.guild.create_voice_channel(LOBBY_CHANNEL)
 
        
    @commands.command()
    async def game_cleanup(self, ctx):
        # TODO: Move these into a generalized helper method
        cc = discord.utils.get(ctx.guild.channels, name = CREW_CHANNEL)
        await cc.delete()
        ic = discord.utils.get(ctx.guild.channels, name = IMPOSTER_CHANNEL)
        await ic.delete()
        mc = discord.utils.get(ctx.guild.channels, name = MEETING_CHANNEL)
        await mc.delete()
        lc = discord.utils.get(ctx.guild.channels, name = LOBBY_CHANNEL)
        await lc.delete()

        started = False
        #players = []

    @commands.command()
    async def game_start(self, ctx):
        meet_ch = discord.utils.get(ctx.guild.channels, name = MEETING_CHANNEL)
        for pl in players:
            memb = await ctx.guild.fetch_member(pl)
            await memb.move_to(meet_ch)

    @commands.command()
    async def lmin(self,ctx):
        if(ctx.channel.name == CREW_CHANNEL):
            players.append("hOLA")
    
    @commands.command()
    async def print(self,ctx):
        print(players)

def setup(bot):
    bot.add_cog(Game(bot))
    print('Init loaded')
    