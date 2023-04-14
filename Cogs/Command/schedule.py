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

time_difference = config['time_difference']
colorMap = config['colorMap']
esports_op_gg_schedules = "https://esports.op.gg/schedules"


class ScheduleButton(discord.ui.View):

    def __init__(self, bot, ctx, msg, banner, box_1_match_schedule_2, msg_schedule_info_1, msg_schedule_info_1_2, box_2_match_schedule_2, msg_schedule_info_2, msg_schedule_info_2_2, box_3_match_schedule_2, msg_schedule_info_3, msg_schedule_info_3_2):
        super().__init__(timeout=60)
        self.bot = bot
        self.ctx = ctx
        self.msg = msg
        self.banner = banner

        if box_1_match_schedule_2 == "해당 일자의 경기 일정이 없습니다.":
            self.schedule_1_1 = []
            self.schedule_1_2 = []
            self.schedule_1_3 = ["해당 일자의 경기 일정이 없습니다."]
        else:
            self.schedule_1_1 = box_1_match_schedule_2
            self.schedule_1_2 = msg_schedule_info_1
            self.schedule_1_3 = msg_schedule_info_1_2

        if box_2_match_schedule_2 == "해당 일자의 경기 일정이 없습니다.":
            self.schedule_2_1 = []
            self.schedule_2_2 = []
            self.schedule_2_3 = ["해당 일자의 경기 일정이 없습니다."]
        else:
            self.schedule_2_1 = box_2_match_schedule_2
            self.schedule_2_2 = msg_schedule_info_2
            self.schedule_2_3 = msg_schedule_info_2_2

        if box_3_match_schedule_2 == "해당 일자의 경기 일정이 없습니다.":
            self.schedule_3_1 = []
            self.schedule_3_2 = []
            self.schedule_3_3 = ["해당 일자의 경기 일정이 없습니다."]
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
        self.league_schedule_1 = []
        self.league_schedule_2 = []
        self.league_schedule_3 = []
        self.league_find = ""
        self.check_all = False
        self.button = ""
        self.callback_select = False
        self.add_item(discord.ui.Button(label="OP.GG E-Sports에서 보기", url=esports_op_gg_schedules, row=1))

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
    async def select_callback(self, select: discord.ui.Select, interaction):
        self.box_select = []
        self.schedules_1 = []
        self.schedules_2 = []
        self.schedules_3 = []
        self.msg_schedule_1 = ""
        self.msg_schedule_2 = ""
        self.msg_schedule_3 = ""
        self.league_schedule_1 = []
        self.league_schedule_2 = []
        self.league_schedule_3 = []
        self.league_find = ""
        self.check_all = False

        for i in range(len(select.values)):
            if select.values[i] == "0": self.box_select.append("all")
            elif select.values[i] == "1": self.box_select.append("LCK")
            elif select.values[i] == "2": self.box_select.append("LPL")
            elif select.values[i] == "3": self.box_select.append("LEC")
            elif select.values[i] == "4": self.box_select.append("LCS")
            elif select.values[i] == "5": self.box_select.append("CBLOL")
            elif select.values[i] == "6": self.box_select.append("VCS")
            elif select.values[i] == "7": self.box_select.append("LCL")
            elif select.values[i] == "8": self.box_select.append("TCL")
            elif select.values[i] == "9": self.box_select.append("PCS")
            elif select.values[i] == "10": self.box_select.append("LLA")
            elif select.values[i] == "11": self.box_select.append("LJL")
            elif select.values[i] == "12": self.box_select.append("LCO")
            elif select.values[i] == "13": self.box_select.append("MSI")
            elif select.values[i] == "14": self.box_select.append("OPL")
            elif select.values[i] == "15": self.box_select.append("LMS")
            elif select.values[i] == "16": self.box_select.append("Worlds")
            else: pass

        self.league_schedule_1 = self.schedule_1_2.split("\n")
        self.league_schedule_2 = self.schedule_2_2.split("\n")
        self.league_schedule_3 = self.schedule_3_2.split("\n")

        self.league_schedule_1 = list(filter(len, self.league_schedule_1))
        self.league_schedule_2 = list(filter(len, self.league_schedule_2))
        self.league_schedule_3 = list(filter(len, self.league_schedule_3))

        if self.league_schedule_1 == []: pass
        else:
            for i in range(len(self.box_select)):
                if self.box_select[i] == "all":
                    self.schedules_1 = []
                    self.schedules_1.append(self.schedule_1_3)
                    break
                else:
                    for j in range(len(self.league_schedule_1)):
                        self.league_find = self.league_schedule_1[j].split("(")[1].split("/")[0]
                        if self.league_find == self.box_select[i]:
                            self.schedules_1.append(self.league_schedule_1[j])

        if self.league_schedule_2 == []: pass
        else:
            for i in range(len(self.box_select)):
                if self.box_select[i] == "all":
                    self.schedules_2 = []
                    self.schedules_2.append(self.schedule_2_3)
                    break
                else:
                    for j in range(len(self.league_schedule_2)):
                        self.league_find = self.league_schedule_2[j].split("(")[1].split("/")[0]
                        if self.league_find == self.box_select[i]:
                            self.schedules_2.append(self.league_schedule_2[j])

        if self.league_schedule_3 == []: pass
        else:
            for i in range(len(self.box_select)):
                if self.box_select[i] == "all":
                    self.schedules_3 = []
                    self.schedules_3.append(self.schedule_3_3)
                    break
                else:
                    for j in range(len(self.league_schedule_3)):
                        self.league_find = self.league_schedule_3[j].split("(")[1].split("/")[0]
                        if self.league_find == self.box_select[i]:
                            self.schedules_3.append(self.league_schedule_3[j])

        if self.schedules_1 == []: self.msg_schedule_1 = "해당 일자의 경기 일정이 없습니다."
        for i in range(len(self.schedules_1)):
            for j in range(len(self.box_select)):
                if self.box_select[j] == "all":
                    self.check_all = True
                    self.msg_schedule_1 = self.schedule_1_3
                else: break
            if self.check_all == True: break
            else:
                self.msg_schedule_1 += f"\n{self.schedules_1[i]}"

        if self.schedules_2 == []: self.msg_schedule_2 = "해당 일자의 경기 일정이 없습니다."
        for i in range(len(self.schedules_2)):
            for j in range(len(self.box_select)):
                if self.box_select[j] == "all":
                    self.check_all = True
                    self.msg_schedule_2 = self.schedule_2_3
                else: break
            if self.check_all == True: break
            else:
                self.msg_schedule_2 += f"\n{self.schedules_2[i]}"

        if self.schedules_3 == []: self.msg_schedule_3 = "해당 일자의 경기 일정이 없습니다."
        for i in range(len(self.schedules_3)):
            for j in range(len(self.box_select)):
                if self.box_select[j] == "all":
                    self.check_all = True
                    self.msg_schedule_3 = self.schedule_3_3
                else: break
            if self.check_all == True: break
            else:
                self.msg_schedule_3 += f"\n{self.schedules_3[i]}"

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

        embed = discord.Embed(title="> 🗓️ 경기 일정", description="", color=colorMap['red'])
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

        if self.schedule_1_3 == "해당 일자의 경기 일정이 없습니다.": self.msg_schedule_1_3 = "해당 일자의 경기 일정이 없습니다."

        embed = discord.Embed(title="> 🗓️ 경기 일정", description="", color=colorMap['red'])
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

        if self.schedule_2_3 == "해당 일자의 경기 일정이 없습니다.": self.msg_schedule_2_3 = "해당 일자의 경기 일정이 없습니다."

        embed = discord.Embed(title="> 🗓️ 경기 일정", description="", color=colorMap['red'])
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

        if self.schedule_3_3 == "해당 일자의 경기 일정이 없습니다.": self.msg_schedule_3_3 = "해당 일자의 경기 일정이 없습니다."

        embed = discord.Embed(title="> 🗓️ 경기 일정", description="", color=colorMap['red'])
        embed.set_footer(text="TIP: 아래 버튼을 눌러 다른 일자의 일정도 살펴볼 수 있어요.", icon_url=self.bot.user.display_avatar.url)
        embed.set_image(url=self.banner)
        if self.callback_select == True:
            embed.add_field(name=f"{self.schedule_3_1[0]} 일정", value=f"└ (총 **3**페이지 중 **3**번째 페이지)\n```{self.msg_schedule_3_2}```", inline=False)
        else:
            embed.add_field(name=f"{self.schedule_3_1[0]} 일정", value=f"└ (총 **3**페이지 중 **3**번째 페이지)\n```{self.msg_schedule_3_3}```", inline=False)
        await interaction.response.edit_message(content="", embed=embed)
        self.box_select.clear()


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
        self.add_item(discord.ui.Button(label="OP.GG E-Sports에서 보기", url=esports_op_gg_schedules, row=1))


class ScheduleCMD(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    _matches = SlashCommandGroup(name="경기", description="경기 명령어", guild_only=False)

    @_matches.command(
        name="일정",
        description="리그 오브 레전드 e스포츠의 경기 일정을 불러와요.",
    )
    async def _scheduleCMD(self, ctx):

        banner_image_url = random.choice(config['banner_image_url'])

        embed = discord.Embed(title="", description="⌛ 정보를 불러오는 중...", color=colorMap['red'])
        msg = await ctx.respond(embed=embed)

        try:
            yesterdayTime = (datetime.datetime.now(pytz.timezone("Asia/Seoul")) + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
            nowTime = datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%Y-%m-%d")
            tomorrowTime = (datetime.datetime.now(pytz.timezone("Asia/Seoul")) + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            dayAfterTomorrowTime = (datetime.datetime.now(pytz.timezone("Asia/Seoul")) + datetime.timedelta(days=2)).strftime("%Y-%m-%d")

            box_1_match_schedule_1 = []
            box_1_match_schedule_2 = []
            box_1_match_info = []
            box_2_match_schedule_1 = []
            box_2_match_schedule_2 = []
            box_2_match_info = []
            box_3_match_schedule_1 = []
            box_3_match_schedule_2 = []
            box_3_match_info = []

            for i in range(4):
                if i == 0: dateTime = yesterdayTime
                elif i == 1: dateTime = nowTime
                elif i == 2: dateTime = tomorrowTime
                elif i == 3: dateTime = dayAfterTomorrowTime
                matches = opgg.load_schedule(date=dateTime)

                if matches['error'] == False:
                    temp_scheduledAt = []
                    box_scheduledAt = []

                    if matches['data'] == None:
                        if dateTime == nowTime:
                            box_1_match_schedule_1 = []
                            box_1_match_schedule_2.append(dateTime)
                        elif dateTime == tomorrowTime:
                            box_2_match_schedule_1 = []
                            box_2_match_schedule_2.append(dateTime)
                        elif dateTime == dayAfterTomorrowTime:
                            box_3_match_schedule_1 = []
                            box_3_match_schedule_2.append(dateTime)
                        else:
                            pass

                    else:
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
                                    elif match_schedule_1 == tomorrowTime:
                                        box_2_match_schedule_1.append(match_schedule_1)
                                        box_2_match_schedule_2.append(match_schedule_3)
                                        box_2_match_info.append(match_info)
                                    elif match_schedule_1 == dayAfterTomorrowTime:
                                        box_3_match_schedule_1.append(match_schedule_1)
                                        box_3_match_schedule_2.append(match_schedule_3)
                                        box_3_match_info.append(match_info)
                                    else:
                                        pass

                else:
                    print(f"[schedule.py] {matches['code']}: {matches['message']}")
                    embed = discord.Embed(title="> ⚠️ 오류", description=f"Code: `{matches['code']}`\nMessage: {matches['message']}", color=colorMap['red'])
                    return await msg.edit_original_response(content="", embed=embed)

            if box_1_match_schedule_1 == []:
                box_1_match_schedule_1 = [""]
                box_1_match_schedule_2 = [datetime.datetime.strptime(nowTime, "%Y-%m-%d").strftime("X%Y년 X%m월 X%d일").replace("X0", "").replace("X", "")]

            if box_2_match_schedule_1 == []:
                box_2_match_schedule_1 = [""]
                box_2_match_schedule_2 = [datetime.datetime.strptime(tomorrowTime, "%Y-%m-%d").strftime("X%Y년 X%m월 X%d일").replace("X0", "").replace("X", "")]

            if box_3_match_schedule_1 == []:
                box_3_match_schedule_1 = [""]
                box_3_match_schedule_2 = [datetime.datetime.strptime(dayAfterTomorrowTime, "%Y-%m-%d").strftime("X%Y년 X%m월 X%d일").replace("X0", "").replace("X", "")]

            if box_1_match_info == []:
                msg_schedule_info_1 = ""
                msg_schedule_info_1_1 = ""
                msg_schedule_info_1_2 = "해당 일자의 경기 일정이 없습니다."

            if box_2_match_info == []:
                msg_schedule_info_2 = ""
                msg_schedule_info_1_1 = ""
                msg_schedule_info_2_2 = "해당 일자의 경기 일정이 없습니다."

            if box_3_match_info == []:
                msg_schedule_info_3 = ""
                msg_schedule_info_1_1 = ""
                msg_schedule_info_3_2 = "해당 일자의 경기 일정이 없습니다."

            if (box_1_match_schedule_1[0] == nowTime) and (box_1_match_info):
                msg_schedule_info_1 = ""
                for i in range(len(box_1_match_info)):
                    if len(box_1_match_info) != 0:
                        msg_schedule_info_1 += "".join(f"\n{box_1_match_info[i]}")

                msg_schedule_info_1_1 = ""
                msg_schedule_info_1_2 = ""
                if len(msg_schedule_info_1.split("\n")) > 25:
                    for k in range(len(msg_schedule_info_1.split("\n"))):
                        if k > 25: break
                        msg_schedule_info_1_1 += "".join("\n" + msg_schedule_info_1.split("\n")[k])
                    msg_schedule_info_1_2 += "".join(f"{msg_schedule_info_1_1}\n...")
                else:
                    msg_schedule_info_1_2 += msg_schedule_info_1

            if (box_2_match_schedule_1[0] == tomorrowTime) and (box_2_match_info):
                msg_schedule_info_2 = ""
                for i in range(len(box_2_match_info)):
                    if len(box_2_match_info) != 0:
                        msg_schedule_info_2 += "".join(f"\n{box_2_match_info[i]}")

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

            if (box_3_match_schedule_1[0] == dayAfterTomorrowTime) and (box_3_match_info):
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

            embed = discord.Embed(title="> 🗓️ 경기 일정", description="", color=colorMap['red'])
            embed.set_footer(text="TIP: 아래 버튼을 눌러 다른 일자의 일정도 살펴볼 수 있어요.", icon_url=self.bot.user.display_avatar.url)
            embed.set_image(url=banner_image_url)
            embed.add_field(name=f"{box_1_match_schedule_2[0]} 일정", value=f"└ (총 **3**페이지 중 **1**번째 페이지)\n```{msg_schedule_info_1_2}```", inline=False)
            await msg.edit_original_response(content="", embed=embed, view=ScheduleButton(bot=self.bot, ctx=ctx, msg=msg, banner=banner_image_url, box_1_match_schedule_2=box_1_match_schedule_2, msg_schedule_info_1=msg_schedule_info_1, msg_schedule_info_1_2=msg_schedule_info_1_2, box_2_match_schedule_2=box_2_match_schedule_2, msg_schedule_info_2=msg_schedule_info_2, msg_schedule_info_2_2=msg_schedule_info_2_2, box_3_match_schedule_2=box_3_match_schedule_2, msg_schedule_info_3=msg_schedule_info_3, msg_schedule_info_3_2=msg_schedule_info_3_2))

        except Exception as error:
            print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
            print(traceback.format_exc())



def setup(bot):
    bot.add_cog(ScheduleCMD(bot))
    print("schedule.py 로드 됨")
