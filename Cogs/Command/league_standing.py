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

esports_op_gg_standing = "https://esports.op.gg/standing"
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


def get_league_standings(tournamentId):

    box_team = []
    team_id = ""
    team_name = ""
    team_acronym = ""
    team_nationality = ""
    team_foundedAt = ""
    team_imageUrl = ""
    team_youtube = ""
    team_twitter = ""
    team_instagram = ""
    team_facebook = ""
    team_website = ""
    team_position = ""
    team_previously = ""
    team_setWin = ""
    team_setLose = ""
    team_recentMatches = ""

    teams_info = opgg.league_standing(tournamentId=tournamentId[0])

    if teams_info['error'] == False:
        for i in range(len(teams_info['data'])):
            team_id = teams_info['data'][i]['team']['id']
            team_name = teams_info['data'][i]['team']['name']
            team_acronym = teams_info['data'][i]['team']['acronym']
            team_nationality = teams_info['data'][i]['team']['nationality']
            team_foundedAt = teams_info['data'][i]['team']['foundedAt']
            team_imageUrl = teams_info['data'][i]['team']['imageUrl']
            team_youtube = teams_info['data'][i]['team']['youtube']
            team_twitter = teams_info['data'][i]['team']['twitter']
            team_instagram = teams_info['data'][i]['team']['instagram']
            team_facebook = teams_info['data'][i]['team']['facebook']
            team_website = teams_info['data'][i]['team']['website']
            team_position = teams_info['data'][i]['position']
            team_previously = teams_info['data'][i]['previously']
            team_point = teams_info['data'][i]['point']
            team_win = teams_info['data'][i]['win']
            team_lose = teams_info['data'][i]['lose']
            team_setWin = teams_info['data'][i]['setWin']
            team_setLose = teams_info['data'][i]['setLose']
            team_recentMatches = teams_info['data'][i]['recentMatches']

            box_team.append({
                "id": team_id,
                "name": team_name,
                "acronym": team_acronym,
                "nationality": team_nationality,
                "foundedAt": team_foundedAt,
                "imageUrl": team_imageUrl,
                "youtube": team_youtube,
                "twitter": team_twitter,
                "instagram": team_instagram,
                "facebook": team_facebook,
                "website": team_website,
                "position": team_position,
                "previously": team_previously,
                "point": team_point,
                "win": team_win,
                "lose": team_lose,
                "setWin": team_setWin,
                "setLose": team_setLose,
                "recentMatches": team_recentMatches
            })

        box_recentMatches = get_recentMatches(team_recentMatches)

    else:
        return teams_info

    return box_team


def get_teamInfo(tournamentId, teams_id):

    box_player = []
    player_templete = {}
    player_check_top = False
    player_check_jun = False
    player_check_mid = False
    player_check_adc = False
    player_check_sup = False
    player_id = ""
    player_nickName = ""
    player_firstName = ""
    player_lastName = ""
    player_position = ""
    player_nationality = ""
    player_imageUrl = ""
    player_birthday = ""
    player_stream = ""
    player_youtube = ""
    player_twitter = ""
    player_instagram = ""
    player_facebook = ""
    player_discord = ""
    player_team_id = ""
    player_team_name = ""
    player_team_acronym = ""
    player_team_imageUrl = ""
    player_stat_games = ""
    player_stat_winRate = ""
    player_stat_wins = ""
    player_stat_loses = ""
    player_stat_kills = ""
    player_stat_deaths = ""
    player_stat_assists = ""
    player_stat_kda = ""
    player_stat_dpm = ""
    player_stat_dtpm = ""
    player_stat_gpm = ""
    player_stat_cspm = ""
    player_stat_dpgr = ""
    player_stat_firstBlood = ""
    player_stat_firstTower = ""
    player_stat_wardsPlaced = ""
    player_stat_wardsKilled = ""

    if tournamentId == None: return None
    players_info = opgg.player_info_by_team(tournamentId[0], teams_id)

    if players_info['error'] == False:
        for i in range(len(players_info['data'])):
            for j in range(len(players_info['data'])):
                player_id = players_info['data'][j]['player']['id']
                player_nickName = players_info['data'][j]['player']['nickName']
                player_firstName = players_info['data'][j]['player']['firstName']
                player_lastName = players_info['data'][j]['player']['lastName']
                player_position = players_info['data'][j]['player']['position'].replace("top", "탑").replace("jun", "정글").replace("mid", "미드").replace("adc", "원딜").replace("sup", "서포터")
                player_nationality = players_info['data'][j]['player']['nationality']
                player_imageUrl = players_info['data'][j]['player']['imageUrl']
                player_birthday = players_info['data'][j]['player']['birthday']
                player_stream = players_info['data'][j]['player']['stream']
                player_youtube = players_info['data'][j]['player']['youtube']
                player_twitter = players_info['data'][j]['player']['twitter']
                player_instagram = players_info['data'][j]['player']['instagram']
                player_facebook = players_info['data'][j]['player']['facebook']
                player_discord = players_info['data'][j]['player']['discord']
                player_team_id = players_info['data'][j]['playerStat']['team']['id']
                player_team_name = players_info['data'][j]['playerStat']['team']['name']
                player_team_acronym = players_info['data'][j]['playerStat']['team']['acronym']
                player_team_imageUrl = players_info['data'][j]['playerStat']['team']['imageUrl']
                player_stat_games = players_info['data'][j]['playerStat']['games']
                player_stat_winRate = (players_info['data'][j]['playerStat']['winRate'] * 100).__round__(2)
                player_stat_wins = players_info['data'][j]['playerStat']['wins']
                player_stat_loses = players_info['data'][j]['playerStat']['loses']
                player_stat_kills = players_info['data'][j]['playerStat']['kills'].__round__(2)
                player_stat_deaths = players_info['data'][j]['playerStat']['deaths'].__round__(2)
                player_stat_assists = players_info['data'][j]['playerStat']['assists'].__round__(2)
                player_stat_kda = players_info['data'][j]['playerStat']['kda'].__round__(2)
                player_stat_dpm = players_info['data'][j]['playerStat']['dpm'].__round__(2)
                player_stat_dtpm = players_info['data'][j]['playerStat']['dtpm'].__round__(2)
                player_stat_gpm = players_info['data'][j]['playerStat']['gpm'].__round__(2)
                player_stat_cspm = players_info['data'][j]['playerStat']['cspm'].__round__(2)
                player_stat_dpgr = players_info['data'][j]['playerStat']['dpgr'].__round__(2)
                player_stat_firstBlood = (players_info['data'][j]['playerStat']['firstBlood'] * 100).__round__(2)
                player_stat_firstTower = (players_info['data'][j]['playerStat']['firstTower'] * 100).__round__(2)
                player_stat_wardsPlaced = players_info['data'][j]['playerStat']['wardsPlaced'].__round__(2)
                player_stat_wardsKilled = players_info['data'][j]['playerStat']['wardsKilled'].__round__(2)

                player_templete = {
                    "id": player_id,
                    "nickName": player_nickName,
                    "firstName": player_firstName,
                    "lastName": player_lastName,
                    "position": player_position,
                    "nationality": player_nationality,
                    "imageUrl": player_imageUrl,
                    "birthday": player_birthday,
                    "stream": player_stream,
                    "youtube": player_youtube,
                    "twitter": player_twitter,
                    "instagram": player_instagram,
                    "facebook": player_facebook,
                    "discord": player_discord,
                    "team_id": player_team_id,
                    "team_name": player_team_name,
                    "team_acronym": player_team_acronym,
                    "team_imageUrl": player_team_imageUrl,
                    "stat_games": player_stat_games,
                    "stat_winRate": player_stat_winRate,
                    "stat_wins": player_stat_wins,
                    "stat_loses": player_stat_loses,
                    "stat_kills": player_stat_kills,
                    "stat_deaths": player_stat_deaths,
                    "stat_assists": player_stat_assists,
                    "stat_kda": player_stat_kda,
                    "stat_dpm": player_stat_dpm,
                    "stat_dtpm": player_stat_dtpm,
                    "stat_gpm": player_stat_gpm,
                    "stat_cspm": player_stat_cspm,
                    "stat_dpgr": player_stat_dpgr,
                    "stat_firstBlood": player_stat_firstBlood,
                    "stat_firstTower": player_stat_firstTower,
                    "stat_wardsPlaced": player_stat_wardsPlaced,
                    "stat_wardsKilled": player_stat_wardsKilled
                }

                if (player_check_top == False) and (player_position == "탑"):
                    box_player.append(player_templete)
                    player_check_top = True
                if (player_check_top == True) and (player_check_jun == False) and (player_position == "정글"):
                    box_player.append(player_templete)
                    player_check_jun = True
                if (player_check_top == True) and (player_check_jun == True) and (player_check_mid == False) and (player_position == "미드"):
                    box_player.append(player_templete)
                    player_check_mid = True
                if (player_check_top == True) and (player_check_jun == True) and (player_check_mid == True) and (player_check_adc == False) and (player_position == "원딜"):
                    box_player.append(player_templete)
                    player_check_adc = True
                if (player_check_top == True) and (player_check_jun == True) and (player_check_mid == True) and (player_check_adc == True) and (player_check_sup == False) and (player_position == "서포터"):
                    box_player.append(player_templete)
                    player_check_sup = True

    else:
        return players_info

    return box_player


def get_recentMatches(recentMatches):

    box_recentMatches = {}

    for i in range(len(recentMatches)):
        match_info = opgg.match_info_by_id(recentMatches[i]['id'])

        match_id = match_info['data'][0]['id']
        match_name = match_info['data'][0]['name']
        match_originalScheduledAt = match_info['data'][0]['originalScheduledAt']
        match_scheduledAt = match_info['data'][0]['scheduledAt']
        match_beginAt = match_info['data'][0]['beginAt']
        match_endAt = match_info['data'][0]['endAt']
        match_status = match_info['data'][0]['status']
        match_numberOfGames = match_info['data'][0]['numberOfGames']
        match_liveSupported = match_info['data'][0]['liveSupported']
        match_liveOpensAt = match_info['data'][0]['liveOpensAt']
        match_streams = match_info['data'][0]['streams']
        match_homeTeam = match_info['data'][0]['homeTeam']
        match_awayTeam = match_info['data'][0]['awayTeam']
        match_ranks = match_info['data'][0]['ranks']

        box_recentMatches[match_id] = {
            "id": match_id,
            "name": match_name,
            "originalScheduledAt": match_originalScheduledAt,
            "scheduledAt": match_scheduledAt,
            "beginAt": match_beginAt,
            "endAt": match_endAt,
            "status": match_status,
            "numberOfGames": match_numberOfGames,
            "liveSupported": match_liveSupported,
            "liveOpensAt": match_liveOpensAt,
            "streams": match_streams,
            "homeTeam": match_homeTeam,
            "awayTeam": match_awayTeam,
            "ranks": match_ranks
        }
        # print("2", i)

    return box_recentMatches


class StandingView(discord.ui.View):

    def __init__(self, bot, ctx, msg, banner, picked_league, button_select, button_select_index, teams_id):
        super().__init__(timeout=60)
        self.bot = bot
        self.ctx = ctx
        self.msg = msg
        self.banner = banner
        self.picked_league = picked_league
        self.teams_id = teams_id
        # self.box_recentMatches = box_recentMatches

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
                embed = discord.Embed(title="> 🏅 시즌 리그 순위", description="리그 오브 레전드 e스포츠의 시즌 팀 순위 정보입니다.", color=colorMap['red'])
                embed.set_image(url=self.banner)
                embed.add_field(name=f"'{self.picked_league}' 리그 정보", value="> 순위 정보가 없습니다.", inline=False)
                return await interaction.response.edit_message(content="", embed=embed, view=StandingView(self.bot, self.ctx, self.msg, self.banner, self.picked_league, True, self.teams_id_index, self.teams_id))
            self.box_team = get_league_standings(tournamentId)
            tournamentId = [] # 초기화

            try:
                print(f"[league_standing.py] {self.box_team['code']}: {self.box_team['message']}")
                embed = discord.Embed(title="> ⚠️ 오류", description=f"Code: `{self.box_team['code']}`\nMessage: {self.box_team['message']}", color=colorMap['red'])
                return await interaction.response.edit_message(content="", embed=embed, view=None)

            except:
                if self.box_team:
                    self.teams_id = []
                    for i in range(len(self.box_team)):
                        self.teams_id.append(self.box_team[i]['id'])

                    embed = discord.Embed(title="> 🏅 시즌 리그 순위", description="리그 오브 레전드 e스포츠의 시즌 팀 순위 정보입니다.", color=colorMap['red'])
                    embed.set_footer(text="TIP: 아래 버튼을 눌러 각 팀의 정보를 확인할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
                    embed.set_image(url=self.banner)
                    if self.box_team == []: embed.add_field(name=f"'{self.picked_league}' 리그 정보", value="> 순위 정보가 없습니다.", inline=False)
                    else: embed.add_field(name=f"'{self.picked_league}' 리그 정보", value="", inline=False)
                    for i in range(len(self.box_team)):
                        if i >= len(self.box_team): break
                        if self.box_team[i]['website']: self.links = f"{self.links}[<:Website:1090657978711027742>]({self.box_team[i]['website']}) "
                        if self.box_team[i]['youtube']: self.links = f"{self.links}[<:YouTube:1090656510213902427>]({self.box_team[i]['youtube']}) "
                        if self.box_team[i]['instagram']: self.links = f"{self.links}[<:Instagram:1090656104163328080>]({self.box_team[i]['instagram']}) "
                        if self.box_team[i]['facebook']: self.links = f"{self.links}[<:Facebook:1090656102565302363>]({self.box_team[i]['facebook']}) "
                        if self.box_team[i]['twitter']: self.links = f"{self.links}[<:Twitter:1090656106814111754>]({self.box_team[i]['twitter']}) "
                        if self.links != "":
                            self.links = self.links[:-1]
                            embed.add_field(name=f"> {i + 1}위 - {self.box_team[i]['acronym']} ({self.box_team[i]['name']})", value=f"[__{self.box_team[i]['point']:,}__포인트] __{self.box_team[i]['win']:,}__승 __{self.box_team[i]['lose']:,}__패 (세트 스코어 __{self.box_team[i]['setWin']:,}__승 __{self.box_team[i]['setLose']:,}__패)\n[<:OPGGEsports:1090660883027464232>]({esports_op_gg_team}{self.box_team[i]['id']}) {self.links}", inline=False)
                        else:
                            embed.add_field(name=f"> {i + 1}위 - {self.box_team[i]['acronym']} ({self.box_team[i]['name']})", value=f"[__{self.box_team[i]['point']:,}__포인트] __{self.box_team[i]['win']:,}__승 __{self.box_team[i]['lose']:,}__패 (세트 스코어 __{self.box_team[i]['setWin']:,}__승 __{self.box_team[i]['setLose']:,}__패)\n[<:OPGGEsports:1090660883027464232>]({esports_op_gg_team}{self.box_team[i]['id']})", inline=False)
                        self.links = ""
                    await interaction.response.edit_message(content="", embed=embed, view=StandingView(self.bot, self.ctx, self.msg, self.banner, self.picked_league, False, "99", self.teams_id))

                else:
                    embed = discord.Embed(title="> 🏅 시즌 리그 순위", description="리그 오브 레전드 e스포츠의 시즌 팀 순위 정보입니다.", color=colorMap['red'])
                    embed.set_image(url=self.banner)
                    embed.add_field(name=f"'{self.picked_league}' 리그 정보", value="> 순위 정보가 없습니다.", inline=False)
                    return await interaction.response.edit_message(content="", embed=embed, view=StandingView(self.bot, self.ctx, self.msg, self.banner, self.picked_league, True, self.teams_id_index, self.teams_id))

    def add_button(self):
        if (self.button_select == True) and (self.button_select_index == "0"):
            team_1 = discord.ui.Button(emoji="1️⃣", style=discord.ButtonStyle.blurple, custom_id="0", row=1)
        else:
            team_1 = discord.ui.Button(emoji="1️⃣", style=discord.ButtonStyle.gray, custom_id="0", row=1)
        if (self.button_select == True) and (self.button_select_index == "1"):
            team_2 = discord.ui.Button(emoji="2️⃣", style=discord.ButtonStyle.blurple, custom_id="1", row=1)
        else:
            team_2 = discord.ui.Button(emoji="2️⃣", style=discord.ButtonStyle.gray, custom_id="1", row=1)
        if (self.button_select == True) and (self.button_select_index == "2"):
            team_3 = discord.ui.Button(emoji="3️⃣", style=discord.ButtonStyle.blurple, custom_id="2", row=1)
        else:
            team_3 = discord.ui.Button(emoji="3️⃣", style=discord.ButtonStyle.gray, custom_id="2", row=1)
        if (self.button_select == True) and (self.button_select_index == "3"):
            team_4 = discord.ui.Button(emoji="4️⃣", style=discord.ButtonStyle.blurple, custom_id="3", row=1)
        else:
            team_4 = discord.ui.Button(emoji="4️⃣", style=discord.ButtonStyle.gray, custom_id="3", row=1)
        if (self.button_select == True) and (self.button_select_index == "4"):
            team_5 = discord.ui.Button(emoji="5️⃣", style=discord.ButtonStyle.blurple, custom_id="4", row=1)
        else:
            team_5 = discord.ui.Button(emoji="5️⃣", style=discord.ButtonStyle.gray, custom_id="4", row=1)
        if (self.button_select == True) and (self.button_select_index == "5"):
            team_6 = discord.ui.Button(emoji="6️⃣", style=discord.ButtonStyle.blurple, custom_id="5", row=2)
        else:
            team_6 = discord.ui.Button(emoji="6️⃣", style=discord.ButtonStyle.gray, custom_id="5", row=2)
        if (self.button_select == True) and (self.button_select_index == "6"):
            team_7 = discord.ui.Button(emoji="7️⃣", style=discord.ButtonStyle.blurple, custom_id="6", row=2)
        else:
            team_7 = discord.ui.Button(emoji="7️⃣", style=discord.ButtonStyle.gray, custom_id="6", row=2)
        if (self.button_select == True) and (self.button_select_index == "7"):
            team_8 = discord.ui.Button(emoji="8️⃣", style=discord.ButtonStyle.blurple, custom_id="7", row=2)
        else:
            team_8 = discord.ui.Button(emoji="8️⃣", style=discord.ButtonStyle.gray, custom_id="7", row=2)
        if (self.button_select == True) and (self.button_select_index == "8"):
            team_9 = discord.ui.Button(emoji="9️⃣", style=discord.ButtonStyle.blurple, custom_id="8", row=2)
        else:
            team_9 = discord.ui.Button(emoji="9️⃣", style=discord.ButtonStyle.gray, custom_id="8", row=2)
        if (self.button_select == True) and (self.button_select_index == "9"):
            team_10 = discord.ui.Button(emoji="🔟", style=discord.ButtonStyle.blurple, custom_id="9", row=2)
        else:
            team_10 = discord.ui.Button(emoji="🔟", style=discord.ButtonStyle.gray, custom_id="9", row=2)

        async def callback_all(interaction: discord.Interaction):
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
                    embed = discord.Embed(title="> 🏅 시즌 리그 순위", description="리그 오브 레전드 e스포츠의 시즌 팀 순위 정보입니다.", color=colorMap['red'])
                    embed.set_image(url=self.banner)
                    embed.add_field(name=f"'{self.picked_league}' 리그 정보", value="> 순위 정보가 없습니다.", inline=False)
                    return await interaction.response.edit_message(content="", embed=embed, view=StandingView(self.bot, self.ctx, self.msg, self.banner, self.picked_league, True, self.teams_id_index, self.teams_id))
                                        
                self.box_team = get_league_standings(tournamentId)
                tournamentId = [] # 초기화

                try:
                    print(f"[league_standing.py] {self.box_team['code']}: {self.box_team['message']}")
                    embed = discord.Embed(title="> ⚠️ 오류", description=f"Code: `{self.box_team['code']}`\nMessage: {self.box_team['message']}", color=colorMap['red'])
                    return await interaction.response.edit_message(content="", embed=embed, view=None)

                except:
                    if self.box_team:
                        self.teams_id = []
                        for i in range(len(self.box_team)):
                            self.teams_id.append(self.box_team[i]['id'])

                        embed = discord.Embed(title="> 🏅 시즌 리그 순위", description="리그 오브 레전드 e스포츠의 시즌 팀 순위 정보입니다.", color=colorMap['red'])
                        embed.set_footer(text="TIP: 아래 버튼을 눌러 각 팀의 정보를 확인할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
                        embed.set_image(url=self.banner)
                        if self.box_team == []: embed.add_field(name=f"'{self.picked_league}' 리그 정보", value="> 순위 정보가 없습니다.", inline=False)
                        else: embed.add_field(name=f"'{self.picked_league}' 리그 정보", value="", inline=False)
                        for i in range(len(self.box_team)):
                            if i >= len(self.box_team): break
                            if self.box_team[i]['website']: self.links = f"{self.links}[<:Website:1090657978711027742>]({self.box_team[i]['website']}) "
                            if self.box_team[i]['youtube']: self.links = f"{self.links}[<:YouTube:1090656510213902427>]({self.box_team[i]['youtube']}) "
                            if self.box_team[i]['instagram']: self.links = f"{self.links}[<:Instagram:1090656104163328080>]({self.box_team[i]['instagram']}) "
                            if self.box_team[i]['facebook']: self.links = f"{self.links}[<:Facebook:1090656102565302363>]({self.box_team[i]['facebook']}) "
                            if self.box_team[i]['twitter']: self.links = f"{self.links}[<:Twitter:1090656106814111754>]({self.box_team[i]['twitter']}) "
                            if self.links != "":
                                self.links = self.links[:-1]
                                embed.add_field(name=f"> {i + 1}위 - {self.box_team[i]['acronym']} ({self.box_team[i]['name']})", value=f"[__{self.box_team[i]['point']:,}__포인트] __{self.box_team[i]['win']:,}__승 __{self.box_team[i]['lose']:,}__패 (세트 스코어 __{self.box_team[i]['setWin']:,}__승 __{self.box_team[i]['setLose']:,}__패)\n[<:OPGGEsports:1090660883027464232>]({esports_op_gg_team}{self.box_team[i]['id']}) {self.links}", inline=False)
                            else:
                                embed.add_field(name=f"> {i + 1}위 - {self.box_team[i]['acronym']} ({self.box_team[i]['name']})", value=f"[__{self.box_team[i]['point']:,}__포인트] __{self.box_team[i]['win']:,}__승 __{self.box_team[i]['lose']:,}__패 (세트 스코어 __{self.box_team[i]['setWin']:,}__승 __{self.box_team[i]['setLose']:,}__패)\n[<:OPGGEsports:1090660883027464232>]({esports_op_gg_team}{self.box_team[i]['id']})", inline=False)
                            self.links = ""
                        await interaction.response.edit_message(content="", embed=embed, view=StandingView(self.bot, self.ctx, self.msg, self.banner, self.picked_league, False, "99", self.teams_id))

                    else:
                        embed = discord.Embed(title="> 🏅 시즌 리그 순위", description="리그 오브 레전드 e스포츠의 시즌 팀 순위 정보입니다.", color=colorMap['red'])
                        embed.set_footer(text="TIP: 아래 버튼을 눌러 각 팀의 정보를 확인할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
                        embed.set_image(url=self.banner)
                        embed.add_field(name=f"'{self.picked_league}' 리그 정보", value="> 순위 정보가 없습니다.", inline=False)
                        return await interaction.response.edit_message(content="", embed=embed, view=StandingView(self.bot, self.ctx, self.msg, self.banner, self.picked_league, True, self.teams_id_index, self.teams_id))

        async def team_1_callback(interaction: discord.Interaction):
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
                self.box_player = get_teamInfo(tournamentId, self.teams_id[int(self.teams_id_index)])
            except:
                embed = discord.Embed(title="> 📊 팀 정보", description="리그 오브 레전드 e스포츠의 팀 정보입니다.", color=colorMap['red'])
                embed.set_footer(text="TIP: 아래 버튼을 눌러 각 팀의 정보를 확인할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
                embed.set_image(url=self.banner)
                embed.add_field(name=f"[{self.picked_league}]", value="> 팀 정보가 없습니다.", inline=False)
                return await interaction.response.edit_message(content="", embed=embed, view=StandingView(self.bot, self.ctx, self.msg, self.banner, self.picked_league, True, self.teams_id_index, self.teams_id))

            try:
                print(f"[league_standing.py] {self.box_player['code']}: {self.box_player['message']}")
                embed = discord.Embed(title="> ⚠️ 오류", description=f"Code: `{self.box_player['code']}`\nMessage: {self.box_player['message']}", color=colorMap['red'])
                return await interaction.response.edit_message(content="", embed=embed, view=None)

            except:
                if self.box_player:
                    for i in range(len(self.box_player)):
                        self.msg_player = f"{self.msg_player}> [{self.box_player[i]['team_acronym']}]({esports_op_gg_team}{self.box_player[i]['team_id']}) [{self.box_player[i]['nickName']}]({esports_op_gg_player}{self.box_player[i]['id']}) ({self.box_player[i]['position']})\n{self.box_player[i]['stat_kda']} 평점 `({self.box_player[i]['stat_kills']} / {self.box_player[i]['stat_deaths']} / {self.box_player[i]['stat_assists']})`\n승률: __{self.box_player[i]['stat_winRate']}__% (__{self.box_player[i]['stat_wins']:,}__승 __{self.box_player[i]['stat_loses']:,}__패)\n"

                    embed = discord.Embed(title="> 📊 팀 정보", description="리그 오브 레전드 e스포츠의 팀 정보입니다.", color=colorMap['red'])
                    embed.set_footer(text="TIP: 아래 버튼을 눌러 각 팀의 정보를 확인할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
                    embed.set_image(url=self.banner)
                    embed.set_thumbnail(url=self.box_player[0]['team_imageUrl'])
                    embed.add_field(name=f"{self.box_player[0]['team_acronym']} ({self.box_player[0]['team_name']}) [{self.picked_league}]", value=self.msg_player, inline=False)
                    await interaction.response.edit_message(content="", embed=embed, view=StandingView(self.bot, self.ctx, self.msg, self.banner, self.picked_league, True, self.teams_id_index, self.teams_id))

                else:
                    embed = discord.Embed(title="> 📊 팀 정보", description="리그 오브 레전드 e스포츠의 팀 정보입니다.", color=colorMap['red'])
                    embed.set_footer(text="TIP: 아래 버튼을 눌러 각 팀의 정보를 확인할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
                    embed.set_image(url=self.banner)
                    embed.add_field(name=f"[{self.picked_league}]", value="> 팀 정보가 없습니다.", inline=False)
                    await interaction.response.edit_message(content="", embed=embed, view=StandingView(self.bot, self.ctx, self.msg, self.banner, self.picked_league, True, self.teams_id_index, self.teams_id))

        async def team_2_callback(interaction: discord.Interaction):
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
                self.box_player = get_teamInfo(tournamentId, self.teams_id[int(self.teams_id_index)])
            except:
                embed = discord.Embed(title="> 📊 팀 정보", description="리그 오브 레전드 e스포츠의 팀 정보입니다.", color=colorMap['red'])
                embed.set_footer(text="TIP: 아래 버튼을 눌러 각 팀의 정보를 확인할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
                embed.set_image(url=self.banner)
                embed.add_field(name=f"[{self.picked_league}]", value="> 팀 정보가 없습니다.", inline=False)
                return await interaction.response.edit_message(content="", embed=embed, view=StandingView(self.bot, self.ctx, self.msg, self.banner, self.picked_league, True, self.teams_id_index, self.teams_id))

            try:
                print(f"[league_standing.py] {self.box_player['code']}: {self.box_player['message']}")
                embed = discord.Embed(title="> ⚠️ 오류", description=f"Code: `{self.box_player['code']}`\nMessage: {self.box_player['message']}", color=colorMap['red'])
                return await interaction.response.edit_message(content="", embed=embed, view=None)

            except:
                if self.box_player:
                    for i in range(len(self.box_player)):
                        self.msg_player = f"{self.msg_player}> [{self.box_player[i]['team_acronym']}]({esports_op_gg_team}{self.box_player[i]['team_id']}) [{self.box_player[i]['nickName']}]({esports_op_gg_player}{self.box_player[i]['id']}) ({self.box_player[i]['position']})\n{self.box_player[i]['stat_kda']} 평점 `({self.box_player[i]['stat_kills']} / {self.box_player[i]['stat_deaths']} / {self.box_player[i]['stat_assists']})`\n승률: __{self.box_player[i]['stat_winRate']}__% (__{self.box_player[i]['stat_wins']:,}__승 __{self.box_player[i]['stat_loses']:,}__패)\n"

                    embed = discord.Embed(title="> 📊 팀 정보", description="리그 오브 레전드 e스포츠의 팀 정보입니다.", color=colorMap['red'])
                    embed.set_footer(text="TIP: 아래 버튼을 눌러 각 팀의 정보를 확인할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
                    embed.set_image(url=self.banner)
                    embed.set_thumbnail(url=self.box_player[0]['team_imageUrl'])
                    embed.add_field(name=f"{self.box_player[0]['team_acronym']} ({self.box_player[0]['team_name']}) [{self.picked_league}]", value=self.msg_player, inline=False)
                    await interaction.response.edit_message(content="", embed=embed, view=StandingView(self.bot, self.ctx, self.msg, self.banner, self.picked_league, True, self.teams_id_index, self.teams_id))

                else:
                    embed = discord.Embed(title="> 📊 팀 정보", description="리그 오브 레전드 e스포츠의 팀 정보입니다.", color=colorMap['red'])
                    embed.set_footer(text="TIP: 아래 버튼을 눌러 각 팀의 정보를 확인할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
                    embed.set_image(url=self.banner)
                    embed.add_field(name=f"[{self.picked_league}]", value="> 팀 정보가 없습니다.", inline=False)
                    await interaction.response.edit_message(content="", embed=embed, view=StandingView(self.bot, self.ctx, self.msg, self.banner, self.picked_league, True, self.teams_id_index, self.teams_id))

        async def team_3_callback(interaction: discord.Interaction):
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
                self.box_player = get_teamInfo(tournamentId, self.teams_id[int(self.teams_id_index)])
            except:
                embed = discord.Embed(title="> 📊 팀 정보", description="리그 오브 레전드 e스포츠의 팀 정보입니다.", color=colorMap['red'])
                embed.set_footer(text="TIP: 아래 버튼을 눌러 각 팀의 정보를 확인할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
                embed.set_image(url=self.banner)
                embed.add_field(name=f"[{self.picked_league}]", value="> 팀 정보가 없습니다.", inline=False)
                return await interaction.response.edit_message(content="", embed=embed, view=StandingView(self.bot, self.ctx, self.msg, self.banner, self.picked_league, True, self.teams_id_index, self.teams_id))

            try:
                print(f"[league_standing.py] {self.box_player['code']}: {self.box_player['message']}")
                embed = discord.Embed(title="> ⚠️ 오류", description=f"Code: `{self.box_player['code']}`\nMessage: {self.box_player['message']}", color=colorMap['red'])
                return await interaction.response.edit_message(content="", embed=embed, view=None)

            except:
                if self.box_player:
                    for i in range(len(self.box_player)):
                        self.msg_player = f"{self.msg_player}> [{self.box_player[i]['team_acronym']}]({esports_op_gg_team}{self.box_player[i]['team_id']}) [{self.box_player[i]['nickName']}]({esports_op_gg_player}{self.box_player[i]['id']}) ({self.box_player[i]['position']})\n{self.box_player[i]['stat_kda']} 평점 `({self.box_player[i]['stat_kills']} / {self.box_player[i]['stat_deaths']} / {self.box_player[i]['stat_assists']})`\n승률: __{self.box_player[i]['stat_winRate']}__% (__{self.box_player[i]['stat_wins']:,}__승 __{self.box_player[i]['stat_loses']:,}__패)\n"

                    embed = discord.Embed(title="> 📊 팀 정보", description="리그 오브 레전드 e스포츠의 팀 정보입니다.", color=colorMap['red'])
                    embed.set_footer(text="TIP: 아래 버튼을 눌러 각 팀의 정보를 확인할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
                    embed.set_image(url=self.banner)
                    embed.set_thumbnail(url=self.box_player[0]['team_imageUrl'])
                    embed.add_field(name=f"{self.box_player[0]['team_acronym']} ({self.box_player[0]['team_name']}) [{self.picked_league}]", value=self.msg_player, inline=False)
                    await interaction.response.edit_message(content="", embed=embed, view=StandingView(self.bot, self.ctx, self.msg, self.banner, self.picked_league, True, self.teams_id_index, self.teams_id))

                else:
                    embed = discord.Embed(title="> 📊 팀 정보", description="리그 오브 레전드 e스포츠의 팀 정보입니다.", color=colorMap['red'])
                    embed.set_footer(text="TIP: 아래 버튼을 눌러 각 팀의 정보를 확인할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
                    embed.set_image(url=self.banner)
                    embed.add_field(name=f"[{self.picked_league}]", value="> 팀 정보가 없습니다.", inline=False)
                    await interaction.response.edit_message(content="", embed=embed, view=StandingView(self.bot, self.ctx, self.msg, self.banner, self.picked_league, True, self.teams_id_index, self.teams_id))

        async def team_4_callback(interaction: discord.Interaction):
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
                self.box_player = get_teamInfo(tournamentId, self.teams_id[int(self.teams_id_index)])
            except:
                embed = discord.Embed(title="> 📊 팀 정보", description="리그 오브 레전드 e스포츠의 팀 정보입니다.", color=colorMap['red'])
                embed.set_footer(text="TIP: 아래 버튼을 눌러 각 팀의 정보를 확인할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
                embed.set_image(url=self.banner)
                embed.add_field(name=f"[{self.picked_league}]", value="> 팀 정보가 없습니다.", inline=False)
                return await interaction.response.edit_message(content="", embed=embed, view=StandingView(self.bot, self.ctx, self.msg, self.banner, self.picked_league, True, self.teams_id_index, self.teams_id))

            try:
                print(f"[league_standing.py] {self.box_player['code']}: {self.box_player['message']}")
                embed = discord.Embed(title="> ⚠️ 오류", description=f"Code: `{self.box_player['code']}`\nMessage: {self.box_player['message']}", color=colorMap['red'])
                return await interaction.response.edit_message(content="", embed=embed, view=None)

            except:
                if self.box_player:
                    for i in range(len(self.box_player)):
                        self.msg_player = f"{self.msg_player}> [{self.box_player[i]['team_acronym']}]({esports_op_gg_team}{self.box_player[i]['team_id']}) [{self.box_player[i]['nickName']}]({esports_op_gg_player}{self.box_player[i]['id']}) ({self.box_player[i]['position']})\n{self.box_player[i]['stat_kda']} 평점 `({self.box_player[i]['stat_kills']} / {self.box_player[i]['stat_deaths']} / {self.box_player[i]['stat_assists']})`\n승률: __{self.box_player[i]['stat_winRate']}__% (__{self.box_player[i]['stat_wins']:,}__승 __{self.box_player[i]['stat_loses']:,}__패)\n"

                    embed = discord.Embed(title="> 📊 팀 정보", description="리그 오브 레전드 e스포츠의 팀 정보입니다.", color=colorMap['red'])
                    embed.set_footer(text="TIP: 아래 버튼을 눌러 각 팀의 정보를 확인할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
                    embed.set_image(url=self.banner)
                    embed.set_thumbnail(url=self.box_player[0]['team_imageUrl'])
                    embed.add_field(name=f"{self.box_player[0]['team_acronym']} ({self.box_player[0]['team_name']}) [{self.picked_league}]", value=self.msg_player, inline=False)
                    await interaction.response.edit_message(content="", embed=embed, view=StandingView(self.bot, self.ctx, self.msg, self.banner, self.picked_league, True, self.teams_id_index, self.teams_id))

                else:
                    embed = discord.Embed(title="> 📊 팀 정보", description="리그 오브 레전드 e스포츠의 팀 정보입니다.", color=colorMap['red'])
                    embed.set_footer(text="TIP: 아래 버튼을 눌러 각 팀의 정보를 확인할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
                    embed.set_image(url=self.banner)
                    embed.add_field(name=f"[{self.picked_league}]", value="> 팀 정보가 없습니다.", inline=False)
                    await interaction.response.edit_message(content="", embed=embed, view=StandingView(self.bot, self.ctx, self.msg, self.banner, self.picked_league, True, self.teams_id_index, self.teams_id))

        async def team_5_callback(interaction: discord.Interaction):
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
                self.box_player = get_teamInfo(tournamentId, self.teams_id[int(self.teams_id_index)])
            except:
                embed = discord.Embed(title="> 📊 팀 정보", description="리그 오브 레전드 e스포츠의 팀 정보입니다.", color=colorMap['red'])
                embed.set_footer(text="TIP: 아래 버튼을 눌러 각 팀의 정보를 확인할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
                embed.set_image(url=self.banner)
                embed.add_field(name=f"[{self.picked_league}]", value="> 팀 정보가 없습니다.", inline=False)
                return await interaction.response.edit_message(content="", embed=embed, view=StandingView(self.bot, self.ctx, self.msg, self.banner, self.picked_league, True, self.teams_id_index, self.teams_id))

            try:
                print(f"[league_standing.py] {self.box_player['code']}: {self.box_player['message']}")
                embed = discord.Embed(title="> ⚠️ 오류", description=f"Code: `{self.box_player['code']}`\nMessage: {self.box_player['message']}", color=colorMap['red'])
                return await interaction.response.edit_message(content="", embed=embed, view=None)

            except:
                if self.box_player:
                    for i in range(len(self.box_player)):
                        self.msg_player = f"{self.msg_player}> [{self.box_player[i]['team_acronym']}]({esports_op_gg_team}{self.box_player[i]['team_id']}) [{self.box_player[i]['nickName']}]({esports_op_gg_player}{self.box_player[i]['id']}) ({self.box_player[i]['position']})\n{self.box_player[i]['stat_kda']} 평점 `({self.box_player[i]['stat_kills']} / {self.box_player[i]['stat_deaths']} / {self.box_player[i]['stat_assists']})`\n승률: __{self.box_player[i]['stat_winRate']}__% (__{self.box_player[i]['stat_wins']:,}__승 __{self.box_player[i]['stat_loses']:,}__패)\n"

                    embed = discord.Embed(title="> 📊 팀 정보", description="리그 오브 레전드 e스포츠의 팀 정보입니다.", color=colorMap['red'])
                    embed.set_footer(text="TIP: 아래 버튼을 눌러 각 팀의 정보를 확인할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
                    embed.set_image(url=self.banner)
                    embed.set_thumbnail(url=self.box_player[0]['team_imageUrl'])
                    embed.add_field(name=f"{self.box_player[0]['team_acronym']} ({self.box_player[0]['team_name']}) [{self.picked_league}]", value=self.msg_player, inline=False)
                    await interaction.response.edit_message(content="", embed=embed, view=StandingView(self.bot, self.ctx, self.msg, self.banner, self.picked_league, True, self.teams_id_index, self.teams_id))

                else:
                    embed = discord.Embed(title="> 📊 팀 정보", description="리그 오브 레전드 e스포츠의 팀 정보입니다.", color=colorMap['red'])
                    embed.set_footer(text="TIP: 아래 버튼을 눌러 각 팀의 정보를 확인할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
                    embed.set_image(url=self.banner)
                    embed.add_field(name=f"[{self.picked_league}]", value="> 팀 정보가 없습니다.", inline=False)
                    await interaction.response.edit_message(content="", embed=embed, view=StandingView(self.bot, self.ctx, self.msg, self.banner, self.picked_league, True, self.teams_id_index, self.teams_id))

        async def team_6_callback(interaction: discord.Interaction):
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
                self.box_player = get_teamInfo(tournamentId, self.teams_id[int(self.teams_id_index)])
            except:
                embed = discord.Embed(title="> 📊 팀 정보", description="리그 오브 레전드 e스포츠의 팀 정보입니다.", color=colorMap['red'])
                embed.set_footer(text="TIP: 아래 버튼을 눌러 각 팀의 정보를 확인할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
                embed.set_image(url=self.banner)
                embed.add_field(name=f"[{self.picked_league}]", value="> 팀 정보가 없습니다.", inline=False)
                return await interaction.response.edit_message(content="", embed=embed, view=StandingView(self.bot, self.ctx, self.msg, self.banner, self.picked_league, True, self.teams_id_index, self.teams_id))

            try:
                print(f"[league_standing.py] {self.box_player['code']}: {self.box_player['message']}")
                embed = discord.Embed(title="> ⚠️ 오류", description=f"Code: `{self.box_player['code']}`\nMessage: {self.box_player['message']}", color=colorMap['red'])
                return await interaction.response.edit_message(content="", embed=embed, view=None)

            except:
                if self.box_player:
                    for i in range(len(self.box_player)):
                        self.msg_player = f"{self.msg_player}> [{self.box_player[i]['team_acronym']}]({esports_op_gg_team}{self.box_player[i]['team_id']}) [{self.box_player[i]['nickName']}]({esports_op_gg_player}{self.box_player[i]['id']}) ({self.box_player[i]['position']})\n{self.box_player[i]['stat_kda']} 평점 `({self.box_player[i]['stat_kills']} / {self.box_player[i]['stat_deaths']} / {self.box_player[i]['stat_assists']})`\n승률: __{self.box_player[i]['stat_winRate']}__% (__{self.box_player[i]['stat_wins']:,}__승 __{self.box_player[i]['stat_loses']:,}__패)\n"

                    embed = discord.Embed(title="> 📊 팀 정보", description="리그 오브 레전드 e스포츠의 팀 정보입니다.", color=colorMap['red'])
                    embed.set_footer(text="TIP: 아래 버튼을 눌러 각 팀의 정보를 확인할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
                    embed.set_image(url=self.banner)
                    embed.set_thumbnail(url=self.box_player[0]['team_imageUrl'])
                    embed.add_field(name=f"{self.box_player[0]['team_acronym']} ({self.box_player[0]['team_name']}) [{self.picked_league}]", value=self.msg_player, inline=False)
                    await interaction.response.edit_message(content="", embed=embed, view=StandingView(self.bot, self.ctx, self.msg, self.banner, self.picked_league, True, self.teams_id_index, self.teams_id))

                else:
                    embed = discord.Embed(title="> 📊 팀 정보", description="리그 오브 레전드 e스포츠의 팀 정보입니다.", color=colorMap['red'])
                    embed.set_footer(text="TIP: 아래 버튼을 눌러 각 팀의 정보를 확인할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
                    embed.set_image(url=self.banner)
                    embed.add_field(name=f"[{self.picked_league}]", value="> 팀 정보가 없습니다.", inline=False)
                    await interaction.response.edit_message(content="", embed=embed, view=StandingView(self.bot, self.ctx, self.msg, self.banner, self.picked_league, True, self.teams_id_index, self.teams_id))

        async def team_7_callback(interaction: discord.Interaction):
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
                self.box_player = get_teamInfo(tournamentId, self.teams_id[int(self.teams_id_index)])
            except:
                embed = discord.Embed(title="> 📊 팀 정보", description="리그 오브 레전드 e스포츠의 팀 정보입니다.", color=colorMap['red'])
                embed.set_footer(text="TIP: 아래 버튼을 눌러 각 팀의 정보를 확인할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
                embed.set_image(url=self.banner)
                embed.add_field(name=f"[{self.picked_league}]", value="> 팀 정보가 없습니다.", inline=False)
                return await interaction.response.edit_message(content="", embed=embed, view=StandingView(self.bot, self.ctx, self.msg, self.banner, self.picked_league, True, self.teams_id_index, self.teams_id))

            try:
                print(f"[league_standing.py] {self.box_player['code']}: {self.box_player['message']}")
                embed = discord.Embed(title="> ⚠️ 오류", description=f"Code: `{self.box_player['code']}`\nMessage: {self.box_player['message']}", color=colorMap['red'])
                return await interaction.response.edit_message(content="", embed=embed, view=None)

            except:
                if self.box_player:
                    for i in range(len(self.box_player)):
                        self.msg_player = f"{self.msg_player}> [{self.box_player[i]['team_acronym']}]({esports_op_gg_team}{self.box_player[i]['team_id']}) [{self.box_player[i]['nickName']}]({esports_op_gg_player}{self.box_player[i]['id']}) ({self.box_player[i]['position']})\n{self.box_player[i]['stat_kda']} 평점 `({self.box_player[i]['stat_kills']} / {self.box_player[i]['stat_deaths']} / {self.box_player[i]['stat_assists']})`\n승률: __{self.box_player[i]['stat_winRate']}__% (__{self.box_player[i]['stat_wins']:,}__승 __{self.box_player[i]['stat_loses']:,}__패)\n"

                    embed = discord.Embed(title="> 📊 팀 정보", description="리그 오브 레전드 e스포츠의 팀 정보입니다.", color=colorMap['red'])
                    embed.set_footer(text="TIP: 아래 버튼을 눌러 각 팀의 정보를 확인할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
                    embed.set_image(url=self.banner)
                    embed.set_thumbnail(url=self.box_player[0]['team_imageUrl'])
                    embed.add_field(name=f"{self.box_player[0]['team_acronym']} ({self.box_player[0]['team_name']}) [{self.picked_league}]", value=self.msg_player, inline=False)
                    await interaction.response.edit_message(content="", embed=embed, view=StandingView(self.bot, self.ctx, self.msg, self.banner, self.picked_league, True, self.teams_id_index, self.teams_id))

                else:
                    embed = discord.Embed(title="> 📊 팀 정보", description="리그 오브 레전드 e스포츠의 팀 정보입니다.", color=colorMap['red'])
                    embed.set_footer(text="TIP: 아래 버튼을 눌러 각 팀의 정보를 확인할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
                    embed.set_image(url=self.banner)
                    embed.add_field(name=f"[{self.picked_league}]", value="> 팀 정보가 없습니다.", inline=False)
                    await interaction.response.edit_message(content="", embed=embed, view=StandingView(self.bot, self.ctx, self.msg, self.banner, self.picked_league, True, self.teams_id_index, self.teams_id))

        async def team_8_callback(interaction: discord.Interaction):
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
                self.box_player = get_teamInfo(tournamentId, self.teams_id[int(self.teams_id_index)])
            except:
                embed = discord.Embed(title="> 📊 팀 정보", description="리그 오브 레전드 e스포츠의 팀 정보입니다.", color=colorMap['red'])
                embed.set_footer(text="TIP: 아래 버튼을 눌러 각 팀의 정보를 확인할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
                embed.set_image(url=self.banner)
                embed.add_field(name=f"[{self.picked_league}]", value="> 팀 정보가 없습니다.", inline=False)
                return await interaction.response.edit_message(content="", embed=embed, view=StandingView(self.bot, self.ctx, self.msg, self.banner, self.picked_league, True, self.teams_id_index, self.teams_id))

            try:
                print(f"[league_standing.py] {self.box_player['code']}: {self.box_player['message']}")
                embed = discord.Embed(title="> ⚠️ 오류", description=f"Code: `{self.box_player['code']}`\nMessage: {self.box_player['message']}", color=colorMap['red'])
                return await interaction.response.edit_message(content="", embed=embed, view=None)

            except:
                if self.box_player:
                    for i in range(len(self.box_player)):
                        self.msg_player = f"{self.msg_player}> [{self.box_player[i]['team_acronym']}]({esports_op_gg_team}{self.box_player[i]['team_id']}) [{self.box_player[i]['nickName']}]({esports_op_gg_player}{self.box_player[i]['id']}) ({self.box_player[i]['position']})\n{self.box_player[i]['stat_kda']} 평점 `({self.box_player[i]['stat_kills']} / {self.box_player[i]['stat_deaths']} / {self.box_player[i]['stat_assists']})`\n승률: __{self.box_player[i]['stat_winRate']}__% (__{self.box_player[i]['stat_wins']:,}__승 __{self.box_player[i]['stat_loses']:,}__패)\n"

                    embed = discord.Embed(title="> 📊 팀 정보", description="리그 오브 레전드 e스포츠의 팀 정보입니다.", color=colorMap['red'])
                    embed.set_footer(text="TIP: 아래 버튼을 눌러 각 팀의 정보를 확인할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
                    embed.set_image(url=self.banner)
                    embed.set_thumbnail(url=self.box_player[0]['team_imageUrl'])
                    embed.add_field(name=f"{self.box_player[0]['team_acronym']} ({self.box_player[0]['team_name']}) [{self.picked_league}]", value=self.msg_player, inline=False)
                    await interaction.response.edit_message(content="", embed=embed, view=StandingView(self.bot, self.ctx, self.msg, self.banner, self.picked_league, True, self.teams_id_index, self.teams_id))

                else:
                    embed = discord.Embed(title="> 📊 팀 정보", description="리그 오브 레전드 e스포츠의 팀 정보입니다.", color=colorMap['red'])
                    embed.set_footer(text="TIP: 아래 버튼을 눌러 각 팀의 정보를 확인할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
                    embed.set_image(url=self.banner)
                    embed.add_field(name=f"[{self.picked_league}]", value="> 팀 정보가 없습니다.", inline=False)
                    await interaction.response.edit_message(content="", embed=embed, view=StandingView(self.bot, self.ctx, self.msg, self.banner, self.picked_league, True, self.teams_id_index, self.teams_id))

        async def team_9_callback(interaction: discord.Interaction):
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
                self.box_player = get_teamInfo(tournamentId, self.teams_id[int(self.teams_id_index)])
            except:
                embed = discord.Embed(title="> 📊 팀 정보", description="리그 오브 레전드 e스포츠의 팀 정보입니다.", color=colorMap['red'])
                embed.set_footer(text="TIP: 아래 버튼을 눌러 각 팀의 정보를 확인할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
                embed.set_image(url=self.banner)
                embed.add_field(name=f"[{self.picked_league}]", value="> 팀 정보가 없습니다.", inline=False)
                return await interaction.response.edit_message(content="", embed=embed, view=StandingView(self.bot, self.ctx, self.msg, self.banner, self.picked_league, True, self.teams_id_index, self.teams_id))

            try:
                print(f"[league_standing.py] {self.box_player['code']}: {self.box_player['message']}")
                embed = discord.Embed(title="> ⚠️ 오류", description=f"Code: `{self.box_player['code']}`\nMessage: {self.box_player['message']}", color=colorMap['red'])
                return await interaction.response.edit_message(content="", embed=embed, view=None)

            except:
                if self.box_player:
                    for i in range(len(self.box_player)):
                        self.msg_player = f"{self.msg_player}> [{self.box_player[i]['team_acronym']}]({esports_op_gg_team}{self.box_player[i]['team_id']}) [{self.box_player[i]['nickName']}]({esports_op_gg_player}{self.box_player[i]['id']}) ({self.box_player[i]['position']})\n{self.box_player[i]['stat_kda']} 평점 `({self.box_player[i]['stat_kills']} / {self.box_player[i]['stat_deaths']} / {self.box_player[i]['stat_assists']})`\n승률: __{self.box_player[i]['stat_winRate']}__% (__{self.box_player[i]['stat_wins']:,}__승 __{self.box_player[i]['stat_loses']:,}__패)\n"

                    embed = discord.Embed(title="> 📊 팀 정보", description="리그 오브 레전드 e스포츠의 팀 정보입니다.", color=colorMap['red'])
                    embed.set_footer(text="TIP: 아래 버튼을 눌러 각 팀의 정보를 확인할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
                    embed.set_image(url=self.banner)
                    embed.set_thumbnail(url=self.box_player[0]['team_imageUrl'])
                    embed.add_field(name=f"{self.box_player[0]['team_acronym']} ({self.box_player[0]['team_name']}) [{self.picked_league}]", value=self.msg_player, inline=False)
                    await interaction.response.edit_message(content="", embed=embed, view=StandingView(self.bot, self.ctx, self.msg, self.banner, self.picked_league, True, self.teams_id_index, self.teams_id))

                else:
                    embed = discord.Embed(title="> 📊 팀 정보", description="리그 오브 레전드 e스포츠의 팀 정보입니다.", color=colorMap['red'])
                    embed.set_footer(text="TIP: 아래 버튼을 눌러 각 팀의 정보를 확인할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
                    embed.set_image(url=self.banner)
                    embed.add_field(name=f"[{self.picked_league}]", value="> 팀 정보가 없습니다.", inline=False)
                    await interaction.response.edit_message(content="", embed=embed, view=StandingView(self.bot, self.ctx, self.msg, self.banner, self.picked_league, True, self.teams_id_index, self.teams_id))

        async def team_10_callback(interaction: discord.Interaction):
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
                self.box_player = get_teamInfo(tournamentId, self.teams_id[int(self.teams_id_index)])
            except:
                embed = discord.Embed(title="> 📊 팀 정보", description="리그 오브 레전드 e스포츠의 팀 정보입니다.", color=colorMap['red'])
                embed.set_footer(text="TIP: 아래 버튼을 눌러 각 팀의 정보를 확인할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
                embed.set_image(url=self.banner)
                embed.add_field(name=f"[{self.picked_league}]", value="> 팀 정보가 없습니다.", inline=False)
                return await interaction.response.edit_message(content="", embed=embed, view=StandingView(self.bot, self.ctx, self.msg, self.banner, self.picked_league, True, self.teams_id_index, self.teams_id))

            try:
                print(f"[league_standing.py] {self.box_player['code']}: {self.box_player['message']}")
                embed = discord.Embed(title="> ⚠️ 오류", description=f"Code: `{self.box_player['code']}`\nMessage: {self.box_player['message']}", color=colorMap['red'])
                return await interaction.response.edit_message(content="", embed=embed, view=None)

            except:
                if self.box_player:
                    for i in range(len(self.box_player)):
                        self.msg_player = f"{self.msg_player}> [{self.box_player[i]['team_acronym']}]({esports_op_gg_team}{self.box_player[i]['team_id']}) [{self.box_player[i]['nickName']}]({esports_op_gg_player}{self.box_player[i]['id']}) ({self.box_player[i]['position']})\n{self.box_player[i]['stat_kda']} 평점 `({self.box_player[i]['stat_kills']} / {self.box_player[i]['stat_deaths']} / {self.box_player[i]['stat_assists']})`\n승률: __{self.box_player[i]['stat_winRate']}__% (__{self.box_player[i]['stat_wins']:,}__승 __{self.box_player[i]['stat_loses']:,}__패)\n"

                    embed = discord.Embed(title="> 📊 팀 정보", description="리그 오브 레전드 e스포츠의 팀 정보입니다.", color=colorMap['red'])
                    embed.set_footer(text="TIP: 아래 버튼을 눌러 각 팀의 정보를 확인할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
                    embed.set_image(url=self.banner)
                    embed.set_thumbnail(url=self.box_player[0]['team_imageUrl'])
                    embed.add_field(name=f"{self.box_player[0]['team_acronym']} ({self.box_player[0]['team_name']}) [{self.picked_league}]", value=self.msg_player, inline=False)
                    await interaction.response.edit_message(content="", embed=embed, view=StandingView(self.bot, self.ctx, self.msg, self.banner, self.picked_league, True, self.teams_id_index, self.teams_id))

                else:
                    embed = discord.Embed(title="> 📊 팀 정보", description="리그 오브 레전드 e스포츠의 팀 정보입니다.", color=colorMap['red'])
                    embed.set_footer(text="TIP: 아래 버튼을 눌러 각 팀의 정보를 확인할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
                    embed.set_image(url=self.banner)
                    embed.add_field(name=f"[{self.picked_league}]", value="> 팀 정보가 없습니다.", inline=False)
                    await interaction.response.edit_message(content="", embed=embed, view=StandingView(self.bot, self.ctx, self.msg, self.banner, self.picked_league, True, self.teams_id_index, self.teams_id))

        if (self.button_select == True) and (self.button_select_index == "0"):
            team_1.callback = callback_all
        else:
            team_1.callback = team_1_callback
        if (self.button_select == True) and (self.button_select_index == "1"):
            team_2.callback = callback_all
        else:
            team_2.callback = team_2_callback
        if (self.button_select == True) and (self.button_select_index == "2"):
            team_3.callback = callback_all
        else:
            team_3.callback = team_3_callback
        if (self.button_select == True) and (self.button_select_index == "3"):
            team_4.callback = callback_all
        else:
            team_4.callback = team_4_callback
        if (self.button_select == True) and (self.button_select_index == "4"):
            team_5.callback = callback_all
        else:
            team_5.callback = team_5_callback
        if (self.button_select == True) and (self.button_select_index == "5"):
            team_6.callback = callback_all
        else:
            team_6.callback = team_6_callback
        if (self.button_select == True) and (self.button_select_index == "6"):
            team_7.callback = callback_all
        else:
            team_7.callback = team_7_callback
        if (self.button_select == True) and (self.button_select_index == "7"):
            team_8.callback = callback_all
        else:
            team_8.callback = team_8_callback
        if (self.button_select == True) and (self.button_select_index == "8"):
            team_9.callback = callback_all
        else:
            team_9.callback = team_9_callback
        if (self.button_select == True) and (self.button_select_index == "9"):
            team_10.callback = callback_all
        else:
            team_10.callback = team_10_callback

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
    @option("리그", description="리그를 선택해주세요.", required=True, autocomplete=get_league)
    async def _mvpCMD(self, ctx: discord.AutocompleteContext, 리그: str):

        picked_league = 리그
        links = ""
        box_team = []
        teams_id = []
        box_recentMatches = {}
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
                    embed = discord.Embed(title="> 🏅 시즌 리그 순위", description="리그 오브 레전드 e스포츠의 시즌 팀 순위 정보입니다.", color=colorMap['red'])
                    embed.set_image(url=banner_image_url)
                    embed.add_field(name=f"'{picked_league}' 리그 정보", value="> 순위 정보가 없습니다.", inline=False)
                    return await msg.edit_original_response(content="", embed=embed, view=DisabledButton())
                box_team = get_league_standings(tournamentId)
                tournamentId = [] # 초기화

                try:
                    print(f"[league_standing.py] {box_team['code']}: {box_team['message']}")
                    embed = discord.Embed(title="> ⚠️ 오류", description=f"Code: `{box_team['code']}`\nMessage: {box_team['message']}", color=colorMap['red'])
                    return await msg.edit_original_response(content="", embed=embed)

                except:
                    if box_team:
                        for i in range(len(box_team)):
                            teams_id.append(box_team[i]['id'])

                        embed = discord.Embed(title="> 🏅 시즌 리그 순위", description="리그 오브 레전드 e스포츠의 시즌 팀 순위 정보입니다.", color=colorMap['red'])
                        embed.set_footer(text="TIP: 아래 버튼을 눌러 각 팀의 정보를 확인할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
                        embed.set_image(url=banner_image_url)
                        if box_team == []: embed.add_field(name=f"'{picked_league}' 리그 정보", value="> 순위 정보가 없습니다.", inline=False)
                        else: embed.add_field(name=f"'{picked_league}' 리그 정보", value="", inline=False)
                        for i in range(len(box_team)):
                            if i >= len(box_team): break
                            if box_team[i]['website']: links = f"{links}[<:Website:1090657978711027742>]({box_team[i]['website']}) "
                            if box_team[i]['youtube']: links = f"{links}[<:YouTube:1090656510213902427>]({box_team[i]['youtube']}) "
                            if box_team[i]['instagram']: links = f"{links}[<:Instagram:1090656104163328080>]({box_team[i]['instagram']}) "
                            if box_team[i]['facebook']: links = f"{links}[<:Facebook:1090656102565302363>]({box_team[i]['facebook']}) "
                            if box_team[i]['twitter']: links = f"{links}[<:Twitter:1090656106814111754>]({box_team[i]['twitter']}) "
                            if links != "":
                                links = links[:-1]
                                embed.add_field(name=f"> {i + 1}위 - {box_team[i]['acronym']} ({box_team[i]['name']})", value=f"[__{box_team[i]['point']:,}__포인트] __{box_team[i]['win']:,}__승 __{box_team[i]['lose']:,}__패 (세트 스코어 __{box_team[i]['setWin']:,}__승 __{box_team[i]['setLose']:,}__패)\n[<:OPGGEsports:1090660883027464232>]({esports_op_gg_team}{box_team[i]['id']}) {links}", inline=False)
                            else:
                                embed.add_field(name=f"> {i + 1}위 - {box_team[i]['acronym']} ({box_team[i]['name']})", value=f"[__{box_team[i]['point']:,}__포인트] __{box_team[i]['win']:,}__승 __{box_team[i]['lose']:,}__패 (세트 스코어 __{box_team[i]['setWin']:,}__승 __{box_team[i]['setLose']:,}__패)\n[<:OPGGEsports:1090660883027464232>]({esports_op_gg_team}{box_team[i]['id']})", inline=False)
                            links = ""
                        await msg.edit_original_response(content="", embed=embed, view=StandingView(self.bot, ctx, msg, banner_image_url, picked_league, False, "99", teams_id))

        except Exception as error:
            print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
            print(traceback.format_exc())



def setup(bot):
    bot.add_cog(LeagueStandingCMD(bot))
    print("league_standing.py 로드 됨")
