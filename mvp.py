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
    else:
        return ["LCK", "LPL", "LEC", "LCS", "CBLOL", "VCS", "LCL", "TCL", "PCS", "LLA", "LJL"]


class MvpButton(discord.ui.View):

    def __init__(self, bot, ctx, msg, banner, picked_league, picked_lane, box_mvp_player_id, box_mvp_player_nickName, box_mvp_player_nationality, box_mvp_player_image, box_mvp_player_position, box_mvp_player_currently, box_mvp_player_previously, box_mvp_player_mvpPoint, box_mvp_player_games, box_mvp_player_kda, box_mvp_player_kills, box_mvp_player_deaths, box_mvp_player_assists, box_mvp_team_id, box_mvp_team_name, box_mvp_team_acronym):
        super().__init__(timeout=60)
        self.bot = bot
        self.ctx = ctx
        self.msg = msg
        self.banner = banner
        self.picked_league = picked_league
        self.picked_lane = picked_lane
        self.box_mvp_player_id = box_mvp_player_id
        self.box_mvp_player_nickName = box_mvp_player_nickName
        self.box_player_nationality = box_mvp_player_nationality
        self.box_mvp_player_image = box_mvp_player_image
        self.box_mvp_player_position = box_mvp_player_position
        self.box_mvp_player_currently = box_mvp_player_currently
        self.box_mvp_player_previously = box_mvp_player_previously
        self.box_mvp_player_mvpPoint = box_mvp_player_mvpPoint
        self.box_mvp_player_games = box_mvp_player_games
        self.box_mvp_player_kda = box_mvp_player_kda
        self.box_mvp_player_kills = box_mvp_player_kills
        self.box_mvp_player_deaths = box_mvp_player_deaths
        self.box_mvp_player_assists = box_mvp_player_assists
        self.box_mvp_team_id = box_mvp_team_id
        self.box_mvp_team_name = box_mvp_team_name
        self.box_mvp_team_acronym = box_mvp_team_acronym

        self.box_select = []
        self.schedules_1 = []
        self.schedules_2 = []
        self.schedules_3 = []
        self.msg_schedule_1 = ""
        self.msg_schedule_2 = ""
        self.msg_schedule_3 = ""
        self.league_1_max = False
        self.league_2_max = False
        self.league_3_max = False
        self.button = ""
        self.callback_select = False
        self.add_item(discord.ui.Button(label="OP.GG Esports에서 보기", url=esports_op_gg_mvp, row=1))

    @discord.ui.select(
        placeholder="리그 선택하기",
        min_values=1,
        max_values=16,
        options=[
            discord.SelectOption(label="LCK / KR", value="1", description="League of Legends Champions Korea"),
            discord.SelectOption(label="LPL / CN ", value="2", description="League of Legends Pro League"),
            discord.SelectOption(label="LEC / EU", value="3", description="League of Legends European Championship"),
            discord.SelectOption(label="LCS / NA", value="4", description="League of Legends Championship Series"),
            discord.SelectOption(label="LCO / OCE", value="5", description="League of Legends Circuit Oceania"),
            discord.SelectOption(label="PCS / SEA", value="6", description="Pacific Championship Series"),
            discord.SelectOption(label="LLA / LAT", value="7", description="Liga Latinoamérica"),
            discord.SelectOption(label="VCS / VN", value="8", description="Vietnam Championship Series"),
            discord.SelectOption(label="LCL / CIS", value="9", description="League of Legends Continental League"),
            discord.SelectOption(label="LJL / JP", value="10", description="League of Legends Japan League"),
            discord.SelectOption(label="TCL / TR", value="11", description="Turkish Championship League"),
            discord.SelectOption(label="CBLOL / BR", value="12", description="Campeonato Brasileiro de League of Legends"),
        ],
        row=0
    )
    async def select_callback(self, select: discord.ui.Select, interaction):
        self.msg_schedule_1 = ""
        self.msg_schedule_2 = ""
        self.msg_schedule_3 = ""
        self.league_1_max = False
        self.league_2_max = False
        self.league_3_max = False

        for i in range(len(select.values)):
            if select.values[i] == "1": self.box_select.append("LCK")
            elif select.values[i] == "2": self.box_select.append("LPL")
            elif select.values[i] == "3": self.box_select.append("LEC")
            elif select.values[i] == "4": self.box_select.append("LCS")
            elif select.values[i] == "5": self.box_select.append("LCO")
            elif select.values[i] == "6": self.box_select.append("PCS")
            elif select.values[i] == "7": self.box_select.append("LLA")
            elif select.values[i] == "8": self.box_select.append("VCS")
            elif select.values[i] == "9": self.box_select.append("LCL")
            elif select.values[i] == "10": self.box_select.append("LJL")
            elif select.values[i] == "11": self.box_select.append("TCL")
            elif select.values[i] == "12": self.box_select.append("CBLOL")
            else: pass


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
        description="리그 오브 레전드 리그의 베스트 플레이어 정보를 보여줘요.",
    )
    @option("리그", description="리그를 선택해주세요.", required=True, autocomplete=get_league)
    async def _mvpCMD(self, ctx: discord.AutocompleteContext, 리그: str):

        picked_lane = "모든 라인"
        picked_league = 리그
        banner_image_url = random.choice(config['banner_image_url'])

        embed = discord.Embed(title="", description="⌛ 정보를 불러오는 중...", color=colorMap['red'])
        msg = await ctx.respond(embed=embed)

        try:
            for i in range(16):
                if   leagues[i]['id'] == "99": tournamentId = leagues[i]['tournamentId']
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
                else: pass

                if tournamentId == []: continue
                elif tournamentId == None: continue
                players = opgg.player_mvp_rank(tournamentId=tournamentId[0])
                tournamentId = [] # 초기화

                if players['error'] == False:

                    box_mvp_player_id = []
                    box_mvp_player_nickName = []
                    box_mvp_player_nationality = []
                    box_mvp_player_image = []
                    box_mvp_player_position = []
                    box_mvp_player_currently = []
                    box_mvp_player_previously = []
                    box_mvp_player_mvpPoint = []
                    box_mvp_player_games = []
                    box_mvp_player_kda = []
                    box_mvp_player_kills = []
                    box_mvp_player_deaths = []
                    box_mvp_player_assists = []
                    box_mvp_team_id = []
                    box_mvp_team_name = []
                    box_mvp_team_acronym = []

                    box_LCK = []
                    box_LPL = []
                    box_LEC = []
                    box_LCS = []
                    box_LCO = []
                    box_PCS = []
                    box_LLA = []
                    box_VCS = []
                    box_LCL = []
                    box_LJL = []
                    box_TCL = []
                    box_CBLOL = []

                    for i in range(len(players['data']['mvps'])):
                        mvp_player_id = players['data']['mvps'][i]['player']['id']
                        mvp_player_nickName = players['data']['mvps'][i]['player']['nickName']
                        mvp_player_nationality = players['data']['mvps'][i]['player']['nationality']
                        mvp_player_image = players['data']['mvps'][i]['player']['imageUrl']
                        mvp_player_position = (players['data']['mvps'][i]['position']).replace("top", "탑").replace("jun", "정글").replace("mid", "미드").replace("adc", "원딜").replace("sup", "서포터")
                        mvp_player_currently = players['data']['mvps'][i]['currently']
                        mvp_player_previously = players['data']['mvps'][i]['previously']
                        mvp_player_mvpPoint = players['data']['mvps'][i]['mvpPoint']
                        mvp_player_games = players['data']['mvps'][i]['games']
                        mvp_player_kda = (players['data']['mvps'][i]['kda']).__round__(2)
                        mvp_player_kills = (players['data']['mvps'][i]['kills']).__round__(2)
                        mvp_player_deaths = (players['data']['mvps'][i]['deaths']).__round__(2)
                        mvp_player_assists = (players['data']['mvps'][i]['assists']).__round__(2)
                        mvp_team_id = players['data']['mvps'][i]['team']['id']
                        mvp_team_name = players['data']['mvps'][i]['team']['name']
                        mvp_team_acronym = players['data']['mvps'][i]['team']['acronym']

                        # box_mvp_player_id.append(mvp_player_id)
                        # box_mvp_player_nickName.append(mvp_player_nickName)
                        # box_mvp_player_nationality.append(mvp_player_nationality)
                        # box_mvp_player_image.append(mvp_player_image)
                        # box_mvp_player_position.append(mvp_player_position)
                        # box_mvp_player_currently.append(mvp_player_currently)
                        # box_mvp_player_previously.append(mvp_player_previously)
                        # box_mvp_player_mvpPoint.append(mvp_player_mvpPoint)
                        # box_mvp_player_games.append(mvp_player_games)
                        # box_mvp_player_kda.append(mvp_player_kda)
                        # box_mvp_player_kills.append(mvp_player_kills)
                        # box_mvp_player_deaths.append(mvp_player_deaths)
                        # box_mvp_player_assists.append(mvp_player_assists)
                        # box_mvp_team_id.append(mvp_team_id)
                        # box_mvp_team_name.append(mvp_team_name)
                        # box_mvp_team_acronym.append(mvp_team_acronym)

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
                        elif leagues[i]['shortName'] == "LCO": box_LCO.append(box_mvp_info)
                        elif leagues[i]['shortName'] == "PCS": box_PCS.append(box_mvp_info)
                        elif leagues[i]['shortName'] == "LLA": box_LLA.append(box_mvp_info)
                        elif leagues[i]['shortName'] == "VCS": box_VCS.append(box_mvp_info)
                        elif leagues[i]['shortName'] == "LCL": box_LCL.append(box_mvp_info)
                        elif leagues[i]['shortName'] == "LJL": box_LJL.append(box_mvp_info)
                        elif leagues[i]['shortName'] == "CBLOL": box_CBLOL.append(box_mvp_info)

                msg_mvp_info_1 = ""
                for i in range(16):
                    if 
                    for j in range(len(box_mvp_info[i])):
                    msg_mvp_info_1 = f"{msg_mvp_info_1}**{i + 1}위** - {box_mvp_info[i]} {box_mvp_player_nickName[i]} ({box_mvp_player_position[i]})\n└ {box_mvp_player_kda[i]} 평점 `({box_mvp_player_kills[i]} / {box_mvp_player_deaths[i]} / {box_mvp_player_assists[i]})`\n\n"

                embed = discord.Embed(title="> 🏆 베스트 플레이어", description="리그 오브 레전드의 리그 베스트 플레이어 정보입니다.", color=colorMap['red'])
                embed.set_footer(text="TIP: 아래 버튼을 눌러 다른 포지션의 랭킹도 확인할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
                embed.set_image(url=banner_image_url)
                embed.add_field(name=f"'{picked_lane}' 포지션 ({picked_league})", value=f"{msg_mvp_info_1}", inline=False)
                # await msg.edit_original_response(content="", embed=embed)
                await msg.edit_original_response(content="", embed=embed, view=MvpButton(self.bot, ctx, msg, banner_image_url, picked_league, picked_lane, box_mvp_player_id, box_mvp_player_nickName, box_mvp_player_nationality box_mvp_player_image, box_mvp_player_position, box_mvp_player_currently, box_mvp_player_previously, box_mvp_player_mvpPoint, box_mvp_player_games, box_mvp_player_kda, box_mvp_player_kills, box_mvp_player_deaths, box_mvp_player_assists, box_mvp_team_id, box_mvp_team_name, box_mvp_team_acronym))

        except Exception as error:
            print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
            print(traceback.format_exc())



def setup(bot):
    bot.add_cog(MvpCMD(bot))
    print("mvp.py 로드 됨")
