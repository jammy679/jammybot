import discord
from discord.ext import commands
import requests
import datetime

def fetch_timezone(place):
    tz = ''
    with open('commands/timezone.txt','r') as timezones:
        timezones = timezones.readlines()
        for timezone in timezones:
            timezone = timezone.strip()
            if place in timezone.lower():                    
                tz = timezone
                break     
        
    if tz == '':
        tz = False
    
    return tz

class TimeIn(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command(aliases = ['ti'])
    async def timein(self,ctx, *, city):
        city = city.split(' ')
        city = '_'.join(city)
        timezone = fetch_timezone(city) 
        if timezone == False:
            await ctx.send('Could not find that city.')
        else:
            url = 'http://worldtimeapi.org/api/timezone/{}'.format(timezone)
            req = requests.get(url= url)
            resp_time = req.json()
            name = resp_time['timezone'].split('/')
            name = name[len(name) - 1].split('_')
            name = ' '.join(name)
            time = resp_time['datetime'][11:16] 
            date = datetime.datetime.strptime(resp_time['datetime'][0:10], '%Y-%m-%d')
            date = datetime.datetime.strftime(date,'%A %B %m, %Y')
            timeembed = discord.Embed(
                title = name,
                colour = discord.Colour.from_rgb(35, 81, 105),
            )
            timeembed.add_field(name = '\u200b', value ='📅  '+ date + '\n⌚  ' + time, inline=False)
            timezone = timezone.split('_')
            timezone = ' '.join(timezone)
            timeembed.set_author(name= 'Timezone: ' + timezone, icon_url='https://icon-library.com/images/globe-png-icon/globe-png-icon-18.jpg')
            await ctx.send(embed = timeembed)


def setup(bot):
    bot.add_cog(TimeIn(bot))