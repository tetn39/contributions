import discord
from discord.ext import commands
import os
import requests
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.members = True

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='?', activity=discord.Game('?で実行'), case_insensitive=True, intents=intents)


@bot.event
async def on_ready():
    print(f'ボットが起動しました {bot.user}')

@bot.command()
async def check(ctx):
    """contributins 更新 check"""
    url = 'https://github-contributions-api.deno.dev/tetn39.json'
    url_json = requests.get(url).json()
    await ctx.send(url_json['contributions'][-1][-1]['contributionCount'])

bot.run(TOKEN)