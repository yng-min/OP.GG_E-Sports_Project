# -*- coding: utf-8 -*-

# 패키지 라이브러리 설정
import opgg
import discord
from discord.ext import commands
import sqlite3
import json
import datetime
import pytz
import traceback
import os
import requests

# config.json Config 파일 불러오기
try:
    with open(r"./config.json", "rt", encoding="UTF8") as configJson:
        config = json.load(configJson)
except:
    print("config.json이 로드되지 않음")

id_owner = config['id_owner']
prefix_developer = config['prefix_developer']
time_difference = config['time_difference']
webhook_url = config['webhook_url']
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
colorMap = {
    "default": 0x2F3136,
    "red": 0xff4438,
    "green": 0x90ee90
}


class DeveloperCMD(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="모듈로드", aliases=['로드'])
    async def _load(self, ctx, *, module: str):

        if ctx.author.id != id_owner:
            return await ctx.send("> ⛔ 이 명령어는 개발자 전용 명령어입니다.")

        if module is None:
            return await ctx.send("> ⚠️ 로드할 모듈을 입력해주세요.")

        # module = module.lower()

        try:
            self.bot.load_extension(f"Cogs.{module}")

        except Exception as error:
            print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
            print(traceback.format_exc())
            await ctx.send(f"> ⚠️ 알 수 없는 오류로 인해 모듈을 불러오지 못했습니다.\nERROR: `{error}`")

        else:
            await ctx.message.delete()
            await ctx.send(f"> ✅ 성공적으로 `{module}` 모듈을 불러왔습니다.", delete_after=5)

    @commands.command(name="모듈언로드", aliases=['언로드'])
    async def _unload(self, ctx, *, module: str):

        if ctx.author.id != id_owner:
            return await ctx.send("> ⛔ 이 명령어는 개발자 전용 명령어입니다.")

        if module is None:
            return await ctx.send("> ⚠️ 언로드할 모듈을 입력해주세요.")

        # module = module.lower()

        try:
            self.bot.unload_extension(f"Cogs.{module}")

        except Exception as error:
            print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
            print(traceback.format_exc())
            await ctx.send(f"> ⚠️ 알 수 없는 오류로 인해 모듈을 불러오지 못했습니다.\nERROR: `{error}`")

        else:
            await ctx.message.delete()
            await ctx.send(f"> ✅ 성공적으로 `{module}` 모듈을 내보냈습니다.", delete_after=5)

    @commands.command(name="모듈리로드", aliases=['리로드'])
    async def _reload(self, ctx, *, module: str):

        if ctx.author.id != id_owner:
            return await ctx.send("> ⛔ 이 명령어는 개발자 전용 명령어입니다.")

        if module is None:
            return await ctx.send("> ⚠️ 리로드할 모듈을 입력해주세요.")

        # module = module.lower()

        try:
            if module == ".":
                for cog_files in os.listdir(r"./Cogs"):
                    if cog_files.endswith(".py"):
                        self.bot.reload_extension("Cogs." + cog_files[:-3])

            else:
                self.bot.reload_extension(f"Cogs.{module}")

        except Exception as error:
            print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
            print(traceback.format_exc())
            await ctx.send(f"> ⚠️ 알 수 없는 오류로 인해 모듈을 불러오지 못했습니다.\nERROR: `{error}`")

        else:
            await ctx.message.delete()
            await ctx.send(f"> ✅ 성공적으로 `{module}` 모듈을 불러왔습니다.", delete_after=5)

    @commands.command(name="일정저장", aliases=['save-schedule'])
    async def _developer_save_schedule(self, ctx):

        if ctx.author.id != id_owner:
            embed = discord.Embed(title="", description="> ⛔ 해당 명령어는 개발자 전용 명령어입니다.", color=colorMap['red'])
            return await ctx.reply(embed=embed, mention_author=False)

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

                    # DB 초기화
                    for i in range(16):
                        scheduleCURSOR.execute(f"DELETE FROM {leagues[i]['shortName']}")
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
                            try: match_name = schedules['data'][i]['name'].split(': ')[1]
                            except: match_name = schedules['data'][i]['name']
                            if schedules['data'][i]['tournament']['serie']['league']['shortName'] == leagues[j]['shortName']:
                                scheduleCURSOR.execute(f"INSERT INTO {leagues[j]['shortName']}(ID, TournamentID, Name, OriginalScheduledAt, ScheduledAt, Status) VALUES(?, ?, ?, ?, ?, ?)", (schedules['data'][i]['id'], schedules['data'][i]['tournamentId'], match_name, box_originalScheduledAt[i], box_scheduledAt[i], schedules['data'][i]['status']))
                        print(f"- Saved match: [{schedules['data'][i]['tournament']['serie']['league']['shortName']}] {match_name} ({schedules['data'][i]['id']})")

                        content_msg += f"\n- Saved match: `[{schedules['data'][i]['tournament']['serie']['league']['shortName']}] {match_name} ({schedules['data'][i]['id']})`"

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

                else:
                    print(f"{schedules['code']}: {schedules['message']}")

        except Exception as error:
            print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
            print(traceback.format_exc())



def setup(bot):
    bot.add_cog(DeveloperCMD(bot))
    print("developer.py 로드 됨")
