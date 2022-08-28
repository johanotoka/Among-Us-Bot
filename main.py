import discord
from discord.ext import commands
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
bot = commands.Bot(command_prefix='!')

@bot.command()
@commands.has_any_role("MOD", "Game Leader")
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    print(f'{extension} loaded')

@bot.command()
@commands.has_any_role("MOD", "Game Leader")
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    print(f'{extension} unloaded')

@bot.command()
@commands.has_any_role("MOD", "Game Leader")
async def reload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    print(f'{extension} reloaded')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        if filename == 'player.py':
            print("skipped")
        else:
            bot.load_extension(f'cogs.{filename[:-3]}')
   

bot.run(os.getenv('DISCORD_BOT_TOKEN'))
