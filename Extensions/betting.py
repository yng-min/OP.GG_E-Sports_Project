# -*- coding: utf-8 -*-

# 패키지 라이브러리 설정
import discord
import sqlite3
import datetime
import pytz
import traceback
import os

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


class LinkButton(discord.ui.View):

    def __init__(self, url: str):
        super().__init__()
        self.add_item(discord.ui.Button(label="OP.GG Esports에서 보기", url=url))


class BettingButton(discord.ui.View):

    def __init__(self, bot, msg, url, matchID, team_1, team_2):
        super().__init__(timeout=900)
        self.bot = bot
        self.msg = msg
        self.url = url
        self.matchID = matchID
        self.team_1 = team_1
        self.team_2 = team_2
        self.add_item(discord.ui.Button(label="OP.GG Esports에서 보기", url=url, row=1))
        self.add_button()

    def add_button(self):
        home_team = discord.ui.Button(label=f"'{self.team_1}' 팀 예측하기", style=discord.ButtonStyle.blurple, custom_id=f"{self.matchID}/{self.team_1}", row=0)
        away_team = discord.ui.Button(label=f"'{self.team_2}' 팀 예측하기", style=discord.ButtonStyle.blurple, custom_id=f"{self.matchID}/{self.team_2}", row=0)

        async def callback_1(interaction: discord.Interaction):
            user = interaction.user

            if os.path.isfile(rf"./Data/User/user_{user.id}.sqlite"):
                userDB = sqlite3.connect(rf"./Data/User/user_{user.id}.sqlite", isolation_level=None)
                userCURSOR = userDB.cursor()
                userDATA = userCURSOR.execute(f"SELECT * FROM data WHERE UserID = '{user.id}'").fetchone()

                modal = BettingModal_1(self.bot, self.msg, self.url, self.matchID, self.team_1, self.team_2, userDATA[2], title=f"리그 승부 예측 ({self.team_1} vs {self.team_2})")
                await interaction.response.send_modal(modal)

            else:
                embed = discord.Embed(title="> ⛔ 리그 승부 예측 불가", description="서비스에 가입하셔야 이용할 수 있는 기능입니다.", color=colorMap['red'])
                return await interaction.response.send_message(embed=embed, ephemeral=True)

        async def callback_2(interaction: discord.Interaction):
            user = interaction.user

            if os.path.isfile(rf"./Data/User/user_{user.id}.sqlite"):
                userDB = sqlite3.connect(rf"./Data/User/user_{user.id}.sqlite", isolation_level=None)
                userCURSOR = userDB.cursor()
                userDATA = userCURSOR.execute(f"SELECT * FROM data WHERE UserID = '{user.id}'").fetchone()

                modal = BettingModal_2(self.bot, self.msg, self.url, self.matchID, self.team_1, self.team_2, userDATA[2], title=f"리그 승부 예측 ({self.team_1} vs {self.team_2})")
                await interaction.response.send_modal(modal)

            else:
                embed = discord.Embed(title="> ⛔ 리그 승부 예측 불가", description="서비스에 가입하셔야 이용할 수 있는 기능입니다.", color=colorMap['red'])
                return await interaction.response.send_message(embed=embed, ephemeral=True)

        home_team.callback = callback_1
        away_team.callback = callback_2

        self.add_item(home_team)
        self.add_item(away_team)

    async def on_timeout(self):

        try:
            for data_guild in os.listdir(r"./Data/Guild"):

                if data_guild.endswith(".sqlite"):
                    guildDB = sqlite3.connect(rf"./Data/Guild/{data_guild}", isolation_level=None)
                    guildCURSOR = guildDB.cursor()

                    role_id = guildCURSOR.execute("SELECT NoticeRoleID FROM main").fetchone()[0]
                    msg_content = f"<@&{role_id}>"

                    guildDB.close()

        except Exception as error:
            print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
            print(traceback.format_exc())

        await self.msg.edit(content=msg_content, view=DisabledButton(self.bot, self.msg, self.url, self.matchID, self.team_1, self.team_2))


class BettingModal_1(discord.ui.Modal):

    def __init__(self, bot, msg, url, matchID, team_1, team_2, data, *args, **kwargs) -> None:
        self.bot = bot
        self.msg = msg
        self.url = url
        self.matchID = matchID
        self.team_1 = team_1
        self.team_2 = team_2
        self.data = data
        super().__init__(*args, **kwargs)
        self.add_item(discord.ui.InputText(label="베팅할 포인트 (숫자로만 입력하세요.)", placeholder=f"'{self.team_1}' 팀 승부 예측에 베팅할 포인트를 입력해 주세요.\n(소지 중인 포인트 : {self.data}포인트)", style=discord.InputTextStyle.long, min_length=3, max_length=7))
        self.add_item(discord.ui.InputText(label="주의사항", placeholder="※ 유의할 점: 승부 예측은 리그 결과와 관계 없이 1세트 경기 결과만이 유효합니다.", style=discord.InputTextStyle.long, min_length=0, max_length=1, required=False))

    async def callback(self, interaction: discord.Interaction):
        user = interaction.user

        try:
            bet_point = int(self.children[0].value)
        except:
            embed = discord.Embed(title="> ⛔ 리그 승부 예측 불가", description=f"잘못된 포인트 값을 입력하였어요. 숫자로만 입력해 주세요. 😅", color=colorMap['red'])
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        try:
            if os.path.isfile(rf"./Data/User/user_{user.id}.sqlite"):
                userDB = sqlite3.connect(rf"./Data/User/user_{user.id}.sqlite", isolation_level=None)
                userCURSOR = userDB.cursor()

                scheduleDB = sqlite3.connect(rf"./Data/schedule.sqlite", isolation_level=None)
                scheduleCURSOR = scheduleDB.cursor()

                bettingDB = sqlite3.connect(rf"./Data/betting.sqlite", isolation_level=None)
                bettingCURSOR = bettingDB.cursor()

                try:
                    result = userCURSOR.execute(f"SELECT * FROM \"{self.matchID}\" WHERE UserID = {user.id}").fetchone()
                    if result[1]:
                        embed = discord.Embed(title="> ⛔ 리그 승부 예측 불가", description=f"이미 `{result[1]}` 팀에 승부를 예측하였어요.", color=colorMap['red'])
                        return await interaction.response.send_message(embed=embed, ephemeral=True)
                    else:
                        print(result)

                except:
                    resultData = userCURSOR.execute(f"SELECT * FROM data WHERE UserID = {user.id}").fetchone()

                    if resultData and (resultData[1] >= bet_point):

                        box_schedule = []
                        box_match = []
                        for i in range(16):
                            result = bettingCURSOR.execute(f"SELECT * FROM {leagues[i]['shortName']}").fetchall()
                            box_schedule.append(result)
                            if box_schedule[i] != []:
                                for j in range(len(result)):
                                    box_match.append(box_schedule[i][j])

                        for i in range(16):
                            for j in range(len(box_match)):
                                if str(self.matchID) == str(box_match[j][0]):
                                    bettingCURSOR.execute(f"UPDATE {leagues[i]['shortName']} SET TotalBet = ?, TotalPoint = ?, HomeBet = ?, HomePoint = ? WHERE ID = ?", ((box_match[j][3] + 1), (box_match[j][4] + bet_point), (box_match[j][5] + 1), (box_match[j][6] + bet_point), self.matchID))

                        userCURSOR.execute("UPDATE data SET Point = ?, TotalAnswer = ? WHERE UserID = ?", ((resultData[2] - bet_point), (resultData[3] + 1), user.id))

                        userCURSOR.execute(f"CREATE TABLE IF NOT EXISTS \"{self.matchID}\"(UserID INTERGER, Answer TEXT, BettingPoint INTERGER)") # 베팅 테이블 생성
                        userCURSOR.execute(f"INSERT INTO \"{self.matchID}\"(UserID, Answer, BettingPoint) VALUES(?, ?, ?)", (user.id, self.team_1, bet_point)) # 베팅 테이블 데이터 입력

                    elif not resultData or (resultData[1] <= bet_point):
                        embed = discord.Embed(title="> ⛔ 리그 승부 예측 불가", description=f"아쉽지만 베팅할 포인트가 모자라요. 😭", color=colorMap['red'])
                        return await interaction.response.send_message(embed=embed, ephemeral=True)

                    embed = discord.Embed(title="> 🎲 리그 승부 예측", description=f"`{self.team_1}` 팀에 _**{bet_point:,}**_포인트를 베팅하였습니다. 행운을 빌죠! 🍀", color=colorMap['red'])
                    embed.set_footer(text=f"잔여 포인트 : {(resultData[2] - bet_point):,}포인트")
                    await interaction.response.send_message(embed=embed, ephemeral=True)

                userDB.close()
                scheduleDB.close()

            else:
                embed = discord.Embed(title="> ⛔ 리그 승부 예측 불가", description="서비스에 가입하셔야 이용할 수 있는 기능입니다.", color=colorMap['red'])
                return await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as error:
            print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
            print(traceback.format_exc())
            embed = discord.Embed(title="> ⚠️ 리그 승부 예측 실패", description=f"아래의 오류로 인해 승부 예측에 실패했어요. 해당 문제가 지속된다면 개발자에게 문의해주세요.\n`{error}`", color=colorMap['red'])
            return await interaction.response.send_message(embed=embed, ephemeral=True)


class BettingModal_2(discord.ui.Modal):

    def __init__(self, bot, msg, url, matchID, team_1, team_2, data, *args, **kwargs) -> None:
        self.bot = bot
        self.msg = msg
        self.url = url
        self.matchID = matchID
        self.team_1 = team_1
        self.team_2 = team_2
        self.data = data
        super().__init__(*args, **kwargs)
        self.add_item(discord.ui.InputText(label="베팅할 포인트 (숫자로만 입력하세요.)", placeholder=f"'{self.team_2}' 팀 승부 예측에 베팅할 포인트를 입력해 주세요.\n(소지 중인 포인트 : {self.data}포인트)", style=discord.InputTextStyle.long, min_length=3, max_length=7))
        self.add_item(discord.ui.InputText(label="주의사항", placeholder="※ 유의할 점: 승부 예측은 리그 결과와 관계 없이 1세트 경기 결과만이 유효합니다.", style=discord.InputTextStyle.long, min_length=0, max_length=1, required=False))

    async def callback(self, interaction: discord.Interaction):
        user = interaction.user

        try:
            bet_point = int(self.children[0].value)
        except:
            embed = discord.Embed(title="> ⛔ 리그 승부 예측 불가", description=f"잘못된 포인트 값을 입력하였어요. 숫자로만 입력해 주세요. 😅", color=colorMap['red'])
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        try:
            if os.path.isfile(rf"./Data/User/user_{user.id}.sqlite"):
                userDB = sqlite3.connect(rf"./Data/User/user_{user.id}.sqlite", isolation_level=None)
                userCURSOR = userDB.cursor()

                bettingDB = sqlite3.connect(rf"./Data/betting.sqlite", isolation_level=None)
                bettingCURSOR = bettingDB.cursor()

                try:
                    result = userCURSOR.execute(f"SELECT * FROM \"{self.matchID}\" WHERE UserID = {user.id}").fetchone()
                    if result[1]:
                        embed = discord.Embed(title="> ⛔ 리그 승부 예측 불가", description=f"이미 `{result[1]}` 팀에 승부를 예측하였어요.", color=colorMap['red'])
                        return await interaction.response.send_message(embed=embed, ephemeral=True)
                    else:
                        print(result)

                except:
                    resultData = userCURSOR.execute(f"SELECT * FROM data WHERE UserID = {user.id}").fetchone()

                    if resultData and (resultData[1] >= bet_point):

                        box_schedule = []
                        box_match = []
                        for i in range(16):
                            result = bettingCURSOR.execute(f"SELECT * FROM {leagues[i]['shortName']}").fetchall()
                            box_schedule.append(result)
                            if box_schedule[i] != []:
                                for j in range(len(result)):
                                    box_match.append(box_schedule[i][j])

                        for i in range(16):
                            for j in range(len(box_match)):
                                if str(self.matchID) == str(box_match[j][0]):
                                    bettingCURSOR.execute(f"UPDATE {leagues[i]['shortName']} SET TotalBet = ?, TotalPoint = ?, AwayBet = ?, AwayPoint = ? WHERE ID = ?", ((box_match[j][3] + 1), (box_match[j][4] + bet_point), (box_match[j][7] + 1), (box_match[j][8] + bet_point), self.matchID))

                        userCURSOR.execute("UPDATE data SET Point = ?, TotalAnswer = ? WHERE UserID = ?", ((resultData[2] - bet_point), (resultData[3] + 1), user.id))

                        userCURSOR.execute(f"CREATE TABLE IF NOT EXISTS \"{self.matchID}\"(UserID INTERGER, Answer TEXT, BettingPoint INTERGER)") # 베팅 테이블 생성
                        userCURSOR.execute(f"INSERT INTO \"{self.matchID}\"(UserID, Answer, BettingPoint) VALUES(?, ?, ?)", (user.id, self.team_2, bet_point)) # 베팅 테이블 데이터 입력

                    elif not resultData or (resultData[1] <= bet_point):
                        embed = discord.Embed(title="> ⛔ 리그 승부 예측 불가", description=f"아쉽지만 베팅할 포인트가 모자라요. 😭", color=colorMap['red'])
                        return await interaction.response.send_message(embed=embed, ephemeral=True)

                    embed = discord.Embed(title="> 🎲 리그 승부 예측", description=f"`{self.team_2}` 팀에 _**{bet_point:,}**_포인트를 베팅하였습니다. 행운을 빌죠! 🍀", color=colorMap['red'])
                    embed.set_footer(text=f"잔여 포인트 : {(resultData[2] - bet_point):,}포인트")
                    await interaction.response.send_message(embed=embed, ephemeral=True)

                userDB.close()
                bettingDB.close()

            else:
                embed = discord.Embed(title="> ⛔ 리그 승부 예측 불가", description="서비스에 가입하셔야 이용할 수 있는 기능입니다.", color=colorMap['red'])
                return await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as error:
            print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
            print(traceback.format_exc())
            embed = discord.Embed(title="> ⚠️ 리그 승부 예측 실패", description=f"아래의 오류로 인해 승부 예측에 실패했어요. 해당 문제가 지속된다면 개발자에게 문의해주세요.\n`{error}`", color=colorMap['red'])
            return await interaction.response.send_message(embed=embed, ephemeral=True)


class DisabledButton(discord.ui.View):

    def __init__(self, bot, msg, url, matchID, team_1, team_2):
        super().__init__(timeout=None)
        self.bot = bot
        self.msg = msg
        self.matchID = matchID
        self.team_1 = team_1
        self.team_2 = team_2
        self.add_item(discord.ui.Button(label=f"'{self.team_1}' 팀 예측하기", style=discord.ButtonStyle.blurple, custom_id=f"{self.matchID}/{self.team_1}", disabled=True, row=0))
        self.add_item(discord.ui.Button(label="OP.GG Esports에서 보기", url=url, row=1))
        self.add_item(discord.ui.Button(label=f"'{self.team_2}' 팀 예측하기", style=discord.ButtonStyle.blurple, custom_id=f"{self.matchID}/{self.team_2}", disabled=True, row=0))
