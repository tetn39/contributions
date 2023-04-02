import discord
from discord.ext import commands, tasks
import os
import requests
from dotenv import load_dotenv
import sqlite3

load_dotenv()

intents = discord.Intents.all()
intents.members = True
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='?', activity=discord.Game('?で実行'), case_insensitive=True, intents=intents)

dbname = 'MAIN.db'
conn = sqlite3.connect(dbname)
cur = conn.cursor()


@bot.event
async def on_ready():
    print(f'ボットが起動しました {bot.user}')


@bot.command()
async def login(ctx, name='default'):
    """githubの名前を登録する"""
    if name == 'default':
        await ctx.send('名前を入力してください')
        return
    cur.execute('SELECT name FROM users WHERE name = ?', (name,))
    for row in cur:
        if row[0] == name:
            await ctx.send('その名前はすでに登録されています')
            return

    cur.execute('INSERT INTO users (name, mention) VALUES (?, ?)', (name, ctx.author.mention))
    conn.commit()

    await ctx.send(f'{name}を登録しました')

@bot.command()
async def logout(ctx, name='default'):
    """githubの名前を削除する"""
    if name == 'default':
        await ctx.send('名前を入力してください')
        return
    

    cur.execute('DELETE FROM users WHERE name = ?', (name,))
    conn.commit()

    await ctx.send('削除しました\n`?showdb`で確認してください')

@bot.command()
async def check(ctx):
    """contributionsをチェックする"""
    mention = ctx.author.mention
    cur.execute('SELECT name, mention FROM users WHERE mention = ?', (mention,))
    message = []
    for row in cur:
        name = row[0]
        mention = row[1]
        url = f'https://github-contributions-api.deno.dev/{name}.json'
        url_json = requests.get(url).json()
        message.append(f'{mention}\n今日の`{name}`のcontributionsは{url_json["contributions"][-1][-1]["contributionCount"]}回です')
    if len(message) == 0:
        await ctx.send('まだ名前が登録されていません')
        return
    await ctx.send('\n'.join(message))

@bot.command()
async def start(ctx):
    """loopを開始する"""
    checker.start(ctx)
    await ctx.send('contributionsをチェックします')
    cur.execute('SELECT name, mention FROM users')
    for row in cur:
        name = row[0]
        mention = row[1]
        url = f'https://github-contributions-api.deno.dev/{name}.json'
        url_json = requests.get(url).json()
        await ctx.send(f'{mention}\n今日のcontributionsは{url_json["contributions"][-1][-1]["contributionCount"]}回です')

@bot.command()
async def showdb(ctx):
    """dbの内容を表示する"""
    cur.execute('SELECT * FROM users')
    for row in cur:
        await ctx.send(f'`{row}`')

@bot.command()
async def stop(ctx):
    """ループを止める"""
    checker.stop()
    await ctx.send('ループを止めました')

@tasks.loop(seconds=10)
async def checker(ctx):
    """contributionsをチェックする"""
    cur.execute('SELECT name, mention FROM users')
    for row in cur:
        name = row[0]
        mention = row[1]
        url = f'https://github-contributions-api.deno.dev/{name}.json'
        url_json = requests.get(url).json()
        await ctx.send(f'{mention}\n今日のcontributionsは{url_json["contributions"][-1][-1]["contributionCount"]}回です')


bot.run(TOKEN)