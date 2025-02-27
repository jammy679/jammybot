import discord
from discord.ext import commands
import os
import asyncpg
import asyncio
from dotenv import load_dotenv

# https://www.pythondiscord.com/pages/guides/python-guides/app-commands/ - discord.py 2.0 changes

# loading env variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
# DB_NAME = os.getenv("DB_NAME") 
# DB_USER = os.getenv("DB_USER") 
# DB_PASS = os.getenv("DB_PASS") 
AUTH_TOKEN = os.getenv("AUTH_TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix = '!j ', intents = intents)
bot.remove_command('help')


async def create_db_pool():
    bot.pg_con_pool = await asyncpg.create_pool(DATABASE_URL)
    # bot.pg_con = await asyncpg.create_pool(database=DB_NAME,user=DB_USER,password=DB_PASS)


# !!! IMPORTANT - POSTGRESQL DOES NOT LIKE TABLE NAMES WITH UPPERCASE LETTERS !!!

@bot.event
async def on_guild_join(guild): # when the bot joins a server, creates a table
    # acquire connection, then release back to pool
    async with bot.pg_con_pool.acquire() as pg_con: 
        #column cannot be named 'user'
        await pg_con.execute("""CREATE TABLE IF NOT EXISTS {}(user_id TEXT, points INTEGER)""".format("\""+str(guild.id) + "_leaderboard\"")) #userid is text because integer has numeric limit
        list_users = await pg_con.fetch("SELECT user_id FROM \"{}_leaderboard\"".format(str(guild.id)))
        members_list = guild.members #check if it joins but had already joined before and still has table
        for user in members_list:
            if user.bot == False:
                if str(user.id) not in list_users:
                    await pg_con.execute("INSERT INTO {} (user_id, points) VALUES ({}, 0);".format("\""+str(guild.id) + '_leaderboard\"', "\'"+str(user.id)+"\'"))

#when user join add them to leaderboard with 0 points, if they were in server before don't add them again
@bot.event
async def on_member_join(member):
    async with bot.pg_con_pool.acquire() as pg_con: 
        list_users = await pg_con.fetch("SELECT user_id FROM \"{}_leaderboard\"".format(str(member.guild.id)))
        list_users = [(list(u))[0] for u in list_users] #convert record object to list, for some reason cannot use its attributes
        if str(member.id) not in list_users:
            await pg_con.execute("INSERT INTO {} (user_id, points) VALUES ({}, 0);".format("\""+str(member.guild.id) + '_leaderboard\"', "\'"+str(member.id)+"\'"))

@bot.command() #bot is an object (commands.Bot) and in the object it will add the function 'help' to
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
        'fun`trivia` - get a trivia question and win points!', 
        'fun`leaderboard` - view the leaderboard',
        'uti`weather <city>` - get the 5 day forecast of a city'
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
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='!j help'))
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
@commands.is_owner()
async def load(ctx,extension):
    await bot.load_extension(f'commands.{extension}')
    await ctx.send(extension + ' loaded.')

@bot.command()
@commands.is_owner()
async def unload(ctx,extension):
    await bot.unload_extension(f'commands.{extension}')
    await ctx.send(extension + ' unloaded.')

async def main(): 
    #db connection
    await create_db_pool()

    #load cogs
    for filename in os.listdir('./commands'):
        if filename.endswith('.py'):
            await bot.load_extension(f'commands.{filename[:-3]}')

    await bot.start(token=AUTH_TOKEN)

asyncio.run(main())