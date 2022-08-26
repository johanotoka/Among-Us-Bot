import math

from unicodedata import name
import discord
from discord.ext import commands
import random
import example_code.json_test


CREW_CHANNEL = 'crewmate'
CREW_MATE_ID = 994696028085297212
IMPOSTER_ID = 994696128954110054
DEAD_PLAYER_ID = 998013021634961499
IMPOSTER_CHANNEL = 'imposter'
MEETING_CHANNEL = 'meeting'
DEAD_CHANNEL = 'dead'
DEAD_VOICE_CHANNEL = 'dead (voice)'
LOBBY_CHANNEL = 'lobby (join to play)'
BOT_COMMAND_CHANNEL = 'bot-commands'
BOT_GAME_DATA_CHANNEL_ID = 1012104990669676644

COMMON_TASK_VALUE = 5
SHORT_TASK_VALUE = 3
LONG_TASK_VALUE = 10

players = []
nicknames={}
player_dict={}
task_dict=example_code.json_test.get_task_dict()
imposter_members_list = []
crewmate_members_list = []
dead_imposters_list = []
dead_crewmates_list = []

started = False

number_of_imposters: int
number_of_common_tasks: int
number_of_short_tasks: int
number_of_medium_tasks: int
number_of_long_tasks: int
max_progress_value: int

PROGRESS_BAR_MAX = 10
GREEN_BOX = '🟩'
RED_BOX = '🟥'

max_progress_value = 0
progression = 0
progress_bar = '🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥 0%'


class Game(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role('MOD')
    async def game_init(self, ctx):
        started = True

        #if there was anything in the imposter, crewmate, dead imposters or dead crewmates lists then they must be cleared. This is due to them being global and occurs if the game is initialized more than once.
        imposter_members_list.clear()
        crewmate_members_list.clear()
        dead_imposters_list.clear()
        dead_crewmates_list.clear()

        #create the dead channel.
        crewmate_role = discord.utils.get(ctx.guild.roles, id=CREW_MATE_ID)
        dead_player_role = discord.utils.get(ctx.guild.roles, id=DEAD_PLAYER_ID)
        imposter_role = discord.utils.get(ctx.guild.roles, id=IMPOSTER_ID)
        
        #create imposter channel (only accessible to imposters. Dead players can read the chat).
        imp_overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
            imposter_role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            dead_player_role: discord.PermissionOverwrite(read_messages=True, send_messages=False),
        }
        imposter_channel = await ctx.guild.create_text_channel(IMPOSTER_CHANNEL, overwrites=imp_overwrites)

        #create the crewmate channel (accessible to both imposters and crewmates. Dead players can read the chat).
        crewmate_overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            imposter_role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            dead_player_role: discord.PermissionOverwrite(read_messages=True, send_messages=False),
        }
        crewmate_channel = await ctx.guild.create_text_channel(CREW_CHANNEL, overwrites=crewmate_overwrites)

        #create the dead player channel (only accessible to dead players). 
        dead_overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            dead_player_role: discord.PermissionOverwrite(read_messages=True),
        }
        dead_player_channel = await ctx.guild.create_text_channel(DEAD_CHANNEL, overwrites=dead_overwrites)

        #create the dead voice channel.
        dead_voice_channel = await ctx.guild.create_voice_channel(DEAD_VOICE_CHANNEL, user_limit=21, overwrites=dead_overwrites)

        #create the lobby channel. Dead players cannot join the lobby.
        lobby_overwrites = {
            dead_player_role: discord.PermissionOverwrite(connect=False),
        }
        voice_channel = await ctx.guild.create_voice_channel(LOBBY_CHANNEL, user_limit=21, overwrites=lobby_overwrites)

        await voice_channel.connect()
        

    @commands.command()
    async def game_cleanup(self, ctx):
        # TODO: Move these into a generalized helper method
        imposter_role = ctx.guild.get_role(IMPOSTER_ID)
        crewmate_role = ctx.guild.get_role(CREW_MATE_ID)
        dead_player_role = ctx.guild.get_role(DEAD_PLAYER_ID)

        mc = discord.utils.get(ctx.guild.channels, name=MEETING_CHANNEL)
        if mc:
            for member in mc.members:
                await member.edit(mute=False)
            await mc.delete()

        await self.delete_channel(ctx, CREW_CHANNEL)
        await self.delete_channel(ctx, IMPOSTER_CHANNEL)
        await self.delete_channel(ctx, LOBBY_CHANNEL)
        await self.delete_channel(ctx, DEAD_CHANNEL)
        await self.delete_channel(ctx, DEAD_VOICE_CHANNEL)

        # remove all imposter roles from the imposter member list.
        for imposter in imposter_members_list:
            await imposter.remove_roles(imposter_role)

        # remove all crewmate roles from the crewmate member list.
        for crewmate in crewmate_members_list:
            await crewmate.remove_roles(crewmate_role)

        # remove all dead player roles from the dead crewmate member list.
        for dead_member in dead_crewmates_list:
            await dead_member.remove_roles(dead_player_role)

        # remove all dead player roles from the dead imposter member list.
        for dead_member in dead_imposters_list:
            await dead_member.remove_roles(dead_player_role)

        globals()['started'] = False
        players.clear()
        player_dict={}
        nicknames={}

    async def delete_channel(self, ctx, channel):
        ch = discord.utils.get(ctx.guild.channels, name=channel)
        if ch:
            await ch.delete()

    @commands.command()
    async def game_start(self, ctx):
        # Rename the lobby to meeting, and mute all players
        meet_ch = discord.utils.get(ctx.guild.channels, name=LOBBY_CHANNEL)
        await meet_ch.edit(name=MEETING_CHANNEL)
        
        for member in meet_ch.members:
            if (not member.bot):
                players.append(member.id)
                player_name = f"P{len(players)}"

                # Updating the nickname and muting player
                await member.edit(mute=True,nick=player_name)

                # Making dictionary which is storing player id as key and *nickname as value* 
                nicknames[member.id]=player_name  
            
                tasks_list,task_no=example_code.json_test.get_task()
                #  Creating a new dict with task code to its name
                            
                player_dict[player_name]=[list(tasks_list),[]]

        await self.play_sound(ctx, "audio/among_us_start.mp3")

        # Assigned roles to each player
        imposter_role = ctx.guild.get_role(IMPOSTER_ID)
        crewmate_role = ctx.guild.get_role(CREW_MATE_ID)
        all_members_list = []
        total_players: int = 0
        num_crewmates: int = 0
        bot_data_channel = discord.utils.get(ctx.guild.channels, id=BOT_GAME_DATA_CHANNEL_ID)

        # populating list of all members. The "Among Us Bot" will NOT be included.
        for member in meet_ch.members:
            if(member.name != "Among Us Bot"):
                all_members_list.append(member)
                total_players = total_players + 1

        # if the number of imposters specified is greater than total number of players then the bot will complain.
        if (number_of_imposters > total_players):
            await ctx.send(
                f'There are {total_players} total number of players and {number_of_imposters} number of imposters. Am I a joke to you ?')

        elif (number_of_imposters <= total_players):
            # the "all_members_list" now contains a sequence of non-repeating pseudorandom members.
            random.shuffle(all_members_list)

            # assigning the imposter roles. "all_members_list" is reduced by the number of imposters.
            for i in range(number_of_imposters):
                popped_member = all_members_list.pop(0)
                await popped_member.add_roles(imposter_role, atomic=True)
                imposter_members_list.append(popped_member)
                
                await bot_data_channel.send(f'{popped_member} member is an imposter.')

            # assigning the crewmate roles. "all_members_list" is reduced by the number of crewmates.
            # Note that if there are 0 imposters, everyone will be a crewmate. Also, if everyone was an imposter there will be 0 crewmates.
            num_crewmates = total_players - number_of_imposters
            globals()['max_progress_value'] = num_crewmates*100
            for i in range(num_crewmates):
                popped_member = all_members_list.pop(0)
                await popped_member.add_roles(crewmate_role, atomic=True)
                crewmate_members_list.append(popped_member)
                
                await bot_data_channel.send(f'{popped_member} member is a crewmate.')

            await bot_data_channel.send(f'------------\n')

            # make the bot send the number of imposters to the chat.
            if (number_of_imposters == 1):
                await ctx.send(f'Game has started. There is {number_of_imposters} imposter among us. 😱')
            elif (number_of_imposters > 1):
                await ctx.send(f'Game has started. There are {number_of_imposters} imposters among us. 😱')
            elif (number_of_imposters == 0):
                await ctx.send(f'uhh there are {number_of_imposters} imposters among us... We are all safe... I guess.')

    @commands.command()
    @commands.has_role('MOD')
    #async def game_setting(self, ctx, num_of_imp=4, num_of_com_tasks=2, num_of_s_tasks=4, num_of_m_tasks=1, num_of_l_tasks=1):
    async def game_setting(self, ctx, num_of_imp=4):
        globals()['number_of_imposters'] = num_of_imp
        globals()['number_of_common_tasks'] = 2
        globals()['number_of_short_tasks'] = 4
        globals()['number_of_long_tasks'] = 1
        globals()['number_of_medium_tasks'] = 1


    @commands.command()
    async def lmin(self, ctx):
        if (ctx.channel.name == CREW_CHANNEL):
            players.append("hOLA")

    @commands.command()
    async def print(self, ctx):
        print(players)
        print(player_dict)
        print(task_dict)
        for i in player_dict.keys():
            await ctx.send(f"Player: {i} \nTasks to Be done:\n{player_dict[i][0]}\n Tasks Completed:\n{player_dict[i][1]}")
        # print(number_of_imposters)
        # print(number_of_common_tasks)
        # print(number_of_short_tasks)
        # print(number_of_long_tasks)
        print(imposter_members_list)
        print(crewmate_members_list)
        print(dead_crewmates_list)
        print(dead_imposters_list)
        print("Max Progress: "+str(max_progress_value))
        print("Current Progress: "+str(progression))

    # audio testing commands
    @commands.command()
    async def play_kill(self, ctx):
        await self.play_sound(ctx, "audio/among_us_kill.mp3")

    @commands.command()
    async def play_start(self, ctx):
        await self.play_sound(ctx, "audio/among_us_start.mp3")

    @commands.command()
    async def play_meeting(self, ctx):
        await self.play_sound(ctx, "audio/among_us_meeting.mp3")

    # used to call the sound we want to play
    async def play_sound(self, ctx, sound):
        vc = ctx.guild.voice_client
        if vc:
            vc.stop()
            vc.play(discord.FFmpegPCMAudio(executable="audio/ffmpeg", source=sound))
        else:
            await ctx.send("Not in a voice channel. Initialize a game first!")

    @commands.has_any_role('MOD')
    @commands.command()
    async def td(self,ctx, player, task):
        if ctx.message.channel.name == "report-task-done":
            if(player in player_dict.keys()):
                # print("player is present",player)
                if(task in task_dict.keys()):
                    x=task_dict[task]
                    player_dict[player][0].remove(x)
                    player_dict[player][1].append(x)
                    if (int(task) == 16 or int(task) == 17):
                        globals()['progression'] += 5
                        print('common task done') 
                    elif (1 <= int(task) <= 8):
                        globals()['progression'] += 10
                        print('short task done')
                    elif (9 <= int(task) <=13):
                        globals()['progression'] += 20
                        print('medium task done')
                    else:
                        globals()['progression'] += 30
                        print('long task done')
                    
                    await ctx.send(player +" has completed " + x)
                    self.update_progression()
                    if (progression >= max_progress_value):
                        print("crewmates won by tasks")
                        #await self.crew_win_game(ctx)
                        meet_ch = discord.utils.get(ctx.guild.channels, name=CREW_CHANNEL)
                        await meet_ch.send("Crew Mates have completed all their tasks and won the game!")
                        globals()['started'] = False
        else:
            await ctx.send("Please send the message to right channel period")        

    @commands.command()
    async def mytask(self,ctx):
        meet_ch = discord.utils.get(ctx.guild.channels,name=CREW_CHANNEL)  
        id=ctx.message.author.id
        nameofchannel = ctx.message.channel.name
        x=0
        if nameofchannel=='crewmate':
            for i in nicknames.keys():
                print(i,id)
                if i==id :
                    temp = nicknames[id]
                    x=1
                    await ctx.send(f"Your Current Tasks are:\n {player_dict[temp][0]}\nYou Have completed:\n{player_dict[temp][1]}")
            if x==0:
                await ctx.send("Are you sure you are playing?")
        else:
                await ctx.send("Be Smart, you are in the Wrong Channel")


    def update_progression(self):
        progress_bar_value = (progression / max_progress_value) * 100
        greens = math.floor(progress_bar_value / 10)
        bar = []

        for i in range(PROGRESS_BAR_MAX):
            bar.append(GREEN_BOX) if i in range(greens) else bar.append(RED_BOX)

        bar_str = '{} {:4.2f}%'.format(''.join(bar), progress_bar_value)
        globals()['progress_bar'] = bar_str

    @commands.command()
    async def dead(self, ctx):
        player = ctx.author
        await self.make_dead(ctx, player)

    @commands.command()
    @commands.has_role('MOD')
    async def kill_player(self, ctx, member: discord.Member):
        await self.make_dead(ctx, member)

    #Generalized method to mark a player as dead
    async def make_dead(self, ctx, member):
        #give the dead player role to the member that was just killed by this command.
        dead_player_role = ctx.guild.get_role(DEAD_PLAYER_ID)
        await member.add_roles(dead_player_role, atomic=True)

        #removing the dead player from the crewmate members list and removing their crewmate role IF they are a crewmate.
        memberIndex: int = 0
        player_name: str = ""
        crewmate_role = ctx.guild.get_role(CREW_MATE_ID)
        for crewmate in crewmate_members_list:
            if(member == crewmate):

                #append the dead player to the dead crewmate list.
                dead_crewmates_list.append(member)

                crewmate_members_list.pop(memberIndex)
                await crewmate.remove_roles(crewmate_role)

                #make bot send out a message that the crewmate just got killed. The nickname is printed out to be dead. If not available then their username.
                player_name = await self.getMemberName(member)

                if(len(crewmate_members_list)>= 1):
                    await ctx.send(f'Update: {player_name} was not an imposter ... {number_of_imposters} imposters remaining ... 😨')
                else:
                    await ctx.send(f'Update: {player_name} was the last crewmate and they just died! ... 😳')

                break
            memberIndex = memberIndex + 1

        #removing the dead player from the imposter members list and removing their imposter role IF they are a imposter. 
        memberIndex = 0
        imposter_role = ctx.guild.get_role(IMPOSTER_ID)
        for imposter in imposter_members_list:
            if(member == imposter):
                imposter_members_list.pop(memberIndex)
                
                #append the dead player to the dead imposter list.
                dead_imposters_list.append(member)
                await imposter.remove_roles(imposter_role)

                #make bot send out a message that the imposter just got killed. The nickname is printed out to be dead. If not available then their username.
                player_name = await self.getMemberName(member)

                if(len(imposter_members_list) >= 1):
                    await ctx.send(f'Update: {player_name} was an imposter ... {len(imposter_members_list)} imposters remaining ... 😨')
                else:
                    await ctx.send(f'Update: {player_name} was the last imposter! ... {len(imposter_members_list)} imposters remaining 🎉')

                break
            memberIndex = memberIndex + 1

        #check for whether the imposters won or the crewmates won after this player just died.
        await self.check_win(ctx)

        #Moving the killed player from the lobby voice channel to the dead voice channel.
        dead_voice_channel = discord.utils.get(ctx.guild.channels, name=DEAD_VOICE_CHANNEL)
        await member.move_to(dead_voice_channel)

    # helper function to check for a win. This is either when all the imposters are dead, or all crewmates are dead, or TODO: all tasks have been completed and the crewmates have won. 
    async def check_win(self, ctx):
        imposterNames: str = ""
        crewmateNames: str = ""
        deadCrewmates: str = ""
        deadImposters: str = ""
        temp_name: str = ""

        #the crewmate members list is length 0. This means that the imposters has won. The imposter and dead imposter nicknames will be printed out and if thats not available then their username.
        #the imposter members list length cannot also be 0 because then this branch executes for edge case 1 imposter dies and is the only player.
        if( len(crewmate_members_list) == 0 and len(imposter_members_list) != 0 ):
            for imposter in imposter_members_list:
                
                temp_name = await self.getMemberName(imposter)
                imposterNames = imposterNames + temp_name + " 😈 \n"

            for dead_player in dead_imposters_list:

                temp_name = await self.getMemberName(dead_player)
                deadImposters = deadImposters + temp_name + " 😈 \n"
            
            if(deadImposters != ""):
                await ctx.send(f'All crewmates have been killed !\nImposters have won the game !\nCongratulations to the imposters:\n{imposterNames}\nShoutout to the dead imposters:\n{deadImposters}')
            elif(deadImposters == ""):
                await ctx.send(f'All crewmates have been killed !\nImposters have won the game !\nCongratulations to the imposters:\n{imposterNames}\nNo imposters died during the duration of the game !')
            
            #print the among us bot art.
            await self.printAmongUsArt(ctx)

        #the imposter members list is length 0. This means that the crewmates have won. The crewmates and dead crewmates nicknames will be printed out and if thats not available then their username. 
        elif ( len(imposter_members_list) == 0 ):
            for crewmate in crewmate_members_list:

                temp_name = await self.getMemberName(crewmate)
                crewmateNames = crewmateNames + temp_name + " 🥳\n"
            
            for dead_player in dead_crewmates_list:

                temp_name = await self.getMemberName(dead_player)
                deadCrewmates = deadCrewmates + temp_name + " 👻\n"
            
            if(deadCrewmates != ""):
                await ctx.send(f'All imposters have been killed !\nCrewmates have won the game !\nCongratulations to the crewmates:\n{crewmateNames}\nShoutout to the dead crewmates:\n{deadCrewmates}')
            elif(deadCrewmates == ""):
                await ctx.send(f'All imposters have been killed !\nCrewmates have won the game !\nCongratulations to the crewmates:\n{crewmateNames}\nNo crewmates died during the duration of the game !')
            
            #print the among us bot art.
            await self.printAmongUsArt(ctx)

    #helper function to print the amongus art. Used when either the imposter wins or the crewmate wins. 
    async def printAmongUsArt(self, ctx):
        amongUsBotArt: str = ""
        #print each line of the emoji art of the amongus bot by opening the amongus_art file.
        with open('amongus_art.txt') as file:
            for line in file:
                amongUsBotArt = amongUsBotArt + line #note each line already appends a newline "\n" character.
        
        await ctx.send(f'{amongUsBotArt}')
    
    #helper function which will return the nickname of the member passed if available. If the nickname is not available then their discord named is returned.
    async def getMemberName(self, player):
        temp_name: str = ""
        if(player.nick != None):
            temp_name = player.nick
        elif(player.nick == None):
            temp_name = player.name
        
        return temp_name

    async def crew_win_game(ctx, self):
        meet_ch = discord.utils.get(ctx.guild.channels, name=MEETING_CHANNEL)
        await meet_ch.send("Crew Mates have completed all their tasks and won the game!")
        globals()['started'] = False

def setup(bot):
    bot.add_cog(Game(bot))
    print('Game loaded')