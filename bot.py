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

@bot.command()
async def member(ctx):
    for guild in bot.guilds:
        for member in guild.members:
            print(member)

@bot.command()
async def mention(ctx):
    user = discord.utils.get(ctx.guild.members, name=ctx.message.author.name)
    await ctx.send(f"hello, {user.mention}")

@bot.command()
async def 안녕(ctx):
    my_name = discord.utils.get(ctx.guild.members, name = ctx.message.author.name)
    await ctx.send("안녕하세요 {}님".format(my_name.mention))

@bot.command()
async def help(ctx):
    user = discord.utils.get(ctx.guild.members, name=ctx.message.author.name)
    channel = await user.create_dm()
    embed = discord.Embed(colour = discord.Colour.red())
    #embed를 생성하고, embed의 색상을 blue로 지정합니다
    embed.set_author(name = "도움말")
    #embed의 author를 "Help"로 지정합니다.
    embed.add_field(name = "!안녕",value = "봇이 인사해줍니다",inline=False)
    embed.add_field(name = "!공수",value = "공격/수비별로 각각 가장 많이 플레이한 2명의 오퍼 전적을 알려줍니다.", inline=False)
    embed.add_field(name = "!검색 (오퍼이름)",value = "오퍼의 전적을 알려줍니다.", inline=False)
    await channel.send(embed=embed)
    #embed 를 전송합니다.

"""
"""
bot.run(os.environ['token'])
