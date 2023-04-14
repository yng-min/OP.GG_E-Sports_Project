# -*- coding: utf-8 -*-

# 패키지 라이브러리 설정
import discord
from discord.ext import commands
from discord.commands import Option, SlashCommandGroup
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
    db_version_guild = botCURSOR.execute("SELECT DBVersionGuild FROM main").fetchall()[0]
    botDB.close()
except Exception as error:
    print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
    print(traceback.format_exc())

prefix = config['prefix_normal']
colorMap = config['colorMap']
role_name_notice = config['role_name_league_notification']


class LeagueSelect(discord.ui.Select):

    def __init__(self, bot, ctx, msg):
        self.bot = bot
        self.ctx = ctx
        self.msg = msg
        self.st_league = []
        self.leagues = []
        self.leagueNum = 0

        self.league_0 = 0
        self.league_1 = 0
        self.league_2 = 0
        self.league_3 = 0
        self.league_4 = 0
        self.league_5 = 0
        self.league_6 = 0
        self.league_7 = 0
        self.league_8 = 0
        self.league_9 = 0
        self.league_10 = 0
        self.league_11 = 0
        self.league_12 = 0
        self.league_13 = 0
        self.league_14 = 0
        self.league_15 = 0
        self.league_16 = 0

        for league in leagues:
            self.leagues.append(league)

        super().__init__(
            placeholder="리그 선택하기",
            min_values=1,
            max_values=17,
            options=[
            discord.SelectOption(label="모든 리그", value="0", description="모든 리그의 정보를 보고 싶어요!"),
            discord.SelectOption(label="LCK / KR", value="1", description="League of Legends Champions Korea"),
            discord.SelectOption(label="LPL / CN ", value="2", description="League of Legends Pro League"),
            discord.SelectOption(label="LEC / EU", value="3", description="League of Legends European Championship"),
            discord.SelectOption(label="LCS / NA", value="4", description="League of Legends Championship Series"),
            discord.SelectOption(label="CBLOL / BR", value="5", description="Campeonato Brasileiro de League of Legends"),
            discord.SelectOption(label="VCS / VN", value="6", description="Vietnam Championship Series"),
            discord.SelectOption(label="LCL / CIS", value="7", description="League of Legends Continental League"),
            discord.SelectOption(label="TCL / TR", value="8", description="Turkish Championship League"),
            discord.SelectOption(label="PCS / SEA", value="9", description="Pacific Championship Series"),
            discord.SelectOption(label="LLA / LAT", value="10", description="Liga Latinoamérica"),
            discord.SelectOption(label="LJL / JP", value="11", description="League of Legends Japan League"),
            discord.SelectOption(label="LCO / OCE", value="12", description="League of Legends Circuit Oceania"),
            discord.SelectOption(label="MSI / INT", value="13", description="Mid-Season Invitational"),
            discord.SelectOption(label="OPL / COE", value="14", description="Oceanic Pro League"),
            discord.SelectOption(label="LMS / LMS", value="15", description="League of Legends Master Series"),
            discord.SelectOption(label="Worlds / INT", value="16", description="League of Legends World Championship")
            ],
            row=0
        )

    async def callback(self, interaction: discord.Interaction):

        if not self.ctx.author.guild_permissions.administrator:
            embed = discord.Embed(title="> ⛔ 설정 불가", description="이 명령어는 서버의 __관리자 권한__을 가진 이용자만 사용할 수 있어요.", color=colorMap['red'])
            return await interaction.response.edit_message(content="", embed=embed, view=None)

        if not os.path.isfile(rf"./Database/Guild/guild_{self.ctx.guild.id}.sqlite"):
            embed = discord.Embed(title="> ⛔ 설정 불가", description=f"이 서버는 설정이 완료되지 않았어요. `{prefix}설정 셋업` 명령어를 통해 초기 설정을 먼저 진행해주세요.", color=colorMap['red'])
            return await interaction.response.edit_message(content="", embed=embed, view=None)

        for i in range(len(self.values)):
            if self.values[i] == "0": self.st_league.append("all")
            elif self.values[i] == "1": self.st_league.append("LCK")
            elif self.values[i] == "2": self.st_league.append("LPL")
            elif self.values[i] == "3": self.st_league.append("LEC")
            elif self.values[i] == "4": self.st_league.append("LCS")
            elif self.values[i] == "5": self.st_league.append("CBLOL")
            elif self.values[i] == "6": self.st_league.append("VCS")
            elif self.values[i] == "7": self.st_league.append("LCL")
            elif self.values[i] == "8": self.st_league.append("TCL")
            elif self.values[i] == "9": self.st_league.append("PCS")
            elif self.values[i] == "10": self.st_league.append("LLA")
            elif self.values[i] == "11": self.st_league.append("LJL")
            elif self.values[i] == "12": self.st_league.append("LCO")
            elif self.values[i] == "13": self.st_league.append("MSI")
            elif self.values[i] == "14": self.st_league.append("OPL")
            elif self.values[i] == "15": self.st_league.append("LMS")
            elif self.values[i] == "16": self.st_league.append("Worlds")
            else: pass

        for i in range(len(self.st_league)):
            if self.st_league[0] == "all":
                self.league_0 = 1
                break
            if "LCK" == self.st_league[i]: self.league_1 = 1
            if "LPL" == self.st_league[i]: self.league_2 = 1
            if "LEC" == self.st_league[i]: self.league_3 = 1
            if "LCS" == self.st_league[i]: self.league_4 = 1
            if "CBLOL" == self.st_league[i]: self.league_5 = 1
            if "VCS" == self.st_league[i]: self.league_6 = 1
            if "LCL" == self.st_league[i]: self.league_7 = 1
            if "TCL" == self.st_league[i]: self.league_8 = 1
            if "PCS" == self.st_league[i]: self.league_9 = 1
            if "LLA" == self.st_league[i]: self.league_10 = 1
            if "LJL" == self.st_league[i]: self.league_11 = 1
            if "LCO" == self.st_league[i]: self.league_12 = 1
            if "MSI" == self.st_league[i]: self.league_13 = 1
            if "OPL" == self.st_league[i]: self.league_14 = 1
            if "LMS" == self.st_league[i]: self.league_15 = 1
            if "Worlds" == self.st_league[i]: self.league_16 = 1

        try:
            guildDB = sqlite3.connect(rf"./Database/Guild/guild_{self.ctx.guild.id}.sqlite", isolation_level=None)
            guildCURSOR = guildDB.cursor()
            guildCURSOR.execute("""
                CREATE TABLE IF NOT EXISTS league(
                GuildID INTERGER,
                LCO,
                PCS,
                LLA,
                LCS,
                LEC,
                VCS,
                LCL,
                LJL,
                TCL,
                CBLOL,
                OPL,
                Worlds,
                LMS,
                LPL,
                LCK,
                MSI
                )
            """) # 리그 테이블 생성

            guildCURSOR.execute("UPDATE league SET LCO = ?, PCS = ?, LLA = ?, LCS = ?, LEC = ?, VCS = ?, LCL = ?, LJL = ?, TCL = ?, CBLOL = ?, OPL = ?, Worlds = ?, LMS = ?, LPL = ?, LCK = ?, MSI = ? WHERE GuildID = ?", (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, self.ctx.guild.id))

            if self.league_0 == 1:
                guildCURSOR.execute("UPDATE league SET LCO = ?, PCS = ?, LLA = ?, LCS = ?, LEC = ?, VCS = ?, LCL = ?, LJL = ?, TCL = ?, CBLOL = ?, OPL = ?, Worlds = ?, LMS = ?, LPL = ?, LCK = ?, MSI = ? WHERE GuildID = ?", (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, self.ctx.guild.id))
            if self.league_1 == 1:
                guildCURSOR.execute("UPDATE league SET LCK = ? WHERE GuildID = ?", (1, self.ctx.guild.id))
            if self.league_2 == 1:
                guildCURSOR.execute("UPDATE league SET LPL = ? WHERE GuildID = ?", (1, self.ctx.guild.id))
            if self.league_3 == 1:
                guildCURSOR.execute("UPDATE league SET LEC = ? WHERE GuildID = ?", (1, self.ctx.guild.id))
            if self.league_4 == 1:
                guildCURSOR.execute("UPDATE league SET LCS = ? WHERE GuildID = ?", (1, self.ctx.guild.id))
            if self.league_5 == 1:
                guildCURSOR.execute("UPDATE league SET CBLOL = ? WHERE GuildID = ?", (1, self.ctx.guild.id))
            if self.league_6 == 1:
                guildCURSOR.execute("UPDATE league SET VCS = ? WHERE GuildID = ?", (1, self.ctx.guild.id))
            if self.league_7 == 1:
                guildCURSOR.execute("UPDATE league SET LCL = ? WHERE GuildID = ?", (1, self.ctx.guild.id))
            if self.league_8 == 1:
                guildCURSOR.execute("UPDATE league SET TCL = ? WHERE GuildID = ?", (1, self.ctx.guild.id))
            if self.league_9 == 1:
                guildCURSOR.execute("UPDATE league SET PCS = ? WHERE GuildID = ?", (1, self.ctx.guild.id))
            if self.league_10 == 1:
                guildCURSOR.execute("UPDATE league SET LLA = ? WHERE GuildID = ?", (1, self.ctx.guild.id))
            if self.league_11 == 1:
                guildCURSOR.execute("UPDATE league SET LJL = ? WHERE GuildID = ?", (1, self.ctx.guild.id))
            if self.league_12 == 1:
                guildCURSOR.execute("UPDATE league SET LCO = ? WHERE GuildID = ?", (1, self.ctx.guild.id))
            if self.league_13 == 1:
                guildCURSOR.execute("UPDATE league SET MSI = ? WHERE GuildID = ?", (1, self.ctx.guild.id))
            if self.league_14 == 1:
                guildCURSOR.execute("UPDATE league SET OPL = ? WHERE GuildID = ?", (1, self.ctx.guild.id))
            if self.league_15 == 1:
                guildCURSOR.execute("UPDATE league SET LMS = ? WHERE GuildID = ?", (1, self.ctx.guild.id))
            if self.league_16 == 1:
                guildCURSOR.execute("UPDATE league SET Worlds = ? WHERE GuildID = ?", (1, self.ctx.guild.id))

            leagueContent = ""
            if self.league_0 == 1: leagueContent += ", 모든 리그"
            if self.league_1 == 1: leagueContent += ", LCK"
            if self.league_2 == 1: leagueContent += ", LPL"
            if self.league_3 == 1: leagueContent += ", LEC"
            if self.league_4 == 1: leagueContent += ", LCS"
            if self.league_5 == 1: leagueContent += ", CBLOL"
            if self.league_6 == 1: leagueContent += ", VCS"
            if self.league_7 == 1: leagueContent += ", LCL"
            if self.league_8 == 1: leagueContent += ", TCL"
            if self.league_9 == 1: leagueContent += ", PCS"
            if self.league_10 == 1: leagueContent += ", LLA"
            if self.league_11 == 1: leagueContent += ", LJL"
            if self.league_12 == 1: leagueContent += ", LCO"
            if self.league_13 == 1: leagueContent += ", MSI"
            if self.league_14 == 1: leagueContent += ", OPL"
            if self.league_15 == 1: leagueContent += ", LMS"
            if self.league_16 == 1: leagueContent += ", Worlds"
            leagueContent = leagueContent[2:]

            print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
            print(f"{self.ctx.author}({self.ctx.author.id}) | 리그 알림 설정 변경")
            embed = discord.Embed(title="> ✅ 설정 완료", description=f"리그 알림 설정 변경을 완료했어요.\n\n(설정한 리그 : `{leagueContent}`)", color=colorMap['red'])
            await interaction.response.edit_message(content="", embed=embed, view=None)

        except Exception as error:
            print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
            print(traceback.format_exc())
            embed = discord.Embed(title="> ⚠️ 설정 실패", description=f"아래의 오류로 인해 서버 설정 변경에 실패했어요. 해당 문제가 지속된다면 개발자에게 문의해주세요.\n`{error}`", color=colorMap['red'])
            return await self.msg.edit_original_response(content="", embed=embed, view=None)

        try: guildDB.close()
        except: pass


    async def on_timeout(self):
        await self.msg.edit_original_response(content="", view=DisabledSelect())


class DisabledSelect(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Select(placeholder="리그 선택하기", options=[discord.SelectOption(label="asdf", value="1", description="asdf")], disabled=True, row=0))


class LeagueView(discord.ui.View):

    def __init__(self, bot, ctx, msg):
        super().__init__(timeout=None)
        self.bot = bot
        self.ctx = ctx
        self.msg = msg
        self.add_item(LeagueSelect(self.bot, self.ctx, self.msg))


class GuildSettingCMD(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    _guild_settings = SlashCommandGroup(name="설정", description="설정 명령어", guild_only=True, default_member_permissions=discord.Permissions(administrator=True))

    @_guild_settings.command(
        name="셋업",
        description="서비스 이용을 위한 필수 서버 설정을 진행해요."
    )
    async def _setting_setupCMD(self, ctx,
        채널: Option(discord.TextChannel, "경기 일정 알림을 받을 채널을 선택해주세요.", required=True),
    ):

        channel_notice = 채널

        if not ctx.author.guild_permissions.administrator:
            embed = discord.Embed(title="> ⛔ 설정 불가", description="이 명령어는 서버의 __관리자 권한__을 가진 이용자만 사용할 수 있어요.", color=colorMap['red'])
            return await ctx.respond(embed=embed, ephemeral=True)

        if os.path.isfile(rf"./Database/Guild/guild_{ctx.guild.id}.sqlite"):
            embed = discord.Embed(title="> ⛔ 설정 불가", description=f"이 서버는 이미 설정이 완료된 상태예요. 만약 설정을 변경하고 싶으시다면 `{prefix}설정-변경` 명령어를 이용해주세요.", color=colorMap['red'])
            return await ctx.respond(embed=embed, ephemeral=True)

        embed = discord.Embed(title="", description=f"⚙ 설정 진행 중...", color=colorMap['red'])
        msg = await ctx.respond(embed=embed)

        try:
            # embed = discord.Embed(title="", description="> ⚙️ `리그 알림` 역할 추가 중...", color=colorMap['red'])
            # await msg.edit_original_response(content="", embed=embed)
            # role_notice = await ctx.guild.create_role(name=role_name_notice)

            embed = discord.Embed(title="", description="> ⚙️ 정보 저장 중...", color=colorMap['red'])
            await msg.edit_original_response(content="", embed=embed)
            guildDB = sqlite3.connect(rf"./Database/Guild/guild_{ctx.guild.id}.sqlite", isolation_level=None)
            guildCURSOR = guildDB.cursor()

            guildCURSOR.execute("""
                CREATE TABLE IF NOT EXISTS main(
                GuildID INTERGER,
                NoticeAnswer INTERGER,
                NoticeEarlyAnswer INTERGER,
                NoticeCompleteAnswer INTERGER,
                NoticeChannelID INTERGER,
                NoticeRoleID INTERGER
                )
            """) # 메인 테이블 생성
            guildCURSOR.execute("""
                INSERT INTO main(GuildID, NoticeAnswer, NoticeEarlyAnswer, NoticeCompleteAnswer, NoticeChannelID, NoticeRoleID)
                VALUES(?, ?, ?, ?, ?, ?)""",
                # (ctx.guild.id, 1, 1, 1, channel_notice.id, role_notice.id)
                (ctx.guild.id, 1, 1, 1, channel_notice.id, None)
            ) # 메인 테이블 데이터 입력

            guildCURSOR.execute("""
                CREATE TABLE IF NOT EXISTS league(
                GuildID INTERGER,
                LCO,
                PCS,
                LLA,
                LCS,
                LEC,
                VCS,
                LCL,
                LJL,
                TCL,
                CBLOL,
                OPL,
                Worlds,
                LMS,
                LPL,
                LCK,
                MSI
                )
            """) # 리그 테이블 생성
            guildCURSOR.execute("""
                INSERT INTO league(GuildID, LCO, PCS, LLA, LCS, LEC, VCS, LCL, LJL, TCL, CBLOL, OPL, Worlds, LMS, LPL, LCK, MSI)
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (ctx.guild.id, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
            ) # 리그 테이블 데이터 입력

            print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
            print(f"{ctx.author}({ctx.author.id}) | 서버 셋업")
            embed = discord.Embed(title="> ✅ 설정 완료", description="서비스 이용을 위한 설정을 완료했어요.", color=colorMap['red'])
            await msg.edit_original_response(content="", embed=embed)

        except discord.Forbidden: # missing permissions
            embed = discord.Embed(title="> ⚠️ 설정 실패", description=f"서버를 설정하기 위한 권한이 없어요. 봇에게 `역할 관리하기` 권한이 있는지 확인해주세요.", color=colorMap['red'])
            embed.set_footer(text="TIP: 봇의 권한을 '관리자' 권한으로 설정하는게 가장 좋아요.", icon_url=self.bot.user.display_avatar.url)
            return await msg.edit_original_response(content="", embed=embed)

        except Exception as error:
            print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
            print(traceback.format_exc())
            embed = discord.Embed(title="> ⚠️ 설정 실패", description=f"아래의 오류로 인해 서버 설정에 실패했어요. 해당 문제가 지속된다면 개발자에게 문의해주세요.\n`{error}`", color=colorMap['red'])
            return await msg.edit_original_response(content="", embed=embed)

        try: guildDB.close()
        except: pass

    @_guild_settings.command(
        name="리그",
        description="서버에서 알림 받을 리그를 선택할 수 있어요.",
    )
    async def _setting_choice_leagueCMD(self, ctx):

        if not os.path.isfile(rf"./Database/Guild/guild_{ctx.guild.id}.sqlite"):
            embed = discord.Embed(title="> ⛔ 설정 불가", description=f"이 서버는 설정이 완료되지 않았어요. `{prefix}설정 셋업` 명령어를 통해 초기 설정을 먼저 진행해주세요.", color=colorMap['red'])
            return await ctx.respond(embed=embed, ephemeral=True)

        embed = discord.Embed(title="> 📝 리그 알림 설정", description="서버에서 알림을 받을 리그 종류를 선택해 주세요.", color=colorMap['red'])
        msg = await ctx.respond(embed=embed)
        await msg.edit_original_response(content="", embed=embed, view=LeagueView(bot=self.bot, ctx=ctx, msg=msg))

    @_guild_settings.command(
        name="변경",
        description="서버 설정을 변경 또는 수정해요.",
    )
    async def _setting_editCMD(self, ctx,
        알림_1: Option(str, "경기 일정 알림을 받으실 건가요?", choices=["알림 켜기", "알림 끄기"], required=False),
        알림_2: Option(str, "경기 시작 미리 알림을 받으실 건가요?", choices=["알림 켜기", "알림 끄기"], required=False),
        알림_3: Option(str, "경기 종료(결과) 알림을 받으실 건가요?", choices=["알림 켜기", "알림 끄기"], required=False),
        채널: Option(discord.TextChannel, "경기 일정 알림을 받을 채널을 선택해주세요.", required=False),
        초기화: Option(str, "정말 서버 설정을 초기화 하실거라면 '초기화'를 입력해주세요.", required=False),
    ):

        try: notice_answer = 알림_1
        except: notice_answer = None

        try: notice_early_answer = 알림_2
        except: notice_early_answer = None

        try: notice_complete_answer = 알림_3
        except: notice_complete_answer = None

        try: channel_notice = 채널
        except: channel_notice = None

        try: reset_answer = 초기화
        except: reset_answer = None

        if not ctx.author.guild_permissions.administrator:
            embed = discord.Embed(title="> ⛔ 설정 불가", description="이 명령어는 서버의 __관리자 권한__을 가진 이용자만 사용할 수 있어요.", color=colorMap['red'])
            return await ctx.respond(embed=embed, ephemeral=True)

        if not os.path.isfile(rf"./Database/Guild/guild_{ctx.guild.id}.sqlite"):
            embed = discord.Embed(title="> ⛔ 설정 불가", description=f"이 서버는 설정이 완료되지 않았어요. `{prefix}설정 셋업` 명령어를 통해 초기 설정을 먼저 진행해주세요.", color=colorMap['red'])
            return await ctx.respond(embed=embed, ephemeral=True)

        embed = discord.Embed(title="", description=f"⚙ 설정 진행 중...", color=colorMap['red'])
        msg = await ctx.respond(embed=embed)

        try:
            if notice_answer == None: notice_mode_1 = None
            elif notice_answer == "알림 켜기": notice_mode_1 = 1
            elif notice_answer == "알림 끄기": notice_mode_1 = 0

            if notice_early_answer == None: notice_mode_2 = None
            elif notice_early_answer == "알림 켜기": notice_mode_2 = 1
            elif notice_early_answer == "알림 끄기": notice_mode_2 = 0

            if notice_complete_answer == None: notice_mode_3 = None
            elif notice_complete_answer == "알림 켜기": notice_mode_3 = 1
            elif notice_complete_answer == "알림 끄기": notice_mode_3 = 0

            if reset_answer == None: reset_mode = None
            elif reset_answer == "초기화": reset_mode = 1
            else: reset_mode = 0

            guildDB = sqlite3.connect(rf"./Database/Guild/guild_{ctx.guild.id}.sqlite", isolation_level=None)
            guildCURSOR = guildDB.cursor()
            guildCURSOR.execute("""
                CREATE TABLE IF NOT EXISTS main(
                GuildID INTERGER,
                NoticeAnswer INTERGER,
                NoticeEarlyAnswer INTERGER,
                NoticeCompleteAnswer INTERGER,
                NoticeChannelID INTERGER,
                NoticeRoleName INTERGER
                )
            """) # 메인 테이블 생성

            if (notice_mode_1 is None) and (notice_early_answer is None) and (notice_complete_answer is None) and (channel_notice is None) and (reset_mode is None):
                embed = discord.Embed(title="> ⛔ 설정 불가", description="서버 설정을 변경할 옵션을 선택해주세요.", color=colorMap['red'])
                return await msg.edit_original_response(content="", embed=embed)

            if reset_mode == 1:
                guildCURSOR.close()
                guildDB.close()
                os.remove(rf"./Database/Guild/guild_{ctx.guild.id}.sqlite")
                print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
                print(f"{ctx.author}({ctx.author.id}) | 서버 설정 초기화")
                embed = discord.Embed(title="> ✅ 설정 초기화 완료", description="서버 설정을 모두 초기화했어요.", color=colorMap['red'])
                return await msg.edit_original_response(content="", embed=embed)
            elif reset_mode == 0:
                embed = discord.Embed(title="> 📢 설정 초기화 취소", description=f"[`초기화`:`{reset_answer}`] 정확한 문구 입력 실패로 인해 초기화가 취소되었어요.", color=colorMap['red'])
                return await msg.edit_original_response(content="", embed=embed)

            if (notice_mode_1 == 1) or (notice_mode_1 == 0):
                guildCURSOR.execute("UPDATE main SET NoticeAnswer = ? WHERE GuildID = ?", (notice_mode_1, ctx.guild.id))

            if (notice_mode_2 == 1) or (notice_mode_2 == 0):
                guildCURSOR.execute("UPDATE main SET NoticeEarlyAnswer = ? WHERE GuildID = ?", (notice_mode_2, ctx.guild.id))

            if (notice_mode_3 == 1) or (notice_mode_3 == 0):
                guildCURSOR.execute("UPDATE main SET NoticeCompleteAnswer = ? WHERE GuildID = ?", (notice_mode_3, ctx.guild.id))

            if channel_notice:
                guildCURSOR.execute("UPDATE main SET NoticeChannelID = ? WHERE GuildID = ?", (channel_notice.id, ctx.guild.id))

            print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
            print(f"{ctx.author}({ctx.author.id}) | 서버 설정 변경")
            embed = discord.Embed(title="> ✅ 설정 완료", description="서버 설정 변경을 완료했어요.", color=colorMap['red'])
            await msg.edit_original_response(content="", embed=embed)

        except Exception as error:
            print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
            print(traceback.format_exc())
            embed = discord.Embed(title="> ⚠️ 설정 실패", description=f"아래의 오류로 인해 서버 설정 변경에 실패했어요. 해당 문제가 지속된다면 개발자에게 문의해주세요.\n`{error}`", color=colorMap['red'])
            return await msg.edit_original_response(content="", embed=embed)

        try:
            guildCURSOR.close()
            guildDB.close()
        except:
            pass



def setup(bot):
    bot.add_cog(GuildSettingCMD(bot))
    print("guild_settings.py 로드 됨")
