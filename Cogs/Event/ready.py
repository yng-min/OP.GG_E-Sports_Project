# -*- coding: utf-8 -*-

# 패키지 라이브러리 설정
from discord.ext import commands
import json
import datetime
import pytz

# config.json Config 파일 불러오기
try:
    with open(r"./config.json", "rt", encoding="UTF8") as configJson:
        config = json.load(configJson)
except:
    print("config.json이 로드되지 않음")

client_version = config['client_version']


class ReadyEVENT(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):

        print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
        print(f"Online: {self.bot.user.name}({client_version}) [ Index File | Python ]")



def setup(bot):
    bot.add_cog(ReadyEVENT(bot))
    print('ready.py 로드 됨')
