import discord
from discord.ext import commands

CREW_CHANNEL = 'crewmate'
CREW_MATE_ID = 994696028085297212
IMPOSTER_ID = 994696128954110054
IMPOSTER_CHANNEL = 'imposter'
MEETING_CHANNEL = 'meeting'
LOBBY_CHANNEL = 'lobby (join to play)'

COMMON_TASK_VALUE = 5
SHORT_TASK_VALUE = 3
LONG_TASK_VALUE = 10

players = []
started = False

number_of_imposters: int
number_of_common_tasks: int
number_of_short_tasks: int
number_of_long_tasks: int
max_progress_value: int


class Game(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role('MOD')
    async def game_init(self, ctx):
        started = True
        crewmate_channel = await ctx.guild.create_text_channel(CREW_CHANNEL)

        imposter_role = discord.utils.get(ctx.guild.roles, id=IMPOSTER_ID)

        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            imposter_role: discord.PermissionOverwrite(read_messages=True),
        }

        imposter_channel = await ctx.guild.create_text_channel(IMPOSTER_CHANNEL, overwrites=overwrites)

        voice_channel = await ctx.guild.create_voice_channel(LOBBY_CHANNEL, user_limit=20)

    @commands.command()
    async def game_cleanup(self, ctx):
        # TODO: Move these into a generalized helper method
        cc = discord.utils.get(ctx.guild.channels, name=CREW_CHANNEL)
        await cc.delete()
        ic = discord.utils.get(ctx.guild.channels, name=IMPOSTER_CHANNEL)
        await ic.delete()
        mc = discord.utils.get(ctx.guild.channels, name=MEETING_CHANNEL)
        if mc:
            for member in mc.members:
                await member.edit(mute=False)
            await mc.delete()
        lc = discord.utils.get(ctx.guild.channels, name=LOBBY_CHANNEL)
        if lc:
            await lc.delete()

        started = False
        # players = []

    @commands.command()
    async def game_start(self, ctx):
        # Rename the lobby to meeting, and mute all players
        meet_ch = discord.utils.get(ctx.guild.channels, name=LOBBY_CHANNEL)
        await meet_ch.edit(name=MEETING_CHANNEL)
        for member in meet_ch.members:
            await member.edit(mute=True)
            players.append(member.id)

        # TODO: Assign roles to each player

    @commands.command()
    @commands.has_role('MOD')
    async def game_setting(self, ctx, num_of_imp=4, num_of_com_tasks=2, num_of_s_tasks=5, num_of_l_tasks=3):
        globals()['number_of_imposters'] = num_of_imp
        globals()['number_of_common_tasks'] = num_of_com_tasks
        globals()['number_of_short_tasks'] = num_of_s_tasks
        globals()['number_of_long_tasks'] = num_of_l_tasks

    @commands.command()
    async def lmin(self, ctx):
        if (ctx.channel.name == CREW_CHANNEL):
            players.append("hOLA")

    @commands.command()
    async def print(self, ctx):
        print(players)
        print(number_of_imposters)
        print(number_of_common_tasks)
        print(number_of_short_tasks)
        print(number_of_long_tasks)


def setup(bot):
    bot.add_cog(Game(bot))
    print('Init loaded')
