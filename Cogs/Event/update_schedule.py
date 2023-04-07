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

# config.json 파일 불러오기
try:
    with open(r"./config.json", "rt", encoding="UTF8") as configJson:
        config = json.load(configJson)
except:
    print("config.json이 로드되지 않음")

# league.json 파일 불러오기
try:
    with open(r"./league.json", "rt", encoding="UTF8") as leagueJson:
        leagues = json.load(leagueJson)['leagues']
except: print("league.json이 로드되지 않음")

# bot.sqlite 파일 불러오기
try:
    botDB = sqlite3.connect(rf"./Database/bot.sqlite", isolation_level=None)
    botCURSOR = botDB.cursor()
    channel_event = botCURSOR.execute("SELECT ChannelEvent FROM main").fetchone()[0]
    botDB.close()
except Exception as error:
    print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
    print(traceback.format_exc())

time_difference = config['time_difference']


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

            scheduleDB = sqlite3.connect(r"./Database/schedule.sqlite", isolation_level=None)
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
                "username": "OP.GG Esports Log",
                "content": content_msg
            }
            webhook_result = requests.post(webhook_url, json=webhook_data, headers=webhook_headers)
            if 200 <= webhook_result.status_code < 300: pass
            else: print(f'- [LOG] Not sent with {webhook_result.status_code}, response:\n{webhook_result.json()}')

            scheduleDB.close()

        elif match_data['error'] == True:
            # print(f"{match_data['code']}: {match_data['message']}")
            pass # match_complete 파일이랑 에러 메시지가 겹침



def setup(bot):
    bot.add_cog(UpdateScheduleTASK(bot))
    print("update_schedule.py 로드 됨")
