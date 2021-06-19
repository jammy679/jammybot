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

class Utility(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command(aliases = ['ti'])
    async def timein(self,ctx, *, city):
        city = city.split(' ')
        city = '_'.join(city)
        msg = await ctx.send('Finding...')
        timezone = fetch_timezone(city) 
        if timezone == False:
            await msg.edit(content ='Could not find that city.')
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
                colour = discord.Colour.from_rgb(35, 81, 105)
            )
            timeembed.add_field(name = '\u200b', value ='📅  '+ date + '\n⌚  ' + time, inline=False)
            timezone = timezone.split('_')
            timezone = ' '.join(timezone)
            timeembed.set_author(name= 'Timezone: ' + timezone, icon_url='https://icon-library.com/images/globe-png-icon/globe-png-icon-18.jpg')
            await msg.edit(content = '',embed = timeembed)

    @commands.command()
    async def weather(self,ctx,*,city):
        weather_url = "https://api.openweathermap.org/data/2.5/forecast?q={}&appid={}&units=metric".format(city, WEATHER_API_KEY)
        req = requests.get(url=weather_url)
        weather_data = req.json()
        weather_dicts = weather_data['list']
        days = [] #format for each element - {date, avgtemp, realfeel, weather}
        temp_avg =0
        feel_avg = 0
        desc = []
        date = weather_dicts[0]['dt_txt'][:10] 
        #weather api only gives 5 day forecast with temp every 3 hours, so to simplify it i got the average temperature and most common description (e.g. rain) of each day
        for w_dict in weather_dicts:
            current_date = w_dict['dt_txt'][:10]
            if current_date != date:
                weather = max(desc, key=desc.count) #finds most common description for the day
                days.append({'date': date, 'temp':temp_avg/len(desc), 'realfeel':feel_avg/len(desc), 'desc': weather})
                date = current_date 
                temp_avg = 0
                feel_avg = 0
                desc = []
            temp_avg += w_dict['main']['temp']
            feel_avg += w_dict['main']['feels_like']
            desc.append(w_dict['weather'][0]['main'])

        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        forecast = discord.Embed(
            title = '5-day forecast',
            colour = discord.Colour.dark_blue()
        )
        emojis = {'Clear':'☀️', 'Clouds':'☁️','Rain':'🌧️'}
        for weather in days:
            text = '🌡️ Temperature °C: `' + str(round(weather['temp'], 2)) + '`\n☀️ Real-feel: `' + str(round(weather['realfeel'],2)) + '`\n'
            date_obj = datetime.datetime.strptime(weather['date'],'%Y-%m-%d')
            weekday = weekdays[date_obj.weekday()]
            forecast.add_field(name=weekday + ' ' + emojis[weather['desc']], value = text, inline = False)
        forecast.set_thumbnail(url = 'https://images-na.ssl-images-amazon.com/images/I/41hzbXlmykL.png')
        await ctx.send(embed=forecast)

def setup(bot):
    bot.add_cog(Utility(bot))