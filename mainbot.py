import discord
from discord.ext import commands
import requests
import sqlite3
import os
import asyncpg

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix = '!j ', intents = intents)
bot.remove_command('help')



#@bot.event
#async def on_guild_join(guild):
    #conn = sqlite3.connect('discord_server.db')
    #c= conn.cursor()
    #c.execute('''CREATE TABLE IF NOT EXISTS {}(
        #id INTEGER PRIMARY KEY,
        #user TEXT,
        #points INTEGER
    #)
    #'''.format("\'" + str(guild.name) + 's leaderboard' + "\'"))
    #conn.commit()
    #members_list = guild.members 
    #for user in members_list:
        #if user.bot == False:
            #c.execute("INSERT INTO {} (user, points) VALUES({}, 0)".format("\'" + str(guild.name) + 's leaderboard' + "\'", "\'" + user.name+ "\'"))
            #conn.commit()

#add on user join and add to database

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
        'uti`pollhelp` - view commands for making a poll',
        'fun`trivia` - get a trivia question and win points!' 
        ] 
    fc = ''
    uc = ''

    helpemb.add_field(name='Testing/help commands', value= '`test` - if the bot says \'hello\', then it is working!\n`ping` - test ping on bot\n`help` - sends this embed.', inline = False)
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


bot.run(AUTH_TOKEN)