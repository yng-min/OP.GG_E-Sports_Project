# -*- coding: utf-8 -*-

# 패키지 라이브러리 설정
from discord.ext import commands
import sqlite3
import json
import datetime
import pytz
import os

# config.json Config 파일 불러오기
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

client_version = config['client_version']


class DatabaseSETUP(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):

        # bot.sqlite DB 파일 생성
        if not os.path.isfile(rf"./Data/bot.sqlite"):
            print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
            print("bot.sqlite DB 파일 생성 완료")
        botDB = sqlite3.connect(r"./Data/bot.sqlite", isolation_level=None)
        botCURSOR = botDB.cursor()
        botCURSOR.execute("""
            CREATE TABLE IF NOT EXISTS main(
            DBVersionUser INTEGER,
            DBVersionGuild INTEGER,
            ChannelAdmin INTEGER,
            ChannelLog INTEGER,
            ChannelEvent INTEGER,
            ChannelFeedback INTEGER
            )
        """)
        botCURSOR.execute("INSERT INTO main VALUES(?, ?, ?, ?, ?, ?)", (1, 1, 738313164965543946, 1003271459344498748, 999942267752169543, 1004826924599738509))
        botDB.close()


        # schedule.sqlite DB 파일 생성
        if not os.path.isfile(rf"./Data/schedule.sqlite"):
            print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
            print("schedule.sqlite DB 파일 생성 완료")
        scheduleDB = sqlite3.connect(r"./Data/schedule.sqlite", isolation_level=None)
        scheduleCURSOR = scheduleDB.cursor()
        scheduleCURSOR.execute(f"""
            CREATE TABLE IF NOT EXISTS general(
            LastSavedDataAt TEXT
            )
        """)

        for i in range(16):
            scheduleCURSOR.execute(f"""
                CREATE TABLE IF NOT EXISTS {leagues[i]['shortName']}(
                ID TEXT,
                TournamentID TEXT,
                Name TEXT,
                OriginalScheduledAt TEXT,
                ScheduledAt TEXT,
                Status TEXT
                )
            """)
        scheduleDB.close()


        # betting.sqlite DB 파일 생성
        if not os.path.isfile(rf"./Data/betting.sqlite"):
            print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
            print("betting.sqlite DB 파일 생성 완료")
        bettingDB = sqlite3.connect(r"./Data/betting.sqlite", isolation_level=None)
        bettingCURSOR = bettingDB.cursor()

        for i in range(16):
            bettingCURSOR.execute(f"""
                CREATE TABLE IF NOT EXISTS {leagues[i]['shortName']}(
                ID TEXT,
                TournamentID TEXT,
                Name TEXT,
                TotalBet INTEGER,
                TotalPoint INTEGER,
                HomeBet INTEGER,
                HomePoint INTEGER,
                AwayBet INTEGER,
                AwayPoint INTEGER
                )
            """)
        bettingDB.close()


        # # beta.sqlite DB 파일 생성
        # if os.path.isfile(rf"./Data/Beta/beta.sqlite"):
        #     betaDB = sqlite3.connect(r"./Data/Beta/beta.sqlite", isolation_level=None)
        #     betaCURSOR = betaDB.cursor()
        #     betaCURSOR.execute("""
        #         CREATE TABLE IF NOT EXISTS main(
        #         UserID INTEGER,
        #         GuildID INTEGER,
        #         Count INTEGER
        #         )
        #     """)
        #     print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
        #     print("beta.sqlite DB 파일 생성 완료")


        # # settingsDB = sqlite3.connect(r'./Data/settings.sqlite')
        # # settingsCURSOR = settingsDB.cursor()
        # # settingsCURSOR.execute("""
        # #     CREATE TABLE IF NOT EXISTS main(
        # #     X TEXT
        # #     )
        # # """) # settings.sqlite DB 파일 불러오기



def setup(bot):
    bot.add_cog(DatabaseSETUP(bot))
    print('setup_database.py 로드 됨')
