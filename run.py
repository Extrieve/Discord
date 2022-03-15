import discord
import requests
import json
import os
from datetime import date
from numpy import random
from dotenv import load_dotenv

# Create environment variables
load_dotenv()

client = discord.Client()

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

# Get anime quote
def getQuote():
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


def getDay():
    day = str(date.today()).split('-')
    day = [int(x) for x in day]
    week_num = date(day[0], day[1], day[2]).weekday()
    today = week[week_num]

    if today.lower() == 'miercoles':
        rand = random.randint(0, len(miercoles))
        return f'Wednesday my guy\n {miercoles[rand]}'
    elif today.lower() == 'jueves':
        rand = random.randint(0, len(jueves))
        return f'Asuka Bae\n {jueves[rand]}'
    elif today.lower() == 'viernes':
        rand = random.randint(0, len(viernes))
        return f'Viernes :)\n {viernes[rand]}'
    else:
        return f'Hoy es: {today}'



@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    
    if message.content.startswith('$animeQuote'):
        await message.channel.send(getQuote())

    if message.content.startswith('$getDay'):
        await message.channel.send(getDay())

    if message.content.startswith('$getOG'):
        rand = random.randint(0, len(ogMemes))
        await message.channel.send(ogMemes[rand])

client.run(os.getenv('TOKEN'))
