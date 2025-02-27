import discord
from discord.ext import commands
import requests
import random
import asyncio
import html
import string
import asyncpg

class Fun(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.scramble_in_use = False
        self.trivia_in_use = False

    @commands.command()
    async def scramble(self,ctx):
        if self.scramble_in_use:
            await ctx.send('There is already scramble game running.')
        else:
            self.scramble_in_use = True
            ans = ''    
            while len(ans) <= 4:
                with open('commands/google-10000-english.txt','r') as words_file:
                    lines = words_file.readlines()
                    ans = random.choice(lines)
                    ans = ans.strip()

            scrambled = ''
            word = [letter for letter in ans]
            for letter in ans:
                choice = random.choice(word)
                scrambled += choice 
                word.remove(choice)
            await ctx.send('Unscramble the following: ' + scrambled)

            #answering algorithm
            def check(guess):
                return guess.author.bot == False 
            finished = False
            number_of_guesses = 0
            points = 0
            hint_text =''
            if len(ans) > 12:
                points = 10
            elif len(ans) > 8 and len(ans) < 12:
                points = 6 
            elif len(ans) > 6 and len(ans) <= 8:
                points = 4 
            else:
                points = 2 
            while not finished and number_of_guesses != 8:
                guess = ''
                try:
                    guess = await self.bot.wait_for('message', check = check, timeout = 10.0)
                    if guess.content == ans:
                        await ctx.send('Correct! <@!{}> got it right! <a:correct:839094567609434174> +{} points {}'.format(guess.author.id, str(points), hint_text))
                        await self.update_points(guess.author.id, points, ctx.guild.id)
                        finished = True
                    else:
                        number_of_guesses += 1
                        if number_of_guesses == 4:
                            dash = ' _'*(len(ans)-1)
                            await ctx.send('💡Hint: `' + ans[:1] + dash + '`')
                            hint_text = '(Hint used)'
                            points = int(points / 2) 
                except asyncio.TimeoutError:
                    await ctx.send('Times up! The word was \'' + ans + '\'! <a:shakingbell:839095524187176970>')
                    finished = True
            if number_of_guesses == 8:
                await ctx.send('You\'re out of guesses! The word was \''+ ans + '\'! <a:wrong:839094469173182484>')
            self.scramble_in_use = False 

    async def update_points(self, userid, points, guildid):
        async with self.bot.pg_con_pool.acquire() as pg_con:
            user_points = await pg_con.fetch("SELECT points FROM \"{}_leaderboard\" WHERE user_id = \'{}\'".format(str(guildid), str(userid)))
            user_points= [list(u)[0] for u in user_points][0]
            user_points += points
            await pg_con.execute("UPDATE \"{}_leaderboard\" SET points = {} WHERE user_id = \'{}\'".format(str(guildid), str(user_points), str(userid)))

    @commands.command()
    async def trivia(self,ctx):
        if self.trivia_in_use:
            await ctx.send('There is already a trivia game running.')
        else:
            self.trivia_in_use = True
            trivia_api = "https://opentdb.com/api.php?amount=1"
            req = requests.get(url = trivia_api)
            print(req.json())
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
            difficulties = {
                'hard':'https://stoffe.kawaiifabric.com/images/product_images/large_img/solid-red-fabric-Robert-Kaufman-USA-Red-179485-1.JPG', 
                'medium':'https://paperpackagingplace.com/wp-content/uploads/2016/01/Buttercup-Yellow.jpg', 
                'easy':'https://www.deckleedge.co.za/wp-content/uploads/2017/12/9064ed2c814cf785ca71638dd2102b099281f0fa.jpg'
            }

            if question['type'] == 'multiple':
                letters = [letter for letter in string.ascii_uppercase]
                # randomises order of answers
                for i in range(len(question['incorrect_answers'])):
                    choice = random.choice(options)
                    if choice == question['correct_answer']:
                        choice = html.unescape(choice)
                        correct = [(letters[i]).lower(), choice.lower()]
                    answers[letters[i]] = choice
                    options.remove(choice)
                    ans_text += '**' + letters[i] + '.** ' + choice + '\n'

            elif question['type'] == 'boolean':
                ans_text = 'True or False'
                correct = [(question['correct_answer']).lower()]

            triviaembed.add_field(name='\u200b', value = ans_text, inline = False)
            triviaembed.set_footer(text = question['category'])
            triviaembed.set_author(name = question['difficulty'], icon_url = difficulties[question['difficulty']])

            def user_ans(answer):
                if question['type'] == 'multiple':
                    k = ' '.join(answers.keys())
                    v = ' '.join(answers.values())
                    return answer.author.bot == False and (answer.content.lower() in k.lower() or answer.content.lower() in v.lower())
                elif question['type'] == 'boolean':
                    o = ' '.join(options)
                    return answer.author.bot == False and answer.content.lower() in o.lower()
            answered = False
            guesses = 0
            points = 0
        
            await ctx.send(embed = triviaembed)

            #answering algorithm

            if question['difficulty'] == 'hard':
                points = 6
            elif question['difficulty'] == 'medium':
                points = 4
            elif question['difficulty'] == 'easy':
                points = 2
            msg = ''
            while not answered:
                try:
                    msg = await self.bot.wait_for('message', check = user_ans, timeout = 15.0)
                    if msg.content.lower() in correct:
                        await ctx.send('<a:correct:839094567609434174> Correct! <@!{}> got it right! 🎉+{} points'.format(str(msg.author.id), str(points))) 
                        await self.update_points(msg.author.id, points, ctx.guild.id)
                        answered = True
                    else:
                        guesses += 1
                        points = points / 2
                        if question['type'] == 'multiple':
                            if guesses != 2:
                                await ctx.send('<a:shakingbell:839095524187176970> Incorrect! You have one guess left.')
                            else:
                                await ctx.send('<a:wrong:839094469173182484> Incorrect! You have zero guesses left. The correct answer was \'' + html.unescape(question['correct_answer']) + '\'! 0 points earned.')
                                answered = True
                        elif question['type'] == 'boolean':
                            await ctx.send('<a:wrong:839094469173182484> Incorrect! The correct answer was \'' + question['correct_answer']+ '\'! 0 points earned.')
                            answered = True
                except asyncio.TimeoutError:
                    await ctx.send('<a:shakingbell:839095524187176970> Times up! The correct answer was \''+ html.unescape(question['correct_answer']) + '\'! 0 points earned.')
                    answered = True
            self.trivia_in_use = False

    @commands.command()
    async def leaderboard(self,ctx):
        async with self.bot.pg_con_pool.acquire() as pg_con:
            users_points = await pg_con.fetch("SELECT * FROM \"{}_leaderboard\"".format(str(ctx.guild.id)))

        users_points = [tuple(u) for u in users_points]
        def second_elem(elem):
            return elem[1]
        users_points.sort(key=second_elem, reverse=True)
        users= [self.bot.get_user(int(u[0])) for u in users_points]

        user_text= ''
        points_text = ''
        place = 1
        for i in range(len(users_points)):
            points_text += str(users_points[i][1]) + '\n'
            try:
                if place == 1:
                    user_text += "🥇 " + users[i].name + '\n'
                elif place == 2:
                    user_text += "🥈 " + users[i].name + '\n'
                elif place == 3:
                    user_text += "🥉 " + users[i].name + '\n'
                else:
                    user_text += "`" + str(place) + "` " + users[i].name + '\n'
                place +=1
            except AttributeError:
                continue


        board = discord.Embed(
            title = 'Leaderboard!!',
            description = 'Earn points by playing my minigames!',
            colour = discord.Colour.dark_red()
        )
        
        #user_text = "🥇 Example User\n🥈 Example User #2\n🥉 Example User #3\n`4` Example User #4\n`5` Example User #5"
        #points_text = "112\n40\n36\n20\n17"

        board.add_field(name='User', value=user_text, inline=True)
        board.add_field(name='Points', value=points_text, inline=True)
        await ctx.send(embed = board)

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

async def setup(bot):
    await bot.add_cog(Fun(bot))