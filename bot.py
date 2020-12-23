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

#@bot.command()
#async def member(ctx):
#    for guild in bot.guilds:
#        for member in guild.members:
#            print(member)

@bot.command()
async def 안녕(ctx):
    my_name = discord.utils.get(ctx.guild.members, name = ctx.message.author.name)
    await ctx.send("안녕하세요 {}님".format(my_name.mention))

@bot.command()
async def 도움(ctx):
    user = discord.utils.get(ctx.guild.members, name=ctx.message.author.name)
    channel = await user.create_dm()
    embed = discord.Embed(colour = discord.Colour.red())
    #embed를 생성하고, embed의 색상을 blue로 지정합니다
    embed.set_author(name = "도움말")
    #embed의 author를 "Help"로 지정합니다.
    embed.add_field(name = "```기본 명령어```",value = "`!안녕`:봇이 인사해줍니다",inline=False)
    embed.add_field(name = "```레인보우 식스: 시즈 명령어```",value = "`!맵이름`: !맵이름을 치면(ex:!별장) 지명사진을 보냅니다.",inline=False)
    embed.add_field(name = "```테이블탑 시뮬레이터 명령어```",value = "`!추천(숫자)`: !추천(숫자)를 치면(ex: !추천3) n인용 게임을 추천해줍니다.",inline=False)
    await channel.send(embed=embed)
    #embed 를 전송합니다.

"""
"""
bot.run(os.environ['token'])
