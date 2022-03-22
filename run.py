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

    animeDB = json.load(open(
        r'D:\Documents\OneDrive - University of South Florida\Python\Discord\anime_db.json', encoding='utf8'))


    # Get anime quote
    def getQuote(self):
        # Get Api
        s = requests.Session()
        s.verify = False
        response = s.get('https://animechan.vercel.app/api/random')
        # Transform into json
        json_data = json.loads(response.text)
        # quote = json_data['quote'] + ' | Character: ' + \
        #     json_data['character'] + ' | Series: ' + json_data['anime']

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

    
    # def get_roles(self):
    #     roles = discord.utils.get(member.server.roles)
    #     return ", ".join([str(r.id) for r in roles.roles])


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

        # if message.content.startswith('$utils'):
        #     mydir = f'These are the dirs\n{dir(discord.utils.get)}'
        #     await message.channel.send(mydir)

        # if message.content.startswith('$directories'):
        #     mydir = f'These are the dirs\n{dir(self)}'
        #     await message.channel.send(mydir)

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

            # await message.channel.send(self.animeDB['data'][list(matches.keys())[int(option.content) - 1]]['title'])
            # await message.channel.send(self.animeDB['data'][list(matches.keys())[int(option.content) - 1]]['picture'])
            # await message.channel.send(f"Type: {self.animeDB['data'][list(matches.keys())[int(option.content) - 1]]['type']}")
            # await message.channel.send(f"Episodes: {self.animeDB['data'][list(matches.keys())[int(option.content) - 1]]['episodes']}")
            # await message.channel.send(', '.join(self.animeDB['data'][list(matches.keys())[int(option.content) - 1]]['tags']))





intents = discord.Intents.default()
intents.members = True

client = MyClient()
client.run(os.getenv('TOKEN'))
