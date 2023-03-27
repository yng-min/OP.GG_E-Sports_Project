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

time_difference = config['time_difference']
webhook_url = config['webhook_url']


class save_scheduleTASK(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self._routine_1_TASK.start()

    @tasks.loop(seconds=60)
    async def _routine_1_TASK(self):

        # 경기 일정 저장
        try:
            scheduleDB = sqlite3.connect(r"./Data/schedule.sqlite", isolation_level=None)
            scheduleCURSOR = scheduleDB.cursor()
            try: schedule_lastSavedDataAt = scheduleCURSOR.execute("SELECT LastSavedDataAt FROM general").fetchone()[0]
            except: schedule_lastSavedDataAt = None
            scheduleDB.close()

            nowTime = datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%Y-%m-%d")

            if (nowTime != schedule_lastSavedDataAt):
                webhook_headers = {
                    "Content-Type": "application/json"
                }

                print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
                print("경기 일정 저장")

                webhook_data = {
                    "username": "OP.GG Esports Log",
                    "content": "``` ```\n>>> `({})`\n경기 일정 저장".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S"))
                }
                webhook_result = requests.post(webhook_url, json=webhook_data, headers=webhook_headers)
                if 200 <= webhook_result.status_code < 300: pass
                else: print(f'- [LOG] Not sent with {webhook_result.status_code}, response:\n{webhook_result.json()}')

                schedules = opgg.save_schedule()

                if schedules['error'] == False:

                    temp_originalScheduledAt = []
                    box_originalScheduledAt = []
                    for i in range(len(schedules['data'])):
                        temp_originalScheduledAt.append(schedules['data'][i]['originalScheduledAt'].replace("T", " ").split(".000Z")[0])
                        date_temp = datetime.datetime.strptime(temp_originalScheduledAt[i], "%Y-%m-%d %H:%M:%S")
                        date_delta = datetime.timedelta(hours=time_difference)
                        time = date_temp + date_delta
                        if time.strftime("%Y-%m-%d") == nowTime:
                            box_originalScheduledAt.append(time.strftime("%Y-%m-%d %H:%M:%S"))

                    temp_scheduledAt = []
                    box_scheduledAt = []
                    for i in range(len(schedules['data'])):
                        temp_scheduledAt.append(schedules['data'][i]['scheduledAt'].replace("T", " ").split(".000Z")[0])
                        date_temp = datetime.datetime.strptime(temp_scheduledAt[i], "%Y-%m-%d %H:%M:%S")
                        date_delta = datetime.timedelta(hours=time_difference)
                        time = date_temp + date_delta
                        if time.strftime("%Y-%m-%d") == nowTime:
                            box_scheduledAt.append(time.strftime("%Y-%m-%d %H:%M:%S"))

                    scheduleDB = sqlite3.connect(r"./Data/schedule.sqlite", isolation_level=None)
                    scheduleCURSOR = scheduleDB.cursor()
                    bettingDB = sqlite3.connect(r"./Data/betting.sqlite", isolation_level=None)
                    bettingCURSOR = bettingDB.cursor()

                    # DB 초기화
                    for i in range(16):
                        scheduleCURSOR.execute(f"DELETE FROM {leagues[i]['shortName']}")
                        scheduleCURSOR.execute(f"DELETE FROM general")
                    print("- Table Deleted.")

                    webhook_data = {
                        "username": "OP.GG Esports Log",
                        "content": "- Table Deleted."
                    }
                    webhook_result = requests.post(webhook_url, json=webhook_data, headers=webhook_headers)
                    if 200 <= webhook_result.status_code < 300: pass
                    else: print(f'- [LOG] Not sent with {webhook_result.status_code}, response:\n{webhook_result.json()}')

                    # 경기 데이터 저장
                    content_msg = ""
                    for i in range(len(box_scheduledAt)):
                        for j in range(16):
                            if schedules['data'][i]['tournament']['serie']['league']['shortName'] == leagues[j]['shortName']:
                                scheduleCURSOR.execute(f"INSERT INTO {leagues[j]['shortName']}(ID, TournamentID, Name, OriginalScheduledAt, ScheduledAt, Status) VALUES(?, ?, ?, ?, ?, ?)", (schedules['data'][i]['id'], schedules['data'][i]['tournamentId'], schedules['data'][i]['name'], schedules['data'][i]['originalScheduledAt'], schedules['data'][i]['scheduledAt'], schedules['data'][i]['status']))
                                bettingCURSOR.execute(f"INSERT INTO {leagues[j]['shortName']}(ID, TournamentID, Name, TotalBet, TotalPoint, HomeBet, HomePoint, AwayBet, AwayPoint) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", (schedules['data'][i]['id'], schedules['data'][i]['tournamentId'], schedules['data'][i]['name'], 0, 0, 0, 0, 0, 0))
                        print(f"- Saved match: [{schedules['data'][i]['tournament']['serie']['league']['shortName']}] {schedules['data'][i]['name']} ({schedules['data'][i]['id']})")

                        content_msg += f"\n- Saved match: `[{schedules['data'][i]['tournament']['serie']['league']['shortName']}] {schedules['data'][i]['name']} ({schedules['data'][i]['id']})`"

                    if content_msg == "": content_msg = "- No matches."

                    webhook_data = {
                        "username": "OP.GG Esports Log",
                        "content": content_msg
                    }
                    webhook_result = requests.post(webhook_url, json=webhook_data, headers=webhook_headers)
                    if 200 <= webhook_result.status_code < 300: pass
                    else: print(f'- [LOG] Not sent with {webhook_result.status_code}, response:\n{webhook_result.json()}')

                    scheduleCURSOR.execute(f"INSERT INTO general(LastSavedDataAt) VALUES(?)", (nowTime,))
                    scheduleDB.close()
                    bettingDB.close()

                else:
                    print(f"{schedules['code']}: {schedules['message']}")

        except Exception as error:
            print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
            print(traceback.format_exc())



def setup(bot):
    bot.add_cog(save_scheduleTASK(bot))
    print("save_schedule.py 로드 됨")
