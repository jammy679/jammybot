import discord
from discord.ext import commands
import requests
import os

bot = commands.Bot(command_prefix = '!j ')
bot.remove_command('help')

@bot.command()
async def help(ctx):
    helpemb = discord.Embed(
        title = 'Commands',
        colour = discord.Colour.blurple(),
        description = '**Syntax:** `!j <command name>`'
    )

    helpemb.add_field(name='Testing/help commands', value= '`test` - if the bot says \'hello\', then it is working!\n`ping` - test ping on bot\n`help` - sends this embed.', inline = False)
    await ctx.send(embed=helpemb)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='!j help c:'))
    print('Ready')

@bot.command()
async def test(ctx):
    await ctx.send('hello!')

@bot.command()
async def inputtest(ctx):
    msg = await ctx.send('Type something you want me to say.')
    def check(checking):
        return checking.content != '' and ctx.message.author == checking.author
    msg = await bot.wait_for('message', check = check, timeout = 30.0)
    await ctx.send(msg.content)

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