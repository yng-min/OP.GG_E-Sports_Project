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

# config.json Config 파일 불러오기
try:
    with open(r"./config.json", "rt", encoding="UTF8") as configJson:
        config = json.load(configJson)
except:
    print("config.json이 로드되지 않음")

banner_image_url = config['banner_image_url']
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
    "red": 0xf60c50,
    "green": 0x90ee90
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


class LinkButton(discord.ui.View):

    def __init__(self, url: str):
        super().__init__()
        self.add_item(discord.ui.Button(label="OP.GG Esports에서 보기", url=url))


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

        match_data = opgg.match_completed(match_info=eval(ctx.content))

        if (match_data['error'] == False) and (match_data['data']['match_type'] == "complete"):
            print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
            print("경기 결과 알림 전송 중...")

            try: # 셋업된 채널 불러오기
                scheduleURL = f"https://qwer.gg/ko/matches/{match_data['data']['match_id']}"

                box_league = []
                for i in range(16):
                    if leagues[i]['shortName'] == match_data['data']['match_league']:
                        box_league.append(f"{leagues[i]['shortName']}/{leagues[i]['region']}")

                scheduleDB = sqlite3.connect(r"./Data/schedule.sqlite", isolation_level=None)
                scheduleCURSOR = scheduleDB.cursor()
                for i in range(16):
                    try: scheduleCURSOR.execute(f"UPDATE {leagues[i]['shortName']} SET Status = ? WHERE ID = ?", (match_data['data']['match_type'], match_data['data']['match_id']))
                    except: pass

                # 현재 시간
                time_nowDay = datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%Y-%m-%d")
                time_nowTime = datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("X%m월 X%d일").replace("X0", "").replace("X", "")

                # bet_box = []

                for data_guild in os.listdir(r"./Data/Guild"):

                    if data_guild.endswith(".sqlite"):
                        guildDB = sqlite3.connect(rf"./Data/Guild/{data_guild}", isolation_level=None)
                        guildCURSOR = guildDB.cursor()
                        notice_answer = guildCURSOR.execute("SELECT NoticeCompleteAnswer FROM main").fetchone()[0]
                        channel_id = guildCURSOR.execute("SELECT NoticeChannelID FROM main").fetchone()[0]
                        role_id = guildCURSOR.execute("SELECT NoticeRoleID FROM main").fetchone()[0]

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

                        guildCURSOR.close()
                        guildDB.close()

                        if (channel_id) and (notice_answer == 1):
                            channel_notice = self.bot.get_channel(channel_id)

                            if ((box_league[0].split("/")[0] == "LCO") and (leagueLCO == 1)) or ((box_league[0].split("/")[0] == "PCS") and (leaguePCS == 1)) or ((box_league[0].split("/")[0] == "LLA") and (leagueLLA == 1)) or ((box_league[0].split("/")[0] == "LCS") and (leagueLCS == 1)) or ((box_league[0].split("/")[0] == "LEC") and (leagueLEC == 1)) or ((box_league[0].split("/")[0] == "VCS") and (leagueVCS == 1)) or ((box_league[0].split("/")[0] == "LCL") and (leagueLCL == 1)) or ((box_league[0].split("/")[0] == "LJL") and (leagueLJL == 1)) or ((box_league[0].split("/")[0] == "TCL") and (leagueTCL == 1)) or ((box_league[0].split("/")[0] == "CBLOL") and (leagueCBLOL == 1)) or ((box_league[0].split("/")[0] == "OPL") and (leagueOPL == 1)) or ((box_league[0].split("/")[0] == "Worlds") and (leagueWorlds == 1)) or ((box_league[0].split("/")[0] == "LMS") and (leagueLMS == 1)) or ((box_league[0].split("/")[0] == "LPL") and (leagueLPL == 1)) or ((box_league[0].split("/")[0] == "LCK") and (leagueLCK == 1)) or ((box_league[0].split("/")[0] == "MSI") and (leagueMSI == 1)):

                                match_name = f"{match_data['data']['team_1']} vs {match_data['data']['team_2']}"

                                msg_content = f"<@&{role_id}>"
                                msg_title = f"> 📢 {time_nowTime} 경기 결과"
                                # msg_title = f"> 📢 {time_nowTime} 경기 결과 (테스트)"
                                msg_description = f"```{match_name} ({box_league[0]})```"
                                msg_team_1 = f"{match_name.split(' vs ')[0]} 팀 정보"
                                msg_team_2 = f"{match_name.split(' vs ')[1]} 팀 정보"

                                if match_data['data']['dpm'] == "": match_data['data']['dpm'] = "-"
                                if match_data['data']['dtpm'] == "": match_data['data']['dtpm'] = "-"
                                if match_data['data']['gold'] == "": match_data['data']['gold'] = "-"
                                if match_data['data']['cs'] == "": match_data['data']['cs'] = "-"
                                if match_data['data']['firstBlood'] == "": match_data['data']['firstBlood'] = "-"
                                if match_data['data']['mvp'] == "": match_data['data']['mvp'] = "-"

                                # if match_data['data']['match_set'] == 1:
                                #     bettingDB = sqlite3.connect(rf"./Data/betting.sqlite", isolation_level=None)
                                #     bettingCURSOR = bettingDB.cursor()

                                #     box_matches = []
                                #     box_match = []
                                #     for i in range(16):
                                #         result = bettingCURSOR.execute(f"SELECT * FROM {leagues[i]['shortName']}").fetchall()
                                #         box_matches.append(result)
                                #         if box_matches[i] != []:
                                #             for j in range(len(result)):
                                #                 box_match.append(box_matches[i][j])

                                #     bettingDB.close()

                                #     data_bet = []
                                #     for i in range(len(box_match)):
                                #         if str(box_match[i][0]) == str(match_data['data']['matchId']):
                                #             bet_box.append(box_match[i][4])
                                #             bet_box.append(box_match[i][5])
                                #             bet_box.append(box_match[i][7])
                                #             data_bet.append(box_match[i][5])
                                #             data_bet.append(box_match[i][6])
                                #             data_bet.append(box_match[i][7])
                                #             data_bet.append(box_match[i][8])

                                #     try:
                                #         team_user_1 = data_bet[0]
                                #         team_user_2 = data_bet[2]
                                #         team_point_1 = data_bet[1]
                                #         team_point_2 = data_bet[3]

                                #         try: match_name = match_data['data']['title'].split(': ')[1]
                                #         except: match_name = match_data['data']['title']

                                #         if (match_data['data']['winner'] == match_name.split(' vs ')[0]):
                                #             try: reward = (bet_box[0] / bet_box[1]).__round__()
                                #             except ZeroDivisionError: reward = 0
                                #         elif (match_data['data']['winner'] == match_name.split(' vs ')[1]):
                                #             try: reward = (bet_box[0] / bet_box[2]).__round__()
                                #             except ZeroDivisionError: reward = 0

                                #         msg_user_1 = f"총 _**{team_user_1:,}**_명"
                                #         msg_user_2 = f"총 _**{team_user_2:,}**_명"
                                #         msg_point_1 = f"합계 _**{team_point_1:,}**_포인트"
                                #         msg_point_2 = f"합계 _**{team_point_2:,}**_포인트"
                                #         msg_reward = f"_**{reward:,}**_포인트"

                                #         embed = discord.Embed(title=msg_title, description=msg_description, color=colorMap['red'])
                                #         # embed.set_footer(text="Powered by QWER.GG", icon_url=self.bot.user.display_avatar.url)
                                #         embed.set_image(url=banner_image_url)
                                #         embed.add_field(name="\u200b", value=f"**> __{match_data['data']['winnerName']} ({match_data['data']['winner']})__ 승리 [{match_data['data']['set']}세트]**", inline=False)
                                #         embed.add_field(name="MVP 선수", value=match_data['data']['mvp'], inline=True)
                                #         embed.add_field(name="가한 피해량 1위", value=match_data['data']['dpm'], inline=True)
                                #         embed.add_field(name="받은 피해량 1위", value=match_data['data']['dtpm'], inline=True)
                                #         embed.add_field(name="획득한 골드 1위", value=match_data['data']['gold'], inline=True)
                                #         embed.add_field(name="CS 1위", value=match_data['data']['cs'], inline=True)
                                #         embed.add_field(name="선취점", value=match_data['data']['firstBlood'], inline=True)
                                #         embed.add_field(name="\u200b", value=f"**> 리그 승부 예측 결과**", inline=False)
                                #         embed.add_field(name=msg_team_1, value=f"{msg_user_1}\n{msg_point_1}", inline=True)
                                #         embed.add_field(name=msg_team_2, value=f"{msg_user_2}\n{msg_point_2}", inline=True)
                                #         embed.add_field(name="포인트 정산", value=f"__**{match_data['data']['winner']}**__ 팀에 베팅한 유저에게 각각 {msg_reward}가 지급됩니다.", inline=False)
                                #         await channel_notice.send(msg_content, embed=embed, view=LinkButton(scheduleURL))

                                #     except:
                                #         embed = discord.Embed(title=msg_title, description=msg_description, color=colorMap['red'])
                                #         embed.set_footer(text="(Error: 베팅 데이터를 불러올 수 없습니다.)", icon_url=self.bot.user.display_avatar.url)
                                #         embed.set_image(url=banner_image_url)
                                #         embed.add_field(name="\u200b", value=f"**> __{match_data['data']['winnerName']} ({match_data['data']['winner']})__ 승리 [{match_data['data']['set']}세트]**", inline=False)
                                #         embed.add_field(name="MVP 선수", value=match_data['data']['mvp'], inline=True)
                                #         embed.add_field(name="가한 피해량 1위", value=match_data['data']['dpm'], inline=True)
                                #         embed.add_field(name="받은 피해량 1위", value=match_data['data']['dtpm'], inline=True)
                                #         embed.add_field(name="획득한 골드 1위", value=match_data['data']['gold'], inline=True)
                                #         embed.add_field(name="CS 1위", value=match_data['data']['cs'], inline=True)
                                #         embed.add_field(name="선취점", value=match_data['data']['firstBlood'], inline=True)
                                #         await channel_notice.send(msg_content, embed=embed, view=LinkButton(scheduleURL))

                                #         print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
                                #         print("경기 베팅 데이터를 불러올 수 없습니다.")

                                else:
                                    banner_image_url = random.choice(config['banner_image_url'])

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
                                    await channel_notice.send(msg_content, embed=embed, view=LinkButton(scheduleURL))

                # if match_data['data']['set'] == 1:
                #     for data_user in os.listdir(r"./Data/User"):
                #         try: match_name = match_data['data']['title'].split(': ')[1]
                #         except: match_name = match_data['data']['title']

                #         if data_user.endswith(".sqlite"):
                #             userID = int(data_user.replace("user_", "").split(".")[0])

                #             userDB = sqlite3.connect(rf"./Data/User/{data_user}", isolation_level=None)
                #             userCURSOR = userDB.cursor()

                #             try:
                #                 betting_result = userCURSOR.execute(f"SELECT * FROM \"{match_data['data']['matchId']}\"").fetchone()
                #                 result = userCURSOR.execute(f"SELECT * FROM data WHERE UserID = {userID}").fetchone()
                #                 userCURSOR.execute(f"DROP TABLE \"{match_data['data']['matchId']}\"")

                #                 if (betting_result[1] == match_data['data']['winner']):
                #                     if (betting_result[1] == match_name.split(' vs ')[0]): reward = (bet_box[0] / bet_box[1]).__round__()
                #                     elif (betting_result[1] == match_name.split(' vs ')[1]): reward = (bet_box[0] / bet_box[2]).__round__()
                #                     # userCURSOR.execute("UPDATE data SET TotalPoint = ?, Point = ?, CorrectAnswer = ? WHERE UserID = ?", ((result[1] + reward), (result[2] + betting_result[2] + reward), (result[4] + 1), userID))
                #                     userCURSOR.execute("UPDATE data SET TotalPoint = ?, Point = ?, CorrectAnswer = ? WHERE UserID = ?", ((result[1] + reward), (result[2] + reward), (result[4] + 1), userID))

                #                 else:
                #                     userCURSOR.execute("UPDATE data SET WrongAnswer = ? WHERE UserID = ?", ((result[5] + 1), userID))
                #             except:
                #                 pass

                #             userDB.close()

                # else:
                #     pass

            except Exception as error:
                print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
                print(traceback.format_exc())

            # if match_data['data']['set'] == 1:
            #     bettingDB = sqlite3.connect(rf"./Data/betting.sqlite", isolation_level=None)
            #     bettingCURSOR = bettingDB.cursor()

            #     box_matches = []
            #     box_match = []
            #     for i in range(16):
            #         result = bettingCURSOR.execute(f"SELECT * FROM {leagues[i]['shortName']}").fetchall()
            #         try: bettingCURSOR.execute(f"DELETE FROM {leagues[i]['shortName']} WHERE ID = '{match_data['data']['matchId']}'")
            #         except:
            #             pass
            #             # print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
            #             # print(traceback.format_exc())

            #     bettingDB.close()

            print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
            print("경기 결과 알림 전송 완료")

        else:
            print(f"{match_data['code']}: {match_data['message']}")



def setup(bot):
    bot.add_cog(MatchCompleteTASK(bot))
    print("match_complete.py 로드 됨")
