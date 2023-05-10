# -*- coding: utf-8 -*-

# 패키지 라이브러리 설정
import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup, option
import random
import json
import datetime
import pytz
import traceback

import requests

from Extensions.Process.league import get_league_standing
from Extensions.Process.player import get_team_info_by_id

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

# emoji.json 파일 불러오기
try:
    with open(r"./emoji.json", "rt", encoding="UTF8") as emojiJson:
        emoji = json.load(emojiJson)
except: print("emoji.json 파일이 로드되지 않음")

esports_op_gg_standing = "https://esports.op.gg/standing"
esports_op_gg_player = "https://esports.op.gg/players/"
esports_op_gg_team = "https://esports.op.gg/teams/"
time_difference = config['time_difference']
webhook_url = config['all_log_webhook_url']
colorMap = config['colorMap']
emoji_website = emoji['Website']
emoji_esports = emoji['Esports']
emoji_discord = emoji['Discord']
emoji_facebook = emoji['Facebook']
emoji_instagram = emoji['Instagram']
emoji_twitter = emoji['Twitter']
emoji_youtube = emoji['YouTube']


def get_league(ctx: discord.AutocompleteContext):

    picked_league = ctx.options['리그']

    if picked_league == "LCK":
        return ["LCK"]
    elif picked_league == "LPL":
        return ["LPL"]
    elif picked_league == "LEC":
        return ["LEC"]
    elif picked_league == "LCS":
        return ["LCS"]
    elif picked_league == "CBLOL":
        return ["CBLOL"]
    elif picked_league == "VCS":
        return ["VCS"]
    elif picked_league == "LCL":
        return ["LCL"]
    elif picked_league == "TCL":
        return ["TCL"]
    elif picked_league == "PCS":
        return ["PCS"]
    elif picked_league == "LLA":
        return ["LLA"]
    elif picked_league == "LJL":
        return ["LJL"]
    elif picked_league == "LCO":
        return ["LCO"]
    else:
        return ["LCK", "LPL", "LEC", "LCS", "CBLOL", "VCS", "LCL", "TCL", "PCS", "LLA", "LJL", "LCO"]


class StandingView(discord.ui.View):

    def __init__(self, bot, ctx, msg, banner, picked_league, button_select, button_select_index, teams_id):
        super().__init__(timeout=60)
        self.bot = bot
        self.ctx = ctx
        self.msg = msg
        self.banner = banner
        self.picked_league = picked_league
        self.teams_id = teams_id

        self.links = ""
        self.msg_player = ""
        self.box_team = []
        self.box_player = []
        self.teams_id_index = ""

        self.button_select = button_select
        self.button_select_index = button_select_index
        self.add_item(discord.ui.Button(label="OP.GG Esports에서 보기", url=esports_op_gg_standing, row=3))
        self.add_button()

    @discord.ui.select(
        placeholder="리그 선택하기",
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(label="LCK / KR", value="0", description="League of Legends Champions Korea"),
            discord.SelectOption(label="LPL / CN ", value="1", description="League of Legends Pro League"),
            discord.SelectOption(label="LEC / EU", value="2", description="League of Legends European Championship"),
            discord.SelectOption(label="LCS / NA", value="3", description="League of Legends Championship Series"),
            discord.SelectOption(label="CBLOL / BR", value="4", description="Campeonato Brasileiro de League of Legends"),
            discord.SelectOption(label="VCS / VN", value="5", description="Vietnam Championship Series"),
            discord.SelectOption(label="LCL / CIS", value="6", description="League of Legends Continental League"),
            discord.SelectOption(label="TCL / TR", value="7", description="Turkish Championship League"),
            discord.SelectOption(label="PCS / SEA", value="8", description="Pacific Championship Series"),
            discord.SelectOption(label="LLA / LAT", value="9", description="Liga Latinoamérica"),
            discord.SelectOption(label="LJL / JP", value="10", description="League of Legends Japan League"),
            discord.SelectOption(label="LCO / OCE", value="11", description="League of Legends Circuit Oceania")
        ],
        row=0
    )
    async def select_callback(self, select: discord.ui.Select, interaction):
        if interaction.user.id != self.ctx.author.id: return await interaction.response.send_message("> 자신의 메시지에서만 이용할 수 있어요. 😢", ephemeral=True)

        tournamentId = []

        for i in range(16):
            if (select.values[0] == "0") and (leagues[i]['shortName'] == "LCK"):
                self.picked_league = "LCK"
                tournamentId = leagues[i]['tournamentId']
            elif (select.values[0] == "1") and (leagues[i]['shortName'] == "LPL"):
                self.picked_league = "LPL"
                tournamentId = leagues[i]['tournamentId']
            elif (select.values[0] == "2") and (leagues[i]['shortName'] == "LEC"):
                self.picked_league = "LEC"
                tournamentId = leagues[i]['tournamentId']
            elif (select.values[0] == "3") and (leagues[i]['shortName'] == "LCS"):
                self.picked_league = "LCS"
                tournamentId = leagues[i]['tournamentId']
            elif (select.values[0] == "4") and (leagues[i]['shortName'] == "CBLOL"):
                self.picked_league = "CBLOL"
                tournamentId = leagues[i]['tournamentId']
            elif (select.values[0] == "5") and (leagues[i]['shortName'] == "VCS"):
                self.picked_league = "VCS"
                tournamentId = leagues[i]['tournamentId']
            elif (select.values[0] == "6") and (leagues[i]['shortName'] == "LCL"):
                self.picked_league = "LCL"
                tournamentId = leagues[i]['tournamentId']
            elif (select.values[0] == "7") and (leagues[i]['shortName'] == "TCL"):
                self.picked_league = "TCL"
                tournamentId = leagues[i]['tournamentId']
            elif (select.values[0] == "8") and (leagues[i]['shortName'] == "PCS"):
                self.picked_league = "PCS"
                tournamentId = leagues[i]['tournamentId']
            elif (select.values[0] == "9") and (leagues[i]['shortName'] == "LLA"):
                self.picked_league = "LLA"
                tournamentId = leagues[i]['tournamentId']
            elif (select.values[0] == "10") and (leagues[i]['shortName'] == "LJL"):
                self.picked_league = "LJL"
                tournamentId = leagues[i]['tournamentId']
            elif (select.values[0] == "11") and (leagues[i]['shortName'] == "LCO"):
                self.picked_league = "LCO"
                tournamentId = leagues[i]['tournamentId']
            else: pass

            if tournamentId == []: continue
            elif tournamentId == None:
                embed = discord.Embed(title="> 🏅 시즌 리그 순위", description="", color=colorMap['red'])
                embed.set_image(url=self.banner)
                embed.add_field(name=f"'{self.picked_league}' 리그 정보", value="> 순위 정보가 없습니다.", inline=False)
                return await interaction.response.edit_message(content="", embed=embed, view=StandingView(bot=self.bot, ctx=self.ctx, msg=self.msg, banner=self.banner, picked_league=self.picked_league, button_select=True, button_select_index=self.teams_id_index, teams_id=self.teams_id))
            self.box_team = get_league_standing(tournamentId=tournamentId)
            tournamentId = [] # 초기화

            try:
                print(f"[league_standing.py] {self.box_team['code']}: {self.box_team['message']}")
                embed = discord.Embed(title="> ⚠️ 오류", description=f"Code: `{self.box_team['code']}`\nMessage: {self.box_team['message']}", color=colorMap['red'])
                return await interaction.response.edit_message(content="", embed=embed, view=None)

            except:
                if self.box_team:
                    self.teams_id = []
                    embed = discord.Embed(title="> 🏅 시즌 리그 순위", description="", color=colorMap['red'])
                    embed.set_footer(text="TIP: 아래 버튼을 눌러 각 팀의 정보를 확인할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
                    embed.set_image(url=self.banner)
                    if self.box_team == []: embed.add_field(name=f"'{self.picked_league}' 리그 정보", value="> 순위 정보가 없습니다.", inline=False)
                    else: embed.add_field(name=f"'{self.picked_league}' 리그 정보", value="", inline=False)
                    if len(self.box_team) > 10:
                        for i in range(10):
                            self.teams_id.append(self.box_team[i]['id'])
                            self.links = f"[{emoji_esports}]({esports_op_gg_player}{self.box_team[i]['id']}) "
                            if self.box_team[i]['website']: self.links = f"{self.links}[{emoji_website}]({self.box_team[i]['website']}) "
                            if self.box_team[i]['youtube']: self.links = f"{self.links}[{emoji_youtube}]({self.box_team[i]['youtube']}) "
                            if self.box_team[i]['instagram']: self.links = f"{self.links}[{emoji_instagram}]({self.box_team[i]['instagram']}) "
                            if self.box_team[i]['facebook']: self.links = f"{self.links}[{emoji_facebook}]({self.box_team[i]['facebook']}) "
                            if self.box_team[i]['twitter']: self.links = f"{self.links}[{emoji_twitter}]({self.box_team[i]['twitter']}) "
                            if self.box_team[i]['discord']: self.links = f"{self.links}[{emoji_discord}]({self.box_team[i]['discord']}) "
                            self.links = self.links[:-1]
                            embed.add_field(name=f"> {i + 1}위 - {self.box_team[i]['acronym']} ({self.box_team[i]['name']})", value=f"[__{self.box_team[i]['point']:,}__포인트] __{self.box_team[i]['win']:,}__승 __{self.box_team[i]['lose']:,}__패 (세트 스코어 __{self.box_team[i]['setWin']:,}__승 __{self.box_team[i]['setLose']:,}__패)\n{self.links}", inline=False)
                            self.links = ""
                    else:
                        for i in range(len(self.box_team)):
                            if i >= len(self.box_team): break
                            self.teams_id.append(self.box_team[i]['id'])
                            self.links = f"[{emoji_esports}]({esports_op_gg_player}{self.box_team[i]['id']}) "
                            if self.box_team[i]['website']: self.links = f"{self.links}[{emoji_website}]({self.box_team[i]['website']}) "
                            if self.box_team[i]['youtube']: self.links = f"{self.links}[{emoji_youtube}]({self.box_team[i]['youtube']}) "
                            if self.box_team[i]['instagram']: self.links = f"{self.links}[{emoji_instagram}]({self.box_team[i]['instagram']}) "
                            if self.box_team[i]['facebook']: self.links = f"{self.links}[{emoji_facebook}]({self.box_team[i]['facebook']}) "
                            if self.box_team[i]['twitter']: self.links = f"{self.links}[{emoji_twitter}]({self.box_team[i]['twitter']}) "
                            if self.box_team[i]['discord']: self.links = f"{self.links}[{emoji_discord}]({self.box_team[i]['discord']}) "
                            self.links = self.links[:-1]
                            embed.add_field(name=f"> {i + 1}위 - {self.box_team[i]['acronym']} ({self.box_team[i]['name']})", value=f"[__{self.box_team[i]['point']:,}__포인트] __{self.box_team[i]['win']:,}__승 __{self.box_team[i]['lose']:,}__패 (세트 스코어 __{self.box_team[i]['setWin']:,}__승 __{self.box_team[i]['setLose']:,}__패)\n{self.links}", inline=False)
                            self.links = ""
                    await interaction.response.edit_message(content="", embed=embed, view=StandingView(bot=self.bot, ctx=self.ctx, msg=self.msg, banner=self.banner, picked_league=self.picked_league, button_select=False, button_select_index="99", teams_id=self.teams_id))

                else:
                    embed = discord.Embed(title="> 🏅 시즌 리그 순위", description="", color=colorMap['red'])
                    embed.set_image(url=self.banner)
                    embed.add_field(name=f"'{self.picked_league}' 리그 정보", value="> 순위 정보가 없습니다.", inline=False)
                    return await interaction.response.edit_message(content="", embed=embed, view=StandingView(bot=self.bot, ctx=self.ctx, msg=self.msg, banner=self.banner, picked_league=self.picked_league, button_select=True, button_select_index=self.teams_id_index, teams_id=self.teams_id))


    def add_button(self):
        if (self.button_select == True) and (self.button_select_index == "0"):
            team_1 = discord.ui.Button(emoji="1️⃣", style=discord.ButtonStyle.gray, disabled=True, custom_id="0", row=1)
        else:
            team_1 = discord.ui.Button(emoji="1️⃣", style=discord.ButtonStyle.gray, custom_id="0", row=1)
        if (self.button_select == True) and (self.button_select_index == "1"):
            team_2 = discord.ui.Button(emoji="2️⃣", style=discord.ButtonStyle.gray, disabled=True, custom_id="1", row=1)
        else:
            team_2 = discord.ui.Button(emoji="2️⃣", style=discord.ButtonStyle.gray, custom_id="1", row=1)
        if (self.button_select == True) and (self.button_select_index == "2"):
            team_3 = discord.ui.Button(emoji="3️⃣", style=discord.ButtonStyle.gray, disabled=True, custom_id="2", row=1)
        else:
            team_3 = discord.ui.Button(emoji="3️⃣", style=discord.ButtonStyle.gray, custom_id="2", row=1)
        if (self.button_select == True) and (self.button_select_index == "3"):
            team_4 = discord.ui.Button(emoji="4️⃣", style=discord.ButtonStyle.gray, disabled=True, custom_id="3", row=1)
        else:
            team_4 = discord.ui.Button(emoji="4️⃣", style=discord.ButtonStyle.gray, custom_id="3", row=1)
        if (self.button_select == True) and (self.button_select_index == "4"):
            team_5 = discord.ui.Button(emoji="5️⃣", style=discord.ButtonStyle.gray, disabled=True, custom_id="4", row=1)
        else:
            team_5 = discord.ui.Button(emoji="5️⃣", style=discord.ButtonStyle.gray, custom_id="4", row=1)
        if (self.button_select == True) and (self.button_select_index == "5"):
            team_6 = discord.ui.Button(emoji="6️⃣", style=discord.ButtonStyle.gray, disabled=True, custom_id="5", row=2)
        else:
            team_6 = discord.ui.Button(emoji="6️⃣", style=discord.ButtonStyle.gray, custom_id="5", row=2)
        if (self.button_select == True) and (self.button_select_index == "6"):
            team_7 = discord.ui.Button(emoji="7️⃣", style=discord.ButtonStyle.gray, disabled=True, custom_id="6", row=2)
        else:
            team_7 = discord.ui.Button(emoji="7️⃣", style=discord.ButtonStyle.gray, custom_id="6", row=2)
        if (self.button_select == True) and (self.button_select_index == "7"):
            team_8 = discord.ui.Button(emoji="8️⃣", style=discord.ButtonStyle.gray, disabled=True, custom_id="7", row=2)
        else:
            team_8 = discord.ui.Button(emoji="8️⃣", style=discord.ButtonStyle.gray, custom_id="7", row=2)
        if (self.button_select == True) and (self.button_select_index == "8"):
            team_9 = discord.ui.Button(emoji="9️⃣", style=discord.ButtonStyle.gray, disabled=True, custom_id="8", row=2)
        else:
            team_9 = discord.ui.Button(emoji="9️⃣", style=discord.ButtonStyle.gray, custom_id="8", row=2)
        if (self.button_select == True) and (self.button_select_index == "9"):
            team_10 = discord.ui.Button(emoji="🔟", style=discord.ButtonStyle.gray, disabled=True, custom_id="9", row=2)
        else:
            team_10 = discord.ui.Button(emoji="🔟", style=discord.ButtonStyle.gray, custom_id="9", row=2)


        async def callback_all(interaction: discord.Interaction):
            if interaction.user.id != self.ctx.author.id: return await interaction.response.send_message("> 자신의 메시지에서만 이용할 수 있어요. 😢", ephemeral=True)

            tournamentId = []

            for i in range(16):
                if (self.picked_league == "LCK") and (leagues[i]['shortName'] == "LCK"): tournamentId = leagues[i]['tournamentId']
                elif (self.picked_league == "LEC") and (leagues[i]['shortName'] == "LEC"): tournamentId = leagues[i]['tournamentId']
                elif (self.picked_league == "LPL") and (leagues[i]['shortName'] == "LPL"): tournamentId = leagues[i]['tournamentId']
                elif (self.picked_league == "LCS") and (leagues[i]['shortName'] == "LCS"): tournamentId = leagues[i]['tournamentId']
                elif (self.picked_league == "CBLOL") and (leagues[i]['shortName'] == "CBLOL"): tournamentId = leagues[i]['tournamentId']
                elif (self.picked_league == "LJL") and (leagues[i]['shortName'] == "LJL"): tournamentId = leagues[i]['tournamentId']
                elif (self.picked_league == "LCL") and (leagues[i]['shortName'] == "LCL"): tournamentId = leagues[i]['tournamentId']
                elif (self.picked_league == "LLA") and (leagues[i]['shortName'] == "LLA"): tournamentId = leagues[i]['tournamentId']
                elif (self.picked_league == "VCS") and (leagues[i]['shortName'] == "VCS"): tournamentId = leagues[i]['tournamentId']
                elif (self.picked_league == "LCO") and (leagues[i]['shortName'] == "LCO"): tournamentId = leagues[i]['tournamentId']
                else: pass

                if tournamentId == []: continue
                elif tournamentId == None:
                    embed = discord.Embed(title="> 🏅 시즌 리그 순위", description="", color=colorMap['red'])
                    embed.set_image(url=self.banner)
                    embed.add_field(name=f"'{self.picked_league}' 리그 정보", value="> 순위 정보가 없습니다.", inline=False)
                    return await interaction.response.edit_message(content="", embed=embed, view=StandingView(bot=self.bot, ctx=self.ctx, msg=self.msg, banner=self.banner, picked_league=self.picked_league, button_select=True, button_select_index=self.teams_id_index, teams_id=self.teams_id))
                                        
                self.box_team = get_league_standing(tournamentId)
                tournamentId = [] # 초기화

                try:
                    print(f"[league_standing.py] {self.box_team['code']}: {self.box_team['message']}")
                    embed = discord.Embed(title="> ⚠️ 오류", description=f"Code: `{self.box_team['code']}`\nMessage: {self.box_team['message']}", color=colorMap['red'])
                    return await interaction.response.edit_message(content="", embed=embed, view=None)

                except:
                    if self.box_team:
                        self.teams_id = []
                        embed = discord.Embed(title="> 🏅 시즌 리그 순위", description="", color=colorMap['red'])
                        embed.set_footer(text="TIP: 아래 버튼을 눌러 각 팀의 정보를 확인할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
                        embed.set_image(url=self.banner)
                        if self.box_team == []: embed.add_field(name=f"'{self.picked_league}' 리그 정보", value="> 순위 정보가 없습니다.", inline=False)
                        else: embed.add_field(name=f"'{self.picked_league}' 리그 정보", value="", inline=False)
                        if len(self.box_team) > 10:
                            for i in range(10):
                                self.teams_id.append(self.box_team[i]['id'])
                                self.links = f"[{emoji_esports}]({esports_op_gg_player}{self.box_team[i]['id']}) "
                                if self.box_team[i]['website']: self.links = f"{self.links}[{emoji_website}]({self.box_team[i]['website']}) "
                                if self.box_team[i]['youtube']: self.links = f"{self.links}[{emoji_youtube}]({self.box_team[i]['youtube']}) "
                                if self.box_team[i]['instagram']: self.links = f"{self.links}[{emoji_instagram}]({self.box_team[i]['instagram']}) "
                                if self.box_team[i]['facebook']: self.links = f"{self.links}[{emoji_facebook}]({self.box_team[i]['facebook']}) "
                                if self.box_team[i]['twitter']: self.links = f"{self.links}[{emoji_twitter}]({self.box_team[i]['twitter']}) "
                                if self.box_team[i]['discord']: self.links = f"{self.links}[{emoji_discord}]({self.box_team[i]['discord']}) "
                                self.links = self.links[:-1]
                                embed.add_field(name=f"> {i + 1}위 - {self.box_team[i]['acronym']} ({self.box_team[i]['name']})", value=f"[__{self.box_team[i]['point']:,}__포인트] __{self.box_team[i]['win']:,}__승 __{self.box_team[i]['lose']:,}__패 (세트 스코어 __{self.box_team[i]['setWin']:,}__승 __{self.box_team[i]['setLose']:,}__패)\n{self.links}", inline=False)
                                self.links = ""
                        else:
                            for i in range(len(self.box_team)):
                                if i >= len(self.box_team): break
                                self.teams_id.append(self.box_team[i]['id'])
                                self.links = f"[{emoji_esports}]({esports_op_gg_player}{self.box_team[i]['id']}) "
                                if self.box_team[i]['website']: self.links = f"{self.links}[{emoji_website}]({self.box_team[i]['website']}) "
                                if self.box_team[i]['youtube']: self.links = f"{self.links}[{emoji_youtube}]({self.box_team[i]['youtube']}) "
                                if self.box_team[i]['instagram']: self.links = f"{self.links}[{emoji_instagram}]({self.box_team[i]['instagram']}) "
                                if self.box_team[i]['facebook']: self.links = f"{self.links}[{emoji_facebook}]({self.box_team[i]['facebook']}) "
                                if self.box_team[i]['twitter']: self.links = f"{self.links}[{emoji_twitter}]({self.box_team[i]['twitter']}) "
                                if self.box_team[i]['discord']: self.links = f"{self.links}[{emoji_discord}]({self.box_team[i]['discord']}) "
                                self.links = self.links[:-1]
                                embed.add_field(name=f"> {i + 1}위 - {self.box_team[i]['acronym']} ({self.box_team[i]['name']})", value=f"[__{self.box_team[i]['point']:,}__포인트] __{self.box_team[i]['win']:,}__승 __{self.box_team[i]['lose']:,}__패 (세트 스코어 __{self.box_team[i]['setWin']:,}__승 __{self.box_team[i]['setLose']:,}__패)\n{self.links}", inline=False)
                                self.links = ""
                        await interaction.response.edit_message(content="", embed=embed, view=StandingView(bot=self.bot, ctx=self.ctx, msg=self.msg, banner=self.banner, picked_league=self.picked_league, button_select=False, button_select_index="99", teams_id=self.teams_id))

                    else:
                        embed = discord.Embed(title="> 🏅 시즌 리그 순위", description="", color=colorMap['red'])
                        embed.set_image(url=self.banner)
                        embed.add_field(name=f"'{self.picked_league}' 리그 정보", value="> 순위 정보가 없습니다.", inline=False)
                        return await interaction.response.edit_message(content="", embed=embed, view=StandingView(bot=self.bot, ctx=self.ctx, msg=self.msg, banner=self.banner, picked_league=self.picked_league, button_select=True, button_select_index=self.teams_id_index, teams_id=self.teams_id))


        async def team_callback(interaction: discord.Interaction):
            if interaction.user.id != self.ctx.author.id: return await interaction.response.send_message("> 자신의 메시지에서만 이용할 수 있어요. 😢", ephemeral=True)

            for i in range(16):
                if (self.picked_league == "LCK") and (leagues[i]['shortName'] == "LCK"): tournamentId = leagues[i]['tournamentId']
                elif (self.picked_league == "LEC") and (leagues[i]['shortName'] == "LEC"): tournamentId = leagues[i]['tournamentId']
                elif (self.picked_league == "LPL") and (leagues[i]['shortName'] == "LPL"): tournamentId = leagues[i]['tournamentId']
                elif (self.picked_league == "LCS") and (leagues[i]['shortName'] == "LCS"): tournamentId = leagues[i]['tournamentId']
                elif (self.picked_league == "CBLOL") and (leagues[i]['shortName'] == "CBLOL"): tournamentId = leagues[i]['tournamentId']
                elif (self.picked_league == "LJL") and (leagues[i]['shortName'] == "LJL"): tournamentId = leagues[i]['tournamentId']
                elif (self.picked_league == "LCL") and (leagues[i]['shortName'] == "LCL"): tournamentId = leagues[i]['tournamentId']
                elif (self.picked_league == "LLA") and (leagues[i]['shortName'] == "LLA"): tournamentId = leagues[i]['tournamentId']
                elif (self.picked_league == "VCS") and (leagues[i]['shortName'] == "VCS"): tournamentId = leagues[i]['tournamentId']
                elif (self.picked_league == "LCO") and (leagues[i]['shortName'] == "LCO"): tournamentId = leagues[i]['tournamentId']
                else: pass

            self.teams_id_index = interaction.data['custom_id']
            try:
                self.box_player = get_team_info_by_id(tournamentId=tournamentId, teamId=self.teams_id[int(self.teams_id_index)])
            except:
                embed = discord.Embed(title="> 📊 팀 정보", description="", color=colorMap['red'])
                embed.set_footer(text="TIP: 아래 버튼을 눌러 각 팀의 정보를 확인할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
                embed.set_image(url=self.banner)
                embed.add_field(name=f"[{self.picked_league}]", value="> 팀 정보가 없습니다.", inline=False)
                return await interaction.response.edit_message(content="", embed=embed, view=StandingView(bot=self.bot, ctx=self.ctx, msg=self.msg, banner=self.banner, picked_league=self.picked_league, button_select=True, button_select_index=self.teams_id_index, teams_id=self.teams_id))

            try:
                print(f"[league_standing.py] {self.box_player['code']}: {self.box_player['message']}")
                embed = discord.Embed(title="> ⚠️ 오류", description=f"Code: `{self.box_player['code']}`\nMessage: {self.box_player['message']}", color=colorMap['red'])
                return await interaction.response.edit_message(content="", embed=embed, view=None)

            except:
                if self.box_player:
                    for i in range(len(self.box_player)):
                        self.msg_player = f"{self.msg_player}> [{self.box_player[i]['team_acronym']}]({esports_op_gg_team}{self.box_player[i]['team_id']}) [{self.box_player[i]['nickName']}]({esports_op_gg_player}{self.box_player[i]['id']}) ({self.box_player[i]['position']})\n{self.box_player[i]['stat_kda']} 평점 `({self.box_player[i]['stat_kills']}/{self.box_player[i]['stat_deaths']}/{self.box_player[i]['stat_assists']})`\n승률: __{self.box_player[i]['stat_winRate']}__% (__{self.box_player[i]['stat_wins']:,}__승 __{self.box_player[i]['stat_loses']:,}__패)\n"

                    embed = discord.Embed(title="> 📊 팀 정보", description="", color=colorMap['red'])
                    embed.set_footer(text="TIP: 아래 버튼을 눌러 각 팀의 정보를 확인할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
                    embed.set_image(url=self.banner)
                    embed.set_thumbnail(url=self.box_player[0]['team_imageUrl'])
                    embed.add_field(name=f"{self.box_player[0]['team_acronym']} ({self.box_player[0]['team_name']}) [{self.picked_league}]", value=self.msg_player, inline=False)
                    await interaction.response.edit_message(content="", embed=embed, view=StandingView(bot=self.bot, ctx=self.ctx, msg=self.msg, banner=self.banner, picked_league=self.picked_league, button_select=True, button_select_index=self.teams_id_index, teams_id=self.teams_id))

                else:
                    embed = discord.Embed(title="> 📊 팀 정보", description="", color=colorMap['red'])
                    embed.set_footer(text="TIP: 아래 버튼을 눌러 각 팀의 정보를 확인할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
                    embed.set_image(url=self.banner)
                    embed.add_field(name=f"[{self.picked_league}]", value="> 팀 정보가 없습니다.", inline=False)
                    await interaction.response.edit_message(content="", embed=embed, view=StandingView(bot=self.bot, ctx=self.ctx, msg=self.msg, banner=self.banner, picked_league=self.picked_league, button_select=True, button_select_index=self.teams_id_index, teams_id=self.teams_id))

        if self.button_select == True:
            if self.button_select_index == "0": team_1.callback = callback_all
            else: team_1.callback = team_callback
            if self.button_select_index == "1": team_2.callback = callback_all
            else: team_2.callback = team_callback
            if self.button_select_index == "2": team_3.callback = callback_all
            else: team_3.callback = team_callback
            if self.button_select_index == "3": team_4.callback = callback_all
            else: team_4.callback = team_callback
            if self.button_select_index == "4": team_5.callback = callback_all
            else: team_5.callback = team_callback
            if self.button_select_index == "5": team_6.callback = callback_all
            else: team_6.callback = team_callback
            if self.button_select_index == "6": team_7.callback = callback_all
            else: team_7.callback = team_callback
            if self.button_select_index == "7": team_8.callback = callback_all
            else: team_8.callback = team_callback
            if self.button_select_index == "8": team_9.callback = callback_all
            else: team_9.callback = team_callback
            if self.button_select_index == "9": team_10.callback = callback_all
            else: team_10.callback = team_callback
        else:
            team_1.callback = team_callback
            team_2.callback = team_callback
            team_3.callback = team_callback
            team_4.callback = team_callback
            team_5.callback = team_callback
            team_6.callback = team_callback
            team_7.callback = team_callback
            team_8.callback = team_callback
            team_9.callback = team_callback
            team_10.callback = team_callback

        self.add_item(team_1)
        self.add_item(team_2)
        self.add_item(team_3)
        self.add_item(team_4)
        self.add_item(team_5)
        self.add_item(team_6)
        self.add_item(team_7)
        self.add_item(team_8)
        self.add_item(team_9)
        self.add_item(team_10)


    async def on_timeout(self):
        try:
            await self.msg.edit_original_response(content="", view=DisabledButton())
        except discord.NotFound:
            pass


class DisabledButton(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Select(placeholder="리그 선택하기", options=[discord.SelectOption(label="asdf", value="1", description="asdf")], disabled=True, row=0))
        self.add_item(discord.ui.Button(emoji="1️⃣", disabled=True, row=1))
        self.add_item(discord.ui.Button(emoji="2️⃣", disabled=True, row=1))
        self.add_item(discord.ui.Button(emoji="3️⃣", disabled=True, row=1))
        self.add_item(discord.ui.Button(emoji="4️⃣", disabled=True, row=1))
        self.add_item(discord.ui.Button(emoji="5️⃣", disabled=True, row=1))
        self.add_item(discord.ui.Button(emoji="6️⃣", disabled=True, row=2))
        self.add_item(discord.ui.Button(emoji="7️⃣", disabled=True, row=2))
        self.add_item(discord.ui.Button(emoji="8️⃣", disabled=True, row=2))
        self.add_item(discord.ui.Button(emoji="9️⃣", disabled=True, row=2))
        self.add_item(discord.ui.Button(emoji="🔟", disabled=True, row=2))
        self.add_item(discord.ui.Button(label="OP.GG Esports에서 보기", url=esports_op_gg_standing, row=3))


class LeagueStandingCMD(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    _league = SlashCommandGroup(name="리그", description="리그 명령어", guild_only=False)

    @_league.command(
        name="순위",
        description="리그 오브 레전드 e스포츠의 시즌 팀 순위 정보를 확인해보세요.",
    )
    @option(name="리그", description="리그를 선택해주세요.", required=True, autocomplete=get_league)
    async def _mvpCMD(self, ctx: discord.AutocompleteContext, 리그: str):

        picked_league = 리그
        links = ""
        box_team = []
        teams_id = []
        banner_image_url = random.choice(config['banner_image_url'])

        embed = discord.Embed(title="", description="⌛ 정보를 불러오는 중...", color=colorMap['red'])
        msg = await ctx.respond(embed=embed)

        try:
            tournamentId = []

            for i in range(16):
                if (picked_league == "LCK") and (leagues[i]['shortName'] == "LCK"): tournamentId = leagues[i]['tournamentId']
                elif (picked_league == "LPL") and (leagues[i]['shortName'] == "LPL"): tournamentId = leagues[i]['tournamentId']
                elif (picked_league == "LEC") and (leagues[i]['shortName'] == "LEC"): tournamentId = leagues[i]['tournamentId']
                elif (picked_league == "LCS") and (leagues[i]['shortName'] == "LCS"): tournamentId = leagues[i]['tournamentId']
                elif (picked_league == "CBLOL") and (leagues[i]['shortName'] == "CBLOL"): tournamentId = leagues[i]['tournamentId']
                elif (picked_league == "VCS") and (leagues[i]['shortName'] == "VCS"): tournamentId = leagues[i]['tournamentId']
                elif (picked_league == "LCL") and (leagues[i]['shortName'] == "LCL"): tournamentId = leagues[i]['tournamentId']
                elif (picked_league == "TCL") and (leagues[i]['shortName'] == "TCL"): tournamentId = leagues[i]['tournamentId']
                elif (picked_league == "PCS") and (leagues[i]['shortName'] == "PCS"): tournamentId = leagues[i]['tournamentId']
                elif (picked_league == "LLA") and (leagues[i]['shortName'] == "LLA"): tournamentId = leagues[i]['tournamentId']
                elif (picked_league == "LJL") and (leagues[i]['shortName'] == "LJL"): tournamentId = leagues[i]['tournamentId']
                elif (picked_league == "LCO") and (leagues[i]['shortName'] == "LCO"): tournamentId = leagues[i]['tournamentId']
                else: pass

                if tournamentId == []: continue
                elif tournamentId == None:
                    embed = discord.Embed(title="> 🏅 시즌 리그 순위", description="", color=colorMap['red'])
                    embed.set_image(url=banner_image_url)
                    embed.add_field(name=f"'{picked_league}' 리그 정보", value="> 순위 정보가 없습니다.", inline=False)
                    return await msg.edit_original_response(content="", embed=embed, view=DisabledButton())
                box_team = get_league_standing(tournamentId)
                tournamentId = [] # 초기화

                try:
                    print(f"[league_standing.py] {box_team['code']}: {box_team['message']}")
                    embed = discord.Embed(title="> ⚠️ 오류", description=f"Code: `{box_team['code']}`\nMessage: {box_team['message']}", color=colorMap['red'])
                    return await msg.edit_original_response(content="", embed=embed)

                except:
                    if box_team:
                        embed = discord.Embed(title="> 🏅 시즌 리그 순위", description="", color=colorMap['red'])
                        embed.set_footer(text="TIP: 아래 버튼을 눌러 각 팀의 정보를 확인할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
                        embed.set_image(url=banner_image_url)
                        if box_team == []: embed.add_field(name=f"'{picked_league}' 리그 정보", value="> 순위 정보가 없습니다.", inline=False)
                        else: embed.add_field(name=f"'{picked_league}' 리그 정보", value="", inline=False)
                        if len(box_team) > 10:
                            for j in range(10):
                                teams_id.append(box_team[j]['id'])
                                links = f"[{emoji_esports}]({esports_op_gg_player}{box_team[j]['id']}) "
                                if box_team[j]['website']: links = f"{links}[{emoji_website}]({box_team[j]['website']}) "
                                if box_team[j]['youtube']: links = f"{links}[{emoji_youtube}]({box_team[j]['youtube']}) "
                                if box_team[j]['instagram']: links = f"{links}[{emoji_instagram}]({box_team[j]['instagram']}) "
                                if box_team[j]['facebook']: links = f"{links}[{emoji_facebook}]({box_team[j]['facebook']}) "
                                if box_team[j]['twitter']: links = f"{links}[{emoji_twitter}]({box_team[j]['twitter']}) "
                                if box_team[j]['discord']: links = f"{links}[{emoji_discord}]({box_team[j]['discord']}) "
                                links = links[:-1]
                                embed.add_field(name=f"> {j + 1}위 - {box_team[j]['acronym']} ({box_team[j]['name']})", value=f"[__{box_team[j]['point']:,}__포인트] __{box_team[j]['win']:,}__승 __{box_team[j]['lose']:,}__패 (세트 스코어 __{box_team[j]['setWin']:,}__승 __{box_team[j]['setLose']:,}__패)\n{links}", inline=False)
                                links = ""
                        else:
                            for j in range(len(box_team)):
                                if j >= len(box_team): break
                                teams_id.append(box_team[j]['id'])
                                links = f"[{emoji_esports}]({esports_op_gg_player}{box_team[j]['id']}) "
                                if box_team[j]['website']: links = f"{links}[{emoji_website}]({box_team[j]['website']}) "
                                if box_team[j]['youtube']: links = f"{links}[{emoji_youtube}]({box_team[j]['youtube']}) "
                                if box_team[j]['instagram']: links = f"{links}[{emoji_instagram}]({box_team[j]['instagram']}) "
                                if box_team[j]['facebook']: links = f"{links}[{emoji_facebook}]({box_team[j]['facebook']}) "
                                if box_team[j]['twitter']: links = f"{links}[{emoji_twitter}]({box_team[j]['twitter']}) "
                                if box_team[j]['discord']: links = f"{links}[{emoji_discord}]({box_team[j]['discord']}) "
                                embed.add_field(name=f"> {j + 1}위 - {box_team[j]['acronym']} ({box_team[j]['name']})", value=f"[__{box_team[j]['point']:,}__포인트] __{box_team[j]['win']:,}__승 __{box_team[j]['lose']:,}__패 (세트 스코어 __{box_team[j]['setWin']:,}__승 __{box_team[j]['setLose']:,}__패)\n{links}", inline=False)
                                links = ""
                        await msg.edit_original_response(content="", embed=embed, view=StandingView(bot=self.bot, ctx=ctx, msg=msg, banner=banner_image_url, picked_league=picked_league, button_select=False, button_select_index="99", teams_id=teams_id))

        except Exception as error:
            print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
            print(traceback.format_exc())
            webhook_headers = { "Content-Type": "application/json" }
            webhook_data = {
                "username": "OP.GG E-Sports Log",
                "content": f"``` ```\n>>> `({datetime.datetime.now(pytz.timezone('Asia/Seoul')).strftime('%y/%m/%d %H:%M:%S')})`\n{traceback.format_exc()}"
            }
            webhook_result = requests.post(url=webhook_url, json=webhook_data, headers=webhook_headers)
            if 200 <= webhook_result.status_code < 300: pass
            else: print(f'- [LOG] Not sent with {webhook_result.status_code}, response:\n{webhook_result.json()}')



def setup(bot):
    bot.add_cog(LeagueStandingCMD(bot))
    print("league_standing.py 로드 됨")
