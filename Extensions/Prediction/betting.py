# -*- coding: utf-8 -*-

# 패키지 라이브러리 설정
import discord
import sqlite3
import json
import datetime
import pytz
import traceback
import os

# config.json 파일 불러오기
try:
    with open(r"./config.json", "rt", encoding="UTF8") as configJson:
        config = json.load(configJson)
except: print("config.json이 로드되지 않음")

# league.json 파일 불러오기
try:
    with open(r"./league.json", "rt", encoding="UTF8") as leagueJson:
        leagues = json.load(leagueJson)['leagues']
except: print("league.json이 로드되지 않음")

colorMap = config['colorMap']


class LinkButton(discord.ui.View):

    def __init__(self, url: str):
        super().__init__()
        self.add_item(discord.ui.Button(label="OP.GG E-Sports에서 보기", url=url))


class BettingButton(discord.ui.View):

    def __init__(self, bot, msg, url, match_id, team_1, team_2):
        super().__init__(timeout=900)
        self.bot = bot
        self.msg = msg
        self.url = url
        self.match_id = match_id
        self.team_1 = team_1
        self.team_2 = team_2
        self.add_item(discord.ui.Button(label="OP.GG E-Sports에서 보기", url=url, row=1))
        self.add_button()

    def add_button(self):
        home_team = discord.ui.Button(label=f"'{self.team_1}' 팀 예측하기", style=discord.ButtonStyle.blurple, custom_id=f"{self.match_id}/{self.team_1}", row=0)
        away_team = discord.ui.Button(label=f"'{self.team_2}' 팀 예측하기", style=discord.ButtonStyle.blurple, custom_id=f"{self.match_id}/{self.team_2}", row=0)


        async def callback_1(interaction: discord.Interaction):
            user = interaction.user

            if os.path.isfile(rf"./Database/User/user_{user.id}.sqlite"):
                userDB = sqlite3.connect(rf"./Database/User/user_{user.id}.sqlite", isolation_level=None)
                userCURSOR = userDB.cursor()
                userDATA = userCURSOR.execute(f"SELECT * FROM data WHERE UserID = '{user.id}'").fetchone()

                modal = BettingModal_1(bot=self.bot, msg=self.msg, url=self.url, match_id=self.match_id, team_1=self.team_1, team_2=self.team_2, data=userDATA[2], title=f"리그 승부 예측 ({self.team_1} vs {self.team_2})")
                await interaction.response.send_modal(modal)

            else:
                embed = discord.Embed(title="> ⛔ 리그 승부 예측 불가", description="서비스에 가입하셔야 이용할 수 있는 기능입니다.", color=colorMap['red'])
                return await interaction.response.send_message(embed=embed, ephemeral=True)


        async def callback_2(interaction: discord.Interaction):
            user = interaction.user

            if os.path.isfile(rf"./Database/User/user_{user.id}.sqlite"):
                userDB = sqlite3.connect(rf"./Database/User/user_{user.id}.sqlite", isolation_level=None)
                userCURSOR = userDB.cursor()
                userDATA = userCURSOR.execute(f"SELECT * FROM data WHERE UserID = '{user.id}'").fetchone()

                modal = BettingModal_2(bot=self.bot, msg=self.msg, url=self.url, match_id=self.match_id, team_1=self.team_1, team_2=self.team_2, data=userDATA[2], title=f"리그 승부 예측 ({self.team_1} vs {self.team_2})")
                await interaction.response.send_modal(modal)

            else:
                embed = discord.Embed(title="> ⛔ 리그 승부 예측 불가", description="서비스에 가입하셔야 이용할 수 있는 기능입니다.", color=colorMap['red'])
                return await interaction.response.send_message(embed=embed, ephemeral=True)

        home_team.callback = callback_1
        away_team.callback = callback_2

        self.add_item(home_team)
        self.add_item(away_team)


    async def on_timeout(self):

        # try:
        #     for data_guild in os.listdir(r"./Database/Guild"):
        #         if data_guild.endswith(".sqlite"):
        #             guildDB = sqlite3.connect(rf"./Database/Guild/{data_guild}", isolation_level=None)
        #             guildCURSOR = guildDB.cursor()

        #             role_id = guildCURSOR.execute("SELECT NoticeRoleID FROM main").fetchone()[0]
        #             guild_notice = self.bot.get_guild(int(data_guild.split("_")[1].split(".")[0]))
        #             role_notice = discord.utils.get(guild_notice.roles, id=role_id)

        #             msg_content = f"{role_notice.mention}"

        #             guildDB.close()

        # except discord.NotFound:
        #     pass

        # except Exception as error:
        #     print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
        #     print(traceback.format_exc())

        # await self.msg.edit(content=msg_content, view=DisabledButton(bot=self.bot, msg=self.msg, url=self.url, match_id=self.match_id, team_1=self.team_1, team_2=self.team_2))
        await self.msg.edit(content="", view=DisabledButton(bot=self.bot, msg=self.msg, url=self.url, match_id=self.match_id, team_1=self.team_1, team_2=self.team_2))


class BettingModal_1(discord.ui.Modal):

    def __init__(self, bot, msg, url, match_id, team_1, team_2, data, *args, **kwargs) -> None:
        self.bot = bot
        self.msg = msg
        self.url = url
        self.match_id = match_id
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
            if os.path.isfile(rf"./Database/User/user_{user.id}.sqlite"):
                userDB = sqlite3.connect(rf"./Database/User/user_{user.id}.sqlite", isolation_level=None)
                userCURSOR = userDB.cursor()

                bettingDB = sqlite3.connect(rf"./Database/betting.sqlite", isolation_level=None)
                bettingCURSOR = bettingDB.cursor()

                try:
                    result = userCURSOR.execute(f"SELECT * FROM \"{self.match_id}\" WHERE UserID = {user.id}").fetchone()
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
                                if str(self.match_id) == str(box_match[j][0]):
                                    bettingCURSOR.execute(f"UPDATE {leagues[i]['shortName']} SET TotalBet = ?, TotalPoint = ?, HomeBet = ?, HomePoint = ? WHERE ID = ?", ((box_match[j][3] + 1), (box_match[j][4] + bet_point), (box_match[j][5] + 1), (box_match[j][6] + bet_point), self.match_id))

                        userCURSOR.execute("UPDATE data SET Point = ?, TotalAnswer = ? WHERE UserID = ?", ((resultData[2] - bet_point), (resultData[3] + 1), user.id))

                        userCURSOR.execute(f"CREATE TABLE IF NOT EXISTS \"{self.match_id}\"(UserID INTERGER, Answer TEXT, BettingPoint INTERGER)") # 베팅 테이블 생성
                        userCURSOR.execute(f"INSERT INTO \"{self.match_id}\"(UserID, Answer, BettingPoint) VALUES(?, ?, ?)", (user.id, self.team_1, bet_point)) # 베팅 테이블 데이터 입력

                    elif not resultData or (resultData[1] <= bet_point):
                        embed = discord.Embed(title="> ⛔ 리그 승부 예측 불가", description=f"아쉽지만 베팅할 포인트가 모자라요. 😭", color=colorMap['red'])
                        return await interaction.response.send_message(embed=embed, ephemeral=True)

                    embed = discord.Embed(title="> 🎲 리그 승부 예측", description=f"`{self.team_1}` 팀에 _**{bet_point:,}**_포인트를 베팅하였습니다. 행운을 빌죠! 🍀", color=colorMap['red'])
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


class BettingModal_2(discord.ui.Modal):

    def __init__(self, bot, msg, url, match_id, team_1, team_2, data, *args, **kwargs) -> None:
        self.bot = bot
        self.msg = msg
        self.url = url
        self.match_id = match_id
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
            if os.path.isfile(rf"./Database/User/user_{user.id}.sqlite"):
                userDB = sqlite3.connect(rf"./Database/User/user_{user.id}.sqlite", isolation_level=None)
                userCURSOR = userDB.cursor()

                bettingDB = sqlite3.connect(rf"./Database/betting.sqlite", isolation_level=None)
                bettingCURSOR = bettingDB.cursor()

                try:
                    result = userCURSOR.execute(f"SELECT * FROM \"{self.match_id}\" WHERE UserID = {user.id}").fetchone()
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
                                if str(self.match_id) == str(box_match[j][0]):
                                    bettingCURSOR.execute(f"UPDATE {leagues[i]['shortName']} SET TotalBet = ?, TotalPoint = ?, AwayBet = ?, AwayPoint = ? WHERE ID = ?", ((box_match[j][3] + 1), (box_match[j][4] + bet_point), (box_match[j][7] + 1), (box_match[j][8] + bet_point), self.match_id))

                        userCURSOR.execute("UPDATE data SET Point = ?, TotalAnswer = ? WHERE UserID = ?", ((resultData[2] - bet_point), (resultData[3] + 1), user.id))

                        userCURSOR.execute(f"CREATE TABLE IF NOT EXISTS \"{self.match_id}\"(UserID INTERGER, Answer TEXT, BettingPoint INTERGER)") # 베팅 테이블 생성
                        userCURSOR.execute(f"INSERT INTO \"{self.match_id}\"(UserID, Answer, BettingPoint) VALUES(?, ?, ?)", (user.id, self.team_2, bet_point)) # 베팅 테이블 데이터 입력

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

    def __init__(self, bot, msg, url, match_id, team_1, team_2):
        super().__init__(timeout=None)
        self.bot = bot
        self.msg = msg
        self.match_id = match_id
        self.team_1 = team_1
        self.team_2 = team_2
        self.add_item(discord.ui.Button(label=f"'{self.team_1}' 팀 예측하기", style=discord.ButtonStyle.blurple, custom_id=f"{self.match_id}/{self.team_1}", disabled=True, row=0))
        self.add_item(discord.ui.Button(label=f"'{self.team_2}' 팀 예측하기", style=discord.ButtonStyle.blurple, custom_id=f"{self.match_id}/{self.team_2}", disabled=True, row=0))
        self.add_item(discord.ui.Button(label="OP.GG E-Sports에서 보기", url=url, row=1))
