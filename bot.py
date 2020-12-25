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

print(json.dumps(json_data, indent="\t"))

@bot.event
async def on_ready():
    print(bot.user.id)
    print("ready")
    game = discord.Game("혼자서 놀기")
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
    embed.add_field(name = "**레인보우 식스: 시즈 명령어**",
                    value = "`!지명 (맵이름)`: `!지명 (맵이름)`을 치면(ex:`!지명 별장`) 지명사진을 보냅니다.",
                    inline=False)
    embed.add_field(name = "**테이블탑 시뮬레이터 명령어**",
                    value = """`!추천 (숫자)`: `!추천 (숫자)`를 치면(ex: `!추천 3`) n인용 게임중 랜덤으로 하나를 추천해줍니다. 숫자를 적지 않을시 1인용 보드게임을 추천해줍니다.
                    다운로드 링크를 누르면 창작마당 링크로 이동합니다(웹페이지 로그인 필요)\n게임 한줄평 제보 받습니다.
                    `!검색 (숫자) (난이도)`: `!검색 (숫자) (난이도)` 를 치면 (ex: `!검색 3 하`) n인용 게임중 난이도에 맞는 게임 모두를 알려줍니다. 
                    숫자와 난이도를 적지 않을시 1인용 보드게임 중 난이도 무관하게 알려줍니다. 난이도는 상, 중, 하 로 검색하시면 됩니다.
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
                    inline = n%2)
    await ctx.send(embed = embed)
    return 0

@bot.command()
async def 검색(ctx, *, num = 1, diff = None):
    user = discord.utils.get(ctx.guild.members, name=ctx.message.author.name)
    embed = discord.Embed(colour = discord.Colour.orange(), title =  f"{num}인용 보드게임 추천", 
                          description = "")

    game_list = [game for game in json_data["game"] if str(num) in game["best_num"]]
    print(game_list)
    for n in range(len(game_list)):
        embed.add_field(name = f"**{game_list[n]['name']}**",
                        value = f"[다운로드]({download_link(game_list[n]['download'])})\n[게임 정보]({info_link(game_list[n]['link'])})\n{game_list[n]['comment']}",
                        inline = n%2)
    await ctx.send(embed = embed)
    return 0

#@bot.command(name="청소", pass_context=True)
async def _clear(ctx, *, amount=1):
    await ctx.channel.purge(limit=amount)
    return 0

"""
"""
bot.run(os.environ['token'])