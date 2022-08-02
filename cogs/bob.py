import discord
from discord.ext import commands
from discord_buttons_plugin import *
from main import bot

players=[]

buttons=ButtonsClient(bot)


class Bob(commands.Cog):
    def __init__(self,bot):
        self.bot =bot


    @commands.command()
    async def hi(self,ctx):
        await buttons.send(
        content= "Hey There",
        channel = ctx.channel.id,
        components=[
            ActionRow([Button(
                style = ButtonType().Primary,
                label="Hi",
                custom_id="hib",
            ),
            Button(
                style = ButtonType().Success,
                label="Click",
                custom_id="b",
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
    