# -*- coding: utf-8 -*-

# 패키지 라이브러리 설정
import opgg
import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup, option
import random
import json
import datetime
import pytz
import traceback

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

esports_op_gg_mvp = "https://esports.op.gg/players"
esports_op_gg_player = "https://esports.op.gg/players/"
esports_op_gg_team = "https://esports.op.gg/teams/"
time_difference = config['time_difference']
colorMap = config['colorMap']


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


class MvpView(discord.ui.View):

    def __init__(self, bot, ctx, msg, banner, picked_league, picked_lane, button_select, box_LCK, box_LPL, box_LEC, box_LCS, box_CBLOL, box_VCS, box_LCL, box_TCL, box_PCS, box_LLA, box_LJL, box_LCO):
        super().__init__(timeout=60)
        self.bot = bot
        self.ctx = ctx
        self.msg = msg
        self.banner = banner
        self.picked_league = picked_league
        self.picked_lane = picked_lane
        self.box_LCK = box_LCK
        self.box_LPL = box_LPL
        self.box_LEC = box_LEC
        self.box_LCS = box_LCS
        self.box_CBLOL = box_CBLOL
        self.box_VCS = box_VCS
        self.box_LCL = box_LCL
        self.box_TCL = box_TCL
        self.box_PCS = box_PCS
        self.box_LLA = box_LLA
        self.box_LJL = box_LJL
        self.box_LCO = box_LCO

        self.box_data = {}
        self.box_lane_data = []
        self.msg_mvp_1 = ""
        self.msg_mvp_2 = ""
        self.button_select = button_select
        self.add_item(discord.ui.Button(label="OP.GG Esports에서 보기", url=esports_op_gg_mvp, row=2))
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

        if select.values[0] == "0":
            self.picked_league = "LCK"
            self.box_data = self.box_LCK
        elif select.values[0] == "1":
            self.picked_league = "LPL"
            self.box_data = self.box_LPL
        elif select.values[0] == "2":
            self.picked_league = "LEC"
            self.box_data = self.box_LEC
        elif select.values[0] == "3":
            self.picked_league = "LCS"
            self.box_data = self.box_LCS
        elif select.values[0] == "4":
            self.picked_league = "CBLOL"
            self.box_data = self.box_CBLOL
        elif select.values[0] == "5":
            self.picked_league = "VCS"
            self.box_data = self.box_VCS
        elif select.values[0] == "6":
            self.picked_league = "LCL"
            self.box_data = self.box_LCL
        elif select.values[0] == "7":
            self.picked_league = "TCL"
            self.box_data = self.box_TCL
        elif select.values[0] == "8":
            self.picked_league = "PCS"
            self.box_data = self.box_PCS
        elif select.values[0] == "9":
            self.picked_league = "LLA"
            self.box_data = self.box_LLA
        elif select.values[0] == "10":
            self.picked_league = "LJL"
            self.box_data = self.box_LJL
        elif select.values[0] == "11":
            self.picked_league = "LCO"
            self.box_data = self.box_LCO

        k = 0
        for i in range(5):
            for j in range(len(self.box_data)):
                self.msg_mvp_1 = f"{self.msg_mvp_1}> {i + 1}위 - [{self.box_data[k]['team_acronym']}]({esports_op_gg_team}{self.box_data[k]['team_id']}) [{self.box_data[k]['nickName']}]({esports_op_gg_player}{self.box_data[k]['id']})\n[{self.box_data[k]['position']}] {self.box_data[k]['kda']} 평점\n`({self.box_data[k]['kills']} / {self.box_data[k]['deaths']} / {self.box_data[k]['assists']})`\n"
                k += 1
                break

        k = 5
        for i in range(5, 10):
            for j in range(len(self.box_data)):
                self.msg_mvp_2 = f"{self.msg_mvp_2}> {i + 1}위 - [{self.box_data[k]['team_acronym']}]({esports_op_gg_team}{self.box_data[k]['team_id']}) [{self.box_data[k]['nickName']}]({esports_op_gg_player}{self.box_data[k]['id']})\n[{self.box_data[k]['position']}] {self.box_data[k]['kda']} 평점\n`({self.box_data[k]['kills']} / {self.box_data[k]['deaths']} / {self.box_data[k]['assists']})`\n"
                k += 1
                break

        if self.msg_mvp_1 == "":
            self.msg_mvp_1 = "> 플레이어 정보가 없습니다."

        self.button_select = False
        embed = discord.Embed(title="> 🏆 시즌 베스트 플레이어", description="리그 오브 레전드 e스포츠의 시즌 베스트 플레이어 정보입니다.", color=colorMap['red'])
        embed.set_footer(text="TIP: 아래 버튼을 눌러 다른 포지션의 랭킹도 확인할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
        embed.set_image(url=self.banner)
        embed.add_field(name=f"'{self.picked_lane}' 포지션 ({self.picked_league})", value=self.msg_mvp_1, inline=True)
        embed.add_field(name="\u200b", value=self.msg_mvp_2, inline=True)
        await interaction.response.edit_message(content="", embed=embed, view=MvpView(self.bot, self.ctx, self.msg, self.banner, self.picked_league, self.picked_lane, self.button_select, self.box_LCK, self.box_LPL, self.box_LEC, self.box_LCS, self.box_CBLOL, self.box_VCS, self.box_LCL, self.box_TCL, self.box_PCS, self.box_LLA, self.box_LJL, self.box_LCO))


    def add_button(self):
        if (self.button_select == True) and (self.picked_lane == "탑"):
            button_top = discord.ui.Button(label="탑", style=discord.ButtonStyle.blurple, row=1)
        else:
            button_top = discord.ui.Button(label="탑", style=discord.ButtonStyle.gray, row=1)
        if (self.button_select == True) and (self.picked_lane == "정글"):
            button_jun = discord.ui.Button(label="정글", style=discord.ButtonStyle.blurple, row=1)
        else:
            button_jun = discord.ui.Button(label="정글", style=discord.ButtonStyle.gray, row=1)
        if (self.button_select == True) and (self.picked_lane == "미드"):
            button_mid = discord.ui.Button(label="미드", style=discord.ButtonStyle.blurple, row=1)
        else:
            button_mid = discord.ui.Button(label="미드", style=discord.ButtonStyle.gray, row=1)
        if (self.button_select == True) and (self.picked_lane == "원딜"):
            button_adc = discord.ui.Button(label="원딜", style=discord.ButtonStyle.blurple, row=1)
        else:
            button_adc = discord.ui.Button(label="원딜", style=discord.ButtonStyle.gray, row=1)
        if (self.button_select == True) and (self.picked_lane == "서포터"):
            button_sup = discord.ui.Button(label="서포터", style=discord.ButtonStyle.blurple, row=1)
        else:
            button_sup = discord.ui.Button(label="서포터", style=discord.ButtonStyle.gray, row=1)

        embed = discord.Embed(title="> 🏆 시즌 베스트 플레이어", description="리그 오브 레전드 e스포츠의 시즌 베스트 플레이어 정보입니다.", color=colorMap['red'])
        embed.set_footer(text="TIP: 아래 버튼을 눌러 다른 포지션의 랭킹도 확인할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
        embed.set_image(url=self.banner)

        async def callback_all(interaction: discord.Interaction):
            self.picked_lane = "모든 라인"

            if self.picked_league == "LCK": self.box_data = self.box_LCK
            elif self.picked_league == "LPL": self.box_data = self.box_LPL
            elif self.picked_league == "LEC": self.box_data = self.box_LEC
            elif self.picked_league == "LCS": self.box_data = self.box_LCS
            elif self.picked_league == "CBLOL": self.box_data = self.box_CBLOL
            elif self.picked_league == "VCS": self.box_data = self.box_VCS
            elif self.picked_league == "LCL": self.box_data = self.box_LCL
            elif self.picked_league == "TCL": self.box_data = self.box_TCL
            elif self.picked_league == "PCS": self.box_data = self.box_PCS
            elif self.picked_league == "LLA": self.box_data = self.box_LLA
            elif self.picked_league == "LJL": self.box_data = self.box_LJL
            elif self.picked_league == "LCO": self.box_data = self.box_LCO

            for i in range(5):
                if i >= len(self.box_data): break
                self.msg_mvp_1 = f"{self.msg_mvp_1}> {i + 1}위 - [{self.box_data[i]['team_acronym']}]({esports_op_gg_team}{self.box_data[i]['team_id']}) [{self.box_data[i]['nickName']}]({esports_op_gg_player}{self.box_data[i]['id']})\n[{self.box_data[i]['position']}] {self.box_data[i]['kda']} 평점\n`({self.box_data[i]['kills']} / {self.box_data[i]['deaths']} / {self.box_data[i]['assists']})`\n"

            for i in range(5, 10):
                if i >= len(self.box_data): break
                self.msg_mvp_2 = f"{self.msg_mvp_2}> {i + 1}위 - [{self.box_data[i]['team_acronym']}]({esports_op_gg_team}{self.box_data[i]['team_id']}) [{self.box_data[i]['nickName']}]({esports_op_gg_player}{self.box_data[i]['id']})\n[{self.box_data[i]['position']}] {self.box_data[i]['kda']} 평점\n`({self.box_data[i]['kills']} / {self.box_data[i]['deaths']} / {self.box_data[i]['assists']})`\n"

            if self.msg_mvp_1 == "":
                self.msg_mvp_1 = "> 플레이어 정보가 없습니다."

            self.button_select = False
            embed.add_field(name=f"'{self.picked_lane}' 포지션 ({self.picked_league})", value=self.msg_mvp_1, inline=True)
            embed.add_field(name="\u200b", value=self.msg_mvp_2, inline=True)
            await interaction.response.edit_message(content="", embed=embed, view=MvpView(self.bot, self.ctx, self.msg, self.banner, self.picked_league, self.picked_lane, self.button_select, self.box_LCK, self.box_LPL, self.box_LEC, self.box_LCS, self.box_CBLOL, self.box_VCS, self.box_LCL, self.box_TCL, self.box_PCS, self.box_LLA, self.box_LJL, self.box_LCO))

        async def callback_top(interaction: discord.Interaction):
            self.picked_lane = "탑"

            if self.picked_league == "LCK": self.box_data = self.box_LCK
            elif self.picked_league == "LPL": self.box_data = self.box_LPL
            elif self.picked_league == "LEC": self.box_data = self.box_LEC
            elif self.picked_league == "LCS": self.box_data = self.box_LCS
            elif self.picked_league == "CBLOL": self.box_data = self.box_CBLOL
            elif self.picked_league == "VCS": self.box_data = self.box_VCS
            elif self.picked_league == "LCL": self.box_data = self.box_LCL
            elif self.picked_league == "TCL": self.box_data = self.box_TCL
            elif self.picked_league == "PCS": self.box_data = self.box_PCS
            elif self.picked_league == "LLA": self.box_data = self.box_LLA
            elif self.picked_league == "LJL": self.box_data = self.box_LJL
            elif self.picked_league == "LCO": self.box_data = self.box_LCO

            for i in range(len(self.box_data)):
                if self.box_data[i]['position'] == "탑":
                    self.box_lane_data.append(self.box_data[i])

            for i in range(5):
                if i >= len(self.box_lane_data): break
                self.msg_mvp_1 = f"{self.msg_mvp_1}> {i + 1}위 - [{self.box_lane_data[i]['team_acronym']}]({esports_op_gg_team}{self.box_lane_data[i]['team_id']}) [{self.box_lane_data[i]['nickName']}]({esports_op_gg_player}{self.box_lane_data[i]['id']})\n[{self.box_lane_data[i]['position']}] {self.box_lane_data[i]['kda']} 평점\n`({self.box_lane_data[i]['kills']} / {self.box_lane_data[i]['deaths']} / {self.box_lane_data[i]['assists']})`\n"

            for i in range(5, 10):
                if i >= len(self.box_lane_data): break
                self.msg_mvp_2 = f"{self.msg_mvp_2}> {i + 1}위 - [{self.box_lane_data[i]['team_acronym']}]({esports_op_gg_team}{self.box_lane_data[i]['team_id']}) [{self.box_lane_data[i]['nickName']}]({esports_op_gg_player}{self.box_lane_data[i]['id']})\n[{self.box_lane_data[i]['position']}] {self.box_lane_data[i]['kda']} 평점\n`({self.box_lane_data[i]['kills']} / {self.box_lane_data[i]['deaths']} / {self.box_lane_data[i]['assists']})`\n"

            if self.msg_mvp_1 == "":
                self.msg_mvp_1 = "> 플레이어 정보가 없습니다."

            self.button_select = True
            embed.add_field(name=f"'{self.picked_lane}' 포지션 ({self.picked_league})", value=self.msg_mvp_1, inline=True)
            embed.add_field(name="\u200b", value=self.msg_mvp_2, inline=True)
            await interaction.response.edit_message(content="", embed=embed, view=MvpView(self.bot, self.ctx, self.msg, self.banner, self.picked_league, self.picked_lane, self.button_select, self.box_LCK, self.box_LPL, self.box_LEC, self.box_LCS, self.box_CBLOL, self.box_VCS, self.box_LCL, self.box_TCL, self.box_PCS, self.box_LLA, self.box_LJL, self.box_LCO))

        async def callback_jun(interaction: discord.Interaction):
            self.picked_lane = "정글"

            if self.picked_league == "LCK": self.box_data = self.box_LCK
            elif self.picked_league == "LPL": self.box_data = self.box_LPL
            elif self.picked_league == "LEC": self.box_data = self.box_LEC
            elif self.picked_league == "LCS": self.box_data = self.box_LCS
            elif self.picked_league == "CBLOL": self.box_data = self.box_CBLOL
            elif self.picked_league == "VCS": self.box_data = self.box_VCS
            elif self.picked_league == "LCL": self.box_data = self.box_LCL
            elif self.picked_league == "TCL": self.box_data = self.box_TCL
            elif self.picked_league == "PCS": self.box_data = self.box_PCS
            elif self.picked_league == "LLA": self.box_data = self.box_LLA
            elif self.picked_league == "LJL": self.box_data = self.box_LJL
            elif self.picked_league == "LCO": self.box_data = self.box_LCO

            for i in range(len(self.box_data)):
                if self.box_data[i]['position'] == "정글":
                    self.box_lane_data.append(self.box_data[i])

            for i in range(5):
                if i >= len(self.box_lane_data): break
                self.msg_mvp_1 = f"{self.msg_mvp_1}> {i + 1}위 - [{self.box_lane_data[i]['team_acronym']}]({esports_op_gg_team}{self.box_lane_data[i]['team_id']}) [{self.box_lane_data[i]['nickName']}]({esports_op_gg_player}{self.box_lane_data[i]['id']})\n[{self.box_lane_data[i]['position']}] {self.box_lane_data[i]['kda']} 평점\n`({self.box_lane_data[i]['kills']} / {self.box_lane_data[i]['deaths']} / {self.box_lane_data[i]['assists']})`\n"

            for i in range(5, 10):
                if i >= len(self.box_lane_data): break
                self.msg_mvp_2 = f"{self.msg_mvp_2}> {i + 1}위 - [{self.box_lane_data[i]['team_acronym']}]({esports_op_gg_team}{self.box_lane_data[i]['team_id']}) [{self.box_lane_data[i]['nickName']}]({esports_op_gg_player}{self.box_lane_data[i]['id']})\n[{self.box_lane_data[i]['position']}] {self.box_lane_data[i]['kda']} 평점\n`({self.box_lane_data[i]['kills']} / {self.box_lane_data[i]['deaths']} / {self.box_lane_data[i]['assists']})`\n"

            if self.msg_mvp_1 == "":
                self.msg_mvp_1 = "> 플레이어 정보가 없습니다."

            self.button_select = True
            embed.add_field(name=f"'{self.picked_lane}' 포지션 ({self.picked_league})", value=self.msg_mvp_1, inline=True)
            embed.add_field(name="\u200b", value=self.msg_mvp_2, inline=True)
            await interaction.response.edit_message(content="", embed=embed, view=MvpView(self.bot, self.ctx, self.msg, self.banner, self.picked_league, self.picked_lane, self.button_select, self.box_LCK, self.box_LPL, self.box_LEC, self.box_LCS, self.box_CBLOL, self.box_VCS, self.box_LCL, self.box_TCL, self.box_PCS, self.box_LLA, self.box_LJL, self.box_LCO))

        async def callback_mid(interaction: discord.Interaction):
            self.picked_lane = "미드"

            if self.picked_league == "LCK": self.box_data = self.box_LCK
            elif self.picked_league == "LPL": self.box_data = self.box_LPL
            elif self.picked_league == "LEC": self.box_data = self.box_LEC
            elif self.picked_league == "LCS": self.box_data = self.box_LCS
            elif self.picked_league == "CBLOL": self.box_data = self.box_CBLOL
            elif self.picked_league == "VCS": self.box_data = self.box_VCS
            elif self.picked_league == "LCL": self.box_data = self.box_LCL
            elif self.picked_league == "TCL": self.box_data = self.box_TCL
            elif self.picked_league == "PCS": self.box_data = self.box_PCS
            elif self.picked_league == "LLA": self.box_data = self.box_LLA
            elif self.picked_league == "LJL": self.box_data = self.box_LJL
            elif self.picked_league == "LCO": self.box_data = self.box_LCO

            for i in range(len(self.box_data)):
                if self.box_data[i]['position'] == "미드":
                    self.box_lane_data.append(self.box_data[i])

            for i in range(5):
                if i >= len(self.box_lane_data): break
                self.msg_mvp_1 = f"{self.msg_mvp_1}> {i + 1}위 - [{self.box_lane_data[i]['team_acronym']}]({esports_op_gg_team}{self.box_lane_data[i]['team_id']}) [{self.box_lane_data[i]['nickName']}]({esports_op_gg_player}{self.box_lane_data[i]['id']})\n[{self.box_lane_data[i]['position']}] {self.box_lane_data[i]['kda']} 평점\n`({self.box_lane_data[i]['kills']} / {self.box_lane_data[i]['deaths']} / {self.box_lane_data[i]['assists']})`\n"

            for i in range(5, 10):
                if i >= len(self.box_lane_data): break
                self.msg_mvp_2 = f"{self.msg_mvp_2}> {i + 1}위 - [{self.box_lane_data[i]['team_acronym']}]({esports_op_gg_team}{self.box_lane_data[i]['team_id']}) [{self.box_lane_data[i]['nickName']}]({esports_op_gg_player}{self.box_lane_data[i]['id']})\n[{self.box_lane_data[i]['position']}] {self.box_lane_data[i]['kda']} 평점\n`({self.box_lane_data[i]['kills']} / {self.box_lane_data[i]['deaths']} / {self.box_lane_data[i]['assists']})`\n"

            if self.msg_mvp_1 == "":
                self.msg_mvp_1 = "> 플레이어 정보가 없습니다."

            self.button_select = True
            embed.add_field(name=f"'{self.picked_lane}' 포지션 ({self.picked_league})", value=self.msg_mvp_1, inline=True)
            embed.add_field(name="\u200b", value=self.msg_mvp_2, inline=True)
            await interaction.response.edit_message(content="", embed=embed, view=MvpView(self.bot, self.ctx, self.msg, self.banner, self.picked_league, self.picked_lane, self.button_select, self.box_LCK, self.box_LPL, self.box_LEC, self.box_LCS, self.box_CBLOL, self.box_VCS, self.box_LCL, self.box_TCL, self.box_PCS, self.box_LLA, self.box_LJL, self.box_LCO))

        async def callback_adc(interaction: discord.Interaction):
            self.picked_lane = "원딜"

            if self.picked_league == "LCK": self.box_data = self.box_LCK
            elif self.picked_league == "LPL": self.box_data = self.box_LPL
            elif self.picked_league == "LEC": self.box_data = self.box_LEC
            elif self.picked_league == "LCS": self.box_data = self.box_LCS
            elif self.picked_league == "CBLOL": self.box_data = self.box_CBLOL
            elif self.picked_league == "VCS": self.box_data = self.box_VCS
            elif self.picked_league == "LCL": self.box_data = self.box_LCL
            elif self.picked_league == "TCL": self.box_data = self.box_TCL
            elif self.picked_league == "PCS": self.box_data = self.box_PCS
            elif self.picked_league == "LLA": self.box_data = self.box_LLA
            elif self.picked_league == "LJL": self.box_data = self.box_LJL
            elif self.picked_league == "LCO": self.box_data = self.box_LCO

            for i in range(len(self.box_data)):
                if self.box_data[i]['position'] == "원딜":
                    self.box_lane_data.append(self.box_data[i])

            for i in range(5):
                if i >= len(self.box_lane_data): break
                self.msg_mvp_1 = f"{self.msg_mvp_1}> {i + 1}위 - [{self.box_lane_data[i]['team_acronym']}]({esports_op_gg_team}{self.box_lane_data[i]['team_id']}) [{self.box_lane_data[i]['nickName']}]({esports_op_gg_player}{self.box_lane_data[i]['id']})\n[{self.box_lane_data[i]['position']}] {self.box_lane_data[i]['kda']} 평점\n`({self.box_lane_data[i]['kills']} / {self.box_lane_data[i]['deaths']} / {self.box_lane_data[i]['assists']})`\n"

            for i in range(5, 10):
                if i >= len(self.box_lane_data): break
                self.msg_mvp_2 = f"{self.msg_mvp_2}> {i + 1}위 - [{self.box_lane_data[i]['team_acronym']}]({esports_op_gg_team}{self.box_lane_data[i]['team_id']}) [{self.box_lane_data[i]['nickName']}]({esports_op_gg_player}{self.box_lane_data[i]['id']})\n[{self.box_lane_data[i]['position']}] {self.box_lane_data[i]['kda']} 평점\n`({self.box_lane_data[i]['kills']} / {self.box_lane_data[i]['deaths']} / {self.box_lane_data[i]['assists']})`\n"

            if self.msg_mvp_1 == "":
                self.msg_mvp_1 = "> 플레이어 정보가 없습니다."

            self.button_select = True
            embed.add_field(name=f"'{self.picked_lane}' 포지션 ({self.picked_league})", value=self.msg_mvp_1, inline=True)
            embed.add_field(name="\u200b", value=self.msg_mvp_2, inline=True)
            await interaction.response.edit_message(content="", embed=embed, view=MvpView(self.bot, self.ctx, self.msg, self.banner, self.picked_league, self.picked_lane, self.button_select, self.box_LCK, self.box_LPL, self.box_LEC, self.box_LCS, self.box_CBLOL, self.box_VCS, self.box_LCL, self.box_TCL, self.box_PCS, self.box_LLA, self.box_LJL, self.box_LCO))

        async def callback_sup(interaction: discord.Interaction):
            self.picked_lane = "서포터"

            if self.picked_league == "LCK": self.box_data = self.box_LCK
            elif self.picked_league == "LPL": self.box_data = self.box_LPL
            elif self.picked_league == "LEC": self.box_data = self.box_LEC
            elif self.picked_league == "LCS": self.box_data = self.box_LCS
            elif self.picked_league == "CBLOL": self.box_data = self.box_CBLOL
            elif self.picked_league == "VCS": self.box_data = self.box_VCS
            elif self.picked_league == "LCL": self.box_data = self.box_LCL
            elif self.picked_league == "TCL": self.box_data = self.box_TCL
            elif self.picked_league == "PCS": self.box_data = self.box_PCS
            elif self.picked_league == "LLA": self.box_data = self.box_LLA
            elif self.picked_league == "LJL": self.box_data = self.box_LJL
            elif self.picked_league == "LCO": self.box_data = self.box_LCO

            for i in range(len(self.box_data)):
                if self.box_data[i]['position'] == "서포터":
                    self.box_lane_data.append(self.box_data[i])

            for i in range(5):
                if i >= len(self.box_lane_data): break
                self.msg_mvp_1 = f"{self.msg_mvp_1}> {i + 1}위 - [{self.box_lane_data[i]['team_acronym']}]({esports_op_gg_team}{self.box_lane_data[i]['team_id']}) [{self.box_lane_data[i]['nickName']}]({esports_op_gg_player}{self.box_lane_data[i]['id']})\n[{self.box_lane_data[i]['position']}] {self.box_lane_data[i]['kda']} 평점\n`({self.box_lane_data[i]['kills']} / {self.box_lane_data[i]['deaths']} / {self.box_lane_data[i]['assists']})`\n"

            for i in range(5, 10):
                if i >= len(self.box_lane_data): break
                self.msg_mvp_2 = f"{self.msg_mvp_2}> {i + 1}위 - [{self.box_lane_data[i]['team_acronym']}]({esports_op_gg_team}{self.box_lane_data[i]['team_id']}) [{self.box_lane_data[i]['nickName']}]({esports_op_gg_player}{self.box_lane_data[i]['id']})\n[{self.box_lane_data[i]['position']}] {self.box_lane_data[i]['kda']} 평점\n`({self.box_lane_data[i]['kills']} / {self.box_lane_data[i]['deaths']} / {self.box_lane_data[i]['assists']})`\n"

            if self.msg_mvp_1 == "":
                self.msg_mvp_1 = "> 플레이어 정보가 없습니다."

            self.button_select = True
            embed.add_field(name=f"'{self.picked_lane}' 포지션 ({self.picked_league})", value=self.msg_mvp_1, inline=True)
            embed.add_field(name="\u200b", value=self.msg_mvp_2, inline=True)
            await interaction.response.edit_message(content="", embed=embed, view=MvpView(self.bot, self.ctx, self.msg, self.banner, self.picked_league, self.picked_lane, self.button_select, self.box_LCK, self.box_LPL, self.box_LEC, self.box_LCS, self.box_CBLOL, self.box_VCS, self.box_LCL, self.box_TCL, self.box_PCS, self.box_LLA, self.box_LJL, self.box_LCO))

        if (self.button_select == True) and (self.picked_lane == "탑"):
            button_top.callback = callback_all
        else:
            button_top.callback = callback_top
        if (self.button_select == True) and (self.picked_lane == "정글"):
            button_jun.callback = callback_all
        else:
            button_jun.callback = callback_jun
        if (self.button_select == True) and (self.picked_lane == "미드"):
            button_mid.callback = callback_all
        else:
            button_mid.callback = callback_mid
        if (self.button_select == True) and (self.picked_lane == "원딜"):
            button_adc.callback = callback_all
        else:
            button_adc.callback = callback_adc
        if (self.button_select == True) and (self.picked_lane == "서포터"):
            button_sup.callback = callback_all
        else:
            button_sup.callback = callback_sup

        self.add_item(button_top)
        self.add_item(button_jun)
        self.add_item(button_mid)
        self.add_item(button_adc)
        self.add_item(button_sup)

    async def on_timeout(self):
        try:
            await self.msg.edit_original_response(content="", view=DisabledButton())
        except discord.NotFound:
            pass


class DisabledButton(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Select(placeholder="리그 선택하기", options=[discord.SelectOption(label="asdf", value="1", description="asdf")], disabled=True, row=0))
        self.add_item(discord.ui.Button(label="탑", disabled=True, row=1))
        self.add_item(discord.ui.Button(label="정글", disabled=True, row=1))
        self.add_item(discord.ui.Button(label="미드", disabled=True, row=1))
        self.add_item(discord.ui.Button(label="원딜", disabled=True, row=1))
        self.add_item(discord.ui.Button(label="서포터", disabled=True, row=1))
        self.add_item(discord.ui.Button(label="OP.GG Esports에서 보기", url=esports_op_gg_mvp, row=2))


class MvpCMD(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    _mvps = SlashCommandGroup(name="베스트", description="MVP 명령어", guild_only=False)

    @_mvps.command(
        name="플레이어",
        description="리그 오브 레전드 e스포츠의 시즌 베스트 플레이어 정보를 보여줘요.",
    )
    @option("리그", description="리그를 선택해주세요.", required=True, autocomplete=get_league)
    async def _mvpCMD(self, ctx: discord.AutocompleteContext, 리그: str):

        picked_lane = "모든 라인"
        picked_league = 리그
        button_select = False
        banner_image_url = random.choice(config['banner_image_url'])

        box_data = {}
        box_LCK = []
        box_LPL = []
        box_LEC = []
        box_LCS = []
        box_CBLOL = []
        box_VCS = []
        box_LCL = []
        box_TCL = []
        box_PCS = []
        box_LLA = []
        box_LJL = []
        box_LCO = []

        embed = discord.Embed(title="", description="⌛ 정보를 불러오는 중...", color=colorMap['red'])
        msg = await ctx.respond(embed=embed)

        try:
            for i in range(16):
                if leagues[i]['id'] == "99": tournamentId = leagues[i]['tournamentId']
                elif leagues[i]['id'] == "98": tournamentId = leagues[i]['tournamentId']
                elif leagues[i]['id'] == "89": tournamentId = leagues[i]['tournamentId']
                elif leagues[i]['id'] == "88": tournamentId = leagues[i]['tournamentId']
                elif leagues[i]['id'] == "94": tournamentId = leagues[i]['tournamentId']
                elif leagues[i]['id'] == "90": tournamentId = leagues[i]['tournamentId']
                elif leagues[i]['id'] == "91": tournamentId = leagues[i]['tournamentId']
                elif leagues[i]['id'] == "93": tournamentId = leagues[i]['tournamentId']
                elif leagues[i]['id'] == "86": tournamentId = leagues[i]['tournamentId']
                elif leagues[i]['id'] == "87": tournamentId = leagues[i]['tournamentId']
                elif leagues[i]['id'] == "92": tournamentId = leagues[i]['tournamentId']
                elif leagues[i]['id'] == "85": tournamentId = leagues[i]['tournamentId']
                else: pass

                try:
                    if tournamentId == []: continue
                    elif tournamentId == None: continue
                    players = opgg.player_mvp_rank(tournamentId=tournamentId[0])
                    tournamentId = [] # 초기화

                    if players['error'] == False:

                        for j in range(len(players['data']['mvps'])):
                            mvp_player_id = players['data']['mvps'][j]['player']['id']
                            mvp_player_nickName = players['data']['mvps'][j]['player']['nickName']
                            mvp_player_nationality = players['data']['mvps'][j]['player']['nationality']
                            mvp_player_image = players['data']['mvps'][j]['player']['imageUrl']
                            mvp_player_position = (players['data']['mvps'][j]['position']).replace("top", "탑").replace("jun", "정글").replace("mid", "미드").replace("adc", "원딜").replace("sup", "서포터")
                            mvp_player_currently = players['data']['mvps'][j]['currently']
                            mvp_player_previously = players['data']['mvps'][j]['previously']
                            mvp_player_mvpPoint = players['data']['mvps'][j]['mvpPoint']
                            mvp_player_games = players['data']['mvps'][j]['games']
                            mvp_player_kda = (players['data']['mvps'][j]['kda']).__round__(2)
                            mvp_player_kills = (players['data']['mvps'][j]['kills']).__round__(2)
                            mvp_player_deaths = (players['data']['mvps'][j]['deaths']).__round__(2)
                            mvp_player_assists = (players['data']['mvps'][j]['assists']).__round__(2)
                            mvp_team_id = players['data']['mvps'][j]['team']['id']
                            mvp_team_name = players['data']['mvps'][j]['team']['name']
                            mvp_team_acronym = players['data']['mvps'][j]['team']['acronym']

                            box_mvp_info = {
                                "id": mvp_player_id,
                                "nickName": mvp_player_nickName,
                                "nationality": mvp_player_nationality,
                                "imageUrl": mvp_player_image,
                                "position": mvp_player_position,
                                "currently": mvp_player_currently,
                                "previously": mvp_player_previously,
                                "mvpPoint": mvp_player_mvpPoint,
                                "games": mvp_player_games,
                                "kda": mvp_player_kda,
                                "kills": mvp_player_kills,
                                "deaths": mvp_player_deaths,
                                "assists": mvp_player_assists,
                                "team_id": mvp_team_id,
                                "team_name": mvp_team_name,
                                "team_acronym": mvp_team_acronym
                            }

                            if leagues[i]['shortName'] == "LCK": box_LCK.append(box_mvp_info)
                            elif leagues[i]['shortName'] == "LPL": box_LPL.append(box_mvp_info)
                            elif leagues[i]['shortName'] == "LEC": box_LEC.append(box_mvp_info)
                            elif leagues[i]['shortName'] == "LCS": box_LCS.append(box_mvp_info)
                            elif leagues[i]['shortName'] == "CBLOL": box_CBLOL.append(box_mvp_info)
                            elif leagues[i]['shortName'] == "VCS": box_VCS.append(box_mvp_info)
                            elif leagues[i]['shortName'] == "LCL": box_LCL.append(box_mvp_info)
                            elif leagues[i]['shortName'] == "TCL": box_TCL.append(box_mvp_info)
                            elif leagues[i]['shortName'] == "PCS": box_PCS.append(box_mvp_info)
                            elif leagues[i]['shortName'] == "LLA": box_LLA.append(box_mvp_info)
                            elif leagues[i]['shortName'] == "LJL": box_LJL.append(box_mvp_info)
                            elif leagues[i]['shortName'] == "LCO": box_LCO.append(box_mvp_info)

                    else:
                        print(f"[schedule.py] {players['code']}: {players['message']}")
                        embed = discord.Embed(title="> ⚠️ 오류", description=f"Code: `{players['code']}`\nMessage: {players['message']}", color=colorMap['red'])
                        return await msg.edit_original_response(content="", embed=embed)

                except:
                    pass

            if picked_league == "LCK": box_data = box_LCK
            elif picked_league == "LPL": box_data = box_LPL
            elif picked_league == "LEC": box_data = box_LEC
            elif picked_league == "LCS": box_data = box_LCS
            elif picked_league == "CBLOL": box_data = box_CBLOL
            elif picked_league == "VCS": box_data = box_VCS
            elif picked_league == "LCL": box_data = box_LCL
            elif picked_league == "TCL": box_data = box_TCL
            elif picked_league == "PCS": box_data = box_PCS
            elif picked_league == "LLA": box_data = box_LLA
            elif picked_league == "LJL": box_data = box_LJL
            elif picked_league == "LCO": box_data = box_LCO

            msg_mvp_1 = ""
            msg_mvp_2 = ""

            for i in range(5):
                if i >= len(box_data): break
                msg_mvp_1 = f"{msg_mvp_1}> {i + 1}위 - [{box_data[i]['team_acronym']}]({esports_op_gg_team}{box_data[i]['team_id']}) [{box_data[i]['nickName']}]({esports_op_gg_player}{box_data[i]['id']})\n[{box_data[i]['position']}] {box_data[i]['kda']} 평점\n`({box_data[i]['kills']} / {box_data[i]['deaths']} / {box_data[i]['assists']})`\n"

            for i in range(5, 10):
                if i >= len(box_data): break
                msg_mvp_2 = f"{msg_mvp_2}> {i + 1}위 - [{box_data[i]['team_acronym']}]({esports_op_gg_team}{box_data[i]['team_id']}) [{box_data[i]['nickName']}]({esports_op_gg_player}{box_data[i]['id']})\n[{box_data[i]['position']}] {box_data[i]['kda']} 평점\n`({box_data[i]['kills']} / {box_data[i]['deaths']} / {box_data[i]['assists']})`\n"

            if msg_mvp_1 == "":
                msg_mvp_1 = "> 플레이어 정보가 없습니다."

            embed = discord.Embed(title="> 🏆 시즌 베스트 플레이어", description="리그 오브 레전드 e스포츠의 시즌 베스트 플레이어 정보입니다.", color=colorMap['red'])
            embed.set_footer(text="TIP: 아래 버튼을 눌러 다른 포지션의 랭킹도 확인할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
            embed.set_image(url=banner_image_url)
            embed.add_field(name=f"'{picked_lane}' 포지션 ({picked_league})", value=msg_mvp_1, inline=True)
            embed.add_field(name="\u200b", value=msg_mvp_2, inline=True)
            await msg.edit_original_response(content="", embed=embed, view=MvpView(self.bot, ctx, msg, banner_image_url, picked_league, picked_lane, button_select, box_LCK, box_LPL, box_LEC, box_LCS, box_CBLOL, box_VCS, box_LCL, box_TCL, box_PCS, box_LLA, box_LJL, box_LCO))

        except Exception as error:
            print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
            print(traceback.format_exc())



def setup(bot):
    bot.add_cog(MvpCMD(bot))
    print("mvp.py 로드 됨")
