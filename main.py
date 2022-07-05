import discord
from discord.ext import commands
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
bot = commands.Bot(command_prefix='!')

@bot.event 
async def on_ready():
    await bot.change_presence(activity=discord.Game(name='Among Us'))
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.run(os.getenv('DISCORD_BOT_TOKEN'))