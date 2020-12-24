import discord
import asyncio
import os

from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')

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
                    value = "`!추천 (숫자)`: `!추천 (숫자)`를 치면(ex: `!추천3`) n인용 게임을 추천해줍니다.\n보드게임 제목을 누르면 창작마당 링크로 이동합니다(웹페이지 로그인 필요)",
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
async def 추천(ctx, *, num = "1"):
    user = discord.utils.get(ctx.guild.members, name=ctx.message.author.name)
    embed = discord.Embed(colour = discord.Colour.orange())
    embed.set_author(name = f"{num}인용 보드게임 추천")
    embed.add_field(name = "**[지도 제작자들](<https://steamcommunity.com/sharedfiles/filedetails/?id=1817723272&searchtext=%EC%A7%80%EB%8F%84+%EC%A0%9C%EC%9E%91%EC%9E%90%EB%93%A4>)**",
                    value = "완벽한 지도를 탄생시키세요!",inline=False)
    embed.add_field(name = "[**플리트 주사위 게임**](<https://steamcommunity.com/sharedfiles/filedetails/?id=1815452941&searchtext=Fleet%3A+The+Dice>)",
                    value = "`!지명 (맵이름)`: `!지명 (맵이름)`을 치면(ex:`!지명 별장`) 지명사진을 보냅니다.",inline=False)
    embed.add_field(name = "**테이블탑 시뮬레이터 명령어**",
                    value = "`!추천 (숫자)`: `!추천 (숫자)`를 치면(ex: `!추천3`) n인용 게임을 추천해줍니다.",inline=False)
    await ctx.send(embed = embed)
    return 0



#@bot.command(name="청소", pass_context=True)
async def _clear(ctx, *, amount=1):
    await ctx.channel.purge(limit=amount)
    return 0

"""
"""
bot.run(os.environ['token'])