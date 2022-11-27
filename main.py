import os
import random
import time

import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, permission=8)
music_pl_ch = 1046426403354181694

slist = []

@bot.listen("on_ready")
async def on_ready():
    print(f"{bot.user.name} 작동 완료")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("리듬게임 생각"))
    # 인터페이스 시작
    embed = discord.Embed(title="노래의 주소를 채팅창에 넣어주세요", color=0x00ff00)
    embed.set_author(name='음악이 재생중이 아님', icon_url='https://cdn-icons-png.flaticon.com/512/1941/1941064.png')
    embed.set_image(url="https://media.tenor.com/5FmfYNNPcwQAAAAC/dance-music.gif")
    global temp
    temp = await bot.get_channel(music_pl_ch).send(embed=embed)
@bot.listen('on_message')
async def on_message(message):
    # 음악재생
    if message.channel.id == music_pl_ch and message.content.startswith("https"):
        await message.delete()
        await temp.delete()
        url = message.content
        global vc
        if message.channel.id == music_pl_ch:
            try:
                vc = await message.author.voice.channel.connect()
            except:
                try:
                    await vc.move_to(message.author.voice.channel)
                except:
                    temp = await message.channel.send(embed=discord.Embed(title='이런!', description='일단 보이스 채널에 들어오고 해야지', color=0x26DBFF))
                    time.sleep(3)
                    await temp.delete()

            YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
            FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                              'options': '-vn'}

            if not vc.is_playing():
                with YoutubeDL(YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(url, download=False)
                URL = info['formats'][0]['url']
                vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
                embed = discord.Embed(title="재생 중인 노래 다운", url=URL, description=f"{url}", color=0x00ff00)
                embed.set_author(name='음악 재생중', icon_url='https://cdn-icons-png.flaticon.com/512/1941/1941064.png')
                sliced_url = url[32:]
                thumbnail = 'https://img.youtube.com/vi/' + sliced_url + '/0.jpg'
                embed.set_image(url=thumbnail)
                await message.channel.send(embed=embed)
            else:
                await message.channel.send(embed=discord.Embed(title='앗!', description='이미 음악이 재생 중입니다', color=0x26DBFF))
        else:
            await message.channel.send(
                embed=discord.Embed(title='흠...거기가 아닌데', description='음악 재생 채널로 가세요', color=0x26DBFF))


# @bot.command()
# async def test(ctx):
#     embed = discord.Embed(title='테스트', description='This message is for test', color=0x00ff00)
#     embed.set_author(name='test', icon_url='http://media.tenor.com/5FmfYNNPcwQAAAAC/dance-music.gif')
#     embed.set_image(url="https://media.tenor.com/5FmfYNNPcwQAAAAC/dance-music.gif")
#     await ctx.send(embed=embed)


# 봇 음악재생 명령어
# @bot.command()
# async def play(ctx, *, url):
#     global channel
#     global vc
#     channel = ctx.message.author.voice.channel
#     if ctx.message.channel.id == 1045278508580098088:
#         try:
#             vc = await channel.connect()
#         except:
#             try:
#                 await vc.move_to(ctx.message.author.voice.channel)
#             except:
#                 await ctx.send(embed=discord.Embed(title='이런!', description='일단 보이스 채널에 들어오고 해야지', color=0x26DBFF))
#
#         YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
#         FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
#                           'options': '-vn'}
#
#         if not vc.is_playing():
#             with YoutubeDL(YDL_OPTIONS) as ydl:
#                 info = ydl.extract_info(url, download=False)
#             URL = info['formats'][0]['url']
#             vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
#             embed = discord.Embed(title="재생 중인 노래 다운", url=URL, description=f"{url}", color=0x00ff00)
#             embed.set_author(name='음악 재생중', icon_url='https://cdn-icons-png.flaticon.com/512/1941/1941064.png')
#             sliced_url = url[32:]
#             thumbnail = 'https://img.youtube.com/vi/' + sliced_url + '/0.jpg'
#             embed.set_image(url=thumbnail)
#             await ctx.send(embed=embed)
#         else:
#             await ctx.send(embed=discord.Embed(title='앗!', description='이미 음악이 재생 중입니다', color=0x26DBFF))
#     else:
#         await ctx.send(embed=discord.Embed(title='흠...거기가 아닌데', description='음악 재생 채널로 가세요', color=0x26DBFF))

# 봇 연결 해제 명령어
@bot.command()
async def stop(ctx):
    try:
        await vc.disconnect()
    except:
        await ctx.send(embed=discord.Embed(title='흠...', description='난 이미 없다', color=0x26DBFF))

@bot.command()
async def test(ctx):
    temp = await ctx.send(embed=discord.Embed(title='테스트용', description='이 메시지는 3초뒤 삭제됩니다.', color=0x26DBFF))
    time.sleep(3)
    await temp.delete()
def start():
    try:
        token = os.environ["TOKEN"]
        bot.run(token)
    except:
        from TOKEN import load_token
        token = load_token()
        bot.run(token)

start()