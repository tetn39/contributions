import discord
from discord.ext import commands, tasks
import os
import requests
from dotenv import load_dotenv

intents = discord.Intents.all()
intents.members = True

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='?', activity=discord.Game('?で実行'), case_insensitive=True, intents=intents)


@bot.event
async def on_ready():
    print(f'ボットが起動しました {bot.user}')

@bot.command()
async def check(ctx, name):
    # nameを取得してloopを起動する
    checker.start(ctx, name)

@bot.command()
async def stop(ctx):
    """ループを止める"""
    checker.stop()

@tasks.loop(seconds=10)
async def checker(ctx, name):
    url = f'https://github-contributions-api.deno.dev/{name}.json'
    url_json = requests.get(url).json()
    await ctx.send(url_json['contributions'][-1][-1]['contributionCount'])


bot.run(TOKEN)