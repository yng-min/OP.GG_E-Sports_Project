# -*- coding: utf-8 -*-

# 패키지 라이브러리 설정
import opgg
import discord
from discord.ext import commands
from discord.commands import slash_command
import random
import json
import datetime
import pytz
import traceback

import requests

from Extensions.i18n.substitution import Substitution

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

# en.json 파일 불러오기
try:
    with open(r"./Languages/en.json", "rt", encoding="UTF8") as enJson:
        lang_en = json.load(enJson)
except: print("en.json이 로드되지 않음")

# ko.json 파일 불러오기
try:
    with open(r"./Languages/ko.json", "rt", encoding="UTF8") as koJson:
        lang_ko = json.load(koJson)
except: print("ko.json이 로드되지 않음")

time_difference = config['time_difference']
webhook_url = config['all_log_webhook_url']
colorMap = config['colorMap']
esports_op_gg_schedules = "https://esports.op.gg/schedules"


def embed_setup(bot, banner,title, description, footer, match_schedule, schedule_info):

    embed = discord.Embed(title=title, description=description, color=colorMap['red'])
    embed.set_footer(text=footer, icon_url=bot.user.display_avatar.url)
    embed.set_image(url=banner)
    embed.add_field(name=match_schedule, value=schedule_info, inline=False)
    return embed


class ScheduleSelect(discord.ui.Select):

    def __init__(self, language, bot, ctx, msg, banner, button, box_1_match_schedule_2, msg_schedule_info_1, msg_schedule_info_1_2, box_2_match_schedule_2, msg_schedule_info_2, msg_schedule_info_2_2, box_3_match_schedule_2, msg_schedule_info_3, msg_schedule_info_3_2):
        super().__init__()
        self.language = language
        self.bot = bot
        self.ctx = ctx
        self.msg = msg
        self.banner = banner
        self.button = button

        if msg_schedule_info_1 == self.language['schedule.py']['output']['string-no_schedule']:
            self.schedule_1_1 = box_1_match_schedule_2
            self.schedule_1_2 = self.language['schedule.py']['output']['string-no_schedule']
            self.schedule_1_3 = [self.language['schedule.py']['output']['string-no_schedule']]
        else:
            self.schedule_1_1 = box_1_match_schedule_2
            self.schedule_1_2 = msg_schedule_info_1
            self.schedule_1_3 = msg_schedule_info_1_2

        if msg_schedule_info_2 == self.language['schedule.py']['output']['string-no_schedule']:
            self.schedule_2_1 = box_2_match_schedule_2
            self.schedule_2_2 = self.language['schedule.py']['output']['string-no_schedule']
            self.schedule_2_3 = [self.language['schedule.py']['output']['string-no_schedule']]
        else:
            self.schedule_2_1 = box_2_match_schedule_2
            self.schedule_2_2 = msg_schedule_info_2
            self.schedule_2_3 = msg_schedule_info_2_2

        if msg_schedule_info_3 == self.language['schedule.py']['output']['string-no_schedule']:
            self.schedule_3_1 = box_3_match_schedule_2
            self.schedule_3_2 = self.language['schedule.py']['output']['string-no_schedule']
            self.schedule_3_3 = [self.language['schedule.py']['output']['string-no_schedule']]
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
        self.callback_select = False

        super().__init__(
            placeholder=self.language['schedule.py']['output']['select-pick_league']['placeholder'],
            min_values=1,
            max_values=17,
            options=[
                discord.SelectOption(label=self.language['schedule.py']['output']['select-pick_league']['options']['option_all']['label'], value="0", description=language['schedule.py']['output']['select-pick_league']['options']['option_all']['description']),
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
        if interaction.user.id != self.ctx.author.id: return await interaction.response.send_message(self.language['schedule.py']['output']['string-only_author_can_use'], ephemeral=True)

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

        for i in range(len(self.values)):
            if self.values[i] == "0": self.box_select.append("all")
            elif self.values[i] == "1": self.box_select.append("LCK")
            elif self.values[i] == "2": self.box_select.append("LPL")
            elif self.values[i] == "3": self.box_select.append("LEC")
            elif self.values[i] == "4": self.box_select.append("LCS")
            elif self.values[i] == "5": self.box_select.append("CBLOL")
            elif self.values[i] == "6": self.box_select.append("VCS")
            elif self.values[i] == "7": self.box_select.append("LCL")
            elif self.values[i] == "8": self.box_select.append("TCL")
            elif self.values[i] == "9": self.box_select.append("PCS")
            elif self.values[i] == "10": self.box_select.append("LLA")
            elif self.values[i] == "11": self.box_select.append("LJL")
            elif self.values[i] == "12": self.box_select.append("LCO")
            elif self.values[i] == "13": self.box_select.append("MSI")
            elif self.values[i] == "14": self.box_select.append("OPL")
            elif self.values[i] == "15": self.box_select.append("LMS")
            elif self.values[i] == "16": self.box_select.append("Worlds")
            else: pass

        try:
            self.league_schedule_1 = self.schedule_1_2.split("\n")
            self.league_schedule_1 = list(filter(len, self.league_schedule_1))
        except:
            pass

        try:
            self.league_schedule_2 = self.schedule_2_2.split("\n")
            self.league_schedule_2 = list(filter(len, self.league_schedule_2))
        except:
            pass

        try:
            self.league_schedule_3 = self.schedule_3_2.split("\n")
            self.league_schedule_3 = list(filter(len, self.league_schedule_3))
        except:
            pass

        if self.league_schedule_1 == []: pass
        else:
            for i in range(len(self.box_select)):
                if self.box_select[i] == "all":
                    self.schedules_1 = []
                    self.schedules_1.append(self.schedule_1_3)
                    break
                else:
                    for j in range(len(self.league_schedule_1)):
                        try:
                            self.league_find = self.league_schedule_1[j].split("(")[1].split("/")[0]
                            if self.league_find == self.box_select[i]:
                                self.schedules_1.append(self.league_schedule_1[j])
                        except:
                            pass

        if self.league_schedule_2 == []: pass
        else:
            for i in range(len(self.box_select)):
                if self.box_select[i] == "all":
                    self.schedules_2 = []
                    self.schedules_2.append(self.schedule_2_3)
                    break
                else:
                    for j in range(len(self.league_schedule_2)):
                        try:
                            self.league_find = self.league_schedule_2[j].split("(")[1].split("/")[0]
                            if self.league_find == self.box_select[i]:
                                self.schedules_2.append(self.league_schedule_2[j])
                        except:
                            pass

        if self.league_schedule_3 == []: pass
        else:
            for i in range(len(self.box_select)):
                if self.box_select[i] == "all":
                    self.schedules_3 = []
                    self.schedules_3.append(self.schedule_3_3)
                    break
                else:
                    for j in range(len(self.league_schedule_3)):
                        try:
                            self.league_find = self.league_schedule_3[j].split("(")[1].split("/")[0]
                            if self.league_find == self.box_select[i]:
                                self.schedules_3.append(self.league_schedule_3[j])
                        except:
                            pass

        if self.schedules_1 == []: self.msg_schedule_1 = self.language['schedule.py']['output']['string-no_schedule']
        for i in range(len(self.schedules_1)):
            for j in range(len(self.box_select)):
                if self.box_select[j] == "all":
                    self.check_all = True
                    self.msg_schedule_1 = self.schedule_1_3
                else: break
            if self.check_all == True: break
            else:
                self.msg_schedule_1 += f"\n{self.schedules_1[i]}"

        if self.schedules_2 == []: self.msg_schedule_2 = self.language['schedule.py']['output']['string-no_schedule']
        for i in range(len(self.schedules_2)):
            for j in range(len(self.box_select)):
                if self.box_select[j] == "all":
                    self.check_all = True
                    self.msg_schedule_2 = self.schedule_2_3
                else: break
            if self.check_all == True: break
            else:
                self.msg_schedule_2 += f"\n{self.schedules_2[i]}"

        if self.schedules_3 == []: self.msg_schedule_3 = self.language['schedule.py']['output']['string-no_schedule']
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
        try:
            if (len(self.msg_schedule_1) != 0) and (len(self.msg_schedule_1.split("\n")) > 25):
                for k in range(len(self.msg_schedule_1.split("\n"))):
                    if k > 25: break
                    self.msg_schedule_1_1 += "".join("\n" + self.msg_schedule_1.split("\n")[k])
                self.msg_schedule_1_2 += "".join(f"{self.msg_schedule_1_1}\n...")
            else:
                self.msg_schedule_1_2 += self.msg_schedule_1
        except:
            self.msg_schedule_1_2 = self.msg_schedule_1[0]

        self.msg_schedule_2_1 = ""
        self.msg_schedule_2_2 = ""
        try:
            if (len(self.msg_schedule_2) != 0) and (len(self.msg_schedule_2.split("\n")) > 25):
                self.msg_schedule_2_1 = ""
                for k in range(len(self.msg_schedule_2.split("\n"))):
                    if k > 25: break
                    self.msg_schedule_2_1 += "".join("\n" + self.msg_schedule_2.split("\n")[k])
                self.msg_schedule_2_2 += "".join(f"{self.msg_schedule_2_1}\n...")
            else:
                self.msg_schedule_2_2 += self.msg_schedule_2
        except:
            self.msg_schedule_2_2 = self.msg_schedule_2[0]

        self.msg_schedule_3_1 = ""
        self.msg_schedule_3_2 = ""
        try:
            if (len(self.msg_schedule_3) != 0) and (len(self.msg_schedule_3.split("\n")) > 25):
                for k in range(len(self.msg_schedule_3.split("\n"))):
                    if k > 25: break
                    self.msg_schedule_3_1 += "".join("\n" + self.msg_schedule_3.split("\n")[k])
                self.msg_schedule_3_2 += "".join(f"{self.msg_schedule_3_1}\n...")
            else:
                self.msg_schedule_3_2 += self.msg_schedule_3
        except:
            self.msg_schedule_3_2 = self.msg_schedule_3[0]

        if (self.button == "1") or (self.button == ""):
            embed = embed_setup(
                bot=self.bot,
                banner=self.banner,
                title=self.language['schedule.py']['output']['embed-schedule_1']['title'],
                description="",
                footer=self.language['schedule.py']['output']['embed-schedule_1']['footer'],
                match_schedule=self.language['schedule.py']['output']['embed-schedule_1']['field_1']['name'].format(match_schedule=self.schedule_1_1[0]),
                schedule_info=self.language['schedule.py']['output']['embed-schedule_1']['field_1']['value'].format(schedule_info=self.msg_schedule_1_2),
            )
        elif self.button == "2":
            embed = embed_setup(
                bot=self.bot,
                banner=self.banner,
                title=self.language['schedule.py']['output']['embed-schedule_2']['title'],
                description="",
                footer=self.language['schedule.py']['output']['embed-schedule_2']['footer'],
                match_schedule=self.language['schedule.py']['output']['embed-schedule_2']['field_1']['name'].format(match_schedule=self.schedule_2_1[0]),
                schedule_info=self.language['schedule.py']['output']['embed-schedule_2']['field_1']['value'].format(schedule_info=self.msg_schedule_2_2),
            )
        elif self.button == "3":
            embed = embed_setup(
                bot=self.bot,
                banner=self.banner,
                title=self.language['schedule.py']['output']['embed-schedule_3']['title'],
                description="",
                footer=self.language['schedule.py']['output']['embed-schedule_3']['footer'],
                match_schedule=self.language['schedule.py']['output']['embed-schedule_3']['field_1']['name'].format(match_schedule=self.schedule_3_1[0]),
                schedule_info=self.language['schedule.py']['output']['embed-schedule_3']['field_1']['value'].format(schedule_info=self.msg_schedule_3_2),
            )
        await interaction.response.edit_message(content="", embed=embed, view=ScheduleView(language=self.language, bot=self.bot, ctx=self.ctx, msg=self.msg, banner=self.banner, button=self.button, box_1_match_schedule_2=self.schedule_1_1, msg_schedule_info_1=self.schedule_1_2, msg_schedule_info_1_2=self.schedule_1_3, box_2_match_schedule_2=self.schedule_2_1, msg_schedule_info_2=self.schedule_2_2, msg_schedule_info_2_2=self.schedule_2_3, box_3_match_schedule_2=self.schedule_3_1, msg_schedule_info_3=self.schedule_3_2, msg_schedule_info_3_2=self.schedule_3_3))

        self.callback_select = True


class ScheduleView(discord.ui.View):

    def __init__(self, language, bot, ctx, msg, banner, button, box_1_match_schedule_2, msg_schedule_info_1, msg_schedule_info_1_2, box_2_match_schedule_2, msg_schedule_info_2, msg_schedule_info_2_2, box_3_match_schedule_2, msg_schedule_info_3, msg_schedule_info_3_2):
        super().__init__(timeout=60)
        self.language = language
        self.bot = bot
        self.ctx = ctx
        self.msg = msg
        self.banner = banner
        self.button = button

        if msg_schedule_info_1 == self.language['schedule.py']['output']['string-no_schedule']:
            self.schedule_1_1 = box_1_match_schedule_2
            self.schedule_1_2 = self.language['schedule.py']['output']['string-no_schedule']
            self.schedule_1_3 = [self.language['schedule.py']['output']['string-no_schedule']]
        else:
            self.schedule_1_1 = box_1_match_schedule_2
            self.schedule_1_2 = msg_schedule_info_1
            self.schedule_1_3 = msg_schedule_info_1_2

        if msg_schedule_info_2 == self.language['schedule.py']['output']['string-no_schedule']:
            self.schedule_2_1 = box_2_match_schedule_2
            self.schedule_2_2 = self.language['schedule.py']['output']['string-no_schedule']
            self.schedule_2_3 = [self.language['schedule.py']['output']['string-no_schedule']]
        else:
            self.schedule_2_1 = box_2_match_schedule_2
            self.schedule_2_2 = msg_schedule_info_2
            self.schedule_2_3 = msg_schedule_info_2_2

        if msg_schedule_info_3 == self.language['schedule.py']['output']['string-no_schedule']:
            self.schedule_3_1 = box_3_match_schedule_2
            self.schedule_3_2 = self.language['schedule.py']['output']['string-no_schedule']
            self.schedule_3_3 = [self.language['schedule.py']['output']['string-no_schedule']]
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
        self.callback_select = False
        self.add_item(ScheduleSelect(language=language, bot=bot, ctx=ctx, msg=msg, banner=banner, button=self.button, box_1_match_schedule_2=box_1_match_schedule_2, msg_schedule_info_1=msg_schedule_info_1, msg_schedule_info_1_2=msg_schedule_info_1_2, box_2_match_schedule_2=box_2_match_schedule_2, msg_schedule_info_2=msg_schedule_info_2, msg_schedule_info_2_2=msg_schedule_info_2_2, box_3_match_schedule_2=box_3_match_schedule_2, msg_schedule_info_3=msg_schedule_info_3, msg_schedule_info_3_2=msg_schedule_info_3_2))
        self.add_item(discord.ui.Button(label=self.language['schedule.py']['output']['button-jump_esports'], url=esports_op_gg_schedules, row=1))


    @discord.ui.button(emoji="1️⃣", style=discord.ButtonStyle.gray, row=1)
    async def _one(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id: return await interaction.response.send_message(self.language['schedule.py']['output']['string-only_author_can_use'], ephemeral=True)

        self.button = "1"

        self.msg_schedule_1_1 = ""
        self.msg_schedule_1_3 = ""
        if (len(self.schedule_1_2) != 0) and (len(self.schedule_1_2.split("\n")) > 25):
            for k in range(len(self.schedule_1_2.split("\n"))):
                if k > 25: break
                self.msg_schedule_1_1 += "".join("\n" + self.schedule_1_2.split("\n")[k])
            self.msg_schedule_1_3 += "".join(f"{self.msg_schedule_1_1}\n...")
        else:
            self.msg_schedule_1_3 += self.schedule_1_2

        if self.schedule_1_3 == self.language['schedule.py']['output']['string-no_schedule']: self.msg_schedule_1_3 = self.language['schedule.py']['output']['string-no_schedule']

        if self.callback_select == True:
            embed = embed_setup(
                bot=self.bot,
                banner=self.banner,
                title=self.language['schedule.py']['output']['embed-schedule_1']['title'],
                description="",
                footer=self.language['schedule.py']['output']['embed-schedule_1']['footer'],
                match_schedule=self.language['schedule.py']['output']['embed-schedule_1']['field_1']['name'].format(match_schedule=self.schedule_1_1[0]),
                schedule_info=self.language['schedule.py']['output']['embed-schedule_1']['field_1']['value'].format(schedule_info=self.msg_schedule_1_2),
            )
        else:
            embed = embed_setup(
                bot=self.bot,
                banner=self.banner,
                title=self.language['schedule.py']['output']['embed-schedule_1']['title'],
                description="",
                footer=self.language['schedule.py']['output']['embed-schedule_1']['footer'],
                match_schedule=self.language['schedule.py']['output']['embed-schedule_1']['field_1']['name'].format(match_schedule=self.schedule_1_1[0]),
                schedule_info=self.language['schedule.py']['output']['embed-schedule_1']['field_1']['value'].format(schedule_info=self.msg_schedule_1_3),
            )
        await interaction.response.edit_message(content="", embed=embed, view=ScheduleView(language=self.language, bot=self.bot, ctx=self.ctx, msg=self.msg, banner=self.banner, button=self.button, box_1_match_schedule_2=self.schedule_1_1, msg_schedule_info_1=self.schedule_1_2, msg_schedule_info_1_2=self.schedule_1_3, box_2_match_schedule_2=self.schedule_2_1, msg_schedule_info_2=self.schedule_2_2, msg_schedule_info_2_2=self.schedule_2_3, box_3_match_schedule_2=self.schedule_3_1, msg_schedule_info_3=self.schedule_3_2, msg_schedule_info_3_2=self.schedule_3_3))
        self.box_select.clear()


    @discord.ui.button(emoji="2️⃣", style=discord.ButtonStyle.gray, row=1)
    async def _two(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id: return await interaction.response.send_message(self.language['schedule.py']['output']['string-only_author_can_use'], ephemeral=True)

        self.button = "2"

        self.msg_schedule_2_1 = ""
        self.msg_schedule_2_3 = ""
        if (len(self.schedule_2_2) != 0) and (len(self.schedule_2_2.split("\n")) > 25):
            self.msg_schedule_2_1 = ""
            for k in range(len(self.schedule_2_2.split("\n"))):
                if k > 25: break
                self.msg_schedule_2_1 += "".join("\n" + self.schedule_2_2.split("\n")[k])
            self.msg_schedule_2_3 += "".join(f"{self.msg_schedule_2_1}\n...")
        else:
            self.msg_schedule_2_3 += self.schedule_2_2

        if self.schedule_2_3 == self.language['schedule.py']['output']['string-no_schedule']: self.msg_schedule_2_3 = self.language['schedule.py']['output']['string-no_schedule']

        if self.callback_select == True:
            embed = embed_setup(
                bot=self.bot,
                banner=self.banner,
                title=self.language['schedule.py']['output']['embed-schedule_2']['title'],
                description="",
                footer=self.language['schedule.py']['output']['embed-schedule_2']['footer'],
                match_schedule=self.language['schedule.py']['output']['embed-schedule_2']['field_1']['name'].format(match_schedule=self.schedule_2_1[0]),
                schedule_info=self.language['schedule.py']['output']['embed-schedule_2']['field_1']['value'].format(schedule_info=self.msg_schedule_2_2),
            )
        else:
            embed = embed_setup(
                bot=self.bot,
                banner=self.banner,
                title=self.language['schedule.py']['output']['embed-schedule_2']['title'],
                description="",
                footer=self.language['schedule.py']['output']['embed-schedule_2']['footer'],
                match_schedule=self.language['schedule.py']['output']['embed-schedule_2']['field_1']['name'].format(match_schedule=self.schedule_2_1[0]),
                schedule_info=self.language['schedule.py']['output']['embed-schedule_2']['field_1']['value'].format(schedule_info=self.msg_schedule_2_3),
            )
        await interaction.response.edit_message(content="", embed=embed, view=ScheduleView(language=self.language, bot=self.bot, ctx=self.ctx, msg=self.msg, banner=self.banner, button=self.button, box_1_match_schedule_2=self.schedule_1_1, msg_schedule_info_1=self.schedule_1_2, msg_schedule_info_1_2=self.schedule_1_3, box_2_match_schedule_2=self.schedule_2_1, msg_schedule_info_2=self.schedule_2_2, msg_schedule_info_2_2=self.schedule_2_3, box_3_match_schedule_2=self.schedule_3_1, msg_schedule_info_3=self.schedule_3_2, msg_schedule_info_3_2=self.schedule_3_3))
        self.box_select.clear()


    @discord.ui.button(emoji="3️⃣", style=discord.ButtonStyle.gray, row=1)
    async def _three(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id: return await interaction.response.send_message(self.language['schedule.py']['output']['string-only_author_can_use'], ephemeral=True)

        self.button = "3"

        self.msg_schedule_3_1 = ""
        self.msg_schedule_3_3 = ""
        if (len(self.schedule_3_2) != 0) and (len(self.schedule_3_2.split("\n")) > 25):
            for k in range(len(self.schedule_3_2.split("\n"))):
                if k > 25: break
                self.msg_schedule_3_1 += "".join("\n" + self.schedule_3_2.split("\n")[k])
            self.msg_schedule_3_3 += "".join(f"{self.msg_schedule_3_1}\n...")
        else:
            self.msg_schedule_3_3 += self.schedule_3_2

        if self.schedule_3_3 == self.language['schedule.py']['output']['string-no_schedule']: self.msg_schedule_3_3 = self.language['schedule.py']['output']['string-no_schedule']

        if self.callback_select == True:
            embed = embed_setup(
                bot=self.bot,
                banner=self.banner,
                title=self.language['schedule.py']['output']['embed-schedule_3']['title'],
                description="",
                footer=self.language['schedule.py']['output']['embed-schedule_3']['footer'],
                match_schedule=self.language['schedule.py']['output']['embed-schedule_3']['field_1']['name'].format(match_schedule=self.schedule_3_1[0]),
                schedule_info=self.language['schedule.py']['output']['embed-schedule_3']['field_1']['value'].format(schedule_info=self.msg_schedule_3_2),
            )
        else:
            embed = embed_setup(
                bot=self.bot,
                banner=self.banner,
                title=self.language['schedule.py']['output']['embed-schedule_3']['title'],
                description="",
                footer=self.language['schedule.py']['output']['embed-schedule_3']['footer'],
                match_schedule=self.language['schedule.py']['output']['embed-schedule_3']['field_1']['name'].format(match_schedule=self.schedule_3_1[0]),
                schedule_info=self.language['schedule.py']['output']['embed-schedule_3']['field_1']['value'].format(schedule_info=self.msg_schedule_3_3),
            )
        await interaction.response.edit_message(content="", embed=embed, view=ScheduleView(language=self.language, bot=self.bot, ctx=self.ctx, msg=self.msg, banner=self.banner, button=self.button, box_1_match_schedule_2=self.schedule_1_1, msg_schedule_info_1=self.schedule_1_2, msg_schedule_info_1_2=self.schedule_1_3, box_2_match_schedule_2=self.schedule_2_1, msg_schedule_info_2=self.schedule_2_2, msg_schedule_info_2_2=self.schedule_2_3, box_3_match_schedule_2=self.schedule_3_1, msg_schedule_info_3=self.schedule_3_2, msg_schedule_info_3_2=self.schedule_3_3))
        self.box_select.clear()


    async def on_timeout(self):
        try:
            await self.msg.edit_original_response(content="", view=DisabledButton(language=self.language))
        except discord.NotFound:
            pass


class DisabledButton(discord.ui.View):

    def __init__(self, language):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Select(placeholder=language['schedule.py']['output']['select-pick_league']['placeholder'], options=[discord.SelectOption(label="asdf", value="1", description="asdf")], disabled=True, row=0))
        self.add_item(discord.ui.Button(emoji="1️⃣", disabled=True, row=1))
        self.add_item(discord.ui.Button(emoji="2️⃣", disabled=True, row=1))
        self.add_item(discord.ui.Button(emoji="3️⃣", disabled=True, row=1))
        self.add_item(discord.ui.Button(label=language['schedule.py']['output']['button-jump_esports'], url=esports_op_gg_schedules, row=1))


class ScheduleCMD(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name=lang_en['schedule.py']['command']['name'],
        name_localizations={
            "ko": lang_ko['schedule.py']['command']['name']
        },
        description=lang_en['schedule.py']['command']['description'],
        description_localizations={
            "ko": lang_ko['schedule.py']['command']['description']
        }
    )
    async def _scheduleCMD(self, ctx):

        language = Substitution.substitution(ctx)
        banner_image_url = random.choice(config['banner_image_url'])

        embed = discord.Embed(title="", description=language['schedule.py']['output']['embed-loading']['description'], color=colorMap['red'])
        msg = await ctx.respond(embed=embed)

        try:
            yesterdayTime = (datetime.datetime.now(pytz.timezone(language['global']['timezone'])) + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
            nowTime = datetime.datetime.now(pytz.timezone(language['global']['timezone'])).strftime("%Y-%m-%d")
            tomorrowTime = (datetime.datetime.now(pytz.timezone(language['global']['timezone'])) + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            dayAfterTomorrowTime = (datetime.datetime.now(pytz.timezone(language['global']['timezone'])) + datetime.timedelta(days=2)).strftime("%Y-%m-%d")

            box_1_match_schedule_1 = []
            box_1_match_schedule_2 = []
            box_1_match_info = []
            box_2_match_schedule_1 = []
            box_2_match_schedule_2 = []
            box_2_match_info = []
            box_3_match_schedule_1 = []
            box_3_match_schedule_2 = []
            box_3_match_info = []

            msg_schedule_info_1 = ""
            msg_schedule_info_1_1 = ""
            msg_schedule_info_1_2 = ""
            msg_schedule_info_2 = ""
            msg_schedule_info_2_1 = ""
            msg_schedule_info_2_2 = ""
            msg_schedule_info_3 = ""
            msg_schedule_info_3_1 = ""
            msg_schedule_info_3_2 = ""

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
                                    match_schedule_3 = datetime.datetime.strptime(match_schedule_1, "%Y-%m-%d").strftime(language['schedule.py']['output']['string-match_schedule']).replace("X0", "").replace("X", "")
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
                    embed = discord.Embed(title=language['schedule.py']['output']['embed-no_data']['title'], description=language['schedule.py']['output']['embed-no_data']['description'].format(code=matches['code'], message=matches['message']), color=colorMap['red'])
                    return await msg.edit_original_response(content="", embed=embed)

            if box_1_match_schedule_1 == []:
                box_1_match_schedule_1 = [""]
                box_1_match_schedule_2 = [datetime.datetime.strptime(nowTime, "%Y-%m-%d").strftime(language['schedule.py']['output']['string-match_schedule']).replace("X0", "").replace("X", "")]

            if box_2_match_schedule_1 == []:
                box_2_match_schedule_1 = [""]
                box_2_match_schedule_2 = [datetime.datetime.strptime(tomorrowTime, "%Y-%m-%d").strftime(language['schedule.py']['output']['string-match_schedule']).replace("X0", "").replace("X", "")]

            if box_3_match_schedule_1 == []:
                box_3_match_schedule_1 = [""]
                box_3_match_schedule_2 = [datetime.datetime.strptime(dayAfterTomorrowTime, "%Y-%m-%d").strftime(language['schedule.py']['output']['string-match_schedule']).replace("X0", "").replace("X", "")]

            if (box_1_match_schedule_1[0] == nowTime) and (box_1_match_info):
                for i in range(len(box_1_match_info)):
                    if len(box_1_match_info) != 0:
                        msg_schedule_info_1 += "".join(f"\n{box_1_match_info[i]}")

                if (len(msg_schedule_info_1) != 0) and (len(msg_schedule_info_1.split("\n")) > 25):
                    for k in range(len(msg_schedule_info_1.split("\n"))):
                        if k > 25: break
                        msg_schedule_info_1_1 += "".join("\n" + msg_schedule_info_1.split("\n")[k])
                    msg_schedule_info_1_2 += "".join(f"{msg_schedule_info_1_1}\n...")
                else:
                    msg_schedule_info_1_2 += msg_schedule_info_1

            if (box_2_match_schedule_1[0] == tomorrowTime) and (box_2_match_info):
                for i in range(len(box_2_match_info)):
                    if len(box_2_match_info) != 0:
                        msg_schedule_info_2 += "".join(f"\n{box_2_match_info[i]}")

                if (len(msg_schedule_info_2) != 0) and (len(msg_schedule_info_2.split("\n")) > 25):
                    for k in range(len(msg_schedule_info_2.split("\n"))):
                        if k > 25: break
                        msg_schedule_info_2_1 += "".join("\n" + msg_schedule_info_2.split("\n")[k])
                    msg_schedule_info_2_2 += "".join(f"{msg_schedule_info_2_1}\n...")
                else:
                    msg_schedule_info_2_2 += msg_schedule_info_2

            if (box_3_match_schedule_1[0] == dayAfterTomorrowTime) and (box_3_match_info):
                for i in range(len(box_3_match_info)):
                    if len(box_3_match_info) != 0:
                        msg_schedule_info_3 += "".join(f"\n{box_3_match_info[i]}")

                if (len(msg_schedule_info_3) != 0) and (len(msg_schedule_info_3.split("\n")) > 25):
                    for k in range(len(msg_schedule_info_3.split("\n"))):
                        if k > 25: break
                        msg_schedule_info_3_1 += "".join("\n" + msg_schedule_info_3.split("\n")[k])
                    msg_schedule_info_3_2 += "".join(f"{msg_schedule_info_3_1}\n...")
                else:
                    msg_schedule_info_3_2 += msg_schedule_info_3

            if msg_schedule_info_1 == "": msg_schedule_info_1 = language['schedule.py']['output']['string-no_schedule']
            if msg_schedule_info_1_1 == "": msg_schedule_info_1_1 = language['schedule.py']['output']['string-no_schedule']
            if msg_schedule_info_1_2 == "": msg_schedule_info_1_2 = language['schedule.py']['output']['string-no_schedule']
            if msg_schedule_info_2 == "": msg_schedule_info_2 = language['schedule.py']['output']['string-no_schedule']
            if msg_schedule_info_2_1 == "": msg_schedule_info_2_1 = language['schedule.py']['output']['string-no_schedule']
            if msg_schedule_info_2_2 == "": msg_schedule_info_2_2 = language['schedule.py']['output']['string-no_schedule']
            if msg_schedule_info_3 == "": msg_schedule_info_3 = language['schedule.py']['output']['string-no_schedule']
            if msg_schedule_info_3_1 == "": msg_schedule_info_3_1 = language['schedule.py']['output']['string-no_schedule']
            if msg_schedule_info_3_2 == "": msg_schedule_info_3_2 = language['schedule.py']['output']['string-no_schedule']

            embed = embed_setup(
                bot=self.bot,
                banner=banner_image_url,
                title=language['schedule.py']['output']['embed-schedule_1']['title'],
                description="",
                footer=language['schedule.py']['output']['embed-schedule_1']['footer'],
                match_schedule=language['schedule.py']['output']['embed-schedule_1']['field_1']['name'].format(match_schedule=box_1_match_schedule_2[0]),
                schedule_info=language['schedule.py']['output']['embed-schedule_1']['field_1']['value'].format(schedule_info=msg_schedule_info_1_2),
            )
            await msg.edit_original_response(content="", embed=embed, view=ScheduleView(language=language, bot=self.bot, ctx=ctx, msg=msg, banner=banner_image_url, button="", box_1_match_schedule_2=box_1_match_schedule_2, msg_schedule_info_1=msg_schedule_info_1, msg_schedule_info_1_2=msg_schedule_info_1_2, box_2_match_schedule_2=box_2_match_schedule_2, msg_schedule_info_2=msg_schedule_info_2, msg_schedule_info_2_2=msg_schedule_info_2_2, box_3_match_schedule_2=box_3_match_schedule_2, msg_schedule_info_3=msg_schedule_info_3, msg_schedule_info_3_2=msg_schedule_info_3_2))

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
    bot.add_cog(ScheduleCMD(bot))
    print("schedule.py 로드 됨")
