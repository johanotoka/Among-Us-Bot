import discord
from discord.ext import commands
import random

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
imposter_members_list = []
crewmate_members_list = []

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
        imposter_role = ctx.guild.get_role(IMPOSTER_ID)
        crewmate_role = ctx.guild.get_role(CREW_MATE_ID)

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

        #remove all imposter roles from the imposter member list.
        for imposter in imposter_members_list:
            await imposter.remove_roles(imposter_role)
        
        #remove all crewmate roles from the crewmate member list.
        for crewmate in crewmate_members_list:
            await crewmate.remove_roles(crewmate_role)

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

        # Assigned roles to each player
        imposter_role = ctx.guild.get_role(IMPOSTER_ID)
        crewmate_role = ctx.guild.get_role(CREW_MATE_ID)
        all_members_list = []
        total_players: int = 0
        num_crewmates: int = 0

        #populating list of all members.
        for member in meet_ch.members:
            all_members_list.append(member)
            total_players = total_players + 1

        #if the number of imposters specified is greater than total number of players then the bot will complain.
        if(number_of_imposters > total_players):
            await ctx.send(f'There are {total_players} total number of players and {number_of_imposters} number of imposters. Am I a joke to you ?')

        elif(number_of_imposters <= total_players):
            #the "all_members_list" now contains a sequence of non-repeating pseudorandom members.
            random.shuffle(all_members_list)

            #assigning the imposter roles. "all_members_list" is reduced by the number of imposters. 
            for i in range(number_of_imposters):
                popped_member = all_members_list.pop(0)
                await popped_member.add_roles(imposter_role, atomic=True)
                imposter_members_list.append(popped_member)
                print(f'{popped_member} member is an imposter.')

            #assigning the crewmate roles. "all_members_list" is reduced by the number of crewmates. 
            # Note that if there are 0 imposters, everyone will be a crewmate. Also, if everyone was an imposter there will be 0 crewmates.
            num_crewmates = total_players - number_of_imposters
            for i in range(num_crewmates):
                popped_member = all_members_list.pop(0)
                await popped_member.add_roles(crewmate_role, atomic=True) 
                crewmate_members_list.append(popped_member)
                print(f'{popped_member} member is a crewmate.')
            
            print(f'------\n')

            #make the bot send the number of imposters to the chat.
            if(number_of_imposters == 1):
                await ctx.send(f'Game has started. There is {number_of_imposters} imposter among us. 😱')
            elif (number_of_imposters > 1):
                await ctx.send(f'Game has started. There are {number_of_imposters} imposters among us. 😱')
            elif(number_of_imposters == 0):
                await ctx.send(f'uhh there are {number_of_imposters} imposters among us... We are all safe... I guess.')

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
