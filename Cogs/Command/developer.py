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

id_owner = config['id_owner']
prefix_developer = config['prefix_developer']
time_difference = config['time_difference']
webhook_url = config['webhook_url']
colorMap = config['colorMap']


class DeveloperCMD(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="모듈로드", aliases=["로드", "load"])
    async def _load(self, ctx, *, module: str):

        if ctx.author.id != id_owner:
            return await ctx.send("> ⛔ 이 명령어는 개발자 전용 명령어입니다.")

        if module is None:
            return await ctx.send("> ⚠️ 로드할 모듈을 입력해주세요.")

        # module = module.lower()

        try:
            # print(f"- Loaded: Cogs.{module}")
            self.bot.load_extension(f"Cogs.{module}")

        except Exception as error:
            print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
            print(traceback.format_exc())
            await ctx.send(f"> ⚠️ 알 수 없는 오류로 인해 모듈을 불러오지 못했습니다.\nERROR: `{error}`")

        else:
            try: await ctx.message.delete()
            except discord.Forbidden: pass # missing permissions
            await ctx.send(f"> ✅ 성공적으로 `{module}` 모듈을 불러왔습니다.", delete_after=5)

    @commands.command(name="모듈언로드", aliases=["언로드", "unload"])
    async def _unload(self, ctx, *, module: str):

        if ctx.author.id != id_owner:
            return await ctx.send("> ⛔ 이 명령어는 개발자 전용 명령어입니다.")

        if module is None:
            return await ctx.send("> ⚠️ 언로드할 모듈을 입력해주세요.")

        # module = module.lower()

        try:
            # print(f"- Unloaded: Cogs.{module}")
            self.bot.unload_extension(f"Cogs.{module}")

        except Exception as error:
            print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
            print(traceback.format_exc())
            await ctx.send(f"> ⚠️ 알 수 없는 오류로 인해 모듈을 불러오지 못했습니다.\nERROR: `{error}`")

        else:
            try: await ctx.message.delete()
            except discord.Forbidden: pass # missing permissions
            await ctx.send(f"> ✅ 성공적으로 `{module}` 모듈을 내보냈습니다.", delete_after=5)

    @commands.command(name="모듈리로드", aliases=["리로드", "reload"])
    async def _reload(self, ctx, *, module: str):

        if ctx.author.id != id_owner:
            return await ctx.send("> ⛔ 이 명령어는 개발자 전용 명령어입니다.")

        if module is None:
            return await ctx.send("> ⚠️ 리로드할 모듈을 입력해주세요.")

        # module = module.lower()

        try:
            if module == ".":
                for cog_directory in os.listdir(r"./Cogs"):
                    for cog_files in os.listdir(r"./Cogs/" + cog_directory):
                        if cog_files.endswith(".py"):
                            # print(f"- Reloaded: Cogs.{cog_directory}.{cog_files}")
                            self.bot.reload_extension(f"Cogs.{cog_directory}.{cog_files[:-3]}")

            else:
                # print(f"- Reloaded: Cogs.{module}")
                self.bot.reload_extension(f"Cogs.{module}")

        except Exception as error:
            print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
            print(traceback.format_exc())
            await ctx.send(f"> ⚠️ 알 수 없는 오류로 인해 모듈을 불러오지 못했습니다.\nERROR: `{error}`")

        else:
            try: await ctx.message.delete()
            except discord.Forbidden: pass # missing permissions
            await ctx.send(f"> ✅ 성공적으로 `{module}` 모듈을 불러왔습니다.", delete_after=5)

    @commands.command(name="일정저장", aliases=["save-schedule"])
    async def _developer_save_schedule(self, ctx):

        if ctx.author.id != id_owner:
            embed = discord.Embed(title="", description="> ⛔ 해당 명령어는 개발자 전용 명령어입니다.", color=colorMap['red'])
            return await ctx.reply(embed=embed, mention_author=False)

        # 경기 일정 저장
        try:
            scheduleDB = sqlite3.connect(r"./Database/schedule.sqlite", isolation_level=None)
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

                    scheduleDB = sqlite3.connect(r"./Database/schedule.sqlite", isolation_level=None)
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
