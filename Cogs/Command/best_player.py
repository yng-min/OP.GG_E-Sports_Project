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

from Extensions.Process.league import get_player_mvp_rank

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

        self.box_player = {}
        self.box_lane_data = []
        self.msg_mvp_1 = ""
        self.msg_mvp_2 = ""
        self.button_select = button_select
        self.add_item(discord.ui.Button(label="OP.GG E-Sports에서 보기", url=esports_op_gg_mvp, row=2))
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

        if select.values[0] == "0":
            self.picked_league = "LCK"
            self.box_player = self.box_LCK
        elif select.values[0] == "1":
            self.picked_league = "LPL"
            self.box_player = self.box_LPL
        elif select.values[0] == "2":
            self.picked_league = "LEC"
            self.box_player = self.box_LEC
        elif select.values[0] == "3":
            self.picked_league = "LCS"
            self.box_player = self.box_LCS
        elif select.values[0] == "4":
            self.picked_league = "CBLOL"
            self.box_player = self.box_CBLOL
        elif select.values[0] == "5":
            self.picked_league = "VCS"
            self.box_player = self.box_VCS
        elif select.values[0] == "6":
            self.picked_league = "LCL"
            self.box_player = self.box_LCL
        elif select.values[0] == "7":
            self.picked_league = "TCL"
            self.box_player = self.box_TCL
        elif select.values[0] == "8":
            self.picked_league = "PCS"
            self.box_player = self.box_PCS
        elif select.values[0] == "9":
            self.picked_league = "LLA"
            self.box_player = self.box_LLA
        elif select.values[0] == "10":
            self.picked_league = "LJL"
            self.box_player = self.box_LJL
        elif select.values[0] == "11":
            self.picked_league = "LCO"
            self.box_player = self.box_LCO

        k = 0
        for i in range(5):
            for j in range(len(self.box_player)):
                self.msg_mvp_1 = f"{self.msg_mvp_1}> {i + 1}위 - [{self.box_player[k]['team_acronym']}]({esports_op_gg_team}{self.box_player[k]['team_id']}) [{self.box_player[k]['nickName']}]({esports_op_gg_player}{self.box_player[k]['id']})\n[{self.box_player[k]['position']}] {self.box_player[k]['kda']} 평점\n`({self.box_player[k]['kills']}/{self.box_player[k]['deaths']}/{self.box_player[k]['assists']})`\n"
                k += 1
                break

        k = 5
        for i in range(5, 10):
            for j in range(len(self.box_player)):
                self.msg_mvp_2 = f"{self.msg_mvp_2}> {i + 1}위 - [{self.box_player[k]['team_acronym']}]({esports_op_gg_team}{self.box_player[k]['team_id']}) [{self.box_player[k]['nickName']}]({esports_op_gg_player}{self.box_player[k]['id']})\n[{self.box_player[k]['position']}] {self.box_player[k]['kda']} 평점\n`({self.box_player[k]['kills']}/{self.box_player[k]['deaths']}/{self.box_player[k]['assists']})`\n"
                k += 1
                break

        if self.msg_mvp_1 == "":
            self.msg_mvp_1 = "> 플레이어 정보가 없습니다."

        self.button_select = False
        embed = discord.Embed(title="> 🏆 시즌 베스트 플레이어", description="", color=colorMap['red'])
        embed.set_footer(text="TIP: 아래 버튼을 눌러 다른 포지션의 랭킹도 확인할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
        embed.set_image(url=self.banner)
        embed.add_field(name=f"'{self.picked_lane}' 포지션 ({self.picked_league})", value=self.msg_mvp_1, inline=True)
        embed.add_field(name="\u200b", value=self.msg_mvp_2, inline=True)
        await interaction.response.edit_message(content="", embed=embed, view=MvpView(bot=self.bot, ctx=self.ctx, msg=self.msg, banner=self.banner, picked_league=self.picked_league, picked_lane=self.picked_lane, button_select=self.button_select, box_LCK=self.box_LCK, box_LPL=self.box_LPL, box_LEC=self.box_LEC, box_LCS=self.box_LCS, box_CBLOL=self.box_CBLOL, box_VCS=self.box_VCS, box_LCL=self.box_LCL, box_TCL=self.box_TCL, box_PCS=self.box_PCS, box_LLA=self.box_LLA, box_LJL=self.box_LJL, box_LCO=self.box_LCO))


    def add_button(self):
        if (self.button_select == True) and (self.picked_lane == "탑"): button_top = discord.ui.Button(label="탑", style=discord.ButtonStyle.blurple, custom_id="탑", row=1)
        else: button_top = discord.ui.Button(label="탑", style=discord.ButtonStyle.gray, custom_id="탑", row=1)
        if (self.button_select == True) and (self.picked_lane == "정글"): button_jun = discord.ui.Button(label="정글", style=discord.ButtonStyle.blurple, custom_id="정글", row=1)
        else: button_jun = discord.ui.Button(label="정글", style=discord.ButtonStyle.gray, custom_id="정글", row=1)
        if (self.button_select == True) and (self.picked_lane == "미드"): button_mid = discord.ui.Button(label="미드", style=discord.ButtonStyle.blurple, custom_id="미드", row=1)
        else: button_mid = discord.ui.Button(label="미드", style=discord.ButtonStyle.gray, custom_id="미드", row=1)
        if (self.button_select == True) and (self.picked_lane == "원딜"): button_adc = discord.ui.Button(label="원딜", style=discord.ButtonStyle.blurple, custom_id="원딜", row=1)
        else: button_adc = discord.ui.Button(label="원딜", style=discord.ButtonStyle.gray, custom_id="원딜", row=1)
        if (self.button_select == True) and (self.picked_lane == "서포터"): button_sup = discord.ui.Button(label="서포터", style=discord.ButtonStyle.blurple, custom_id="서포터", row=1)
        else: button_sup = discord.ui.Button(label="서포터", style=discord.ButtonStyle.gray, custom_id="서포터", row=1)

        embed = discord.Embed(title="> 🏆 시즌 베스트 플레이어", description="", color=colorMap['red'])
        embed.set_footer(text="TIP: 아래 버튼을 눌러 다른 포지션의 랭킹도 확인할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
        embed.set_image(url=self.banner)


        async def callback_all(interaction: discord.Interaction):
            if interaction.user.id != self.ctx.author.id: return await interaction.response.send_message("> 자신의 메시지에서만 이용할 수 있어요. 😢", ephemeral=True)

            self.picked_lane = "모든 라인"

            if self.picked_league == "LCK": self.box_player = self.box_LCK
            elif self.picked_league == "LPL": self.box_player = self.box_LPL
            elif self.picked_league == "LEC": self.box_player = self.box_LEC
            elif self.picked_league == "LCS": self.box_player = self.box_LCS
            elif self.picked_league == "CBLOL": self.box_player = self.box_CBLOL
            elif self.picked_league == "VCS": self.box_player = self.box_VCS
            elif self.picked_league == "LCL": self.box_player = self.box_LCL
            elif self.picked_league == "TCL": self.box_player = self.box_TCL
            elif self.picked_league == "PCS": self.box_player = self.box_PCS
            elif self.picked_league == "LLA": self.box_player = self.box_LLA
            elif self.picked_league == "LJL": self.box_player = self.box_LJL
            elif self.picked_league == "LCO": self.box_player = self.box_LCO

            for i in range(5):
                if i >= len(self.box_player): break
                self.msg_mvp_1 = f"{self.msg_mvp_1}> {i + 1}위 - [{self.box_player[i]['team_acronym']}]({esports_op_gg_team}{self.box_player[i]['team_id']}) [{self.box_player[i]['nickName']}]({esports_op_gg_player}{self.box_player[i]['id']})\n[{self.box_player[i]['position']}] {self.box_player[i]['kda']} 평점\n`({self.box_player[i]['kills']}/{self.box_player[i]['deaths']}/{self.box_player[i]['assists']})`\n"

            for i in range(5, 10):
                if i >= len(self.box_player): break
                self.msg_mvp_2 = f"{self.msg_mvp_2}> {i + 1}위 - [{self.box_player[i]['team_acronym']}]({esports_op_gg_team}{self.box_player[i]['team_id']}) [{self.box_player[i]['nickName']}]({esports_op_gg_player}{self.box_player[i]['id']})\n[{self.box_player[i]['position']}] {self.box_player[i]['kda']} 평점\n`({self.box_player[i]['kills']}/{self.box_player[i]['deaths']}/{self.box_player[i]['assists']})`\n"

            if self.msg_mvp_1 == "":
                self.msg_mvp_1 = "> 플레이어 정보가 없습니다."

            self.button_select = False
            embed.add_field(name=f"'{self.picked_lane}' 포지션 ({self.picked_league})", value=self.msg_mvp_1, inline=True)
            embed.add_field(name="\u200b", value=self.msg_mvp_2, inline=True)
            await interaction.response.edit_message(content="", embed=embed, view=MvpView(bot=self.bot, ctx=self.ctx, msg=self.msg, banner=self.banner, picked_league=self.picked_league, picked_lane=self.picked_lane, button_select=self.button_select, box_LCK=self.box_LCK, box_LPL=self.box_LPL, box_LEC=self.box_LEC, box_LCS=self.box_LCS, box_CBLOL=self.box_CBLOL, box_VCS=self.box_VCS, box_LCL=self.box_LCL, box_TCL=self.box_TCL, box_PCS=self.box_PCS, box_LLA=self.box_LLA, box_LJL=self.box_LJL, box_LCO=self.box_LCO))


        async def callback_lane(interaction: discord.Interaction):
            if interaction.user.id != self.ctx.author.id: return await interaction.response.send_message("> 자신의 메시지에서만 이용할 수 있어요. 😢", ephemeral=True)

            self.picked_lane = interaction.custom_id

            if self.picked_league == "LCK": self.box_player = self.box_LCK
            elif self.picked_league == "LPL": self.box_player = self.box_LPL
            elif self.picked_league == "LEC": self.box_player = self.box_LEC
            elif self.picked_league == "LCS": self.box_player = self.box_LCS
            elif self.picked_league == "CBLOL": self.box_player = self.box_CBLOL
            elif self.picked_league == "VCS": self.box_player = self.box_VCS
            elif self.picked_league == "LCL": self.box_player = self.box_LCL
            elif self.picked_league == "TCL": self.box_player = self.box_TCL
            elif self.picked_league == "PCS": self.box_player = self.box_PCS
            elif self.picked_league == "LLA": self.box_player = self.box_LLA
            elif self.picked_league == "LJL": self.box_player = self.box_LJL
            elif self.picked_league == "LCO": self.box_player = self.box_LCO

            for i in range(len(self.box_player)):
                if self.box_player[i]['position'] == self.picked_lane:
                    self.box_lane_data.append(self.box_player[i])

            for i in range(5):
                if i >= len(self.box_lane_data): break
                self.msg_mvp_1 = f"{self.msg_mvp_1}> {i + 1}위 - [{self.box_lane_data[i]['team_acronym']}]({esports_op_gg_team}{self.box_lane_data[i]['team_id']}) [{self.box_lane_data[i]['nickName']}]({esports_op_gg_player}{self.box_lane_data[i]['id']})\n[{self.box_lane_data[i]['position']}] {self.box_lane_data[i]['kda']} 평점\n`({self.box_lane_data[i]['kills']}/{self.box_lane_data[i]['deaths']}/{self.box_lane_data[i]['assists']})`\n"

            for i in range(5, 10):
                if i >= len(self.box_lane_data): break
                self.msg_mvp_2 = f"{self.msg_mvp_2}> {i + 1}위 - [{self.box_lane_data[i]['team_acronym']}]({esports_op_gg_team}{self.box_lane_data[i]['team_id']}) [{self.box_lane_data[i]['nickName']}]({esports_op_gg_player}{self.box_lane_data[i]['id']})\n[{self.box_lane_data[i]['position']}] {self.box_lane_data[i]['kda']} 평점\n`({self.box_lane_data[i]['kills']}/{self.box_lane_data[i]['deaths']}/{self.box_lane_data[i]['assists']})`\n"

            if self.msg_mvp_1 == "":
                self.msg_mvp_1 = "> 플레이어 정보가 없습니다."

            self.button_select = True
            embed.add_field(name=f"'{self.picked_lane}' 포지션 ({self.picked_league})", value=self.msg_mvp_1, inline=True)
            embed.add_field(name="\u200b", value=self.msg_mvp_2, inline=True)
            await interaction.response.edit_message(content="", embed=embed, view=MvpView(bot=self.bot, ctx=self.ctx, msg=self.msg, banner=self.banner, picked_league=self.picked_league, picked_lane=self.picked_lane, button_select=self.button_select, box_LCK=self.box_LCK, box_LPL=self.box_LPL, box_LEC=self.box_LEC, box_LCS=self.box_LCS, box_CBLOL=self.box_CBLOL, box_VCS=self.box_VCS, box_LCL=self.box_LCL, box_TCL=self.box_TCL, box_PCS=self.box_PCS, box_LLA=self.box_LLA, box_LJL=self.box_LJL, box_LCO=self.box_LCO))

        if self.button_select == True:
            if self.picked_lane == "탑": button_top.callback = callback_all
            else: button_top.callback = callback_lane
            if self.picked_lane == "정글": button_jun.callback = callback_all
            else: button_jun.callback = callback_lane
            if self.picked_lane == "미드": button_mid.callback = callback_all
            else: button_mid.callback = callback_lane
            if self.picked_lane == "원딜": button_adc.callback = callback_all
            else: button_adc.callback = callback_lane
            if self.picked_lane == "서포터": button_sup.callback = callback_all
            else: button_sup.callback = callback_lane
        else:
            button_top.callback = callback_lane
            button_jun.callback = callback_lane
            button_mid.callback = callback_lane
            button_adc.callback = callback_lane
            button_sup.callback = callback_lane

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
        self.add_item(discord.ui.Button(label="OP.GG E-Sports에서 보기", url=esports_op_gg_mvp, row=2))


class MvpCMD(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    _mvp = SlashCommandGroup(name="베스트", description="MVP 명령어", guild_only=False)

    @_mvp.command(
        name="플레이어",
        description="리그 오브 레전드 e스포츠의 시즌 베스트 플레이어 정보를 보여줘요.",
    )
    @option("리그", description="리그를 선택해주세요.", required=True, autocomplete=get_league)
    async def _mvpCMD(self, ctx: discord.AutocompleteContext, 리그: str):

        picked_lane = "모든 라인"
        picked_league = 리그
        button_select = False
        banner_image_url = random.choice(config['banner_image_url'])

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

                if tournamentId == []: continue
                elif tournamentId == None: continue
                players = get_player_mvp_rank(tournamentId=tournamentId)
                tournamentId = [] # 초기화

                if leagues[i]['shortName'] == "LCK": box_LCK.append(players)
                elif leagues[i]['shortName'] == "LPL": box_LPL.append(players)
                elif leagues[i]['shortName'] == "LEC": box_LEC.append(players)
                elif leagues[i]['shortName'] == "LCS": box_LCS.append(players)
                elif leagues[i]['shortName'] == "CBLOL": box_CBLOL.append(players)
                elif leagues[i]['shortName'] == "VCS": box_VCS.append(players)
                elif leagues[i]['shortName'] == "LCL": box_LCL.append(players)
                elif leagues[i]['shortName'] == "TCL": box_TCL.append(players)
                elif leagues[i]['shortName'] == "PCS": box_PCS.append(players)
                elif leagues[i]['shortName'] == "LLA": box_LLA.append(players)
                elif leagues[i]['shortName'] == "LJL": box_LJL.append(players)
                elif leagues[i]['shortName'] == "LCO": box_LCO.append(players)

            try: box_LCK = box_LCK[0]
            except: pass
            try: box_LPL = box_LPL[0]
            except: pass
            try: box_LEC = box_LEC[0]
            except: pass
            try: box_LCS = box_LCS[0]
            except: pass
            try: box_CBLOL = box_CBLOL[0]
            except: pass
            try: box_VCS = box_VCS[0]
            except: pass
            try: box_LCL = box_LCL[0]
            except: pass
            try: box_TCL = box_TCL[0]
            except: pass
            try: box_PCS = box_PCS[0]
            except: pass
            try: box_LLA = box_LLA[0]
            except: pass
            try: box_LJL = box_LJL[0]
            except: pass
            try: box_LCO = box_LCO[0]
            except: pass

            if picked_league == "LCK": box_player = box_LCK
            elif picked_league == "LPL": box_player = box_LPL
            elif picked_league == "LEC": box_player = box_LEC
            elif picked_league == "LCS": box_player = box_LCS
            elif picked_league == "CBLOL": box_player = box_CBLOL
            elif picked_league == "VCS": box_player = box_VCS
            elif picked_league == "LCL": box_player = box_LCL
            elif picked_league == "TCL": box_player = box_TCL
            elif picked_league == "PCS": box_player = box_PCS
            elif picked_league == "LLA": box_player = box_LLA
            elif picked_league == "LJL": box_player = box_LJL
            elif picked_league == "LCO": box_player = box_LCO

            try:
                print(f"[best_player.py] {box_player['code']}: {box_player['message']}")
                embed = discord.Embed(title="> ⚠️ 오류", description=f"Code: `{box_player['code']}`\nMessage: {box_player['message']}", color=colorMap['red'])
                return await msg.edit_original_response(content="", embed=embed)

            except:
                msg_mvp_1 = ""
                msg_mvp_2 = ""

                for j in range(5):
                    if j >= len(box_player): break
                    msg_mvp_1 = f"{msg_mvp_1}> {j + 1}위 - [{box_player[j]['team_acronym']}]({esports_op_gg_team}{box_player[j]['team_id']}) [{box_player[j]['nickName']}]({esports_op_gg_player}{box_player[j]['id']})\n[{box_player[j]['position']}] {box_player[j]['kda']} 평점\n`({box_player[j]['kills']}/{box_player[j]['deaths']}/{box_player[j]['assists']})`\n"

                for j in range(5, 10):
                    if j >= len(box_player): break
                    msg_mvp_2 = f"{msg_mvp_2}> {j + 1}위 - [{box_player[j]['team_acronym']}]({esports_op_gg_team}{box_player[j]['team_id']}) [{box_player[j]['nickName']}]({esports_op_gg_player}{box_player[j]['id']})\n[{box_player[j]['position']}] {box_player[j]['kda']} 평점\n`({box_player[j]['kills']}/{box_player[j]['deaths']}/{box_player[j]['assists']})`\n"

                if msg_mvp_1 == "":
                    msg_mvp_1 = "> 플레이어 정보가 없습니다."

                embed = discord.Embed(title="> 🏆 시즌 베스트 플레이어", description="", color=colorMap['red'])
                embed.set_footer(text="TIP: 아래 버튼을 눌러 다른 포지션의 랭킹도 확인할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
                embed.set_image(url=banner_image_url)
                embed.add_field(name=f"'{picked_lane}' 포지션 ({picked_league})", value=msg_mvp_1, inline=True)
                embed.add_field(name="\u200b", value=msg_mvp_2, inline=True)
                await msg.edit_original_response(content="", embed=embed, view=MvpView(bot=self.bot, ctx=ctx, msg=msg, banner=banner_image_url, picked_league=picked_league, picked_lane=picked_lane, button_select=button_select, box_LCK=box_LCK, box_LPL=box_LPL, box_LEC=box_LEC, box_LCS=box_LCS, box_CBLOL=box_CBLOL, box_VCS=box_VCS, box_LCL=box_LCL, box_TCL=box_TCL, box_PCS=box_PCS, box_LLA=box_LLA, box_LJL=box_LJL, box_LCO=box_LCO))

        except Exception as error:
            print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
            print(traceback.format_exc())



def setup(bot):
    bot.add_cog(MvpCMD(bot))
    print("best_player.py 로드 됨")
