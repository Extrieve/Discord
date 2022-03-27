import os
import discord
import requests
import json
import numpy as np
import datetime
import youtube_dl
import asyncio
from keep_running import keep_alive
from replit import db
from discord.utils import get
from discord.ext import commands
from datetime import date


client = discord.Client()
intents = discord.Intents.default()
intents.members = True

description = '''Extrieve / Nick Discord Bot, an experiment, like you anon.'''

# Initializing the music object.
bot = commands.Bot(command_prefix='~',
                   description=description, intents=intents)

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

memelist = np.array(['https://imgur.com/ST9RRdZ', 'https://imgur.com/YOFy6O2', 'https://imgur.com/NHJscWK',
                    'https://imgur.com/AQrKLHS', 'https://imgur.com/T2kmXqQ', 'https://imgur.com/xSrY6F3', 'https://imgur.com/NfFlB1a'])

greats = np.array(['https://cdn.discordapp.com/attachments/193188992857014272/859280267352080384/e3012c5d489016f804b00696a7b0427e.mp4', 'https://cdn.discordapp.com/attachments/193188992857014272/859163415079813130/Junkiesbeseethinginthecoments_8d0f7dc9b13e41603fa14fb38bc8bb73.mp4', 'https://cdn.discordapp.com/attachments/193188992857014272/858198346844864562/Whatarethepurposeofthesecomicsjustcirclejerk_ea8428881b521b3e489f5516fc48f0d9.mp4', 'https://cdn.discordapp.com/attachments/193188992857014272/845385715427704862/Depressedrook_49d925_8440415.mp4', 'https://discord.com/channels/193188992857014272/193188992857014272/840789509532024833', 'https://cdn.discordapp.com/attachments/193188992857014272/824357641048162334/1fb7394de568f412c32e28ef6f63f86c.mp4', 'https://cdn.discordapp.com/attachments/595792876873580546/857081275193491517/video0-143.mp4', 'https://cdn.discordapp.com/attachments/787867027775029259/852957245804249099/video0-18.mp4', 'https://cdn.discordapp.com/attachments/386718408982528000/854385108295483442/video0.mov', 'https://cdn.discordapp.com/attachments/564169696547700746/854191093830516786/IM_GOING_TO_KILL_CHAOS.mp4',
                  'https://cdn.discordapp.com/attachments/825060471937040415/833469538108178442/sus.mp4', 'https://cdn.discordapp.com/attachments/193188992857014272/860225401703628820/qwe.mp4', 'https://cdn.discordapp.com/attachments/193188992857014272/856647303476805673/a_tu_casa.mp4', 'https://cdn.discordapp.com/attachments/193188992857014272/850526888421097502/video_1.mp4', 'https://cdn.discordapp.com/attachments/193188992857014272/850140189178200094/xdd.mp4', 'https://cdn.discordapp.com/attachments/193188992857014272/847901681777377281/getfvid_191184229_503335914218882_4166493292746332674_n.mp4', 'https://cdn.discordapp.com/attachments/715909144267456543/773793957146263582/123289186_364189861337254_4649832349965682829_n.mp4', 'https://cdn.discordapp.com/attachments/729055475445923964/759092722627117056/AngryChineseGuy.mov', 'https://cdn.discordapp.com/attachments/228646713026543618/861732683452776488/mzl2q7QxGDf8qbYDftcg_02_e908eaa7b460ecbf27ba255aca6d7fa8_video.mp4', 'https://2eu.funnyjunk.com/movies/Boom_7648b0_7820344.mp4', 'https://cdn.discordapp.com/attachments/193188992857014272/583096390964740106/meandtheboys.mp4', 'https://cdn.discordapp.com/attachments/371357409010253824/874368278183694427/videoplayback.mp4'])

dota = ['https://cdn.discordapp.com/attachments/862790378925850624/867206248469757982/479019.mp4',
        'https://cdn.discordapp.com/attachments/222852560422174720/861740384336740363/DOTA_2_RAGE_-_PERUANO_Y_VENEZOLANO_ENOJADOS__.mp4']

miercoles = [
    'https://cdn.discordapp.com/attachments/862790378925850624/867642282203414528/5n5dibawgvd61.png']

jueves = ['https://tenor.com/view/asuka-feliz-jueves-running-happy-thursday-gif-16469364',
          'https://cdn.discordapp.com/attachments/862790378925850624/867203979996954684/feliz_jueves.mp4']

viernes = [
    'https://cdn.discordapp.com/attachments/193188992857014272/762724813147209788/hapifr.mp4']


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    # bind to ipv4 since ipv6 addresses cause issues sometimes
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


# Registering an event


def get_anime():
  # Get API
  response = requests.get('https://api.jikan.moe/v3')


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def weaboo(self, ctx):
      # Get Api
      response = requests.get('https://animechan.vercel.app/api/random')
      # Transform into json
      json_data = json.loads(response.text)
      quote = json_data['quote'] + ' | Character: ' + \
          json_data['character'] + ' | Series: ' + json_data['anime']
      await ctx.send(quote)

    @commands.command()
    async def ogMeme(self, ctx):
      # Get Api
      randnum = np.random.randint(0, len(memelist))
      await ctx.send(memelist[randnum])

    @commands.command()
    async def goodShit(self, ctx):
      # Get Api
      randnum = np.random.randint(0, len(greats))
      await ctx.send(greats[randnum])

    @commands.command()
    async def get_day(self, ctx):
      week = ["Lunes", "Martes", "Miercoles",
              "Jueves", "Viernes", "Sabado", "Domingo"]
      day = str(date.today()).split('-')
      day = [int(x) for x in day]
      week_num = datetime.date(day[0], day[1], day[2]).weekday()
      current_day = week[week_num]

      if(current_day.lower() == 'miercoles'):
        randnum = np.random.randint(0, len(miercoles))
        await ctx.send(f"_It is Wednesday my dudes._ Hang in there sailor~\n{miercoles[randnum]}")
      elif(current_day.lower() == 'jueves'):
        randnum = np.random.randint(0, len(jueves))
        await ctx.send(f"Feliz *{current_day}* gettin' close :ricardo:\n{jueves[randnum]}")
      elif(current_day.lower() == 'viernes'):
        randnum = np.random.randint(0, len(viernes))
        await ctx.send(f'Feliz *{current_day}*, you made it :yeehaw:\n{viernes[randnum]}')
      else:
        await ctx.send(f'Feliz *{current_day}*\nEsperabas algo mas putita?')

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    async def play(self, ctx, *, query):
        """Plays a file from the local filesystem"""

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print(
            f'Player error: {e}') if e else None)

        await ctx.send(f'Now playing: {query}')

    @commands.command()
    async def yt(self, ctx, *, url):
        """Plays from a url (almost anything youtube_dl supports)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print(
                f'Player error: {e}') if e else None)

        await ctx.send(f'Now playing: {player.title}')

    @commands.command()
    async def stream(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(
                f'Player error: {e}') if e else None)

        await ctx.send(f'Now playing: {player.title}')

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()

    @play.before_invoke
    @yt.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError(
                    "Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


@bot.event
async def on_ready():
  print(f'We have logged in as {bot.user}\n---------')


@client.event
async def on_message(msg):

  if msg.author == bot.user:
    return

  if 'Ans' in str(msg.author):
    if 'pi' in msg.content:
      await msg.channel.send('Tu vieja ma ni to')
    elif 'dota' in msg.content.lower():
      randnum = np.random.randint(0, len(dota))
      await msg.channel.send(dota[randnum])

  if 'Renato' in str(msg.author):
    if 'twitter.com' in msg.content:
      await msg.channel.send('Formatea bien tu meme csm')


@bot.event
async def on_member_join(self, member):
  guild = member.guild
  role = get(message.server.roles, name='Normies')
  if guild.system_channel is not None:
      await member.add_roles(role)

# Run the bot, use environment variable to hide token.
bot.add_cog(Music(bot))
keep_alive()
bot.run(os.environ['bot_token'])
