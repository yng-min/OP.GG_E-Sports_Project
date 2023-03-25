# -*- coding: utf-8 -*-

# 패키지 라이브러리 설정
import discord
from discord.ext import commands
from discord.commands import slash_command
import sqlite3
import json
import datetime
import pytz
import traceback
import os

colorMap = {
    "default": 0x2F3136,
    "red": 0xf60c50,
    "green": 0x90ee90
}


class ProfileCMD(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="프로필",
        description="프로필 정보를 조회할 수 있어요.",
    )
    async def _profileCMD(self, ctx):

        if not os.path.isfile(rf"./Data/User/user_{ctx.author.id}.sqlite"):
            embed = discord.Embed(title="> ⛔ 프로필 조회 불가", description="서비스에 가입하셔야 이용할 수 있는 기능입니다.", color=colorMap['red'])
            return await ctx.respond(embed=embed)

        try:
            userDB = sqlite3.connect(rf"./Data/User/user_{ctx.author.id}.sqlite", isolation_level=None)
            userCURSOR = userDB.cursor()
            resultMain = userCURSOR.execute(f"SELECT * FROM main WHERE UserID = {ctx.author.id}").fetchone()
            resultData = userCURSOR.execute(f"SELECT * FROM data WHERE UserID = {ctx.author.id}").fetchone()

            try: winRatio = ((resultData[4] / resultData[3]) * 100).__round__(1)
            except ZeroDivisionError: winRatio = 0.0

            embed = discord.Embed(title="> 📋 프로필 정보", description=f"<@{ctx.author.id}> 님의 정보예요.", color=colorMap['red'])
            embed.add_field(name="포인트 통계", value=f"_**{resultData[2]:,}**_포인트\n(누적 _**{resultData[1]:,}**_포인트)", inline=True)
            embed.add_field(name="승부 예측 통계", value=f"성공 : _**{resultData[4]:,}**_번 | 실패 : _**{resultData[5]:,}**_번\n승률 : _**{winRatio}**_% (누적 _**{resultData[3]:,}**_번)", inline=True)
            await ctx.respond(embed=embed)

        except Exception as error:
            print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
            print(traceback.format_exc())
            embed = discord.Embed(title="> ⚠️ 프로필 조회 실패", description=f"아래의 오류로 인해 프로필 조회에 실패했어요. 해당 문제가 지속된다면 개발자에게 문의해주세요.\n`{error}`", color=colorMap['red'])
            return await ctx.respond(embed=embed)

        try: userDB.close()
        except: pass



def setup(bot):
    bot.add_cog(ProfileCMD(bot))
    print("profile.py 로드 됨")
