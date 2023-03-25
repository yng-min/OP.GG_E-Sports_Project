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

client_version = config['client_version']
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


class DatabaseSETUP(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):

        # bot.sqlite DB 파일 생성
        if not os.path.isfile(rf"./Data/bot.sqlite"):
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
            # botCURSOR.execute("INSERT INTO main VALUES(?, ?, ?, ?, ?, ?)", (1, 1, 738313164965543946, 1003271459344498748, 999942267752169543, 1004826924599738509))
            print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
            print("bot.sqlite DB 파일 생성 완료")


        # schedule.sqlite DB 파일 생성
        if not os.path.isfile(rf"./Data/schedule.sqlite"):
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
            print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
            print("schedule.sqlite DB 파일 생성 완료")


        # betting.sqlite DB 파일 생성
        if not os.path.isfile(rf"./Data/betting.sqlite"):
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
            print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
            print("betting.sqlite DB 파일 생성 완료")


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
