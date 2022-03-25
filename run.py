import discord
import requests
import json
import os
import asyncio
import re
from discord.ext import commands
from datetime import date
from numpy import random
from dotenv import load_dotenv

# Create environment variables
load_dotenv()


class MyClient(discord.Client):

    ogMemes = ['https://imgur.com/ST9RRdZ', 'https://imgur.com/YOFy6O2', 'https://imgur.com/NHJscWK',
            'https://imgur.com/AQrKLHS', 'https://imgur.com/T2kmXqQ', 'https://imgur.com/xSrY6F3', 'https://imgur.com/NfFlB1a']

    greats = ['https://cdn.discordapp.com/attachments/193188992857014272/859280267352080384/e3012c5d489016f804b00696a7b0427e.mp4', 'https://cdn.discordapp.com/attachments/193188992857014272/859163415079813130/Junkiesbeseethinginthecoments_8d0f7dc9b13e41603fa14fb38bc8bb73.mp4', 'https://cdn.discordapp.com/attachments/193188992857014272/858198346844864562/Whatarethepurposeofthesecomicsjustcirclejerk_ea8428881b521b3e489f5516fc48f0d9.mp4', 'https://cdn.discordapp.com/attachments/193188992857014272/845385715427704862/Depressedrook_49d925_8440415.mp4', 'https://discord.com/channels/193188992857014272/193188992857014272/840789509532024833', 'https://cdn.discordapp.com/attachments/193188992857014272/824357641048162334/1fb7394de568f412c32e28ef6f63f86c.mp4', 'https://cdn.discordapp.com/attachments/595792876873580546/857081275193491517/video0-143.mp4', 'https://cdn.discordapp.com/attachments/787867027775029259/852957245804249099/video0-18.mp4', 'https://cdn.discordapp.com/attachments/386718408982528000/854385108295483442/video0.mov', 'https://cdn.discordapp.com/attachments/564169696547700746/854191093830516786/IM_GOING_TO_KILL_CHAOS.mp4',
            'https://cdn.discordapp.com/attachments/825060471937040415/833469538108178442/sus.mp4', 'https://cdn.discordapp.com/attachments/193188992857014272/860225401703628820/qwe.mp4', 'https://cdn.discordapp.com/attachments/193188992857014272/856647303476805673/a_tu_casa.mp4', 'https://cdn.discordapp.com/attachments/193188992857014272/850526888421097502/video_1.mp4', 'https://cdn.discordapp.com/attachments/193188992857014272/850140189178200094/xdd.mp4', 'https://cdn.discordapp.com/attachments/193188992857014272/847901681777377281/getfvid_191184229_503335914218882_4166493292746332674_n.mp4', 'https://cdn.discordapp.com/attachments/715909144267456543/773793957146263582/123289186_364189861337254_4649832349965682829_n.mp4', 'https://cdn.discordapp.com/attachments/729055475445923964/759092722627117056/AngryChineseGuy.mov', 'https://cdn.discordapp.com/attachments/228646713026543618/861732683452776488/mzl2q7QxGDf8qbYDftcg_02_e908eaa7b460ecbf27ba255aca6d7fa8_video.mp4', 'https://2eu.funnyjunk.com/movies/Boom_7648b0_7820344.mp4', 'https://cdn.discordapp.com/attachments/193188992857014272/583096390964740106/meandtheboys.mp4']

    dota = ['https://cdn.discordapp.com/attachments/862790378925850624/867206248469757982/479019.mp4',
        'https://cdn.discordapp.com/attachments/222852560422174720/861740384336740363/DOTA_2_RAGE_-_PERUANO_Y_VENEZOLANO_ENOJADOS__.mp4']

    miercoles = [
    'https://cdn.discordapp.com/attachments/862790378925850624/867642282203414528/5n5dibawgvd61.png']

    jueves = ['https://tenor.com/view/asuka-feliz-jueves-running-happy-thursday-gif-16469364',
            'https://cdn.discordapp.com/attachments/862790378925850624/867203979996954684/feliz_jueves.mp4']

    viernes = [
    'https://cdn.discordapp.com/attachments/193188992857014272/762724813147209788/hapifr.mp4']

    week = ["Lunes", "Martes", "Miercoles",
        "Jueves", "Viernes", "Sabado", "Domingo"]

    workingD = os.getcwd()

    animeDB = json.load(open(
        f'{workingD}/anime_db.json', encoding='utf8'))

    categories = ['waifu', 'neko', 'shinobu', 'megumin', 'bully', 'cuddle', 'cry', 'hug', 'awoo', 'kiss', 'lick', 'pat', 'smug', 'bonk', 'yeet', 'blush', 'smile', 'wave', 'highfive', 'handhold', 'nom', 'bite', 'glomp', 'slap', 'kill', 'kick', 'happy', 'wink', 'poke',
                  'dance', 'cringe']


    # Get anime quote
    def getQuote(self):
        # Get Api
        s = requests.Session()
        s.verify = False
        response = s.get('https://animechan.vercel.app/api/random')
        # Transform into json
        json_data = json.loads(response.text)

        quote = f"Quote: {json_data['quote']}\nCharacter: {json_data['character']}\nSeries: {json_data['anime']}"
        return quote


    def getDay(self):
        day = str(date.today()).split('-')
        day = [int(x) for x in day]
        week_num = date(day[0], day[1], day[2]).weekday()
        today = self.week[week_num] 

        if today.lower() == 'miercoles':
            rand = random.randint(0, len(self.miercoles))
            return f'Wednesday my guy\n {self.miercoles[rand]}'
        elif today.lower() == 'jueves':
            rand = random.randint(0, len(self.jueves))
            return f'Asuka Bae\n {self.jueves[rand]}'
        elif today.lower() == 'viernes':
            rand = random.randint(0, len(self.viernes))
            return f'Viernes :)\n {self.viernes[rand]}'
        else:
            return f'Hoy es: {today}'

    def getDefinition(self, word):
        response = requests.get(
            f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}')
        processedResponse = json.loads(response.text)
        return f"Definition: {processedResponse[0]['meanings'][0]['definitions'][0]['definition']}"
    
    def getImage(self, search):
        response = requests.get(
            f'https://imsea.herokuapp.com/api/1?q=<{search}>')
        response_json = json.loads(response.text)
        return response_json['results']


    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_member_join(self, member):
        guild = member.guild
        if guild.system_channel is not None:
            role = discord.utils.get(member.guild.roles, name="Normies")
            member.add_role(role)
            to_send = f'Welcome {member.mention} to {guild.name}'
            await guild.system_channel.send(to_send)

    async def on_message(self, message):
        if message.author == client.user:
            return

        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')
        
        if message.content.startswith('$animeQuote'):
            await message.channel.send(self.getQuote())

        if message.content.startswith('$getDay'):
            await message.channel.send(self.getDay())

        if message.content.startswith('$getOG'):
            rand = random.randint(0, len(self.ogMemes))
            await message.channel.send(self.ogMemes[rand])

        if message.content.startswith('$userInfo'):
            await message.channel.send('What kind of info would you like to retrieve?\n1) Avatar\n2) ID\n3) Discord Account Creation')

            def is_correct(m):
                if m.content.isdigit():
                    if m.content == 1 or 2 or 3:
                        values = True
                    else:
                        values = False
                else:
                    return False

                return m.author == message.author and values

            try:
                option = await self.wait_for('message', check=is_correct, timeout=5.0)
            except asyncio.TimeoutError:
                return await message.channel.send(f'Sorry, you took too long, terminating request...')
            
            if option.content == '1':
                await message.channel.send(message.author.avatar_url)
            elif option.content == '2':
                await message.channel.send(message.author.id)
            elif option.content == '3':
                await message.channel.send(message.author.created_at)
            else:
                await message.channel.send('Unrecognized Input, Terminating...')

        if message.content.startswith('$animeSearch'):
            await message.channel.send('What Anime are you looking for?')

            def longEnough(m):
                return True if len(m.content) > 2 and m.author == message.author else False
            
            try:
                name = await self.wait_for('message', check=longEnough, timeout=10)
            except asyncio.TimeoutError:
                return await message.channel.send(f'Sorry, you took too long, terminating request...')

            # await message.channel.send(f'This is your message: {type(name.content)}')
            matches = dict()
            for i in range(len(self.animeDB['data'])):
                title = self.animeDB['data'][i]['title']
                if re.search(name.content.lower(), title.lower()):
                    matches[i] = title

            if not matches:
                return await message.channel.send('No entries found')

            reply_list = list()
            for i, item in enumerate(matches.values()):
                reply_list.append(f'{i+1}) {item}')

            await message.channel.send('Select an option:')
            await message.channel.send('\n'.join(reply_list))

            def is_correct(m):
                good_range = True if 0 <= int(m.content) <= len(reply_list) else False
                values = True if m.content.isdigit() else False
                return m.author == message.author and values and good_range

            try:
                option = await self.wait_for('message', check=is_correct, timeout=10)
            except asyncio.TimeoutError:
                return await message.channel.send(f'Sorry, you took too long, terminating request...')

            final_res = list()
            final_res.append(self.animeDB['data'][list(matches.keys())[int(option.content) - 1]]['title'])
            final_res.append(
                f"Type: {self.animeDB['data'][list(matches.keys())[int(option.content) - 1]]['type']}")
            final_res.append(
                f"Episodes: {self.animeDB['data'][list(matches.keys())[int(option.content) - 1]]['episodes']}")
            final_res.append(', '.join(self.animeDB['data'][list(
                matches.keys())[int(option.content) - 1]]['tags']))
            final_res.append(self.animeDB['data'][list(matches.keys())[
                int(option.content) - 1]]['picture'])

            await message.channel.send('\n'.join(final_res))
        
        # if users ask for a joke, then reply to them with a joke
        # This is the power of copilot
        if message.content.startswith('$joke'):
            # get joke from api and send it
            joke = requests.get('https://icanhazdadjoke.com/', headers={"Accept": "application/json"})
            await message.channel.send(joke.json()['joke'])

        # Copilot did this
        # if users ask a question, then reply to them with an answer
        if message.content.startswith('$question'):
            await message.channel.send('What is your question?')
            try:
                question = await self.wait_for('message', check=lambda m: m.author == message.author, timeout=12)
            except asyncio.TimeoutError:
                return await message.channel.send(f'Sorry, you took too long, terminating request...')

            # get answer from api and send it
            # make request verification false so that we can get the answer
            s = requests.Session()
            s.verify = False
            
            # reply to their question with a random fact about cars
            # get a random fact about cars
            fact = s.get('https://catfact.ninja/fact')
            await message.channel.send(f'{question.content} You ask? Well...\n{fact.json()["fact"]}')
            
        # if users ask for an anime picture, then reply to them with a picture
        if message.content.startswith('$animePic'):
            # ask them if they want a picture from a random tag or a specific tag
            await message.channel.send('Would you like a picture from a random tag or a specific tag?')

            # if the users asked for a random tag reply with a random picture using tags from self.categories
            try:
                option = await self.wait_for('message', check=lambda m: m.author == message.author, timeout=12)
            except asyncio.TimeoutError:
                return await message.channel.send(f'Sorry, you took too long, terminating request...')
            
            if option.content.lower() == 'random':
                # get a random tag
                rand = random.randint(0, len(self.categories))
                category = self.categories[rand]
                # get a random picture from that tag
                response = requests.get(
                    f'https://api.waifu.pics/sfw/{category}').text
                # get the picture url
                pic = json.loads(response)['url']
                # send the picture
                await message.channel.send(pic)
            else:
                # Display all tags to user from self.categories
                await message.channel.send('Here are all the tags:')
                await message.channel.send(', '.join(self.categories))

                # Make sure the user is asking for a tag that exists
                def is_correct(m):
                    return m.author == message.author and m.content.lower() in self.categories
                
                try:
                    option = await self.wait_for('message', check=is_correct, timeout=12)
                except asyncio.TimeoutError:
                    # tell the user their option is not valid
                    return await message.channel.send(f'Sorry, you took too long, terminating request...')
                
                # get picture from user option
                response = requests.get(
                    f'https://api.waifu.pics/sfw/{option.content.lower()}').text
                pic = json.loads(response)['url']
                # send the picture
                await message.channel.send(pic)

        if message.content.startswith('$definition'):
            await message.channel.send('What word would you like to define?')
            try:
                word = await self.wait_for('message', check=lambda m: m.author == message.author, timeout=12)
            except asyncio.TimeoutError:
                return await message.channel.send(f'Sorry, you took too long, terminating request...')

            # get the definition from the dictionary
            try:
                definition = self.getDefinition(word.content)
            except KeyError:
                return await message.channel.send(f'Sorry, {word.content} is not in the dictionary')

            if definition:
                await message.channel.send(definition)
            else:
                return await message.channel.send('Sorry, that word is not in the dictionary')

        if message.content.startswith('$yomomma'):
            # get a random joke from the api
            yomomma = requests.get(
                'https://yomomma-api.herokuapp.com/jokes').text
            if yomomma:
                await message.channel.send(json.loads(yomomma)['joke'])
            else:
                return await message.channel.send('Sorry, there was an error getting yo momma')

        if message.content.startswith('$randomFact'):
            # get a random fact from the api
            fact = requests.get('https://api.aakhilv.me/fun/facts').text
            fact = fact.replace('[', '').replace(']', '').replace('"', '')
            await message.channel.send(f'Did you know that {fact}')

        if message.content.startswith('$imageSearch'):
            await message.channel.send('What would you like to search for?')
            try:
                search = await self.wait_for('message', check=lambda m: m.author == message.author, timeout=12)
            except asyncio.TimeoutError:
                return await message.channel.send(f'Sorry, you took too long, terminating request...')

            # get the image from the api
            response = self.getImage(search.content)
            if response:
                await message.channel.send(response[0])
            else:
                return await message.channel.send('Sorry, that search did not return any results')
                

intents = discord.Intents.default()
intents.members = True

client = MyClient()
client.run(os.getenv('TOKEN'))
