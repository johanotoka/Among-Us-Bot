import discord
from discord.ext import commands
import main
from datetime import datetime as d
from discord_buttons_plugin import *
from discord.ext.commands.cooldowns import BucketType


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
                globals()['clicked']=True 
                globals()['ptime']=t
                await ctx.reply(f'Who closed the lights :eyes:')
        else:
                print(t, globals()['ptime'])
                await ctx.reply(f"Take a deep breadth you are on cooldown {(timer-(t-globals()['ptime']))*60}min left",flags=MessageFlags().EPHEMERAL)

  
    @buttons.click
    async def ox(ctx):
        t=float(d.now().strftime('%H.%M'))
        if (globals()['clicked']==False or t-globals()['ptime']>timer):
                # TODO Call bot for playing the SOUND
                globals()['clicked']=True
                globals()['ptime']=t
                await ctx.reply(f'Wait is it me or are we losing oxygen :face_with_spiral_eyes:')
        else:
                await ctx.reply(f"Take a deep breadth you are on cooldown {(timer-(t-globals()['ptime']))*60}min left",flags=MessageFlags().EPHEMERAL)

    @buttons.click
    async def reac(ctx):
        t=float(d.now().strftime('%H.%M'))
        if (globals()['clicked']==False or t-globals()['ptime']>timer):
                # TODO Call bot for playing the SOUND
                globals()['clicked']=True 
                globals()['ptime']=t
                await ctx.reply(f'People gotta not mess with the reactor :fire:')
        else:
            await ctx.reply(f"Take a deep breadth you are on cooldown {(timer-(t-globals()['ptime']))*60}min left",flags=MessageFlags().EPHEMERAL)

    @buttons.click
    async def dor(ctx):
        t=float(d.now().strftime('%H.%M'))
        if (globals()['clicked']==False or t-globals()['ptime']>timer):
            # TODO Call bot for playing the SOUND
            globals()['clicked']=True 
            globals()['ptime']= t
            await ctx.reply(f'Everyone doors are closed, Dance and it might open :joy:')
        else:
            await ctx.reply(f"Take a deep breadth you are on cooldown {(timer-(t-globals()['ptime']))*60}min left",flags=MessageFlags().EPHEMERAL)

def setup(bot):
    bot.add_cog(Sabotage(bot))
    print('Sabotage loaded')


