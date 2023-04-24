# -*- coding: utf-8 -*-

# 패키지 라이브러리 설정
import opgg
import discord
from discord.ext import commands
import sqlite3
import random
import json
import datetime
import pytz
import traceback
import os

from Extensions.Prediction.deposit import DepositPoint
from Extensions.Process.match import get_game_info_by_id

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
    botCURSOR.close()
    botDB.close()
except Exception as error:
    print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
    print(traceback.format_exc())

colorMap = config['colorMap']


class LinkButton(discord.ui.View):

    def __init__(self, url: str):
        super().__init__()
        self.add_item(discord.ui.Button(label="OP.GG E-Sports에서 보기", url=url))


class MatchCompleteTASK(commands.Cog):

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

        match_input = eval(ctx.content)

        match_data = opgg.match_completed(match_info=match_input)
        game_info = get_game_info_by_id(match_id=match_input['matchId'], match_set=match_input['set'])

        if (match_data['error'] == False) and (match_data['data']['match_type'] == "complete"):
            match_id = match_data['data']['match_id']
            match_title = f"{match_data['data']['team_1']} vs {match_data['data']['team_2']}"
            match_league = match_data['data']['match_league']

            print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
            print("경기 결과 알림 전송 중...")
            print(f"- Sending match: [{match_league}] {match_title} ({match_id})")

            try: # 셋업된 채널 불러오기
                scheduleURL = f"https://qwer.gg/ko/matches/{match_id}"

                box_league = []
                for i in range(16):
                    if leagues[i]['shortName'] == match_league:
                        box_league.append(f"{leagues[i]['shortName']}/{leagues[i]['region']}")

                scheduleDB = sqlite3.connect(r"./Database/schedule.sqlite", isolation_level=None)
                scheduleCURSOR = scheduleDB.cursor()
                for i in range(16):
                    try:
                        numberOfGames = scheduleCURSOR.execute(f"SELECT NumberOfGames FROM {leagues[i]['shortName']} WHERE ID = {match_data['data']['match_id']}").fetchone()[0]
                        scheduleCURSOR.execute(f"UPDATE {leagues[i]['shortName']} SET Status = ? WHERE ID = ?", (match_data['data']['match_type'], match_id))
                    except:
                        numberOfGames = None
                        pass
                scheduleDB.close()

                # 현재 시간
                time_nowDay = datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%Y-%m-%d")
                time_nowTime = datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("X%m월 X%d일").replace("X0", "").replace("X", "")

                bet_box = []

                for data_guild in os.listdir(r"./Database/Guild"):
                    if data_guild.endswith(".sqlite"):
                        guildDB = sqlite3.connect(rf"./Database/Guild/{data_guild}", isolation_level=None)
                        guildCURSOR = guildDB.cursor()
                        notice_answer = guildCURSOR.execute("SELECT NoticeCompleteAnswer FROM main").fetchone()[0]
                        channel_id = guildCURSOR.execute("SELECT NoticeChannelID FROM main").fetchone()[0]
                        # role_id = guildCURSOR.execute("SELECT NoticeRoleID FROM main").fetchone()[0]

                        leagueLCO = guildCURSOR.execute("SELECT LCO FROM league").fetchone()[0]
                        leaguePCS = guildCURSOR.execute("SELECT PCS FROM league").fetchone()[0]
                        leagueLLA = guildCURSOR.execute("SELECT LLA FROM league").fetchone()[0]
                        leagueLCS = guildCURSOR.execute("SELECT LCS FROM league").fetchone()[0]
                        leagueLEC = guildCURSOR.execute("SELECT LEC FROM league").fetchone()[0]
                        leagueVCS = guildCURSOR.execute("SELECT VCS FROM league").fetchone()[0]
                        leagueLCL = guildCURSOR.execute("SELECT LCL FROM league").fetchone()[0]
                        leagueLJL = guildCURSOR.execute("SELECT LJL FROM league").fetchone()[0]
                        leagueTCL = guildCURSOR.execute("SELECT TCL FROM league").fetchone()[0]
                        leagueCBLOL = guildCURSOR.execute("SELECT CBLOL FROM league").fetchone()[0]
                        leagueOPL = guildCURSOR.execute("SELECT OPL FROM league").fetchone()[0]
                        leagueWorlds = guildCURSOR.execute("SELECT Worlds FROM league").fetchone()[0]
                        leagueLMS = guildCURSOR.execute("SELECT LMS FROM league").fetchone()[0]
                        leagueLPL = guildCURSOR.execute("SELECT LPL FROM league").fetchone()[0]
                        leagueLCK = guildCURSOR.execute("SELECT LCK FROM league").fetchone()[0]
                        leagueMSI = guildCURSOR.execute("SELECT MSI FROM league").fetchone()[0]

                        guildDB.close()

                        if (channel_id) and (notice_answer == 1):
                            if ((box_league[0].split("/")[0] == "LCO") and (leagueLCO == 1)) or ((box_league[0].split("/")[0] == "PCS") and (leaguePCS == 1)) or ((box_league[0].split("/")[0] == "LLA") and (leagueLLA == 1)) or ((box_league[0].split("/")[0] == "LCS") and (leagueLCS == 1)) or ((box_league[0].split("/")[0] == "LEC") and (leagueLEC == 1)) or ((box_league[0].split("/")[0] == "VCS") and (leagueVCS == 1)) or ((box_league[0].split("/")[0] == "LCL") and (leagueLCL == 1)) or ((box_league[0].split("/")[0] == "LJL") and (leagueLJL == 1)) or ((box_league[0].split("/")[0] == "TCL") and (leagueTCL == 1)) or ((box_league[0].split("/")[0] == "CBLOL") and (leagueCBLOL == 1)) or ((box_league[0].split("/")[0] == "OPL") and (leagueOPL == 1)) or ((box_league[0].split("/")[0] == "Worlds") and (leagueWorlds == 1)) or ((box_league[0].split("/")[0] == "LMS") and (leagueLMS == 1)) or ((box_league[0].split("/")[0] == "LPL") and (leagueLPL == 1)) or ((box_league[0].split("/")[0] == "LCK") and (leagueLCK == 1)) or ((box_league[0].split("/")[0] == "MSI") and (leagueMSI == 1)):
                                # guild_notice = self.bot.get_guild(int(data_guild.split("_")[1].split(".")[0]))
                                channel_notice = self.bot.get_channel(channel_id)
                                # role_notice = discord.utils.get(guild_notice.roles, id=role_id)

                                msg_content = ""
                                # msg_content = f"{role_notice.mention}"
                                msg_title = f"> 📢 {time_nowTime} 경기 결과"
                                # msg_title = f"> 📢 {time_nowTime} 경기 결과 (테스트)"
                                msg_description = f"```{match_title} ({box_league[0]})```"
                                msg_team_1 = f"{match_title.split(' vs ')[0]} 팀 정보"
                                msg_team_2 = f"{match_title.split(' vs ')[1]} 팀 정보"
                                banner_image_url = random.choice(config['banner_image_url'])

                                if match_data['data']['dpm'] == "": match_data['data']['dpm'] = "-"
                                if match_data['data']['dtpm'] == "": match_data['data']['dtpm'] = "-"
                                if match_data['data']['gold'] == "": match_data['data']['gold'] = "-"
                                if match_data['data']['cs'] == "": match_data['data']['cs'] = "-"
                                if match_data['data']['firstBlood'] == "": match_data['data']['firstBlood'] = "-"
                                if match_data['data']['mvp'] == "": match_data['data']['mvp'] = "-"

                                if game_info['data']['finished'] == True:
                                    bettingDB = sqlite3.connect(rf"./Database/betting.sqlite", isolation_level=None)
                                    bettingCURSOR = bettingDB.cursor()

                                    box_matches = []
                                    box_match = []
                                    for i in range(16):
                                        result = bettingCURSOR.execute(f"SELECT * FROM {leagues[i]['shortName']}").fetchall()
                                        box_matches.append(result)
                                        if box_matches[i] != []:
                                            for j in range(len(result)):
                                                box_match.append(box_matches[i][j])

                                    bettingDB.close()

                                    data_bet = []
                                    for i in range(len(box_match)):
                                        if str(box_match[i][0]) == str(match_id):
                                            bet_box.append(box_match[i][4])
                                            bet_box.append(box_match[i][5])
                                            bet_box.append(box_match[i][7])
                                            data_bet.append(box_match[i][5])
                                            data_bet.append(box_match[i][6])
                                            data_bet.append(box_match[i][7])
                                            data_bet.append(box_match[i][8])

                                    try:
                                        team_user_1 = data_bet[0]
                                        team_user_2 = data_bet[2]
                                        team_point_1 = data_bet[1]
                                        team_point_2 = data_bet[3]

                                        if (match_data['data']['match_winner_shortName'] == match_title.split(' vs ')[0]):
                                            try: reward = (bet_box[0] / bet_box[1]).__round__()
                                            except ZeroDivisionError: reward = 0
                                        elif (match_data['data']['match_winner_shortName'] == match_title.split(' vs ')[1]):
                                            try: reward = (bet_box[0] / bet_box[2]).__round__()
                                            except ZeroDivisionError: reward = 0

                                        msg_user_1 = f"총 _**{team_user_1:,}**_명"
                                        msg_user_2 = f"총 _**{team_user_2:,}**_명"
                                        msg_point_1 = f"합계 _**{team_point_1:,}**_포인트"
                                        msg_point_2 = f"합계 _**{team_point_2:,}**_포인트"
                                        msg_reward = f"_**{reward:,}**_포인트"

                                        embed = discord.Embed(title=msg_title, description=msg_description, color=colorMap['red'])
                                        # embed.set_footer(text="Powered by QWER.GG", icon_url=self.bot.user.display_avatar.url)
                                        embed.set_image(url=banner_image_url)
                                        embed.add_field(name="\u200b", value=f"**> __{match_data['data']['match_winner_name']} ({match_data['data']['match_winner_shortName']})__ 승리 [{match_data['data']['match_set']}세트]**", inline=False)
                                        embed.add_field(name="MVP 선수", value=match_data['data']['mvp'], inline=True)
                                        embed.add_field(name="가한 피해량 1위", value=match_data['data']['dpm'], inline=True)
                                        embed.add_field(name="받은 피해량 1위", value=match_data['data']['dtpm'], inline=True)
                                        embed.add_field(name="획득한 골드 1위", value=match_data['data']['gold'], inline=True)
                                        embed.add_field(name="CS 1위", value=match_data['data']['cs'], inline=True)
                                        embed.add_field(name="선취점", value=match_data['data']['firstBlood'], inline=True)
                                        embed.add_field(name="\u200b", value=f"**> 리그 승부 예측 결과**", inline=False)
                                        embed.add_field(name=msg_team_1, value=f"{msg_user_1}\n{msg_point_1}", inline=True)
                                        embed.add_field(name=msg_team_2, value=f"{msg_user_2}\n{msg_point_2}", inline=True)
                                        embed.add_field(
                                            name="포인트 정산", value=f"__**{match_data['data']['match_winner_name']}**__ 팀에 베팅한 유저에게 각각 {msg_reward}가 지급됩니다.", inline=False)
                                        # await channel_notice.send(msg_content, embed=embed, view=LinkButton(scheduleURL))
                                        await channel_notice.send(embed=embed, view=LinkButton(scheduleURL))

                                    except:
                                        embed = discord.Embed(title=msg_title, description=msg_description, color=colorMap['red'])
                                        embed.set_footer(text="(Issue: 베팅 데이터를 불러올 수 없습니다.)", icon_url=self.bot.user.display_avatar.url)
                                        embed.set_image(url=banner_image_url)
                                        embed.add_field(name="\u200b", value=f"**> __{match_data['data']['match_winner_name']} ({match_data['data']['match_winner_shortName']})__ 승리 [{match_data['data']['match_set']}세트]**", inline=False)
                                        embed.add_field(name="MVP 선수", value=match_data['data']['mvp'], inline=True)
                                        embed.add_field(name="가한 피해량 1위", value=match_data['data']['dpm'], inline=True)
                                        embed.add_field(name="받은 피해량 1위", value=match_data['data']['dtpm'], inline=True)
                                        embed.add_field(name="획득한 골드 1위", value=match_data['data']['gold'], inline=True)
                                        embed.add_field(name="CS 1위", value=match_data['data']['cs'], inline=True)
                                        embed.add_field(name="선취점", value=match_data['data']['firstBlood'], inline=True)
                                        # await channel_notice.send(msg_content, embed=embed, view=LinkButton(scheduleURL))
                                        await channel_notice.send(embed=embed, view=LinkButton(scheduleURL))

                                        print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
                                        print(f"[{box_league[0]}] {match_title} ({match_id}) | 경기 베팅 데이터를 불러올 수 없습니다.")

                                else:
                                    embed = discord.Embed(title=msg_title, description=msg_description, color=colorMap['red'])
                                    # embed.set_footer(text="Powered by QWER.GG", icon_url=self.bot.user.display_avatar.url)
                                    embed.set_image(url=banner_image_url)
                                    embed.add_field(name="\u200b", value=f"**> __{match_data['data']['match_winner_name']} ({match_data['data']['match_winner_shortName']})__ 승리 [{match_data['data']['match_set']}세트]**", inline=False)
                                    embed.add_field(name="MVP 선수", value=match_data['data']['mvp'], inline=True)
                                    embed.add_field(name="가한 피해량 1위", value=match_data['data']['dpm'], inline=True)
                                    embed.add_field(name="받은 피해량 1위", value=match_data['data']['dtpm'], inline=True)
                                    embed.add_field(name="획득한 골드 1위", value=match_data['data']['gold'], inline=True)
                                    embed.add_field(name="CS 1위", value=match_data['data']['cs'], inline=True)
                                    embed.add_field(name="선취점", value=match_data['data']['firstBlood'], inline=True)
                                    # await channel_notice.send(msg_content, embed=embed, view=LinkButton(scheduleURL))
                                    await channel_notice.send(embed=embed, view=LinkButton(scheduleURL))

                DepositPoint.deposit_point(match_data=match_data, bet_box=bet_box)

            except Exception as error:
                print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
                print(traceback.format_exc())

            print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
            print("경기 결과 알림 전송 완료")

        elif match_data['error'] == True:
            print(f"{match_data['code']}: {match_data['message']}")



def setup(bot):
    bot.add_cog(MatchCompleteTASK(bot))
    print("match_complete.py 로드 됨")
