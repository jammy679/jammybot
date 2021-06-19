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


# !!! IMPORTANT - POSTGRESQL DOES NOT LIKE TABLE NAMES WITH UPPERCASE LETTERS !!!

@bot.event
async def on_guild_join(guild):
    #column cannot be named 'user'
    await bot.pg_con.execute("""CREATE TABLE IF NOT EXISTS {}(user_id TEXT, points INTEGER)""".format("\""+str(guild.id) + "_leaderboard\"")) #userid is text because integer has numeric limit
    list_users = await bot.pg_con.fetch("SELECT user_id FROM \"{}_leaderboard\"".format(str(guild.id)))
    members_list = guild.members 
    for user in members_list:
        if user.bot == False:
            await bot.pg_con.execute("INSERT INTO {} (user_id, points) VALUES ({}, 0);".format("\""+str(guild.id) + '_leaderboard\"', "\'"+str(user.id)+"\'"))

#when user join add them to leaderboard with 0 points, if they were in server before don't add them again
@bot.event
async def on_member_join(member):
    list_users = await bot.pg_con.fetch("SELECT user_id FROM \"{}_leaderboard\"".format(str(member.guild.id)))
    list_users = [(list(u))[0] for u in list_users] #convert record object to list, for some reason cannot use its attributes
    if str(member.id) not in list_users:
        await bot.pg_con.execute("INSERT INTO {} (user_id, points) VALUES ({}, 0);".format("\""+str(member.guild.id) + '_leaderboard\"', "\'"+str(member.id)+"\'"))

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