# -*- coding: utf-8 -*-

# 패키지 라이브러리 설정
import discord
from discord.ext import commands
from discord.commands import slash_command, Option
import random
import json
import datetime
import pytz
import traceback

import requests

from Extensions.i18n.substitution import Substitution
from Extensions.Process.season import get_bans_info, get_picks_info

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

esports_op_gg_champion = "https://esports.op.gg/champions/"
esports_op_gg_banpick = "https://esports.op.gg/banpick/"
time_difference = config['time_difference']
webhook_url = config['all_log_webhook_url']
colorMap = config['colorMap']


async def get_league(ctx: discord.AutocompleteContext):

    picked_league = ctx.options['{}'.format(lang_en['ban_pick.py']['command']['options']['league']['name'])]

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
    elif picked_league == "MSI":
        return ["MSI"]
    elif picked_league == "Worlds":
        return ["Worlds"]
    else:
        return ["LCK", "LPL", "LEC", "LCS", "CBLOL", "VCS", "LCL", "TCL", "PCS", "LLA", "LJL", "LCO", "MSI", "Worlds"]


class BanPickSelect(discord.ui.Select):

    def __init__(self, language, bot, ctx, msg, banner, picked_league):
        self.language = language
        self.bot = bot
        self.ctx = ctx
        self.msg = msg
        self.banner = banner
        self.picked_league = picked_league

        self.bans_info = None
        self.picks_info = None
        self.msg_1 = ""
        self.msg_2 = ""

        super().__init__(
            placeholder=self.language['ban_pick.py']['output']['select-pick_league']['placeholder'],
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
                discord.SelectOption(label="LCO / OCE", value="11", description="League of Legends Circuit Oceania"),
                discord.SelectOption(label="MSI", value="12", description="Mid-Season Invitational"),
                discord.SelectOption(label="Worlds", value="13", description="League of Legends World Championship")
            ],
            row=0
        )

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id: return await interaction.response.send_message(self.language['ban_pick.py']['output']['string-only_author_can_use'], ephemeral=True)

        serieId = []

        for i in range(16):
            if (self.values[0] == "0") and (leagues[i]['shortName'] == "LCK"):
                self.picked_league = "LCK"
                serieId = leagues[i]['serieId'][0]
            elif (self.values[0] == "1") and (leagues[i]['shortName'] == "LPL"):
                self.picked_league = "LPL"
                serieId = leagues[i]['serieId'][0]
            elif (self.values[0] == "2") and (leagues[i]['shortName'] == "LEC"):
                self.picked_league = "LEC"
                serieId = leagues[i]['serieId'][0]
            elif (self.values[0] == "3") and (leagues[i]['shortName'] == "LCS"):
                self.picked_league = "LCS"
                serieId = leagues[i]['serieId'][0]
            elif (self.values[0] == "4") and (leagues[i]['shortName'] == "CBLOL"):
                self.picked_league = "CBLOL"
                serieId = leagues[i]['serieId'][0]
            elif (self.values[0] == "5") and (leagues[i]['shortName'] == "VCS"):
                self.picked_league = "VCS"
                serieId = leagues[i]['serieId'][0]
            elif (self.values[0] == "6") and (leagues[i]['shortName'] == "LCL"):
                self.picked_league = "LCL"
                serieId = leagues[i]['serieId'][0]
            elif (self.values[0] == "7") and (leagues[i]['shortName'] == "TCL"):
                self.picked_league = "TCL"
                serieId = leagues[i]['serieId'][0]
            elif (self.values[0] == "8") and (leagues[i]['shortName'] == "PCS"):
                self.picked_league = "PCS"
                serieId = leagues[i]['serieId'][0]
            elif (self.values[0] == "9") and (leagues[i]['shortName'] == "LLA"):
                self.picked_league = "LLA"
                serieId = leagues[i]['serieId'][0]
            elif (self.values[0] == "10") and (leagues[i]['shortName'] == "LJL"):
                self.picked_league = "LJL"
                serieId = leagues[i]['serieId'][0]
            elif (self.values[0] == "11") and (leagues[i]['shortName'] == "LCO"):
                self.picked_league = "LCO"
                serieId = leagues[i]['serieId'][0]
            elif (self.values[0] == "12") and (leagues[i]['shortName'] == "MSI"):
                self.picked_league = "MSI"
                serieId = leagues[i]['serieId'][0]
            elif (self.values[0] == "13") and (leagues[i]['shortName'] == "Worlds"):
                self.picked_league = "Worlds"
                serieId = leagues[i]['serieId'][0]
            else: pass

            if serieId == []: continue
            elif serieId == None:
                embed = discord.Embed(title=self.language['ban_pick.py']['output']['embed-no_statistics']['title'], description=self.language['ban_pick.py']['output']['embed-statistics']['description'].format(picked_league=self.picked_league), color=colorMap['red'])
                embed.set_image(url=self.banner)
                embed.add_field(name=self.language['ban_pick.py']['output']['embed-statistics']['field_1']['name'], value=self.language['ban_pick.py']['output']['embed-statistics']['field_1']['value'], inline=True)
                embed.add_field(name=self.language['ban_pick.py']['output']['embed-statistics']['field_2']['name'], value=self.language['ban_pick.py']['output']['embed-statistics']['field_2']['value'], inline=True)
                return await interaction.response.edit_message(content="", embed=embed, view=BanPickInfoCMD(bot=self.bot, ctx=self.ctx, msg=self.msg, banner=self.banner, picked_league=self.picked_league))
            self.bans_info = get_bans_info(serieId=serieId)
            self.picks_info = get_picks_info(serieId=serieId)
            serieId = [] # 초기화

            try:
                print(f"[ban_pick.py] {self.bans_info['code']}: {self.bans_info['message']}")
                embed = discord.Embed(title=self.language['ban_pick.py']['output']['embed-no_data']['title'], description=self.language['ban_pick.py']['output']['embed-no_data']['description'].format(code=self.bans_info['code'], message=self.bans_info['message']), color=colorMap['red'])
                return await interaction.response.edit_message(content="", embed=embed, view=None)

            except:
                if (self.bans_info) and (self.picks_info):
                    embed = discord.Embed(title=self.language['ban_pick.py']['output']['embed-banpick']['title'], description=self.language['ban_pick.py']['output']['embed-banpick']['description'].format(picked_league=self.picked_league), color=colorMap['red'])

                    for i in range(len(self.bans_info)):
                        # msg_1 += f"\n{self.bans_info[i]['id']} {self.bans_info[i]['count']:,}회 밴 ({self.bans_info[i]['rate']}% 밴률)"
                        self.msg_1 += self.language['ban_pick.py']['output']['string-ban'].format(esports_champion=esports_op_gg_champion, ban_id=self.bans_info[i]['id'], ban_count=self.bans_info[i]['count'], ban_rate=self.bans_info[i]['rate'])

                    for j in range(len(self.picks_info)):
                        # msg_2 += f"\n{self.picks_info[j]['id']} {self.picks_info[j]['count']:,}회 픽 ({self.picks_info[j]['rate']}% 픽률)"
                        self.msg_2 += self.language['ban_pick.py']['output']['string-pick'].format(esports_champion=esports_op_gg_champion, pick_id=self.picks_info[i]['id'], pick_count=self.picks_info[i]['count'], pick_rate=self.picks_info[i]['rate'])

                    # embed.set_footer(text="TIP: SNS 아이콘을 클릭하면 해당 선수의 SNS로 바로 이동할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
                    embed.set_image(url=self.banner)
                    embed.add_field(name=self.language['ban_pick.py']['output']['embed-banpick']['field_1']['name'], value=self.msg_2, inline=True)
                    embed.add_field(name=self.language['ban_pick.py']['output']['embed-banpick']['field_2']['name'], value=self.msg_1, inline=True)

                    await interaction.response.edit_message(content="", embed=embed, view=BanPickView(language=self.language, bot=self.bot, ctx=self.ctx, msg=self.msg, banner=self.banner, picked_league=self.picked_league))
                else:
                    embed = discord.Embed(title=self.language['ban_pick.py']['output']['embed-no_statistics']['title'], description=self.language['ban_pick.py']['output']['embed-statistics']['description'].format(picked_league=self.picked_league), color=colorMap['red'])
                    embed.set_image(url=self.banner)
                    embed.add_field(name=self.language['ban_pick.py']['output']['embed-statistics']['field_1']['name'], value=self.language['ban_pick.py']['output']['embed-statistics']['field_1']['value'], inline=True)
                    embed.add_field(name=self.language['ban_pick.py']['output']['embed-statistics']['field_2']['name'], value=self.language['ban_pick.py']['output']['embed-statistics']['field_2']['value'], inline=True)
                    return await interaction.response.edit_message(content="", embed=embed, view=BanPickView(language=self.language, bot=self.bot, ctx=self.ctx, msg=self.msg, banner=self.banner, picked_league=self.picked_league))



class BanPickView(discord.ui.View):

    def __init__(self, language, bot, ctx, msg, banner, picked_league):
        super().__init__(timeout=60)
        self.language = language
        self.bot = bot
        self.ctx = ctx
        self.msg = msg
        self.banner = banner
        self.picked_league = picked_league
        self.add_item(discord.ui.Button(label=self.language['ban_pick.py']['output']['button-jump_esports'], url=f"{esports_op_gg_banpick}", row=1))
        self.add_item(BanPickSelect(language=self.language, bot=self.bot, ctx=self.ctx, msg=self.msg, banner=self.banner, picked_league=self.picked_league))

    async def on_timeout(self):
        try:
            await self.msg.edit_original_response(content="", view=DisabledButton(language=self.language))
        except discord.NotFound:
            pass


class DisabledButton(discord.ui.View):

    def __init__(self, language):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Select(placeholder=language['ban_pick.py']['output']['select-pick_league']['placeholder'], options=[discord.SelectOption(label="asdf", value="1", description="asdf")], disabled=True, row=0))
        self.add_item(discord.ui.Button(label=language['ban_pick.py']['output']['button-jump_esports'], url=f"{esports_op_gg_banpick}", row=1))


class BanPickInfoCMD(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name=lang_en['ban_pick.py']['command']['name'],
        name_localizations={
            "ko": lang_ko['ban_pick.py']['command']['name']
        },
        description=lang_en['ban_pick.py']['command']['description'],
        description_localizations={
            "ko": lang_ko['ban_pick.py']['command']['description']
        },
        options=[
            Option(
                name=lang_en['ban_pick.py']['command']['options']['league']['name'],
                name_localizations={
                    "ko": lang_ko['ban_pick.py']['command']['options']['league']['name']
                },
                description=lang_en['ban_pick.py']['command']['options']['league']['description'],
                description_localizations={
                    "ko": lang_ko['ban_pick.py']['command']['options']['league']['description']
                },
                required=True,
                autocomplete=discord.utils.basic_autocomplete(get_league)
            )
        ]
    )
    async def _ban_pickCMD(self, ctx: discord.AutocompleteContext, picked_league: str):

        language = Substitution.substitution(ctx)
        banner_image_url = random.choice(config['banner_image_url'])

        msg_1 = ""
        msg_2 = ""

        embed = discord.Embed(title="", description=language['ban_pick.py']['output']['embed-loading']['description'], color=colorMap['red'])
        msg = await ctx.respond(embed=embed)

        try:
            serieId = []

            for i in range(16):
                if (picked_league == "LCK") and (leagues[i]['shortName'] == "LCK"): serieId = leagues[i]['serieId'][0]
                elif (picked_league == "LPL") and (leagues[i]['shortName'] == "LPL"): serieId = leagues[i]['serieId'][0]
                elif (picked_league == "LEC") and (leagues[i]['shortName'] == "LEC"): serieId = leagues[i]['serieId'][0]
                elif (picked_league == "LCS") and (leagues[i]['shortName'] == "LCS"): serieId = leagues[i]['serieId'][0]
                elif (picked_league == "CBLOL") and (leagues[i]['shortName'] == "CBLOL"): serieId = leagues[i]['serieId'][0]
                elif (picked_league == "VCS") and (leagues[i]['shortName'] == "VCS"): serieId = leagues[i]['serieId'][0]
                elif (picked_league == "LCL") and (leagues[i]['shortName'] == "LCL"): serieId = leagues[i]['serieId'][0]
                elif (picked_league == "TCL") and (leagues[i]['shortName'] == "TCL"): serieId = leagues[i]['serieId'][0]
                elif (picked_league == "PCS") and (leagues[i]['shortName'] == "PCS"): serieId = leagues[i]['serieId'][0]
                elif (picked_league == "LLA") and (leagues[i]['shortName'] == "LLA"): serieId = leagues[i]['serieId'][0]
                elif (picked_league == "LJL") and (leagues[i]['shortName'] == "LJL"): serieId = leagues[i]['serieId'][0]
                elif (picked_league == "LCO") and (leagues[i]['shortName'] == "LCO"): serieId = leagues[i]['serieId'][0]
                elif (picked_league == "MSI") and (leagues[i]['shortName'] == "MSI"): serieId = leagues[i]['serieId'][0]
                elif (picked_league == "Worlds") and (leagues[i]['shortName'] == "Worlds"): serieId = leagues[i]['serieId'][0]
                else: pass

                if serieId == []: continue
                elif serieId == None:
                    embed = discord.Embed(title=language['ban_pick.py']['output']['embed-no_statistics']['title'], description=language['ban_pick.py']['output']['embed-statistics']['description'].format(picked_league=picked_league), color=colorMap['red'])
                    embed.set_image(url=banner_image_url)
                    embed.add_field(name=language['ban_pick.py']['output']['embed-statistics']['field_1']['name'], value=language['ban_pick.py']['output']['embed-statistics']['field_1']['value'], inline=True)
                    embed.add_field(name=language['ban_pick.py']['output']['embed-statistics']['field_2']['name'], value=language['ban_pick.py']['output']['embed-statistics']['field_2']['value'], inline=True)
                    return await msg.edit_original_response(content="", embed=embed, view=DisabledButton())

            embed = discord.Embed(title=language['ban_pick.py']['output']['embed-banpick']['title'], description=language['ban_pick.py']['output']['embed-banpick']['description'].format(picked_league=picked_league), color=colorMap['red'])

            bans_info = get_bans_info(serieId=serieId)
            for i in range(len(bans_info)):
                # msg_1 += f"\n{bans_info[i]['id']} {bans_info[i]['count']:,}회 밴 ({bans_info[i]['rate']}% 밴률)"
                msg_1 += language['ban_pick.py']['output']['string-ban'].format(esports_champion=esports_op_gg_champion, ban_id=bans_info[i]['id'], ban_count=bans_info[i]['count'], ban_rate=bans_info[i]['rate'])

            picks_info = get_picks_info(serieId=serieId)
            for j in range(len(picks_info)):
                # msg_2 += f"\n{picks_info[j]['id']} {picks_info[j]['count']:,}회 픽 ({picks_info[j]['rate']}% 픽률)"
                msg_2 += language['ban_pick.py']['output']['string-pick'].format(esports_champion=esports_op_gg_champion, pick_id=picks_info[j]['id'], pick_count=picks_info[j]['count'], pick_rate=picks_info[j]['rate'])

            # embed.set_footer(text="TIP: SNS 아이콘을 클릭하면 해당 선수의 SNS로 바로 이동할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
            embed.set_image(url=banner_image_url)
            embed.add_field(name=language['ban_pick.py']['output']['embed-banpick']['field_1']['name'], value=msg_2, inline=True)
            embed.add_field(name=language['ban_pick.py']['output']['embed-banpick']['field_2']['name'], value=msg_1, inline=True)

            await msg.edit_original_response(content="", embed=embed, view=BanPickView(language=language, bot=self.bot, ctx=ctx, msg=msg, banner=banner_image_url, picked_league=picked_league))

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
    bot.add_cog(BanPickInfoCMD(bot))
    print("ban_pick.py 로드 됨")
