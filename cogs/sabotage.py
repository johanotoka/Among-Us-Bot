import discord
from discord.ext import commands
import main
from datetime import datetime as d
from discord_buttons_plugin import *
from discord.ext.commands.cooldowns import BucketType

CREW_CHANNEL = 'crewmate'

buttons=ButtonsClient(main.bot)
# imposters=Game.get_imporsters()
rate = 10
per=1
t = BucketType.default
global clicked
clicked =False
global ptime 
ptime= 24.90
timer = 0.02


class Sabotage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
       
 

    @commands.Cog.listener()
    async def on_command_error(self,ctx,error):
        if isinstance(error,commands.CommandOnCooldown):
            msg="Still on cooldown, try again in {:.2f} seconds".format(error.retry_after)
            await ctx.send(msg)



    # @commands.cooldown(rate, per,t)
    @commands.command()
    async def sab(self,ctx): #!hi
        await ctx.message.delete()
  
        globals()['clicked'] = False
        await buttons.send(
        content= "Hey There",
        channel = ctx.channel.id,
        components=[
            ActionRow(
             [
                Button(
                style = ButtonType().Primary,
                label="Electrical",
                custom_id="elc",), 
            
                Button(style=ButtonType().Success,
                label="Oxygen",
                custom_id="ox",),
                
                Button(
                style=ButtonType().Danger,
                label="Reactor",
                custom_id="reac",),

                Button(
                style=ButtonType().Secondary,
                label="Doors",
                custom_id="dor",),

            
             ]
            )
        ]
            )
    
    @buttons.click
    async def elc(ctx):
        t=float(d.now().strftime('%H.%M'))
        if (globals()['clicked']==False or t-globals()['ptime']>timer):
            # TODO Call bot for playing the SOUND
                vc = ctx.guild.voice_client
                if vc:
                    vc.stop()
                    vc.play(discord.FFmpegPCMAudio(executable="audio/ffmpeg.exe", source="audio/among_us_sab.mp3"))
                else:
                    await ctx.reply("Not in a voice channel. Initialize a game first!")
                globals()['clicked']=True 
                globals()['ptime']=t
                await ctx.reply(f'Who closed the lights :eyes:')
                meet_ch = discord.utils.get(ctx.guild.channels, name=CREW_CHANNEL)
                await meet_ch.send("Electrical sabotage is ongoing. Tasks can not be completed until power is restored!")
        else:
                print(t, globals()['ptime'])
                await ctx.reply(f"Take a deep breadth you are on cooldown {(timer-(t-globals()['ptime']))*60}min left",flags=MessageFlags().EPHEMERAL)

  
    @buttons.click
    async def ox(ctx):
        t=float(d.now().strftime('%H.%M'))
        if (globals()['clicked']==False or t-globals()['ptime']>timer):
                # TODO Call bot for playing the SOUND
                vc = ctx.guild.voice_client
                if vc:
                    vc.stop()
                    vc.play(discord.FFmpegPCMAudio(executable="audio/ffmpeg.exe", source="audio/among_us_sab.mp3"))
                else:
                    await ctx.reply("Not in a voice channel. Initialize a game first!")
                globals()['clicked']=True
                globals()['ptime']=t
                await ctx.reply(f'Wait is it me or are we losing oxygen :face_with_spiral_eyes:')
                meet_ch = discord.utils.get(ctx.guild.channels, name=CREW_CHANNEL)
                await meet_ch.send("Oxygen Sabotage is ongoing. Restore oxygen within 45 seconds to avoid dying!")
        else:
                await ctx.reply(f"Take a deep breadth you are on cooldown {(timer-(t-globals()['ptime']))*60}min left",flags=MessageFlags().EPHEMERAL)

    @buttons.click
    async def reac(ctx):
        t=float(d.now().strftime('%H.%M'))
        if (globals()['clicked']==False or t-globals()['ptime']>timer):
                # TODO Call bot for playing the SOUND
                vc = ctx.guild.voice_client
                if vc:
                    vc.stop()
                    vc.play(discord.FFmpegPCMAudio(executable="audio/ffmpeg.exe", source="audio/among_us_sab.mp3"))
                else:
                    await ctx.reply("Not in a voice channel. Initialize a game first!")
                globals()['clicked']=True 
                globals()['ptime']=t
                await ctx.reply(f'People gotta not mess with the reactor :fire:')
                meet_ch = discord.utils.get(ctx.guild.channels, name=CREW_CHANNEL)
                await meet_ch.send("Reactor sabotage is ongoing. Prevent a meltdown within 45 seconds!")
        else:
            await ctx.reply(f"Take a deep breadth you are on cooldown {(timer-(t-globals()['ptime']))*60}min left",flags=MessageFlags().EPHEMERAL)

    @buttons.click
    async def dor(ctx):
        t=float(d.now().strftime('%H.%M'))
        if (globals()['clicked']==False or t-globals()['ptime']>timer):
            # TODO Call bot for playing the SOUND
            vc = ctx.guild.voice_client
            if vc:
                    vc.stop()
                    vc.play(discord.FFmpegPCMAudio(executable="audio/ffmpeg.exe", source="audio/among_us_sab.mp3"))
            else:
                    await ctx.reply("Not in a voice channel. Initialize a game first!")
            globals()['clicked']=True 
            globals()['ptime']= t
            await ctx.reply(f'Everyone doors are closed, Dance and it might open :joy:')
            meet_ch = discord.utils.get(ctx.guild.channels, name=CREW_CHANNEL)
            await meet_ch.send("Doors sabotage is ongoing. Doors will reopen after 10 seconds!")
        else:
            await ctx.reply(f"Take a deep breadth you are on cooldown {(timer-(t-globals()['ptime']))*60}min left",flags=MessageFlags().EPHEMERAL)

def setup(bot):
    bot.add_cog(Sabotage(bot))
    print('Sabotage loaded')


