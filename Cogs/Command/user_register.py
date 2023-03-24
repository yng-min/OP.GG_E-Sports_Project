# -*- coding: utf-8 -*-

# 패키지 라이브러리 설정
import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
import sqlite3
import json
import datetime
import pytz
import traceback
import os

# config.json Config 파일 불러오기
try:
    with open(r"./config.json", "rt", encoding="UTF8") as configJson:
        config = json.load(configJson)
except:
    print("config.json이 로드되지 않음")

colorMap = {
    "default": 0x2F3136,
    "red": 0xf60c50,
    "green": 0x90ee90
}

# bot.sqlite Config 파일 불러오기
try:
    botDB = sqlite3.connect(rf"./Data/bot.sqlite", isolation_level=None)
    botCURSOR = botDB.cursor()
    db_version_user = botCURSOR.execute("SELECT DBVersionUser FROM main").fetchone()[0]
    botDB.close()
except Exception as error:
    print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
    print(traceback.format_exc())


class UserRegisterCMD(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    _register = SlashCommandGroup(name="서비스", description="설정 명령어", guild_only=True, default_member_permissions=discord.Permissions(administrator=True))

    @_register.command(
        name="가입",
        description="서비스 이용을 위한 가입 절차를 진행해요.",
    )
    async def _registerCMD(self, ctx):

        if os.path.isfile(rf"./Data/User/user_{ctx.author.id}.sqlite"):
            embed = discord.Embed(title="> ⛔ 가입 불가", description=f"<@{ctx.author.id}> 님은 이미 서비스에 가입되어 있어요.", color=colorMap['red'])
            return await ctx.respond(embed=embed)

        embed = discord.Embed(title="", description="⚙ 가입 진행 중...", color=colorMap['red'])
        msg = await ctx.respond(embed=embed)

        try:
            userDB = sqlite3.connect(rf"./Data/User/user_{ctx.author.id}.sqlite", isolation_level=None)
            userCURSOR = userDB.cursor()

            # 메인 테이블
            userCURSOR.execute("""
                CREATE TABLE IF NOT EXISTS main(
                UserID INTERGER,
                UserDBVersion INTERGER
                )
            """) # 메인 테이블 생성

            userCURSOR.execute("""
                INSERT INTO main(UserID, UserDBVersion)
                VALUES(?, ?)""",
                (ctx.author.id, 1)
            ) # 메인 테이블 데이터 입력

            # 데이터 테이블
            userCURSOR.execute("""
                CREATE TABLE IF NOT EXISTS data(
                UserID INTERGER,
                TotalPoint INTERGER,
                Point INTERGER,
                TotalAnswer INTERGER,
                CorrectAnswer INTERGER,
                WrongAnswer INTERGER
                )
            """) # 데이터 테이블 생성

            userCURSOR.execute("""
                INSERT INTO data(UserID, TotalPoint, Point, TotalAnswer, CorrectAnswer, WrongAnswer)
                VALUES(?, ?, ?, ?, ?, ?)""",
                (ctx.author.id, 5000, 5000, 0, 0, 0)
            ) # 데이터 테이블 데이터 입력

            print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
            print(f"{ctx.author}({ctx.author.id}) | 서비스 가입")
            embed = discord.Embed(title="> ✅ 가입 완료", description="서비스 가입이 완료되었어요.", color=colorMap['red'])
            await msg.edit_original_response(content="", embed=embed)

            # # 베타
            # betaEmbed = discord.Embed(title="> 📮 베타 테스트 안내", description="현재 QWER.GG 디스코드 봇 서비스가 베타 테스트를 진행 중입니다.\n베타 테스트에 참여하시려면 [서포트 서버](https://discord.gg/opgg) 입장 후, [모집 메시지](https://discord.com/channels/765059633873551360/1010984278001197136/1011905514420043836)를 읽어주세요. 🙂", color=colorMap['red'])
            # await ctx.send(embed=betaEmbed)

        except Exception as error:
            print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
            print(traceback.format_exc())
            embed = discord.Embed(title="> ⚠️ 가입 실패", description=f"아래의 오류로 인해 서비스 가입에 실패했어요. 해당 문제가 지속된다면 개발자에게 문의해주세요.\n`{error}`", color=colorMap['red'])
            return await msg.edit_original_response(content="", embed=embed)

        try: userDB.close()
        except: pass



def setup(bot):
    bot.add_cog(UserRegisterCMD(bot))
    print("user_register.py 로드 됨")
