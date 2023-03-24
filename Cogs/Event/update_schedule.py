# -*- coding: utf-8 -*-

# 패키지 라이브러리 설정
import opgg
from discord.ext import commands, tasks
import sqlite3
import json
import datetime
import pytz
import traceback
import requests

# config.json Config 파일 불러오기
try:
    with open(r"./config.json", "rt", encoding="UTF8") as configJson:
        config = json.load(configJson)
except:
    print("config.json이 로드되지 않음")

time_difference = config['time_difference']
leagues = {
    0: {"id": "85", "name": "League of Legends Circuit Oceania", "shortName": "LCO", "region": "OCE"},
    1: {"id": "86", "name": "Pacific Championship Series", "shortName": "PCS", "region": "SEA"},
    2: {"id": "87", "name": "Liga Latinoamérica", "shortName": "LLA", "region": "LAT"},
    3: {"id": "88", "name": "League of Legends Championship Series", "shortName": "LCS", "region": "NA"},
    4: {"id": "89", "name": "League of Legends European Championship", "shortName": "LEC", "region": "EU"},
    5: {"id": "90", "name": "Vietnam Championship Series", "shortName": "VCS", "region": "VN"},
    6: {"id": "91", "name": "League of Legends Continental League", "shortName": "LCL", "region": "CIS"},
    7: {"id": "92", "name": "League of Legends Japan League", "shortName": "LJL", "region": "JP"},
    8: {"id": "93", "name": "Turkish Championship League", "shortName": "TCL", "region": "TR"},
    9: {"id": "94", "name": "Campeonato Brasileiro de League of Legends", "shortName": "CBLOL", "region": "BR"},
    10: {"id": "95", "name": "Oceanic Pro League", "shortName": "OPL", "region": "COE"},
    11: {"id": "96", "name": "League of Legends World Championship", "shortName": "Worlds", "region": "INT"},
    12: {"id": "97", "name": "League of Legends Master Series", "shortName": "LMS", "region": "LMS"},
    13: {"id": "98", "name": "League of Legends Pro League", "shortName": "LPL", "region": "CN"},
    14: {"id": "99", "name": "League of Legends Champions Korea", "shortName": "LCK", "region": "KR"},
    15: {"id": "100", "name": "Mid-Season Invitational", "shortName": "MSI", "region": "INT"}
}

# bot.sqlite Config 파일 불러오기
try:
    botDB = sqlite3.connect(rf"./Data/bot.sqlite", isolation_level=None)
    botCURSOR = botDB.cursor()
    channel_event = botCURSOR.execute("SELECT ChannelEvent FROM main").fetchone()[0]
    botCURSOR.close()
    botDB.close()
except Exception as error:
    print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
    print(traceback.format_exc())


class UpdateScheduleTASK(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx):

        if ctx.author == self.bot.user:
            return
        # if not ctx.author.bot:
        #     return
        if ctx.channel.id != channel_event:
            return

        match_data = opgg.match_completed(match_info=eval(ctx.content))

        if (match_data['error'] == False) and (match_data['data']['match_type'] == "reschedule"):
            print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
            print("경기 일정 변경")

            scheduleDB = sqlite3.connect(r"./Data/schedule.sqlite", isolation_level=None)
            scheduleCURSOR = scheduleDB.cursor()

            temp_scheduledAt = match_data['data']['match_scheduledAt'].replace("T", " ").split(".000Z")[0]
            date_temp = datetime.datetime.strptime(temp_scheduledAt, "%Y-%m-%d %H:%M:%S")
            date_delta = datetime.timedelta(hours=time_difference)
            time = date_temp + date_delta
            scheduledAt = time.strftime("%Y-%m-%d %H:%M:%S")

            # 경기 데이터 수정
            for i in range(16):
                match_name = f"{match_data['data']['team_1']} vs {match_data['data']['team_2']}"
                if match_data['data']['match_league'] == leagues[i]['shortName']:
                    scheduleCURSOR.execute(f"UPDATE {leagues[i]['shortName']} SET ScheduledAt = ? WHERE ID = ?", (scheduledAt, match_data['data']['match_id']))
            print(f"- Updated match: [{match_data['data']['match_league']}] {match_name} ({match_data['data']['match_id']})")

            content_msg = f"\n- Updated match: `[{match_data['data']['league']}] {match_name} ({match_data['data']['match_id']})`"
            webhook_url = "https://discord.com/api/webhooks/1004831743976689664/iJTrRuleg2KtVPST6Nfo4j4HCNYc9EMla5DnMvWKQbMmrsn0fBuT6i7sG-IkNz6SVDaM"
            webhook_headers = {
                "Content-Type": "application/json"
            }
            webhook_data = {
                "username": "QWER.GG Log",
                "content": content_msg
            }
            webhook_result = requests.post(webhook_url, json=webhook_data, headers=webhook_headers)
            if 200 <= webhook_result.status_code < 300: pass
            else: print(f'- [LOG] Not sent with {webhook_result.status_code}, response:\n{webhook_result.json()}')

            scheduleDB.close()

        else:
            print(f"{match_data['code']}: {match_data['message']}")



def setup(bot):
    bot.add_cog(UpdateScheduleTASK(bot))
    print("update_schedule.py 로드 됨")
