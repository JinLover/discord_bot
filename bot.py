import discord
import asyncio
import os
import json
import random

from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')

with open('game.json', 'r') as f:
    json_data = json.load(f)

def info_link(num):
       return f"http://boardlife.co.kr/bbs_detail.php?bbs_num={num}&id=&tb=boardgame_strategy"

def download_link(num):
       return f"https://steamcommunity.com/sharedfiles/filedetails/?id={num}"

@bot.event
async def on_ready():
    print(bot.user.id)
    print("ready")
    game = discord.Game("명령어:!도움")
    await bot.change_presence(status=discord.Status.online, activity=game)
    return 0

#@bot.command()
#async def member(ctx):
#    for guild in bot.guilds:
#        for member in guild.members:
#            print(member)

@bot.command()
async def 안녕(ctx):
    my_name = discord.utils.get(ctx.guild.members, name = ctx.message.author.name)
    await ctx.send("안녕하세요 {}님".format(my_name.mention))
    return 0

@bot.command()
async def 도움(ctx):
    user = discord.utils.get(ctx.guild.members, name=ctx.message.author.name)
    channel = await user.create_dm()
    embed = discord.Embed(colour = discord.Colour.red())
    embed.set_author(name = "도움말")
    embed.add_field(name = "**기본 명령어**",
                    value = "`!안녕`:봇이 인사해줍니다",
                    inline=False)
    embed.add_field(name = "**테이블탑 시뮬레이터 명령어**",
                    value = """`!추천 (숫자)`: n인용 게임중 랜덤으로 하나를 추천해줍니다. 숫자를 적지 않을시 1인용 보드게임을 추천해줍니다.
                    다운로드 링크를 누르면 창작마당 링크로 이동합니다(웹페이지 로그인 필요)\n게임 한줄평 제보 받습니다.
                    `!검색 (숫자)`: n인용 게임을 15개까지 알려줍니다.
                    `!검색 (게임이름)`: 해당 게임이 있을시 게임에 대한 정보를 알려줍니다. 검색어는 두글자 이상이어야 합니다.
                    `!전부검색 (숫자)`: n인용 게임 전부를 개인 DM으로 알려줍니다.
                    """,
                    inline=False)
    await channel.send(embed=embed)
    return 0


@bot.command()
async def 지명(ctx, *, name = ""):
    user = discord.utils.get(ctx.guild.members, name=ctx.message.author.name)
    if name not in os.listdir(f"./map"):
        await ctx.send(f"{name}은 아직 등록되지 않았거나 없는 지명입니다.")
    else:
        files = os.listdir(f"./map/{name}")
        now = os.getcwd()
        for image in files:
            file = discord.File(f"{now}/map/{name}/{image}")
            await ctx.send(file = file)
    return 0

@bot.command()
async def 추천(ctx, *, num = 1):
    user = discord.utils.get(ctx.guild.members, name=ctx.message.author.name)
    embed = discord.Embed(colour = discord.Colour.orange(), title =  f"{num}인용 보드게임 검색", 
                          description = "")
    game_list = [game for game in json_data["game"] if str(num) in game["best_num"]]
    n = random.randint(0, len(game_list)-1)
    embed.add_field(name = f"**{game_list[n]['name']}**",
                    value = f"[다운로드]({download_link(game_list[n]['download'])})\n[게임 정보]({info_link(game_list[n]['link'])})\n{game_list[n]['comment']}",
                    inline = False)
    await ctx.send(embed = embed)
    return 0

@bot.command()
async def 검색(ctx, *inp, description = ""):
    user = discord.utils.get(ctx.guild.members, name=ctx.message.author.name)
    if len(inp) == 0 or len(inp) == 1 and len(inp[0]) == 1 and inp[0].isalpha():
        embed = discord.Embed(colour = discord.Colour.orange(), title =  "오류!", 
                          description = "숫자 또는 두글자 이상의 검색어를 입력해주세요")
    elif len(inp) == 1 and len(inp[0]) == 1 and inp[0].isdigit():
        num = inp[0]
        
        game_list = [game for game in json_data["game"] if str(num) in game["best_num"]]
        choose = range(len(game_list))

        if len(game_list) > 15:
            choose = random.sample(choose, 15)
            description = "게임 목록이 많아 15개의 게임만 표시되었습니다."

        embed = discord.Embed(colour = discord.Colour.orange(), title =  f"{num}인용 보드게임 목록", 
                          description = description)
        
        for n in choose:
            embed.add_field(name = f"**{game_list[n]['name']}**",
                            value = f"[다운로드]({download_link(game_list[n]['download'])})\n[게임 정보]({info_link(game_list[n]['link'])})\n{game_list[n]['comment']}",
                            inline = True)
    else:
        name = "".join(inp)
        game_list = [game for game in json_data["game"]]
        expect = []
        same = []
        max_match = 0
        for game in game_list:
            match = 0
            for char in name:
                if char in game["name"]:
                    match += 1
            if match == len(name):
                same.append(game)
            if match > max_match:
                max_match = match
                expect.append(game)
        if same:
            embed = discord.Embed(colour = discord.Colour.orange(), title = "검색 결과")
            for game in same:
                embed.add_field(name = game["name"],
                                value = f"[다운로드]({download_link(game['download'])})\n[게임 정보]({info_link(game['link'])})\n{game['comment']}",
                                inline = True)
        elif expect:
            end = len(expect)
            if len(expect) <= 3:
                end = len(expect)
            embed = discord.Embed(colour = discord.Colour.orange(), title = "혹시 이 게임을 찾으셨나요?")
            for n in range(-1, -end - 1, -1):
                embed.add_field(name = f"**{expect[n]['name']}**",
                                value = f"[다운로드]({download_link(expect[n]['download'])})\n[게임 정보]({info_link(expect[n]['link'])})\n{expect[n]['comment']}",
                                inline = True)
        else:
            embed = discord.Embed(colour = discord.Colour.orange(), title = "검색 결과", description = "찾으시는 게임이 없습니다.")

    await ctx.send(embed = embed)
    return 0

@bot.command()
async def 전부검색(ctx, *inp):
    user = discord.utils.get(ctx.guild.members, name=ctx.message.author.name)
    channel = await user.create_dm()
    if len(inp) == 0 or inp[0].isalpha():
        embed = discord.Embed(colour = discord.Colour.orange(), title =  "오류!", 
                          description = "숫자를 입력해주세요")
    else:
        num = inp[0]
        game_list = [game for game in json_data["game"] if str(num) in game["best_num"]]
        embed = discord.Embed(colour = discord.Colour.orange(), title =  f"{num}인용 보드게임 목록")
        
        for n in range(len(game_list)):
            embed.add_field(name = f"**{game_list[n]['name']}**",
                            value = f"[다운로드]({download_link(game_list[n]['download'])})\n[게임 정보]({info_link(game_list[n]['link'])})\n{game_list[n]['comment']}",
                            inline = True)
    await channel.send(embed=embed)
    return 0

#@bot.command(name="청소", pass_context=True)
async def _clear(ctx, *, amount=1):
    await ctx.channel.purge(limit=amount)
    return 0

"""
"""
bot.run(os.environ['token'])