import discord
from discord.ext import commands
import requests
import random
import asyncio
import html
import string

global trivia_in_use
trivia_in_use = False

class Games(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def scramble(self,ctx):
        with open('commands/google-10000-english.txt','r') as words_file:
            lines = words_file.readlines()
            line = random.choice(lines)
            line = line.strip()
            if len(line) > 4:
                scrambled = ''
                word = [letter for letter in line]
                for letter in line:
                    choice = random.choice(word)
                    scrambled += choice 
                    word.remove(choice)
                await ctx.send('Unscramble the following: ' + scrambled + ' <:PepoThink:832072234608099369>')
                def check(guess):
                    return guess.author.bot == False 
                finished = False
                number_of_guesses = 0
                points = 0
                hint_text =''
                if len(line) > 12:
                    points = 10
                elif len(line) > 8 and len(line) < 12:
                    points = 6 
                elif len(line) > 6 and len(line) <= 8:
                    points = 4 
                else:
                    points = 1 
                while not finished and number_of_guesses != 8:
                    try:
                        guess = await self.bot.wait_for('message', check = check, timeout = 10.0)
                        if guess.content == line:
                            await ctx.send('Correct! <@!{}> got it right! <:PogU:715897075249971230> +{} points {}'.format(guess.author.id, str(points), hint_text))
                            finished = True
                        else:
                            number_of_guesses += 1
                            if number_of_guesses == 4:
                                dash = ' _'*(len(line)-1)
                                await ctx.send('💡Hint: `' + line[:1] + dash + '`')
                                hint_text = '(Hint used)'
                                if points >1:
                                    points = int(points / 2) 
                                else:
                                    points = 0
                    except asyncio.TimeoutError:
                        await ctx.send('Times up! The word was \'' + line + '\'!🔔')
                        finished = True
                if number_of_guesses == 8:
                    await ctx.send('You\'re out of guesses! The word was \''+ line + '\'!🔔')
                
    @commands.command()
    async def trivia(self,ctx):
        global trivia_in_use
        if trivia_in_use == True:
            await ctx.send('There is already a trivia game running.')
        else:
            trivia_in_use = True
            trivia_api = "https://opentdb.com/api.php?amount=1"
            req = requests.get(url = trivia_api)
            question = req.json()['results'][0]
            q = html.unescape(question['question'])

            triviaembed = discord.Embed(
                title = 'Trivia',
                description = q,
                colour = discord.Colour.orange()
            )

            answers = {}
            correct = []
            options = question['incorrect_answers']
            options.append(question['correct_answer'])
            ans_text = ''  
            difficulties = {'hard':'https://stoffe.kawaiifabric.com/images/product_images/large_img/solid-red-fabric-Robert-Kaufman-USA-Red-179485-1.JPG', 'medium':'https://paperpackagingplace.com/wp-content/uploads/2016/01/Buttercup-Yellow.jpg', 'easy':'https://images-na.ssl-images-amazon.com/images/I/110CrE7egKL._SX322_BO1,204,203,200_.jpg'}

            if question['type'] == 'multiple':
                letters = [letter for letter in string.ascii_uppercase]
                for i in range(len(question['incorrect_answers'])):
                    choice = random.choice(options)
                    if choice == question['correct_answer']:
                        choice = html.unescape(choice)
                        correct = [(letters[i]).lower(), choice.lower()]
                    answers[letters[i]] = choice
                    options.remove(choice)
                for key,value in answers.items():
                    ans_text += '**'+key + '.** ' + value + '\n'

            elif question['type'] == 'boolean':
                ans_text = 'True or False'
                correct = [(question['correct_answer']).lower()]

            triviaembed.add_field(name='\u200b', value = ans_text, inline = False)
            triviaembed.set_footer(text = question['category'])
            triviaembed.set_author(name = question['difficulty'], icon_url = difficulties[question['difficulty']])

            def user_ans(answer):
                return answer.author.bot == False
            answered = False
            guesses = 0
            points = 0
        
            await ctx.send(embed = triviaembed)

            if question['difficulty'] == 'hard':
                points = 8
            elif question['difficulty'] == 'medium':
                points = 6 
            elif question['difficulty'] == 'easy':
                points = 4

            while not answered:
                try:
                    msg = await self.bot.wait_for('message', check = user_ans, timeout = 15.0)
                    if msg.content.lower() in correct:
                        await ctx.send('<a:correct:839094567609434174> Correct! <@!' + str(msg.author.id) + '> got it right! 🎉' + '+' + points + ' points') 
                        answered = True
                    else:
                        guesses += 1
                        points = points / 2
                        if question['type'] == 'multiple':
                            if guesses != 2:
                                await ctx.send('<a:shakingbell:839095524187176970> Incorrect! You have one guess left.')
                            else:
                                points = 0
                                await ctx.send('<a:wrong:839094469173182484> Incorrect! You have zero guesses left. The correct answer was \'' + html.unescape(question['correct_answer']) + '\'! 0 points earned.')
                                answered = True
                        elif question['type'] == 'boolean':
                            points = 0
                            await ctx.send('<a:wrong:839094469173182484> Incorrect! The correct answer was \'' + question['correct_answer']+ '\'! 0 points earned.')
                            answered = True
                except asyncio.TimeoutError:
                    points = 0
                    await ctx.send('<a:shakingbell:839095524187176970> Times up! The correct answer was \''+ html.unescape(question['correct_answer']) + '\'! 0 points earned.')
                    answered = True
            trivia_in_use = False

    #@commands.command()
    #async def 

        

def setup(bot):
    bot.add_cog(Games(bot))