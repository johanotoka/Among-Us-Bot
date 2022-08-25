
import discord
from discord.ext import commands
from discord_buttons_plugin import *
from main import bot

players=[]
global count
count=0
buttons=ButtonsClient(bot)


class Bob(commands.Cog):
    def __init__(self,bot):
        self.bot =bot

    @commands.command()
    async def em(self,ctx):
        print("entered in hell")
        count=0
        await buttons.send(
            content="Call Emergency Meeting",
            channel= ctx.channel.id,
            components=[ActionRow([Button(style = ButtonType().Danger,
            label ="Call Emergency",
            custom_id="emm"
                                    )],
                            )
                ]
        )
    

    @buttons.click
    async def emm(ctx):
        print("pp")
        if( globals()['count'] <2): # [player.get(ctx.member)].em==0
            try:
                await ctx.reply(f'{ctx.member.display_name} called an Emergency Meeting, Head over to Cafe')
            #TODO Call Audio bot for playing the sound
            except:
                print("eerrorororo")
            globals()['count']+=1

        else:
            await ctx.reply(content=f"{ctx.member.display_name}, How many times you wanna press eh? ", flags=MessageFlags().EPHEMERAL)    
        #TODO Set Clickable for only 2 times




    @commands.command()
    async def hi(self,ctx): #!hi
        await buttons.send(
        content= "Hey There",
        channel = ctx.channel.id,
        components=[
            ActionRow(
                [Button(
                style = ButtonType().Primary,
                label="Hi",
                custom_id="hib",
            )]
            )
        ]

    
            )
    @buttons.click
    async def hib(ctx):        
        if(len(players)<=1 and (ctx.member not in players)):
            try:
                await ctx.reply(f'HI {ctx.member}')
                await players.append(ctx.member)
            except:
                print("error")

        else:
            await ctx.reply(f"Don't be lazy it's Weekzero {ctx.member}")




def setup(bot):
    bot.add_cog(Bob(bot))
    print('player loaded')
    
'''
Tasks  =  { First_task : ['Pas', '1234'] , Secnd_tk  }

!task 1sdf

task 1 Math
Questions: 2+1 2+6 2+9 2+7 1+7 
password :

0 - 100---50
50- 100 ---75
50 - 75 ---65
65 - 75 --- 70   


!done task2 20
{
    if p20 has task 2  ? error
} 


'''
