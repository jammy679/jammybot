import discord
from discord.ext import commands
import requests
import sqlite3
import os
import asyncpg
import asyncio

DATABASE_URL = os.environ.get("DATABASE_URL",None)

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix = '!j ', intents = intents)
bot.remove_command('help')



async def create_db_pool():


    bot.pg_con = await asyncpg.create_pool(DATABASE_URL)


#points system does not work
#suggestions command still not made yet
#the following command wont work because it uses sqlite3

#@bot.event
#async def on_guild_join(guild):

#@bot.command()
#async def make_table(ctx):
    #await bot.pg_con.execute("""
    #CREATE TABLE IF NOT EXISTS {} (
        #user TEXT NOT NULL, 
        #points INTEGER
        #)""".format(ctx.guild.name + "_leaderboard"))
    #members_list = ctx.guild.members 
    #for user in members_list:
        #if user.bot == F   alse:
            #await bot.pg_con.execute("INSERT INTO {} (user, points) VALUES({}, 0)".format(str(ctx.guild.name) + 's leaderboard', user.name))


#add on user join and add to database

@bot.command()
async def make_table(ctx):
    sdfdsf = await bot.pg_con.fetch("SELECT suggestion FROM Suggestions")
    await bot.pg_con.execute("""
    CREATE TABLE IF NOT EXISTS {} (
        user TEXT NOT NULL, 
        points INTEGER
        )""".format(ctx.guild.name + "_leaderboard"))
    members_list = ctx.guild.members 
    for user in members_list:
        if user.bot == False:
            await bot.pg_con.execute("INSERT INTO {} (user, points) VALUES({}, 0)".format(str(ctx.guild.name) + 's leaderboard', user.name))

@bot.command()
async def help(ctx):
    helpemb = discord.Embed(
        title = 'Commands',
        colour = discord.Colour.blurple(),
        description = '**Syntax:** `!j <command name>`'
    )

    commands = [
        'fun`fact` - get a random fact!',
        'uti`timein (or ti) <city>` - find the time in a city',
        'fun`scramble` - unscramble a word and win points!',
        'fun`trivia` - get a trivia question and win points!' 
        ] 
    fc = ''
    uc = ''

    helpemb.add_field(name='Testing/help commands', value= '`test` - if the bot says \'hello\', then it is working!\n`ping` - test ping on bot\n`help` - sends this embed.\n`pollhelp` - view commands for making a poll', inline = False)
    for command in commands:
        if command[0:3] == 'fun':
            fc += command[3:] + '\n'
        elif command[0:3] == 'uti':
            uc += command[3:] + '\n'
    helpemb.add_field(name = 'Fun commands', value = fc, inline=False)
    helpemb.add_field(name='Utility commands', value = uc, inline = False)
    await ctx.send(embed=helpemb)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='!j help c:'))
    print('Ready')

@bot.command()
async def test(ctx):
    await ctx.send('hello!')

    
@bot.event
async def on_command_error(ctx,error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send('The command `' + ctx.invoked_with + '` is missing the argument: `' + error.param.name + '`')
    elif isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send('That command does not exist. Type !j help for a list of commands.')

@bot.command()
async def ping(ctx):
    pingmsg = await ctx.send('Pinging..')
    await pingmsg.edit(content=f'{round(bot.latency * 1000)}ms')

@bot.command()
async def load(ctx,extension):
    bot.load_extension(f'commands.{extension}')

@bot.command()
async def unload(ctx,extension):
    bot.unload_extension(f'commands.{extension}')

for filename in os.listdir('./commands'):
    if filename.endswith('.py'):
        bot.load_extension(f'commands.{filename[:-3]}')

bot.loop.run_until_complete(create_db_pool())
bot.run(AUTH_TOKEN)