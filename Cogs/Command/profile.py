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

from Extensions.i18n.substitution import Substitution

# config.json 파일 불러오기
try:
    with open(r"./config.json", "rt", encoding="UTF8") as configJson:
        config = json.load(configJson)
except: print("config.json이 로드되지 않음")

# en.json 파일 불러오기
try:
    with open(r"./Languages/en.json", "rt", encoding="UTF8") as enJson:
        lang_en = json.load(enJson)
except: print("en.json이 로드되지 않음")

# ko.json 파일 불러오기
try:
    with open(r"./Languages/ko.json", "rt", encoding="UTF8") as koJson:
        lang_ko = json.load(koJson)
except: print("ko.json이 로드되지 않음")

colorMap = config['colorMap']


class ProfileCMD(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name=lang_en['profile.py']['command']['name'],
        name_localizations={
            "ko": lang_ko['profile.py']['command']['name']
        },
        description=lang_en['profile.py']['command']['description'],
        description_localizations={
            "ko": lang_ko['profile.py']['command']['description']
        }
    )
    async def _profileCMD(self, ctx):

        language = Substitution.substitution(ctx)

        if not os.path.isfile(rf"./Database/User/user_{ctx.author.id}.sqlite"):
            embed_title = language['profile.py']['output']['embed-not_register']['title']
            embed_description = language['profile.py']['output']['embed-not_register']['description']

            embed = discord.Embed(title=embed_title, description=embed_description, color=colorMap['red'])
            return await ctx.respond(embed=embed, ephemeral=True)

        try:
            userDB = sqlite3.connect(rf"./Database/User/user_{ctx.author.id}.sqlite", isolation_level=None)
            userCURSOR = userDB.cursor()
            resultMain = userCURSOR.execute(f"SELECT * FROM main WHERE UserID = {ctx.author.id}").fetchone()
            resultData = userCURSOR.execute(f"SELECT * FROM data WHERE UserID = {ctx.author.id}").fetchone()

            try: winRatio = ((resultData[4] / resultData[3]) * 100).__round__(1)
            except ZeroDivisionError: winRatio = 0.0

            embed_title = language['profile.py']['output']['embed-profile']['title']
            embed_description = language['profile.py']['output']['embed-profile']['description'].format(ctx.author.id)
            embed_field_1_name = language['profile.py']['output']['embed-profile']['field_1']['name']
            embed_field_1_value = language['profile.py']['output']['embed-profile']['field_1']['value'].format(point=resultData[2], total_point=resultData[1])
            embed_field_2_name = language['profile.py']['output']['embed-profile']['field_2']['name']
            embed_field_2_value = language['profile.py']['output']['embed-profile']['field_2']['value'].format(success=resultData[4], fail=resultData[5], win_ratio=winRatio, total_prediction=resultData[3])

            embed = discord.Embed(title=embed_title, description=embed_description, color=colorMap['red'])
            embed.add_field(name=embed_field_1_name, value=embed_field_1_value, inline=True)
            embed.add_field(name=embed_field_2_name, value=embed_field_2_value, inline=True)
            await ctx.respond(embed=embed, ephemeral=True)

        except Exception as error:
            print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
            print(traceback.format_exc())

            embed_title = language['profile.py']['output']['embed-error']['title']
            embed_description = language['profile.py']['output']['embed-error']['description'].format(error=error)

            embed = discord.Embed(title=embed_title, description=embed_description, color=colorMap['red'])
            return await ctx.respond(embed=embed, ephemeral=True)

        try: userDB.close()
        except: pass



def setup(bot):
    bot.add_cog(ProfileCMD(bot))
    print("profile.py 로드 됨")
