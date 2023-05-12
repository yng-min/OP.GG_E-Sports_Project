# -*- coding: utf-8 -*-

# 패키지 라이브러리 설정
from discord.ext import commands
import json
import datetime
import pytz

import requests

# config.json 파일 불러오기
try:
    with open(r"./config.json", "rt", encoding="UTF8") as configJson:
        config = json.load(configJson)
except:
    print("config.json이 로드되지 않음")

webhook_url = config['all_log_webhook_url']


class GuildEVENT(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):

        print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
        print(f"Added Guild: {guild.name}({guild.id})")

        webhook_headers = { "Content-Type": "application/json" }
        webhook_data = {
            "username": "OP.GG E-Sports Log",
            "content": f"``` ```\n>>> `({datetime.datetime.now(pytz.timezone('Asia/Seoul')).strftime('%y/%m/%d %H:%M:%S')})`\nAdded Guild: {guild.name}({guild.id})"
        }
        webhook_result = requests.post(url=webhook_url, json=webhook_data, headers=webhook_headers)
        if 200 <= webhook_result.status_code < 300: pass
        else: print(f'- [LOG] Not sent with {webhook_result.status_code}, response:\n{webhook_result.json()}')

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):

        print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
        print(f"Removed Guild: {guild.name}({guild.id})")

        webhook_headers = { "Content-Type": "application/json" }
        webhook_data = {
            "username": "OP.GG E-Sports Log",
            "content": f"``` ```\n>>> `({datetime.datetime.now(pytz.timezone('Asia/Seoul')).strftime('%y/%m/%d %H:%M:%S')})`\nRemoved Guild: {guild.name}({guild.id})"
        }
        webhook_result = requests.post(url=webhook_url, json=webhook_data, headers=webhook_headers)
        if 200 <= webhook_result.status_code < 300: pass
        else: print(f'- [LOG] Not sent with {webhook_result.status_code}, response:\n{webhook_result.json()}')



def setup(bot):
    bot.add_cog(GuildEVENT(bot))
    print('guild_event.py 로드 됨')
