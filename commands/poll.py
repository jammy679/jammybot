import discord
from discord.ext import commands

class Poll:
    def __init__(self,name,owner):
        self.name = name
        self.items = {}
        self.owner = owner
    
    def additem(self, key):
        #format - pollitem: [], where list has list of users that voted for that item
        self.items[key] = [] 
    
    def removeitem(self,key):
        self.items.pop(key)
    
    def addvote(self,key,user):
        if user not in self.items[key]:
            # checks if they already voted
            self.removevote(user)
            self.items[key].append(user)
        else:
            return 'Same item'
    
    def removevote(self, user):
        for k,v in (self.items).items():
            if user in v:
                v.remove(user)
                break

class PollCog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.poll_running = False
        self.current_poll = None
        self.pollembed = None
    
    @commands.command()
    async def startpoll(self,ctx,*, name):
        if self.poll_running == True:
            await ctx.send("There is a poll already running.")
        else:
            self.poll_running = True
            def check_if_author(msg):
                return msg.author == ctx.author
            self.current_poll = Poll(name, ctx.author.id)
            await ctx.send("<@!" + str(ctx.author.id) + "> has started a poll named \'" + name + "\'!")
    
        
    @commands.command(aliases = ['add'])
    async def polladd(self, ctx, *, item):
        if self.poll_running == False:
            await ctx.send('There is currently no poll running.')
        else:
            if ctx.author.id == self.current_poll.owner:
                in_poll = False
                for key, value in (self.current_poll.items).items():
                    if key == item:
                        await ctx.send('That item is already in the poll.')
                        in_poll = True
                        break
                if not in_poll:
                    self.current_poll.additem(item)
                    await ctx.send('Added!')
                    if self.pollembed != None:
                        await self.update(ctx)        
            else:
                await ctx.send('Only the owner, <@!' + str(self.current_poll.owner) + '>, can add or remove items from the current poll.')
    
    @commands.command(aliases = ['remove'])
    async def pollremove(self,ctx,*,item):
        if self.poll_running == False:
            await ctx.send('There is currently no poll running.')
        else:
            if ctx.author.id == self.current_poll.owner:
                in_poll = False
                for key,value in (self.current_poll.items).items():
                    if key == item:
                        self.current_poll.removeitem(item)
                        in_poll = True 
                        await ctx.send('Removed!')
                        if self.pollembed != None:
                            await self.update(ctx)        
                        break

                if not in_poll:
                    await ctx.send('That item is not in the poll.')
            else:
                await ctx.send('Only the owner, <@!' + str(self.current_poll.owner) +'>, can add or remove items from the current poll.')
    
    #command supposed to not be available to users
    async def update(self,ctx):
        if not self.poll_running:
            print('not running')
        else:
            item_str = ''
            value_str = ''
            for key,value in (self.current_poll.items).items():
                item_str += key + '\n'
                value_str += str(len(value)) + '\n' 
            self.pollembed.set_field_at(0, name = 'Item', value = item_str, inline = True)
            self.pollembed.set_field_at(1, name = 'Votes', value = value_str, inline = True)
            await self.pollmsg.edit(embed = self.pollembed)
    
    @commands.command()
    async def vote(self,ctx,*,item):
        if self.poll_running == False:
            await ctx.send('There is currently no poll running.')
        else:
            in_poll = False
            for key,value in (self.current_poll.items).items():
                if item == key:
                    in_poll = True
                    break
            if in_poll:
                voted = self.current_poll.addvote(item, ctx.author.name)
                if voted != None:
                    await ctx.send('You have already voted for this item.')
                else:
                    if self.pollembed != None:
                        await self.update(ctx)        
                    await ctx.send('Voted!')
            else:
                await ctx.send('That item is not in the poll.')
    
    @commands.command()
    async def unvote(self,ctx):
        if not self.poll_running:
            await ctx.send("There is currently no poll running.")
        else:
            self.current_poll.removevote(ctx.author.name)
            await self.update(ctx)        


    @commands.command()
    async def poll(self,ctx):
        if self.poll_running == False:
            await ctx.send('There is currently no poll running.')
        else:
            item_str = ''
            value_str = ''
            for key,value in (self.current_poll.items).items():
                item_str += key + '\n'
                value_str += str(len(value)) + '\n' 
            
            if item_str == '':
                await ctx.send('There are currently no items in the poll.')
            else:
                self.pollembed = discord.Embed(
                    title = self.current_poll.name,
                    colour = discord.Colour.red()
                )

                self.pollembed.add_field(name = 'Item', value = item_str, inline= True)
                self.pollembed.add_field(name = 'Votes', value = value_str, inline = True)
                self.pollmsg = await ctx.send(embed = self.pollembed)
    
    @commands.command(aliases = ['end'])
    async def endpoll(self,ctx):
        if not self.poll_running:
            await ctx.send('There is currently no poll running.')
        else:
            if ctx.author.id == self.current_poll.owner:
                keys = [k for k,v in (self.current_poll.items).items()]
                values = [len(v) for k,v in (self.current_poll.items).items()]
                if not keys or len(keys) == 1:
                    await ctx.send('Poll cancelled.')
                    self.poll_running = False
                else:
                    highest_item = keys[0] 
                    highest_value = values[0] 
                    tied = [0] 
                    for i in range(1,len(values)):
                        if values[i] > highest_value:
                            highest_value = values[i] 
                            highest_item = keys[i]
                            tied = [i]
                        elif values[i] == highest_value:
                            tied.append(i)

                    await ctx.send('<a:shakingbell:839095524187176970> Here are the final results! <a:shakingbell:839095524187176970>', embed = self.pollembed)
                    if len(tied) > 1:
                        for i in range(1,len(tied)-1):
                            highest_item += ', ' + keys[tied[i]]
                        highest_item += ' and ' + keys[tied[len(tied)-1]]
                        await ctx.send('<a:sparklecolors:839827975418675211> `' + highest_item + '` tied with `' + str(highest_value) + '` votes! <a:sparklecolors:839827975418675211>')
                    else: 
                        await ctx.send('<a:sparklecolors:839827975418675211> `' + highest_item + '` won the poll with `' + str(highest_value) + '` votes! <a:sparklecolors:839827975418675211>')
                    self.poll_running = False
            else:
                await ctx.send('Only the owner, <@!' + str(self.current_poll.owner) +'>, can end the current poll.')
    
    @commands.command()
    async def pollhelp(self,ctx):
        phelp = discord.Embed(
            title = 'Poll commands',
            colour = discord.Colour.blurple(),
            description = 'Format: `!j <command name>`'
        )
        commands = [
            '`startpoll <name of poll>` - start a poll\n',
            '`polladd (or add) <item>` - add an item to the poll **(only the owner of the poll can do this)**\n',
            '`pollremove (or remove) <item>` - remove an item from the poll **(only the owner of the poll can do this)**\n',
            '`endpoll (or end)` - end/cancel the poll **(only the owner of the poll can do this)**\n',
            '`vote <item in poll>` - vote for an item in the poll\n',
            '`unvote` - remove your vote from the poll\n',
            '`poll` - view the poll\n'
        ]
        cmd_str =''
        for c in commands:
            cmd_str += c
        phelp.add_field(name = 'Commands', value = cmd_str, inline = False)
        await ctx.send(embed = phelp)


        
def setup(bot):
    bot.add_cog(PollCog(bot))

        