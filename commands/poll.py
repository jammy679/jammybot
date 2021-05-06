import discord
import sqlite3
from discord.ext import commands

global poll_running
global poll_info
global pollembed
poll_running = False
poll_info = {}
pollembed = None


class Poll:
    def __init__(self,name):
        self.name = name
        self.items = {}
    
    def additem(self, key):
        #format - pollitem: [], where list has list of users that voted for that item
        self.items[key] = [] 
    
    def removeitem(self,key):
        self.items.pop(key)
    
    def addvote(self,key,user):
        if user not in self.items[key]:
            for k,v in (self.items).items():
                if user in v:
                    v.remove(user)
                    break
            self.items[key].append(user)
        else:
            return 'Same item'
    
    def removevote(self, key,user):
        if user in self.items[key]:
            self.items[key].remove(user)

class PollCog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command()
    async def startpoll(self,ctx,*, name):
        global poll_running
        global poll_info
        global current_poll
        if poll_running == True:
            await ctx.send("There is a poll already running.")
        else:
            poll_running = True
            def check_if_author(msg):
                return msg.author == ctx.author
            current_poll = Poll(name)
            await ctx.send("Moderator <@!" + str(ctx.author.id) + "> has started a poll named \'" + name + "\'!")
    
        
    @commands.command(aliases = ['add'])
    async def polladd(self, ctx, *, item):
        global current_poll
        global poll_running
        global pollembed
        if poll_running == False:
            await ctx.send('There is currently no poll running.')
        else:
            in_poll = False
            for key, value in (current_poll.items).items():
                if key == item:
                    await ctx.send('That item is already in the poll.')
                    in_poll = True
                    break
            if not in_poll:
                current_poll.additem(item)
                await ctx.send('Added!')
                if pollembed != None:
                    await self.update(ctx)        
    
    @commands.command(aliases = ['remove'])
    async def pollremove(self,ctx,*,item):
        global current_poll
        global poll_running
        global pollembed
        if poll_running == False:
            await ctx.send('There is currently no poll running.')
        else:
            in_poll = False
            for key,value in (current_poll.items).items():
                if key == item:
                    current_poll.removeitem(item)
                    in_poll = True 
                    await ctx.send('Removed!')
                    if pollembed != None:
                        await self.update(ctx)        
                    break

            if not in_poll:
                await ctx.send('That item is not in the poll.')
    
    #command supposed to not be available to users
    @commands.command()
    async def update(self,ctx):
        global pollembed
        global pollmsg
        global item_str
        global value_str
        global current_poll
        global poll_running
        if not poll_running:
            print('not running')
        else:
            item_str = ''
            value_str = ''
            for key,value in (current_poll.items).items():
                item_str += key + '\n'
                value_str += str(len(value)) + '\n' 
            pollembed.set_field_at(0, name = 'Item', value = item_str, inline = True)
            pollembed.set_field_at(1, name = 'Votes', value = value_str, inline = True)
            await pollmsg.edit(embed = pollembed)
    
    @commands.command()
    async def vote(self,ctx,*,item):
        global current_poll
        global poll_running
        global pollembed
        if poll_running == False:
            await ctx.send('There is currently no poll running.')
        else:
            in_poll = False
            for key,value in (current_poll.items).items():
                if item == key:
                    in_poll = True
                    break
            if in_poll:
                voted = current_poll.addvote(item, ctx.author.name)
                if voted != None:
                    await ctx.send('You have already voted for this item.')
                else:
                    if pollembed != None:
                        await self.update(ctx)        
                    await ctx.send('Voted!')
            else:
                await ctx.send('That item is not in the poll.')


    @commands.command()
    async def poll(self,ctx):
        global current_poll
        global poll_running
        global item_str
        global value_str
        global pollmsg
        global pollembed
        if poll_running == False:
            await ctx.send('There is currently no poll running.')
        else:
            item_str = ''
            value_str = ''
            for key,value in (current_poll.items).items():
                item_str += key + '\n'
                value_str += str(len(value)) + '\n' 
            
            if item_str == '':
                await ctx.send('There are currently no items in the poll.')
            else:
                pollembed = discord.Embed(
                    title = current_poll.name,
                    colour = discord.Colour.red()
                )

                pollembed.add_field(name = 'Item', value = item_str, inline= True)
                pollembed.add_field(name = 'Votes', value = value_str, inline = True)
                pollmsg = await ctx.send(embed = pollembed)
    
    @commands.command()
    async def endpoll(self,ctx):
        global pollembed
        global poll_running
        global current_poll
        if not poll_running:
            await ctx.send('There is currently no poll running.')
        else:
            keys = [k for k,v in (current_poll.items).items()]
            values = [v for k,v in (current_poll.items).items()]
            if not keys or len(keys) == 1:
                await ctx.send('Poll cancelled.')
                poll_running = False
            else:
                highest_item = '' 
                highest_value = 0
                for i in range(len(values)):
                    if values[i] > highest_value:
                        highest_value = values[i] 
                        highest_item = keys[i]
                await ctx.send('<a:shakingbell:839095524187176970> Here are the final results! <a:shakingbell:839095524187176970>', embed = pollembed)
                await ctx.send('<a:sparklecolors:839827975418675211> `' + highest_item + '` won the poll with `' + highest_value + '` votes! <a:sparklecolors:839827975418675211>')
                poll_running = False

        
def setup(bot):
    bot.add_cog(PollCog(bot))

        