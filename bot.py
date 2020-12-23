import discord
import asyncio
#import requests
import datetime

#from bs4 import BeautifulSoup
from discord.ext import commands

bot = commands.Bot(command_prefix='!')
bot.remove_command('help')

@bot.event
async def on_ready():
    print(bot.user.id)
    print("ready")
    game = discord.Game("레식 전적 검색")
    await bot.change_presence(status=discord.Status.online, activity=game)

@bot.command()
async def 안녕(ctx):
    my_name = discord.utils.get(ctx.guild.members, name = ctx.author.name)
    await ctx.channel.send("안녕하세요 {}님".format(my_name.mention))

@bot.command()
async def 떡집(ctx):
    a_Datetime = datetime.datetime.now()
    b_Datetime = datetime.datetime.strptime('2020-12-3', '%Y-%m-%d')
    await ctx.channel.send("떡집이 오기까지 %s일"%(b_Datetime-a_Datetime).days)

@bot.command()
async def 등록(ctx):
    flag = 0
    try:
        id_ = ctx.author.id
        nickname = ctx.message.content.split(' ')[1]
        flag = 1
    except:
        await ctx.send("닉네임을 입력해주세요!")

    if flag:
        with open("data.txt", 'r') as f:
            data = f.readlines()
            f.seek(0)
            all_data = f.read()

        with open("data.txt", 'w+') as f:
            if str(id_) not in all_data:
                f.write('%d = %s\n'%(id_, nickname))
                for line in data:
                    f.write(line)

            else:
                for line in data:
                    if str(id_) not in line:
                        f.write(line)
                    else:
                        f.write('%d = %s\n'%(id_, nickname))

        my_name = discord.utils.get(ctx.guild.members, name = ctx.author.name)
        await ctx.channel.send("{}님, {} 닉네임으로 저장되었습니다.".format(my_name.mention, nickname))

@bot.command()
async def 검색(ctx):
    def offer_info(name, playtime, KD_rate, KD, winrate, playround, image):
        url = requests.get("https://r6.op.gg/operators/%s"%name)
        tier = BeautifulSoup(url.content, "html.parser")
        for i in tier.find_all(class_ = "operator-view__name-sub"):
            tier = i.text

        embed = discord.Embed(title = name, description = tier, color = 0x00ff56)
        #embed.set_author(name="저자의 이름", url="저자의 URL", icon_url="저자의 아이콘")
        embed.set_thumbnail(url = image)
        embed.add_field(name = "Playtime", value = playtime)
        embed.add_field(name = "KD rate", value = KD_rate)
        embed.add_field(name = "K/D", value = KD)
        embed.add_field(name = "Winrate", value = winrate)
        embed.add_field(name = "Playround", value = playround)
        #embed.add_field(name = "이것은 필드입니다.", value = "필드의 값입니다.")
        return embed

    id_ = ctx.author.id
    with open("data.txt", 'r') as f:
        if str(id_) not in f.read():
            await ctx.channel.send("먼저 닉네임 등록을 해 주세요!.")
        else:
            f.seek(0)
            for line in f.readlines():
                if str(id_) in line:
                    nickname = line.split(' ')[-1]

    webpage = requests.get("https://r6.op.gg/search?search=%s"%nickname)
    soup = BeautifulSoup(webpage.content, "html.parser")

    contents = soup.find_all(class_ = "stats__contents-box stats__contents-season-box")

    if contents:
        l = [i.text.replace(' ','').strip() for i in contents]
        L = l[0].split()[1:]

        link = [line.find_all("img") for line in soup.find_all(class_ = "stats__contents-box stats__contents-season-box")][0]
        links = [i['src'] for i in link]

        D = {}
        key = 0

        for i in range(len(L)):
            if i%9 == 0:
                key = L[i]
                D[L[i]] = []
            else:
                D[key].append(L[i])

        names = list(D.keys())
        for num in range(5):
            await ctx.channel.send(embed = offer_info(names[num], ' '.join(D[names[num]][0:2]), D[names[num]][2][:-2], ' '.join(D[names[num]][3:5]),
                                                ' '.join(D[names[num]][5:7]), D[names[num]][4], links[num]))
    else:
        await ctx.channel.send("\"%s\" 는 없는 닉네임인것 같습니다. 닉네임을 다시 등록해주세요."%nickname.strip())

@bot.command()
async def help(ctx):
    embed = discord.Embed(colour = discord.Colour.red())
    #embed를 생성하고, embed의 색상을 blue로 지정합니다
    embed.set_author(name = "도움말")
    #embed의 author를 "Help"로 지정합니다.
    embed.add_field(name = "!안녕",value = "철권봇이 인사해줍니다",inline=False)
    embed.add_field(name = "!등록",value = "!등록 (유비소프트 닉네임) 으로 입력하면 닉네임을 등록합니다.", inline=False)
    embed.add_field(name = "!검색",value = "가장 많이 플레이한 5명의 오퍼 전적을 알려줍니다.", inline=False)
    embed.add_field(name = "!공수",value = "공격/수비별로 각각 가장 많이 플레이한 2명의 오퍼 전적을 알려줍니다.", inline=False)
    embed.add_field(name = "!검색 (오퍼이름)",value = "오퍼의 전적을 알려줍니다.", inline=False)
    await ctx.send(embed=embed)
    #embed 를 전송합니다.

"""
"""
bot.run(os.environ['token'])
