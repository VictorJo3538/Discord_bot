import os
import random
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

GYH = 1045304676217798658
JYW = 355676639801114627
LYJ = 366832595906068490
JSM = 340336549411422229
GBG = 1044331314616205403
LDH = 322025515344986122
KDG = 1045198399231754301


@bot.listen("on_ready")
async def on_ready():
    print(f"{bot.user.name} 작동 완료")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("리듬게임 생각"))


@bot.listen('on_message')
async def on_message(message):
    ch = bot.get_channel(1043962135744610445)
    # 권영훈 대답 리스트
    main_message = ['https://cdn.discordapp.com/attachments/1043962135744610445/1045306360448958534/image0.jpg',
                    'https://cdn.discordapp.com/attachments/1043962135744610445/1045305532329771018/image0.jpg',
                    'https://cdn.discordapp.com/attachments/1043962135744610445/1045305551950729276/image0.jpg',
                    'https://cdn.discordapp.com/attachments/1043962135744610445/1045305762009849906/image0.jpg',
                    'https://cdn.discordapp.com/attachments/1043962135744610445/1045615262386372638/image0.jpg',
                    'https://cdn.discordapp.com/attachments/1043962135744610445/1045839910399127612/image0.jpg',
                    'https://cdn.discordapp.com/attachments/1043962135744610445/1045840083388997772/image0.jpg',
                    '깝 ㄴㄴ', 'ㅤ', '👺', 'ㅋㅋ', '너 뭐야', '그래', '싫음', '왜', '흠....', '흠집', '우어', '우어', '이거 진짜 흠인데',
                    '난 그럴수 있다 생각해', '아싸', '헉!', '와..', '얼탱이 없네 🤣', "I'm scared", '나는 두려워', '나이스', 'yee', '킄킄']
    GYH_message = ['모야 이 짭은, 권영훈 안물']
    JYW_message = ['전영우 안물', '전 짱', '전영우 짱바보', '어이 전', '전.....', '저전......', '어이 전씨']
    LYJ_message = ['이유진 짱', '이유진 뭐라는거지?', '이유진 안물', '이유진 짱바보', '이유진진자라']
    JSM_message = ['조승민 안물', '어이 조씨']
    GBG_message = ['금보경 안물', '어이 금씨']
    LDH_message = ['임도현 안믈', '임도현 짱']
    KDG_message = ['강동근 안물', '강동근 전문하사 하자']

    P_list = [GYH, JYW, LYJ, JSM, GBG, LDH, KDG]
    P_Dic = {GYH: GYH_message, JYW: JYW_message, LYJ: LYJ_message, JSM: JSM_message, GBG: GBG_message, LDH: LDH_message,
             KDG: KDG_message}

    # 권영훈수두기
    if message.channel.id == 1043962135744610445 and '권영훈수두기' in message.content:
        if message.author.id == LDH:
            P_Dic[LDH].append('임도현자타임')
            await ch.send(random.choice(P_Dic[LDH]))
            P_Dic[LDH].remove('임도현자타임')
            return

    # 권영훈 대답 매크로
    if message.channel.id == 1043962135744610445 and ('어이 권' in message.content or '영훈' in message.content):
        for P in P_list:
            if message.author.id == P:
                await ch.send(random.choice(P_Dic[P] + main_message))
                return
        await ch.send(random.choice(main_message))

    # 전영우 저전 매크로
    if message.author == bot.user:
        return

    if message.author.id == 355676639801114627 and '전' in message.content:
        await message.channel.send('전영우짱바보')
        return

    if message.content == '전':
        await message.channel.send('저전')

    if message.content.endswith('저전'):
        await message.channel.send('저' + message.content)



    # 음악재생
    if message.channel.id == 1045278508580098088 and message.content.startswith("https"):
        url = message.content
        global channel
        global vc
        channel = message.author.voice.channel
        if message.channel.id == 1045278508580098088:
            try:
                vc = await channel.connect()
            except:
                try:
                    await vc.move_to(message.author.voice.channel)
                except:
                    await message.channel.send(embed=discord.Embed(title='이런!', description='일단 보이스 채널에 들어오고 해야지', color=0x26DBFF))

            YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
            FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                              'options': '-vn'}

            if not channel.connect().is_playing():
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
            await message.channel.send(embed=discord.Embed(title='흠...거기가 아닌데', description='음악 재생 채널로 가세요', color=0x26DBFF))

# @bot.command()
# async def test(ctx):
#     embed = discord.Embed(title='테스트', description='This message is for test', color=0x00ff00)
#     embed.set_author(name='test', icon_url='http://media.tenor.com/5FmfYNNPcwQAAAAC/dance-music.gif')
#     embed.set_image(url="https://media.tenor.com/5FmfYNNPcwQAAAAC/dance-music.gif")
#     await ctx.send(embed=embed)




#봇 음악재생 명령어
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

def start():
    try:
        token = os.environ["TOKEN"]
        bot.run(token)
    except:
        from TOKEN import load_token
        token = load_token()
        bot.run(token)

start()