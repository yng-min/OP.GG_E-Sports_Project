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

    def __init__(self, bot, ctx, msg, banner, picked_league, box_recentMatches):
        super().__init__(timeout=60)
        self.bot = bot
        self.ctx = ctx
        self.msg = msg
        self.banner = banner
        self.picked_league = picked_league
        self.box_recentMatches = box_recentMatches

        self.links = ""
        self.box_team = []

        self.team_id = ""
        self.team_name = ""
        self.team_acronym = ""
        self.team_nationality = ""
        self.team_foundedAt = ""
        self.team_imageUrl = ""
        self.team_youtube = ""
        self.team_twitter = ""
        self.team_instagram = ""
        self.team_facebook = ""
        self.team_website = ""
        self.team_position = ""
        self.team_previously = ""
        self.team_setWin = ""
        self.team_setLose = ""
        self.team_recentMatches = ""

        self.add_item(discord.ui.Button(label="OP.GG Esports에서 보기", url=esports_op_gg_standing, row=2))
        # self.add_button()

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

            try:
                if tournamentId == []: continue
                elif tournamentId == None: continue
                self.teams = opgg.league_standing(tournamentId=tournamentId[0])
                tournamentId = [] # 초기화

                if self.teams['error'] == False:

                    for i in range(10):
                        self.team_id = self.teams['data'][i]['team']['id']
                        self.team_name = self.teams['data'][i]['team']['name']
                        self.team_acronym = self.teams['data'][i]['team']['acronym']
                        self.team_nationality = self.teams['data'][i]['team']['nationality']
                        self.team_foundedAt = self.teams['data'][i]['team']['foundedAt']
                        self.team_imageUrl = self.teams['data'][i]['team']['imageUrl']
                        self.team_youtube = self.teams['data'][i]['team']['youtube']
                        self.team_twitter = self.teams['data'][i]['team']['twitter']
                        self.team_instagram = self.teams['data'][i]['team']['instagram']
                        self.team_facebook = self.teams['data'][i]['team']['facebook']
                        self.team_website = self.teams['data'][i]['team']['website']
                        self.team_position = self.teams['data'][i]['position']
                        self.team_previously = self.teams['data'][i]['previously']
                        self.team_setWin = self.teams['data'][i]['setWin']
                        self.team_setLose = self.teams['data'][i]['setLose']
                        self.team_recentMatches = self.teams['data'][i]['recentMatches']

                        self.box_team.append({
                            "id": self.team_id,
                            "name": self.team_name,
                            "acronym": self.team_acronym,
                            "nationality": self.team_nationality,
                            "foundedAt": self.team_foundedAt,
                            "imageUrl": self.team_imageUrl,
                            "youtube": self.team_youtube,
                            "twitter": self.team_twitter,
                            "instagram": self.team_instagram,
                            "facebook": self.team_facebook,
                            "website": self.team_website,
                            "position": self.team_position,
                            "previously": self.team_previously,
                            "setWin": self.team_setWin,
                            "setLose": self.team_setLose,
                            "recentMatches": self.team_recentMatches
                        })

                    self.box_recentMatches = get_recentMatches(self.team_recentMatches)

                else:
                    print(f"[league_standing.py] {self.teams['code']}: {self.teams['message']}")
                    embed = discord.Embed(title="> ⚠️ 오류", description=f"Code: `{self.teams['code']}`\nMessage: {self.teams['message']}", color=colorMap['red'])
                    return await interaction.response.edit_message(content="", embed=embed, view=None)

            except:
                pass

        embed = discord.Embed(title="> 🏅 리그 순위", description="리그 오브 레전드의 리그 팀 순위 정보입니다.", color=colorMap['red'])
        embed.set_footer(text="TIP: 아래 버튼을 눌러 각 팀의 정보를 확인할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
        embed.set_image(url=self.banner)
        if self.box_team == []: embed.add_field(name=f"'{self.picked_league}' 리그 정보", value="순위 정보가 없습니다.", inline=False)
        else: embed.add_field(name=f"'{self.picked_league}' 리그 정보", value="", inline=False)
        for i in range(10):
            if i >= len(self.box_team): break
            if self.box_team[i]['website']: self.links = f"{self.links}[<:Website:1090657978711027742>]({self.box_team[i]['website']}) "
            if self.box_team[i]['youtube']: self.links = f"{self.links}[<:YouTube:1090656510213902427>]({self.box_team[i]['youtube']}) "
            if self.box_team[i]['instagram']: self.links = f"{self.links}[<:Instagram:1090656104163328080>]({self.box_team[i]['instagram']}) "
            if self.box_team[i]['facebook']: self.links = f"{self.links}[<:Facebook:1090656102565302363>]({self.box_team[i]['facebook']}) "
            if self.box_team[i]['twitter']: self.links = f"{self.links}[<:Twitter:1090656106814111754>]({self.box_team[i]['twitter']}) "
            if self.links != "":
                self.links = self.links[:-1]
                embed.add_field(name=f"• {i + 1}위 - {self.box_team[i]['acronym']} ({self.box_team[i]['name']})", value=f"> {self.box_team[i]['setWin']:,}승 / {self.box_team[i]['setLose']:,}패 - [<:OPGGEsports:1090660883027464232>]({esports_op_gg_team}{self.box_team[i]['id']}) {self.links}", inline=False)
            else:
                embed.add_field(name=f"• {i + 1}위 - {self.box_team[i]['acronym']} ({self.box_team[i]['name']})", value=f"> {self.box_team[i]['setWin']:,}승 / {self.box_team[i]['setLose']:,}패 - [<:OPGGEsports:1090660883027464232>]({esports_op_gg_team}{self.box_team[i]['id']})", inline=False)
            self.links = ""
        await interaction.response.edit_message(content="", embed=embed, view=StandingView(self.bot, self.ctx, self.msg, self.banner, self.picked_league, self.box_recentMatches))

    async def on_timeout(self):
        try:
            await self.msg.edit_original_response(content="", view=DisabledButton())
        except discord.NotFound:
            pass


class DisabledButton(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Select(placeholder="리그 선택하기", options=[discord.SelectOption(label="asdf", value="1", description="asdf")], disabled=True, row=0))
        # self.add_item(discord.ui.Button(label="탑", disabled=True, row=1))
        # self.add_item(discord.ui.Button(label="정글", disabled=True, row=1))
        # self.add_item(discord.ui.Button(label="미드", disabled=True, row=1))
        # self.add_item(discord.ui.Button(label="원딜", disabled=True, row=1))
        # self.add_item(discord.ui.Button(label="서포터", disabled=True, row=1))
        self.add_item(discord.ui.Button(label="OP.GG Esports에서 보기", url=esports_op_gg_standing, row=2))


class LeagueStandingCMD(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    _league = SlashCommandGroup(name="리그", description="리그 명령어", guild_only=False)

    @_league.command(
        name="순위",
        description="리그 오브 레전드 리그의 팀 순위 정보를 확인해보세요.",
    )
    @option("리그", description="리그를 선택해주세요.", required=True, autocomplete=get_league)
    async def _mvpCMD(self, ctx: discord.AutocompleteContext, 리그: str):

        picked_league = 리그
        box_team = []
        box_recentMatches = {}
        banner_image_url = random.choice(config['banner_image_url'])

        embed = discord.Embed(title="", description="⌛ 정보를 불러오는 중...", color=colorMap['red'])
        msg = await ctx.respond(embed=embed)

        try:
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

                try:
                    if tournamentId == []: continue
                    elif tournamentId == None: continue
                    teams = opgg.league_standing(tournamentId=tournamentId[0])
                    tournamentId = [] # 초기화

                    if teams['error'] == False:

                        for i in range(10):
                            team_id = teams['data'][i]['team']['id']
                            team_name = teams['data'][i]['team']['name']
                            team_acronym = teams['data'][i]['team']['acronym']
                            team_nationality = teams['data'][i]['team']['nationality']
                            team_foundedAt = teams['data'][i]['team']['foundedAt']
                            team_imageUrl = teams['data'][i]['team']['imageUrl']
                            team_youtube = teams['data'][i]['team']['youtube']
                            team_twitter = teams['data'][i]['team']['twitter']
                            team_instagram = teams['data'][i]['team']['instagram']
                            team_facebook = teams['data'][i]['team']['facebook']
                            team_website = teams['data'][i]['team']['website']
                            team_position = teams['data'][i]['position']
                            team_previously = teams['data'][i]['previously']
                            team_setWin = teams['data'][i]['setWin']
                            team_setLose = teams['data'][i]['setLose']
                            team_recentMatches = teams['data'][i]['recentMatches']

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
                                "setWin": team_setWin,
                                "setLose": team_setLose,
                                "recentMatches": team_recentMatches
                            })

                        box_recentMatches = get_recentMatches(team_recentMatches)

                    else:
                        print(f"[league_standing.py] {teams['code']}: {teams['message']}")
                        embed = discord.Embed(title="> ⚠️ 오류", description=f"Code: `{teams['code']}`\nMessage: {teams['message']}", color=colorMap['red'])
                        return await msg.edit_original_response(content="", embed=embed)

                except:
                    pass

            links = ""

            embed = discord.Embed(title="> 🏅 리그 순위", description="리그 오브 레전드의 리그 팀 순위 정보입니다.", color=colorMap['red'])
            embed.set_footer(text="TIP: 아래 버튼을 눌러 각 팀의 정보를 확인할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
            embed.set_image(url=banner_image_url)
            if box_team == []: embed.add_field(name=f"'{self.picked_league}' 리그 정보", value="순위 정보가 없습니다.", inline=False)
            else: embed.add_field(name=f"'{picked_league}' 리그 정보", value="", inline=False)
            for i in range(10):
                if i >= len(box_team): break
                if box_team[i]['website']: links = f"{links}[<:Website:1090657978711027742>]({box_team[i]['website']}) "
                if box_team[i]['youtube']: links = f"{links}[<:YouTube:1090656510213902427>]({box_team[i]['youtube']}) "
                if box_team[i]['instagram']: links = f"{links}[<:Instagram:1090656104163328080>]({box_team[i]['instagram']}) "
                if box_team[i]['facebook']: links = f"{links}[<:Facebook:1090656102565302363>]({box_team[i]['facebook']}) "
                if box_team[i]['twitter']: links = f"{links}[<:Twitter:1090656106814111754>]({box_team[i]['twitter']}) "
                if links != "":
                    links = links[:-1]
                    embed.add_field(name=f"• {i + 1}위 - {box_team[i]['acronym']} ({box_team[i]['name']})", value=f"> {box_team[i]['setWin']:,}승 / {box_team[i]['setLose']:,}패 - [<:OPGGEsports:1090660883027464232>]({esports_op_gg_team}{box_team[i]['id']}) {links}", inline=False)
                else:
                    embed.add_field(name=f"• {i + 1}위 - {box_team[i]['acronym']} ({box_team[i]['name']})", value=f"> {box_team[i]['setWin']:,}승 / {box_team[i]['setLose']:,}패 - [<:OPGGEsports:1090660883027464232>]({esports_op_gg_team}{box_team[i]['id']})", inline=False)
                links = ""
            # await msg.edit_original_response(content="", embed=embed)
            await msg.edit_original_response(content="", embed=embed, view=StandingView(self.bot, ctx, msg, banner_image_url, picked_league, box_recentMatches))

        except Exception as error:
            print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
            print(traceback.format_exc())



def setup(bot):
    bot.add_cog(LeagueStandingCMD(bot))
    print("league_standing.py 로드 됨")
