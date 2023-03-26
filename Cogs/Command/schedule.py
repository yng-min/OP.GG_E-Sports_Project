# -*- coding: utf-8 -*-

# 패키지 라이브러리 설정
import opgg
import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
import random
import json
import datetime
import pytz
import traceback

# config.json Config 파일 불러오기
try:
    with open(r"./config.json", "rt", encoding="UTF8") as configJson:
        config = json.load(configJson)
except: print("config.json이 로드되지 않음")

esports_op_gg_schedules = "https://esports.op.gg/ko/schedules"
time_difference = config['time_difference']
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


class ScheduleButton(discord.ui.View):

    def __init__(self, bot, ctx, msg, banner, box_1_match_schedule_2, msg_schedule_info_1, msg_schedule_info_1_2, box_2_match_schedule_2, msg_schedule_info_2, msg_schedule_info_2_2, box_3_match_schedule_2, msg_schedule_info_3, msg_schedule_info_3_2):
        super().__init__(timeout=60)
        self.bot = bot
        self.ctx = ctx
        self.msg = msg
        self.banner = banner

        if box_1_match_schedule_2 == "해당 일자의 리그 일정이 없습니다.":
            self.schedule_1_1 = []
            self.schedule_1_2 = []
            self.schedule_1_3 = ["해당 일자의 리그 일정이 없습니다."]
        else:
            self.schedule_1_1 = box_1_match_schedule_2
            self.schedule_1_2 = msg_schedule_info_1
            self.schedule_1_3 = msg_schedule_info_1_2

        if box_2_match_schedule_2 == "해당 일자의 리그 일정이 없습니다.":
            self.schedule_2_1 = []
            self.schedule_2_2 = []
            self.schedule_2_3 = ["해당 일자의 리그 일정이 없습니다."]
        else:
            self.schedule_2_1 = box_2_match_schedule_2
            self.schedule_2_2 = msg_schedule_info_2
            self.schedule_2_3 = msg_schedule_info_2_2

        if box_3_match_schedule_2 == "해당 일자의 리그 일정이 없습니다.":
            self.schedule_3_1 = []
            self.schedule_3_2 = []
            self.schedule_3_3 = ["해당 일자의 리그 일정이 없습니다."]
        else:
            self.schedule_3_1 = box_3_match_schedule_2
            self.schedule_3_2 = msg_schedule_info_3
            self.schedule_3_3 = msg_schedule_info_3_2

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
        self.add_item(discord.ui.Button(label="OP.GG Esports에서 보기", url=esports_op_gg_schedules, row=1))

    @discord.ui.select(
        placeholder="리그 선택하기",
        min_values=1,
        max_values=17,
        options=[
            discord.SelectOption(label="모든 리그", value="0", description="모든 리그의 정보를 보고 싶어요!"),
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
            discord.SelectOption(label="MSI / INT", value="13", description="Mid-Season Invitational"),
            discord.SelectOption(label="OPL / COE", value="14", description="Oceanic Pro League"),
            discord.SelectOption(label="LMS / LMS", value="15", description="League of Legends Master Series"),
            discord.SelectOption(label="Worlds / INT", value="16", description="League of Legends World Championship"),
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
            if select.values[i] == "0": self.box_select.append("all")
            elif select.values[i] == "1": self.box_select.append("LCK")
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
            elif select.values[i] == "13": self.box_select.append("MSI")
            elif select.values[i] == "14": self.box_select.append("OPL")
            elif select.values[i] == "15": self.box_select.append("LMS")
            elif select.values[i] == "16": self.box_select.append("Worlds")
            else: pass

        league_schedule_1 = self.schedule_1_2.split("\n")
        league_schedule_2 = self.schedule_2_2.split("\n")
        league_schedule_3 = self.schedule_3_2.split("\n")

        league_schedule_1 = list(filter(len, league_schedule_1))
        league_schedule_2 = list(filter(len, league_schedule_2))
        league_schedule_3 = list(filter(len, league_schedule_3))

        if league_schedule_1 == []: self.schedules_1 = []
        else:
            for i in range(len(league_schedule_1)):
                if self.box_select[0] == "all":
                    break
                for j in range(len(select.values)):
                    try:
                        league_find = league_schedule_1[i].split("(")[1].split("/")[0]
                    except:
                        self.league_1_max = True

                    if league_find == self.box_select[j]:
                        self.schedules_1.append(league_schedule_1[i])
                    elif self.league_1_max == True:
                        # self.schedules_1.append("...")
                        self.league_1_max = False
                    else:
                        pass

        if league_schedule_2 == []: self.schedules_2 = []
        else:
            for i in range(len(league_schedule_2)):
                if self.box_select[0] == "all":
                    break
                for j in range(len(select.values)):
                    try:
                        league_find = league_schedule_2[i].split("(")[1].split("/")[0]
                    except:
                        self.league_2_max = True

                    if league_find == self.box_select[j]:
                        self.schedules_2.append(league_schedule_2[i])
                    elif self.league_2_max == True:
                        # self.schedules_2.append("...")
                        self.league_2_max = False
                    else:
                        pass

        if league_schedule_3 == []: self.schedules_3 = []
        else:
            for i in range(len(league_schedule_3)):
                if self.box_select[0] == "all":
                    break
                for j in range(len(select.values)):
                    try:
                        league_find = league_schedule_3[i].split("(")[1].split("/")[0]
                    except:
                        self.league_3_max = True

                    if league_find == self.box_select[j]:
                        self.schedules_3.append(league_schedule_3[i])
                    elif self.league_3_max == True:
                        # self.schedules_3.append("...")
                        self.league_3_max = False
                    else:
                        pass

        if self.box_select[0] == "all":
            self.msg_schedule_1 = self.schedule_1_3
        elif (self.box_select != "all") and (self.schedules_1 == []):
            self.msg_schedule_1 = "해당 일자의 리그 일정이 없습니다."
        else:
            for i in range(len(self.schedules_1)):
                self.msg_schedule_1 += (f"\n{self.schedules_1[i]}")

        if self.box_select[0] == "all":
            self.msg_schedule_2 = self.schedule_2_3
        elif (self.box_select != "all") and (self.schedules_2 == []):
            self.msg_schedule_2 = "해당 일자의 리그 일정이 없습니다."
        else:
            for i in range(len(self.schedules_2)):
                self.msg_schedule_2 += (f"\n{self.schedules_2[i]}")

        if self.box_select[0] == "all":
            self.msg_schedule_3 = self.schedule_3_3
        elif (self.box_select != "all") and (self.schedules_3 == []):
            self.msg_schedule_3 = "해당 일자의 리그 일정이 없습니다."
        else:
            for i in range(len(self.schedules_3)):
                self.msg_schedule_3 += (f"\n{self.schedules_3[i]}")

        self.msg_schedule_1_1 = ""
        self.msg_schedule_1_2 = ""
        if len(self.msg_schedule_1.split("\n")) > 25:
            for k in range(len(self.msg_schedule_1.split("\n"))):
                if k > 25: break
                self.msg_schedule_1_1 += "".join("\n" + self.msg_schedule_1.split("\n")[k])
            self.msg_schedule_1_2 += "".join(f"{self.msg_schedule_1_1}\n...")
        else:
            self.msg_schedule_1_2 += self.msg_schedule_1

        self.msg_schedule_2_1 = ""
        self.msg_schedule_2_2 = ""
        if len(self.msg_schedule_2.split("\n")) > 25:
            self.msg_schedule_2_1 = ""
            for k in range(len(self.msg_schedule_2.split("\n"))):
                if k > 25: break
                self.msg_schedule_2_1 += "".join("\n" + self.msg_schedule_2.split("\n")[k])
            self.msg_schedule_2_2 += "".join(f"{self.msg_schedule_2_1}\n...")
        else:
            self.msg_schedule_2_2 += self.msg_schedule_2

        self.msg_schedule_3_1 = ""
        self.msg_schedule_3_2 = ""
        if len(self.msg_schedule_3.split("\n")) > 25:
            for k in range(len(self.msg_schedule_3.split("\n"))):
                if k > 25: break
                self.msg_schedule_3_1 += "".join("\n" + self.msg_schedule_3.split("\n")[k])
            self.msg_schedule_3_2 += "".join(f"{self.msg_schedule_3_1}\n...")
        else:
            self.msg_schedule_3_2 += self.msg_schedule_3

        embed = discord.Embed(title="> 🗓️ 리그 일정", description="리그 오브 레전드의 리그 경기 일정 정보입니다.", color=colorMap['red'])
        embed.set_footer(text="TIP: 아래 버튼을 눌러 다른 일자의 일정도 살펴볼 수 있어요.", icon_url=self.bot.user.display_avatar.url)
        embed.set_image(url=self.banner)
        if (self.button == "1") or (self.button == ""):
            embed.add_field(name=f"{self.schedule_1_1[0]} 일정", value=f"└ (총 **3**페이지 중 **1**번째 페이지)\n```{self.msg_schedule_1_2}```", inline=False)
        elif self.button == "2":
            embed.add_field(name=f"{self.schedule_2_1[0]} 일정", value=f"└ (총 **3**페이지 중 **2**번째 페이지)\n```{self.msg_schedule_2_2}```", inline=False)
        elif self.button == "3":
            embed.add_field(name=f"{self.schedule_3_1[0]} 일정", value=f"└ (총 **3**페이지 중 **3**번째 페이지)\n```{self.msg_schedule_3_2}```", inline=False)
        await interaction.response.edit_message(content="", embed=embed)

        self.callback_select = True
        self.box_select.clear()
        self.schedules_1.clear()
        self.schedules_2.clear()
        self.schedules_3.clear()

    @discord.ui.button(emoji="1️⃣", style=discord.ButtonStyle.gray, row=1)
    async def _one(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.button = "1"

        self.msg_schedule_1_1 = ""
        self.msg_schedule_1_3 = ""
        if len(self.schedule_1_2.split("\n")) > 25:
            for k in range(len(self.schedule_1_2.split("\n"))):
                if k > 25: break
                self.msg_schedule_1_1 += "".join("\n" + self.schedule_1_2.split("\n")[k])
            self.msg_schedule_1_3 += "".join(f"{self.msg_schedule_1_1}\n...")
        else:
            self.msg_schedule_1_3 += self.schedule_1_2

        if self.schedule_1_3 == "해당 일자의 리그 일정이 없습니다.": self.msg_schedule_1_3 = "해당 일자의 리그 일정이 없습니다."

        embed = discord.Embed(title="> 🗓️ 리그 일정", description="리그 오브 레전드의 리그 경기 일정 정보입니다.", color=colorMap['red'])
        embed.set_footer(text="TIP: 아래 버튼을 눌러 다른 일자의 일정도 살펴볼 수 있어요.", icon_url=self.bot.user.display_avatar.url)
        embed.set_image(url=self.banner)
        if self.callback_select == True:
            embed.add_field(name=f"{self.schedule_1_1[0]} 일정", value=f"└ (총 **3**페이지 중 **1**번째 페이지)\n```{self.msg_schedule_1_2}```", inline=False)
        else:
            embed.add_field(name=f"{self.schedule_1_1[0]} 일정", value=f"└ (총 **3**페이지 중 **1**번째 페이지)\n```{self.msg_schedule_1_3}```", inline=False)
        await interaction.response.edit_message(content="", embed=embed)
        self.box_select.clear()

    @discord.ui.button(emoji="2️⃣", style=discord.ButtonStyle.gray, row=1)
    async def _two(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.button = "2"

        self.msg_schedule_2_1 = ""
        self.msg_schedule_2_3 = ""
        if len(self.schedule_2_2.split("\n")) > 25:
            self.msg_schedule_2_1 = ""
            for k in range(len(self.schedule_2_2.split("\n"))):
                if k > 25: break
                self.msg_schedule_2_1 += "".join("\n" + self.schedule_2_2.split("\n")[k])
            self.msg_schedule_2_3 += "".join(f"{self.msg_schedule_2_1}\n...")
        else:
            self.msg_schedule_2_3 += self.schedule_2_2

        if self.schedule_2_3 == "해당 일자의 리그 일정이 없습니다.": self.msg_schedule_2_3 = "해당 일자의 리그 일정이 없습니다."

        embed = discord.Embed(title="> 🗓️ 리그 일정", description="리그 오브 레전드의 리그 경기 일정 정보입니다.", color=colorMap['red'])
        embed.set_footer(text="TIP: 아래 버튼을 눌러 다른 일자의 일정도 살펴볼 수 있어요.", icon_url=self.bot.user.display_avatar.url)
        embed.set_image(url=self.banner)
        if self.callback_select == True:
            embed.add_field(name=f"{self.schedule_2_1[0]} 일정", value=f"└ (총 **3**페이지 중 **2**번째 페이지)\n```{self.msg_schedule_2_2}```", inline=False)
        else:
            embed.add_field(name=f"{self.schedule_2_1[0]} 일정", value=f"└ (총 **3**페이지 중 **2**번째 페이지)\n```{self.msg_schedule_2_3}```", inline=False)
        await interaction.response.edit_message(content="", embed=embed)
        self.box_select.clear()

    @discord.ui.button(emoji="3️⃣", style=discord.ButtonStyle.gray, row=1)
    async def _three(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.button = "3"

        self.msg_schedule_3_1 = ""
        self.msg_schedule_3_3 = ""
        if len(self.schedule_3_2.split("\n")) > 25:
            for k in range(len(self.schedule_3_2.split("\n"))):
                if k > 25: break
                self.msg_schedule_3_1 += "".join("\n" + self.schedule_3_2.split("\n")[k])
            self.msg_schedule_3_3 += "".join(f"{self.msg_schedule_3_1}\n...")
        else:
            self.msg_schedule_3_3 += self.schedule_3_2

        if self.schedule_3_3 == "해당 일자의 리그 일정이 없습니다.": self.msg_schedule_3_3 = "해당 일자의 리그 일정이 없습니다."

        embed = discord.Embed(title="> 🗓️ 리그 일정", description="리그 오브 레전드의 리그 경기 일정 정보입니다.", color=colorMap['red'])
        embed.set_footer(text="TIP: 아래 버튼을 눌러 다른 일자의 일정도 살펴볼 수 있어요.", icon_url=self.bot.user.display_avatar.url)
        embed.set_image(url=self.banner)
        if self.callback_select == True:
            embed.add_field(name=f"{self.schedule_3_1[0]} 일정", value=f"└ (총 **3**페이지 중 **3**번째 페이지)\n```{self.msg_schedule_3_2}```", inline=False)
        else:
            embed.add_field(name=f"{self.schedule_3_1[0]} 일정", value=f"└ (총 **3**페이지 중 **3**번째 페이지)\n```{self.msg_schedule_3_3}```", inline=False)
        await interaction.response.edit_message(content="", embed=embed)
        self.box_select.clear()

    async def on_timeout(self):
        await self.msg.edit_original_response(content="", view=DisabledButton())


class DisabledButton(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Select(placeholder="리그 선택하기", options=[discord.SelectOption(label="asdf", value="1", description="asdf")], disabled=True, row=0))
        self.add_item(discord.ui.Button(emoji="1️⃣", disabled=True, row=1))
        self.add_item(discord.ui.Button(emoji="2️⃣", disabled=True, row=1))
        self.add_item(discord.ui.Button(emoji="3️⃣", disabled=True, row=1))
        self.add_item(discord.ui.Button(label="OP.GG Esports에서 보기", url=esports_op_gg_schedules, row=1))


class ScheduleCMD(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    _leagues = SlashCommandGroup(name="리그", description="리그 명령어", guild_only=False)

    @_leagues.command(
        name="일정",
        description="리그 오브 레전드 리그의 경기 일정을 불러와요.",
    )
    async def _scheduleCMD(self, ctx):

        banner_image_url = random.choice(config['banner_image_url'])

        embed = discord.Embed(title="", description="⌛ 정보를 불러오는 중...", color=colorMap['red'])
        msg = await ctx.respond(embed=embed)

        try:
            nowTime = datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%Y-%m-%d")
            date_temp = datetime.datetime.strptime(nowTime, "%Y-%m-%d")
            date_delta = datetime.timedelta(hours=time_difference)
            time = date_temp + date_delta
            nowTime = time.strftime("%Y-%m-%d")

            tomorrowTime = (datetime.datetime.now(pytz.timezone("Asia/Seoul")) + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            date_temp = datetime.datetime.strptime(tomorrowTime, "%Y-%m-%d")
            date_delta = datetime.timedelta(hours=time_difference)
            time = date_temp + date_delta
            tomorrowTime = time.strftime("%Y-%m-%d")

            dayAfterTomorrowTime = (datetime.datetime.now(pytz.timezone("Asia/Seoul")) + datetime.timedelta(days=2)).strftime("%Y-%m-%d")
            date_temp = datetime.datetime.strptime(dayAfterTomorrowTime, "%Y-%m-%d")
            date_delta = datetime.timedelta(hours=time_difference)
            time = date_temp + date_delta
            dayAfterTomorrowTime = time.strftime("%Y-%m-%d")

            box_1_match_schedule_1 = []
            box_1_match_schedule_2 = []
            box_1_match_info = []
            box_2_match_schedule_1 = []
            box_2_match_schedule_2 = []
            box_2_match_info = []
            box_3_match_schedule_1 = []
            box_3_match_schedule_2 = []
            box_3_match_info = []

            for i in range(3):
                if i == 0: dateTime = nowTime
                elif i == 1: dateTime = tomorrowTime
                elif i == 2: dateTime = dayAfterTomorrowTime
                matches = opgg.load_schedule(date=dateTime)

                if matches['error'] == False:

                    temp_originalScheduledAt = []
                    box_originalScheduledAt = []
                    for i in range(len(matches['data'])):
                        temp_originalScheduledAt.append(matches['data'][i]['originalScheduledAt'].replace("T", " ").split(".000Z")[0])
                        date_temp = datetime.datetime.strptime(temp_originalScheduledAt[i], "%Y-%m-%d %H:%M:%S")
                        date_delta = datetime.timedelta(hours=time_difference)
                        time = date_temp + date_delta
                        box_originalScheduledAt.append(time.strftime("%Y-%m-%d %H:%M:%S"))

                    temp_scheduledAt = []
                    box_scheduledAt = []
                    for i in range(len(matches['data'])):
                        temp_scheduledAt.append(matches['data'][i]['scheduledAt'].replace("T", " ").split(".000Z")[0])
                        date_temp = datetime.datetime.strptime(temp_scheduledAt[i], "%Y-%m-%d %H:%M:%S")
                        date_delta = datetime.timedelta(hours=time_difference)
                        time = date_temp + date_delta
                        box_scheduledAt.append(time.strftime("%Y-%m-%d %H:%M:%S"))

                    for i in range(len(matches['data'])):
                        for j in range(16):
                            if matches['data'][i]['tournament']['serie']['league']['shortName'] == leagues[j]['shortName']:
                                try: match_acronym = matches['data'][i]['name'].split(': ')[1]
                                except: match_acronym = matches['data'][i]['name']
                                match_schedule_1 = box_scheduledAt[i].split(" ")[0]
                                match_schedule_2 = box_scheduledAt[i].split(" ")[1][0:5]
                                match_schedule_3 = datetime.datetime.strptime(match_schedule_1, "%Y-%m-%d").strftime("X%Y년 X%m월 X%d일").replace("X0", "").replace("X", "")
                                match_league = leagues[j]['shortName']
                                match_region = leagues[j]['region']
                                match_info = f"[{match_schedule_2}] {match_acronym} ({match_league}/{match_region})"

                                if match_schedule_1 == nowTime:
                                    box_1_match_schedule_1.append(match_schedule_1)
                                    box_1_match_schedule_2.append(match_schedule_3)
                                    box_1_match_info.append(match_info)
                                if match_schedule_1 == tomorrowTime:
                                    box_2_match_schedule_1.append(match_schedule_1)
                                    box_2_match_schedule_2.append(match_schedule_3)
                                    box_2_match_info.append(match_info)
                                if match_schedule_1 == dayAfterTomorrowTime:
                                    box_3_match_schedule_1.append(match_schedule_1)
                                    box_3_match_schedule_2.append(match_schedule_3)
                                    box_3_match_info.append(match_info)

                else:
                    print(f"{matches['code']}: {matches['message']}")

            if box_1_match_schedule_1 == []:
                box_1_match_schedule_1 = [""]
                box_1_match_schedule_2 = [datetime.datetime.strptime(nowTime, "%Y-%m-%d").strftime("X%Y년 X%m월 X%d일").replace("X0", "").replace("X", "")]

            if box_2_match_schedule_1 == []:
                box_2_match_schedule_1 = [""]
                box_2_match_schedule_2 = [datetime.datetime.strptime(tomorrowTime, "%Y-%m-%d").strftime("X%Y년 X%m월 X%d일").replace("X0", "").replace("X", "")]

            if box_3_match_schedule_1 == []:
                box_3_match_schedule_1 = [""]
                box_3_match_schedule_2 = [datetime.datetime.strptime(dayAfterTomorrowTime, "%Y-%m-%d").strftime("X%Y년 X%m월 X%d일").replace("X0", "").replace("X", "")]

            if (box_1_match_schedule_1[0] == nowTime) and (box_1_match_info):

                msg_schedule_info_1 = ""
                for i in range(len(box_1_match_info)):
                    if len(box_1_match_info) != 0:
                        msg_schedule_info_1 += "".join(f"\n{box_1_match_info[i]}")

                msg_schedule_info_2 = ""
                for i in range(len(box_2_match_info)):
                    if len(box_2_match_info) != 0:
                        msg_schedule_info_2 += "".join(f"\n{box_2_match_info[i]}")

                msg_schedule_info_3 = ""
                for i in range(len(box_3_match_info)):
                    if len(box_3_match_info) != 0:
                        msg_schedule_info_3 += "".join(f"\n{box_3_match_info[i]}")

                msg_schedule_info_1_1 = ""
                msg_schedule_info_1_2 = ""
                if len(msg_schedule_info_1.split("\n")) > 25:
                    for k in range(len(msg_schedule_info_1.split("\n"))):
                        if k > 25: break
                        msg_schedule_info_1_1 += "".join("\n" + msg_schedule_info_1.split("\n")[k])
                    msg_schedule_info_1_2 += "".join(f"{msg_schedule_info_1_1}\n...")
                else:
                    msg_schedule_info_1_2 += msg_schedule_info_1

                msg_schedule_info_2_1 = ""
                msg_schedule_info_2_2 = ""
                if len(msg_schedule_info_2.split("\n")) > 25:
                    msg_schedule_info_2_1 = ""
                    for k in range(len(msg_schedule_info_2.split("\n"))):
                        if k > 25: break
                        msg_schedule_info_2_1 += "".join("\n" + msg_schedule_info_2.split("\n")[k])
                    msg_schedule_info_2_2 += "".join(f"{msg_schedule_info_2_1}\n...")
                else:
                    msg_schedule_info_2_2 += msg_schedule_info_2

                msg_schedule_info_3_1 = ""
                msg_schedule_info_3_2 = ""
                if len(msg_schedule_info_3.split("\n")) > 25:
                    for k in range(len(msg_schedule_info_3.split("\n"))):
                        if k > 25: break
                        msg_schedule_info_3_1 += "".join("\n" + msg_schedule_info_3.split("\n")[k])
                    msg_schedule_info_3_2 += "".join(f"{msg_schedule_info_3_1}\n...")
                else:
                    msg_schedule_info_3_2 += msg_schedule_info_3

            elif (box_2_match_schedule_1[0] == tomorrowTime) and (box_2_match_info):

                msg_schedule_info_1 = ""
                msg_schedule_info_1_1 = ""
                msg_schedule_info_1_2 = "해당 일자의 리그 일정이 없습니다."

                msg_schedule_info_2 = ""
                for i in range(len(box_2_match_info)):
                    if len(box_2_match_info) != 0:
                        msg_schedule_info_2 += "".join(f"\n{box_2_match_info[i]}")

                msg_schedule_info_3 = ""
                for i in range(len(box_3_match_info)):
                    if len(box_3_match_info) != 0:
                        msg_schedule_info_3 += "".join(f"\n{box_3_match_info[i]}")

                msg_schedule_info_2_1 = ""
                msg_schedule_info_2_2 = ""
                if len(msg_schedule_info_2.split("\n")) > 25:
                    msg_schedule_info_2_1 = ""
                    for k in range(len(msg_schedule_info_2.split("\n"))):
                        if k > 25: break
                        msg_schedule_info_2_1 += "".join("\n" + msg_schedule_info_2.split("\n")[k])
                    msg_schedule_info_2_2 += "".join(f"{msg_schedule_info_2_1}\n...")
                else:
                    msg_schedule_info_2_2 += msg_schedule_info_2

                msg_schedule_info_3_1 = ""
                msg_schedule_info_3_2 = ""
                if len(msg_schedule_info_3.split("\n")) > 25:
                    for k in range(len(msg_schedule_info_3.split("\n"))):
                        if k > 25: break
                        msg_schedule_info_3_1 += "".join("\n" + msg_schedule_info_3.split("\n")[k])
                    msg_schedule_info_3_2 += "".join(f"{msg_schedule_info_3_1}\n...")
                else:
                    msg_schedule_info_3_2 += msg_schedule_info_3

            elif (box_3_match_schedule_1[0] == dayAfterTomorrowTime) and (box_3_match_info):

                msg_schedule_info_1 = ""
                msg_schedule_info_1_1 = ""
                msg_schedule_info_1_2 = "해당 일자의 리그 일정이 없습니다."

                msg_schedule_info_2 = ""
                msg_schedule_info_1_1 = ""
                msg_schedule_info_2_2 = "해당 일자의 리그 일정이 없습니다."

                msg_schedule_info_3 = ""
                for i in range(len(box_3_match_info)):
                    if len(box_3_match_info) != 0:
                        msg_schedule_info_3 += "".join(f"\n{box_3_match_info[i]}")

                msg_schedule_info_3_1 = ""
                msg_schedule_info_3_2 = ""
                if len(msg_schedule_info_3.split("\n")) > 25:
                    for k in range(len(msg_schedule_info_3.split("\n"))):
                        if k > 25: break
                        msg_schedule_info_3_1 += "".join("\n" + msg_schedule_info_3.split("\n")[k])
                    msg_schedule_info_3_2 += "".join(f"{msg_schedule_info_3_1}\n...")
                else:
                    msg_schedule_info_3_2 += msg_schedule_info_3

            else:
                msg_schedule_info_1 = ""
                msg_schedule_info_1_1 = ""
                msg_schedule_info_1_2 = "해당 일자의 리그 일정이 없습니다."

                msg_schedule_info_2 = ""
                msg_schedule_info_1_1 = ""
                msg_schedule_info_2_2 = "해당 일자의 리그 일정이 없습니다."

                msg_schedule_info_3 = ""
                msg_schedule_info_1_1 = ""
                msg_schedule_info_3_2 = "해당 일자의 리그 일정이 없습니다."

            embed = discord.Embed(title="> 🗓️ 리그 일정", description="리그 오브 레전드의 리그 경기 일정 정보입니다.", color=colorMap['red'])
            embed.set_footer(text="TIP: 아래 버튼을 눌러 다른 일자의 일정도 살펴볼 수 있어요.", icon_url=self.bot.user.display_avatar.url)
            embed.set_image(url=banner_image_url)
            embed.add_field(name=f"{box_1_match_schedule_2[0]} 일정", value=f"└ (총 **3**페이지 중 **1**번째 페이지)\n```{msg_schedule_info_1_2}```", inline=False)
            await msg.edit_original_response(content="", embed=embed, view=ScheduleButton(self.bot, ctx, msg, banner_image_url, box_1_match_schedule_2, msg_schedule_info_1, msg_schedule_info_1_2, box_2_match_schedule_2, msg_schedule_info_2, msg_schedule_info_2_2, box_3_match_schedule_2, msg_schedule_info_3, msg_schedule_info_3_2))

        except Exception as error:
            print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
            print(traceback.format_exc())



def setup(bot):
    bot.add_cog(ScheduleCMD(bot))
    print("schedule.py 로드 됨")
