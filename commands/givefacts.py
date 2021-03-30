import discord
from discord.ext import commands
import requests

class Facts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def fact(self,ctx):
        url = 'https://uselessfacts.jsph.pl/random.json?language=en'
        req = requests.get(url=url)
        fact_resp = req.json()
        factembed = discord.Embed(
            title = 'Incoming fact!',
            colour  = discord.Colour.from_rgb(252, 211, 154)
        )
        factembed.set_author(name = 'Get another fact by typing \'!j fact\'!', icon_url = 'https://www.freeiconspng.com/thumbs/lightbulb-png/lightbulb-png-no-circle--lightbulb-10.png')
        factembed.add_field(name= '\u200b', value = fact_resp['text'], inline=False)
        factembed.set_footer(text = 'Fact from ' + fact_resp['source'] + ' - ' + fact_resp['source_url'])
        await ctx.send(embed = factembed)

def setup(bot):
    bot.add_cog(Facts(bot))