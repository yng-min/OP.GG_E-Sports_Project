# -*- coding: utf-8 -*-

# 패키지 라이브러리 설정
import opgg
import asyncio
import discord
from discord.ext import commands, tasks
import datetime
import pytz
import traceback


class StatusEVENT(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.status_content = ""
        self.index = 0
        self.firstData = True

    @commands.Cog.listener()
    async def on_ready(self):
        self._status_TASK.start()

    @tasks.loop(seconds=10)
    async def _status_TASK(self):

        # 현재 시간
        time_nowDetail = datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%H:%M")
        # time_nowDetail = "00:00" # 테스트용

        try:
            if ("00:00" == time_nowDetail) or (self.firstData == True): # 매일 자정에 실행

                self.status_content = None
                self.firstData = False

                season_data = opgg.season_info("99") # LCK 시즌 통계 데이터

                if season_data['error'] == False:
                    self.status_content = season_data

        except Exception as error:
            print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
            print(traceback.format_exc())

        await asyncio.sleep(1)

        # length = f"{self.status_content['data']['baseStats']['length']}"
        # averageLength = f"{self.status_content['data']['baseStats']['averageLength'].__round__(1)}"
        # maxLength = f"리그에서 가장 긴 경기는 {self.status_content['data']['baseStats']['maxLength']}동안 진행됐답니다."
        # minLength = f"리그에서 가장 짧은 경기는 {self.status_content['data']['baseStats']['minLength']}만에 끝났대요!"
        guide = "'/가이드' 명령어를 이용해 보세요."
        description = "리그 통계를 토대로 여러 정보들을 알려드려요."
        try:
            kills = f"선수들은 서로 {self.status_content['data']['baseStats']['kills']:,}번 죽였대요. 😥"
            deaths = f"선수들은 총 {self.status_content['data']['baseStats']['deaths']:,}번 죽었어요. 우리 정글 왜 안 옴??"
            assists = f"선수들은 {self.status_content['data']['baseStats']['assists']:,}번 어시스트했어요. 늦게 오면 어시 없음!"
            baronKills = f"바론은 {self.status_content['data']['baseStats']['baronKills']:,}번 처치 당했어요."
            dragonKills = f"또, 드래곤은 {self.status_content['data']['baseStats']['dragonKills']:,}번 처치 당했대요."
            elderDragonKills = f"장로 드래곤을 두고 {self.status_content['data']['baseStats']['elderDragonKills']:,}번 전투를... <전리품: 장로 버프>"
            heraldKills = f"협곡의 전령은 {self.status_content['data']['baseStats']['heraldKills']:,}번 바위게 친구를 만나러 가다가 그만 사고를 당했대요. R.I.P"
            pentaKills = f"펜타킬은 {self.status_content['data']['baseStats']['pentaKills']:,}번 나왔어요. Legends Never Die 🎶"
            towerKills = f"모두 {self.status_content['data']['baseStats']['towerKills']:,}개의 포탑을 파괴했어요. 역시 타워 밀기 게임이네요"
        except Exception as error:
            print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
            print("status_TASK function error.")
            print(traceback.format_exc())
            print("*" * 10)
            print(self.status_content)

        status_msg = [guide, description, kills, deaths, assists, baronKills, dragonKills, elderDragonKills, heraldKills, pentaKills, towerKills]

        await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(status_msg[self.index]))
        if self.index >= (len(status_msg) - 1):
            self.index = 0
        else:
            self.index += 1



def setup(bot):
    print('status.py 로드 됨')
    bot.add_cog(StatusEVENT(bot))
