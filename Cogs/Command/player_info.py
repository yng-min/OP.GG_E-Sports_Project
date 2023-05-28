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
from Extensions.Process.match import get_game_info_by_id
from Extensions.Process.player import get_player_info_by_nickname, get_team_info_by_id, get_player_recent_matches_by_id
from Extensions.Process.search import get_search_player

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

esports_op_gg_player = "https://esports.op.gg/players/"
esports_op_gg_team = "https://esports.op.gg/teams/"
esports_op_gg_match = "https://esports.op.gg/matches/"
esports_op_gg_champion = "https://esports.op.gg/champions/"
op_gg_player = "https://www.op.gg/summoners/"
time_difference = config['time_difference']
webhook_url = config['all_log_webhook_url']
colorMap = config['colorMap']
emoji_hyperlink = emoji['Hyperlink']
emoji_stream = emoji['LiveStream']
emoji_esports = emoji['Esports']
emoji_discord = emoji['Discord']
emoji_facebook = emoji['Facebook']
emoji_instagram = emoji['Instagram']
emoji_twitter = emoji['Twitter']
emoji_youtube = emoji['YouTube']
emoji_baron = emoji['Baron']
emoji_dragon = emoji['Dragon']
emoji_elder_drake = emoji['ElderDrake']
emoji_herald = emoji['Herald']
emoji_inhibitor = emoji['Inhibitor']
emoji_tower = emoji['Tower']
emoji_blueside = emoji['BlueSide']
emoji_redside = emoji['RedSide']


async def search_player(ctx: discord.AutocompleteContext):

    language = Substitution.substitution(ctx.interaction)
    player_displayed_nickname = ""
    try: keyword = ctx.options['{}'.format(lang_en['player_info.py']['command']['options']['player']['name'])].split(" ")[1]
    except: keyword = ctx.options['{}'.format(lang_en['player_info.py']['command']['options']['player']['name'])]

    try:
        box_search_data = get_search_player(keyword=keyword)

        for i in range(len(box_search_data)):
            player_displayed_nickname = box_search_data[i]['displayedNickname']

        try:
            print(f"[player_info.py] {box_search_data['code']}: {box_search_data['message']}")
            return [ ]

        except:
            if box_search_data == []: return [ ]
            return [ player_displayed_nickname ]

    except:
        return [ ]


def make_game_info_embed(language, picked_match, picked_set, box_player, box_players, box_recent_matches, player_id, player_displayed_nickname, player_nationality):

    picked_match = box_recent_matches[picked_match - 1]
    match_date = datetime.datetime.strptime(picked_match['beginAt'].split("T")[0], "%Y-%m-%d").strftime(language['player_info.py']['output']['string-match_schedule']).replace("X0", "").replace("X", "")

    game_info = get_game_info_by_id(matchId=picked_match['id'], matchSet=str(picked_set))

    try: ban_1_1 = f"[⬜]({esports_op_gg_champion}{game_info['teams'][0]['bans'][0]})"
    except: ban_1_1 = "❌"
    try: ban_1_2 = f"[⬜]({esports_op_gg_champion}{game_info['teams'][0]['bans'][1]})"
    except: ban_1_2 = "❌"
    try: ban_1_3 = f"[⬜]({esports_op_gg_champion}{game_info['teams'][0]['bans'][2]})"
    except: ban_1_3 = "❌"
    try: ban_1_4 = f"[⬜]({esports_op_gg_champion}{game_info['teams'][0]['bans'][3]})"
    except: ban_1_4 = "❌"
    try: ban_1_5 = f"[⬜]({esports_op_gg_champion}{game_info['teams'][0]['bans'][4]})"
    except: ban_1_5 = "❌"
    try: ban_2_1 = f"[⬜]({esports_op_gg_champion}{game_info['teams'][1]['bans'][0]})"
    except: ban_2_1 = "❌"
    try: ban_2_2 = f"[⬜]({esports_op_gg_champion}{game_info['teams'][1]['bans'][1]})"
    except: ban_2_2 = "❌"
    try: ban_2_3 = f"[⬜]({esports_op_gg_champion}{game_info['teams'][1]['bans'][2]})"
    except: ban_2_3 = "❌"
    try: ban_2_4 = f"[⬜]({esports_op_gg_champion}{game_info['teams'][1]['bans'][3]})"
    except: ban_2_4 = "❌"
    try: ban_2_5 = f"[⬜]({esports_op_gg_champion}{game_info['teams'][1]['bans'][4]})"
    except: ban_2_5 = "❌"

    msg_ban_1 = f"🚫) {ban_1_1} {ban_1_2} {ban_1_3} {ban_1_4} {ban_1_5}"
    msg_ban_2 = f"🚫) {ban_2_1} {ban_2_2} {ban_2_3} {ban_2_4} {ban_2_5}"

    msg_object_1 = f"{emoji_tower} **{game_info['teams'][0]['towerKills']:,}** {emoji_inhibitor} **{game_info['teams'][0]['inhibitorKills']:,}** {emoji_herald} **{game_info['teams'][0]['heraldKills']:,}** {emoji_dragon} **{game_info['teams'][0]['dragonKills']:,}** {emoji_elder_drake} **{game_info['teams'][0]['elderDrakeKills']:,}** {emoji_baron} **{game_info['teams'][0]['baronKills']:,}**"
    msg_object_2 = f"{emoji_tower} **{game_info['teams'][1]['towerKills']:,}** {emoji_inhibitor} **{game_info['teams'][1]['inhibitorKills']:,}** {emoji_herald} **{game_info['teams'][1]['heraldKills']:,}** {emoji_dragon} **{game_info['teams'][1]['dragonKills']:,}** {emoji_elder_drake} **{game_info['teams'][1]['elderDrakeKills']:,}** {emoji_baron} **{game_info['teams'][1]['baronKills']:,}**"

    most_kda = []
    for j in range(len(game_info['players'])):
        if game_info['players'][j]['kda'] != "Perfect":
            most_kda.append(game_info['players'][j]['kda'])

    msg_player_1 = ""
    msg_player_2 = ""
    msg_kda_1 = ""
    msg_kda_2 = ""
    msg_damage_1 = ""
    msg_damage_2 = ""
    for k in range(len(game_info['players'])):
        if k < 5:
            if game_info['players'][k]['id'] == player_id:
                # msg_player_1 += f"\n{game_info['players'][k]['championId']} **{game_info['players'][k]['nickName']}**"
                msg_player_1 += f"\n⬜ **[{game_info['players'][k]['team_acronym']}]({esports_op_gg_team}{game_info['players'][k]['team_id']}) [{game_info['players'][k]['nickName']}]({esports_op_gg_player}{game_info['players'][k]['id']})**" # 챔피언 이모티콘 적용될 때까지만 임시
            else:
                # msg_player_1 += f"\n{game_info['players'][k]['championId']} {game_info['players'][k]['nickName']}"
                msg_player_1 += f"\n⬜ [{game_info['players'][k]['team_acronym']}]({esports_op_gg_team}{game_info['players'][k]['team_id']}) [{game_info['players'][k]['nickName']}]({esports_op_gg_player}{game_info['players'][k]['id']})" # 챔피언 이모티콘 적용될 때까지만 임시

            if game_info['players'][k]['kda'] == "Perfect":
                msg_kda_1 += language['player_info.py']['output']['string-kda_1'].format(kills=game_info['players'][k]['kills'], deaths=game_info['players'][k]['deaths'], assists=game_info['players'][k]['assists'], kda=game_info['players'][k]['kda'])
            elif game_info['players'][k]['kda'] == max(most_kda):
                msg_kda_1 += language['player_info.py']['output']['string-kda_2'].format(kills=game_info['players'][k]['kills'], deaths=game_info['players'][k]['deaths'], assists=game_info['players'][k]['assists'], kda=game_info['players'][k]['kda'])
            elif game_info['players'][k]['kda'] >= 3:
                msg_kda_1 += language['player_info.py']['output']['string-kda_3'].format(kills=game_info['players'][k]['kills'], deaths=game_info['players'][k]['deaths'], assists=game_info['players'][k]['assists'], kda=game_info['players'][k]['kda'])
            else:
                msg_kda_1 += language['player_info.py']['output']['string-kda_4'].format(kills=game_info['players'][k]['kills'], deaths=game_info['players'][k]['deaths'], assists=game_info['players'][k]['assists'], kda=game_info['players'][k]['kda'])

            msg_damage_1 += f"\n`{game_info['players'][k]['totalDamageDealtToChampions']:,}`"

        else:
            if game_info['players'][k]['id'] == player_id:
                # msg_player_2 += f"\n{game_info['players'][k]['championId']} **{game_info['players'][k]['nickName']}**"
                msg_player_2 += f"\n⬜ **[{game_info['players'][k]['team_acronym']}]({esports_op_gg_team}{game_info['players'][k]['team_id']}) [{game_info['players'][k]['nickName']}]({esports_op_gg_player}{game_info['players'][k]['id']})**" # 챔피언 이모티콘 적용될 때까지만 임시
            else:
                # msg_player_2 += f"\n{game_info['players'][k]['championId']} {game_info['players'][k]['nickName']}"
                msg_player_2 += f"\n⬜ [{game_info['players'][k]['team_acronym']}]({esports_op_gg_team}{game_info['players'][k]['team_id']}) [{game_info['players'][k]['nickName']}]({esports_op_gg_player}{game_info['players'][k]['id']})" # 챔피언 이모티콘 적용될 때까지만 임시

            if game_info['players'][k]['kda'] == "Perfect":
                msg_kda_2 += language['player_info.py']['output']['string-kda_1'].format(kills=game_info['players'][k]['kills'], deaths=game_info['players'][k]['deaths'], assists=game_info['players'][k]['assists'], kda=game_info['players'][k]['kda'])
            elif game_info['players'][k]['kda'] == max(most_kda):
                msg_kda_2 += language['player_info.py']['output']['string-kda_2'].format(kills=game_info['players'][k]['kills'], deaths=game_info['players'][k]['deaths'], assists=game_info['players'][k]['assists'], kda=game_info['players'][k]['kda'])
            elif game_info['players'][k]['kda'] >= 3:
                msg_kda_2 += language['player_info.py']['output']['string-kda_3'].format(kills=game_info['players'][k]['kills'], deaths=game_info['players'][k]['deaths'], assists=game_info['players'][k]['assists'], kda=game_info['players'][k]['kda'])
            else:
                msg_kda_2 += language['player_info.py']['output']['string-kda_4'].format(kills=game_info['players'][k]['kills'], deaths=game_info['players'][k]['deaths'], assists=game_info['players'][k]['assists'], kda=game_info['players'][k]['kda'])

            msg_damage_2 += f"\n`{game_info['players'][k]['totalDamageDealtToChampions']:,}`"

    embed = discord.Embed(title=language['player_info.py']['output']['embed-match_info']['title'], description="", color=colorMap['red'])
    embed.add_field(name=language['player_info.py']['output']['embed-match_info']['field_1']['name'].format(match_name=picked_match['name'], picked_set=picked_set), value=language['player_info.py']['output']['embed-match_info']['field_1']['value'].format(match_date=match_date), inline=False)

    if game_info['winner_name'] == game_info['teams'][0]['name']:
        embed.add_field(name=language['player_info.py']['output']['embed-match_info']['field_2']['name'].format(emoji_blueside=emoji_blueside, team=game_info['teams'][0]['name']), value=f"{msg_ban_1}ㅤ{msg_object_1}", inline=False)
        embed.add_field(name=language['player_info.py']['output']['embed-match_info']['field_3']['name'], value=msg_player_1, inline=True)
        embed.add_field(name=language['player_info.py']['output']['embed-match_info']['field_4']['name'], value=msg_kda_1, inline=True)
        embed.add_field(name=language['player_info.py']['output']['embed-match_info']['field_5']['name'], value=msg_damage_1, inline=True)
        embed.add_field(name=language['player_info.py']['output']['embed-match_info']['field_6']['name'].format(emoji_redside=emoji_redside, team=game_info['teams'][1]['name']), value=f"{msg_ban_2}ㅤ{msg_object_2}", inline=False)
        embed.add_field(name=language['player_info.py']['output']['embed-match_info']['field_7']['name'], value=msg_player_2, inline=True)
        embed.add_field(name=language['player_info.py']['output']['embed-match_info']['field_8']['name'], value=msg_kda_2, inline=True)
        embed.add_field(name=language['player_info.py']['output']['embed-match_info']['field_9']['name'], value=msg_damage_2, inline=True)
    else:
        embed.add_field(name=language['player_info.py']['output']['embed-match_info']['field_else_2']['name'].format(emoji_blueside=emoji_blueside, team=game_info['teams'][0]['name']), value=f"{msg_ban_1}ㅤ{msg_object_1}", inline=False)
        embed.add_field(name=language['player_info.py']['output']['embed-match_info']['field_3']['name'], value=msg_player_1, inline=True)
        embed.add_field(name=language['player_info.py']['output']['embed-match_info']['field_4']['name'], value=msg_kda_1, inline=True)
        embed.add_field(name=language['player_info.py']['output']['embed-match_info']['field_5']['name'], value=msg_damage_1, inline=True)
        embed.add_field(name=language['player_info.py']['output']['embed-match_info']['field_else_6']['name'].format(emoji_redside=emoji_redside, team=game_info['teams'][1]['name']), value=f"{msg_ban_2}ㅤ{msg_object_2}", inline=False)
        embed.add_field(name=language['player_info.py']['output']['embed-match_info']['field_7']['name'], value=msg_player_2, inline=True)
        embed.add_field(name=language['player_info.py']['output']['embed-match_info']['field_8']['name'], value=msg_kda_2, inline=True)
        embed.add_field(name=language['player_info.py']['output']['embed-match_info']['field_9']['name'], value=msg_damage_2, inline=True)

    return embed


class MatchInfoSelect(discord.ui.Select):

    def __init__(self, language, bot, ctx, msg, origin_embed, picked_match, picked_set, box_player, box_players, box_recent_matches, player_id, player_displayed_nickname, player_nationality):
        self.language = language
        self.bot = bot
        self.ctx = ctx
        self.msg = msg
        self.origin_embed = origin_embed
        self.box_player = box_player
        self.box_players = box_players
        self.box_recent_matches = box_recent_matches
        self.player_id = player_id
        self.player_displayed_nickname = player_displayed_nickname
        self.player_nationality = player_nationality

        if picked_match != None:
            self.picked_match = picked_match
            self.picked_set = picked_set
        else:
            self.picked_match = None
            self.picked_set = 1

        options = []
        for i in range(len(box_recent_matches)):
            if i == 0: emoji = "1️⃣"
            elif i == 1: emoji = "2️⃣"
            elif i == 2: emoji = "3️⃣"
            elif i == 3: emoji = "4️⃣"
            elif i == 4: emoji = "5️⃣"
            options.append(discord.SelectOption(emoji=emoji, label=f"{box_recent_matches[i]['name']}", value=f"{i}", description=""))
        options.append(discord.SelectOption(emoji="↩️", label=self.language['player_info.py']['output']['select-pick_match']['options']['back']['label'], value="back", description=""))

        super().__init__(
            placeholder=self.language['player_info.py']['output']['select-pick_match']['placeholder'],
            min_values=1,
            max_values=1,
            options=options,
            row=0
        )

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id: return await interaction.response.send_message(self.language['player_info.py']['output']['string-only_author_can_use'], ephemeral=True)

        if self.values[0] != "back":
            self.picked_match = int(self.values[0]) + 1
            self.picked_set = 1
        else:
            self.picked_match = None
            self.picked_set = 1
            return await interaction.response.edit_message(content="", embed=self.origin_embed, view=PlayerInfoView(language=self.language, bot=self.bot, ctx=self.ctx, msg=self.msg, origin_embed=self.origin_embed, picked_match=self.picked_match, picked_set=self.picked_set, box_player=self.box_player, box_players=self.box_players, box_recent_matches=self.box_recent_matches, player_id=self.player_id, player_displayed_nickname=self.player_displayed_nickname, player_nationality=self.player_nationality))

        embed = make_game_info_embed(language=self.language, picked_match=self.picked_match, picked_set=self.picked_set, box_player=self.box_player, box_players=self.box_players, box_recent_matches=self.box_recent_matches, player_id=self.player_id, player_displayed_nickname=self.player_displayed_nickname, player_nationality=self.player_nationality)

        try:
            await interaction.response.edit_message(content="", embed=embed, view=PlayerInfoView(language=self.language, bot=self.bot, ctx=self.ctx, msg=self.msg, origin_embed=self.origin_embed, picked_match=self.picked_match, picked_set=self.picked_set, box_player=self.box_player, box_players=self.box_players, box_recent_matches=self.box_recent_matches, player_id=self.player_id, player_displayed_nickname=self.player_displayed_nickname, player_nationality=self.player_nationality))
        except discord.NotFound:
            pass


class PlayerInfoView(discord.ui.View):

    def __init__(self, language, bot, ctx, msg, origin_embed, picked_match, picked_set, box_player, box_players, box_recent_matches, player_id, player_displayed_nickname, player_nationality):
        super().__init__(timeout=60)
        self.language = language
        self.bot = bot
        self.ctx = ctx
        self.msg = msg
        self.origin_embed = origin_embed
        self.picked_match = picked_match
        self.picked_set = picked_set
        self.box_player = box_player
        self.box_players = box_players
        self.box_recent_matches = box_recent_matches
        self.player_id = player_id
        self.player_displayed_nickname = player_displayed_nickname
        self.player_nationality = player_nationality

        self.box_button = []

        self.add_item(MatchInfoSelect(language=self.language, bot=self.bot, ctx=self.ctx, msg=self.msg, origin_embed=self.origin_embed, picked_match=self.picked_match, picked_set=self.picked_set, box_player=self.box_player, box_players=self.box_players, box_recent_matches=self.box_recent_matches, player_id=self.player_id, player_displayed_nickname=self.player_displayed_nickname, player_nationality=self.player_nationality))
        self.add_button()

        if picked_match == None:
            self.add_item(discord.ui.Button(label=self.language['player_info.py']['output']['button-jump_esports'], url=f"{esports_op_gg_player}{self.player_id}", row=2))
            self.add_item(discord.ui.Button(label=self.language['player_info.py']['output']['button-jump_opgg'], url=f"{op_gg_player}{self.player_nationality.lower()}/{self.player_displayed_nickname}", disabled=True, row=2))
        else:
            self.add_item(discord.ui.Button(label=self.language['player_info.py']['output']['button-jump_esports'], url=f"{esports_op_gg_match}{self.box_recent_matches[self.picked_match - 1]['id']}", row=2))

    def add_button(self):
        if self.picked_match == None: return

        for i in range(1, 6):
            if i == 1: emoji = "1️⃣"
            elif i == 2: emoji = "2️⃣"
            elif i == 3: emoji = "3️⃣"
            elif i == 4: emoji = "4️⃣"
            elif i == 5: emoji = "5️⃣"

            try:
                get_game_info_by_id(matchId=self.box_recent_matches[self.picked_match - 1]['id'], matchSet=str(i))
 
                if self.picked_set == i:
                    self.box_button.append(discord.ui.Button(emoji=emoji, style=discord.ButtonStyle.blurple, disabled=True, custom_id=f"{i}", row=1))
                elif self.picked_set != i:
                    self.box_button.append(discord.ui.Button(emoji=emoji, style=discord.ButtonStyle.gray, custom_id=f"{i}", row=1))

            except:
                self.box_button.append(discord.ui.Button(emoji=emoji, style=discord.ButtonStyle.gray, custom_id=f"{i}", row=1, disabled=True))

        async def button_callback(interaction: discord.Interaction):
            if interaction.user.id != self.ctx.author.id: return await interaction.response.send_message(self.language['player_info.py']['output']['string-only_author_can_use'], ephemeral=True)

            self.picked_set = int(interaction.data['custom_id'])

            embed = make_game_info_embed(language=self.language, picked_match=self.picked_match, picked_set=self.picked_set, box_player=self.box_player, box_players=self.box_players, box_recent_matches=self.box_recent_matches, player_id=self.player_id, player_displayed_nickname=self.player_displayed_nickname, player_nationality=self.player_nationality)

            try:
                await interaction.response.edit_message(content="", embed=embed, view=PlayerInfoView(language=self.language, bot=self.bot, ctx=self.ctx, msg=self.msg, origin_embed=self.origin_embed, picked_match=self.picked_match, picked_set=self.picked_set, box_player=self.box_player, box_players=self.box_players, box_recent_matches=self.box_recent_matches, player_id=self.player_id, player_displayed_nickname=self.player_displayed_nickname, player_nationality=self.player_nationality))
            except discord.NotFound:
                pass

        for j in range(len(self.box_button)):
            self.box_button[j].callback = button_callback
            self.add_item(self.box_button[j])


    async def on_timeout(self):
        try:
            return await self.msg.edit_original_response(content="", view=DisabledButton(language=self.language, picked_match=self.picked_match, picked_set=self.picked_set, box_recent_matches=self.box_recent_matches, player_id=self.player_id, player_displayed_nickname=self.player_displayed_nickname, player_nationality=self.player_nationality))
        except discord.NotFound:
            pass
        except TypeError:
            pass


class DisabledButton(discord.ui.View):

    def __init__(self, language, picked_match, picked_set, box_recent_matches, player_id, player_displayed_nickname, player_nationality):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Select(placeholder=language['player_info.py']['output']['select-pick_match']['placeholder'], options=[discord.SelectOption(label="asdf", value="1", description="asdf")], disabled=True, row=0))
        if (picked_match == None) and (picked_set == None):
            self.add_item(discord.ui.Button(label=language['player_info.py']['output']['button-jump_esports'], url=f"{esports_op_gg_player}{player_id}", row=2))
            self.add_item(discord.ui.Button(label=language['player_info.py']['output']['button-jump_opgg'], url=f"{op_gg_player}{player_nationality.lower()}/{player_displayed_nickname}", disabled=True, row=2))
        elif picked_set != None:
            self.add_item(discord.ui.Button(emoji="1️⃣", disabled=True, row=1))
            self.add_item(discord.ui.Button(emoji="2️⃣", disabled=True, row=1))
            self.add_item(discord.ui.Button(emoji="3️⃣", disabled=True, row=1))
            self.add_item(discord.ui.Button(emoji="4️⃣", disabled=True, row=1))
            self.add_item(discord.ui.Button(emoji="5️⃣", disabled=True, row=1))
            self.add_item(discord.ui.Button(label=language['player_info.py']['output']['button-jump_esports'], url=f"{esports_op_gg_match}{box_recent_matches[picked_match - 1]['id']}", row=2))
        else:
            self.add_item(discord.ui.Button(label=language['player_info.py']['output']['button-jump_esports'], url=f"{esports_op_gg_match}{box_recent_matches[picked_match - 1]['id']}", row=2))


class PlayerInfoCMD(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name=lang_en['player_info.py']['command']['name'],
        name_localizations={
            "ko": lang_ko['player_info.py']['command']['name']
        },
        description=lang_en['player_info.py']['command']['description'],
        description_localizations={
            "ko": lang_ko['player_info.py']['command']['description']
        },
        options=[
            Option(
                name=lang_en['player_info.py']['command']['options']['player']['name'],
                name_localizations={
                    "ko": lang_ko['player_info.py']['command']['options']['player']['name']
                },
                description=lang_en['player_info.py']['command']['options']['player']['description'],
                description_localizations={
                    "ko": lang_ko['player_info.py']['command']['options']['player']['description']
                },
                required=True,
                autocomplete=search_player
            )
        ]
    )
    async def _playerCMD(self, ctx: discord.AutocompleteContext, picked_player: str):

        language = Substitution.substitution(ctx)
        try: picked_player = picked_player.split(" ")[1]
        except: picked_player = picked_player
        links = ""
        box_player = []
        box_players = []
        player_id = ""
        player_displayed_nickname = ""
        player_nationality = ""
        player_league_id = ""
        player_birth_day = ""
        banner_image_url = random.choice(config['banner_image_url'])

        embed = discord.Embed(title="", description=language['player_info.py']['output']['embed-loading']['description'], color=colorMap['red'])
        msg = await ctx.respond(embed=embed)

        try:
            try:
                box_player = get_player_info_by_nickname(playerNickname=picked_player)

            except:
                embed = discord.Embed(title=language['player_info.py']['output']['embed-no_player']['title'], description="", color=colorMap['red'])
                embed.set_footer(text=language['player_info.py']['output']['embed-no_player']['footer'], icon_url=self.bot.user.display_avatar.url)
                embed.set_image(url=banner_image_url)
                embed.add_field(name=language['player_info.py']['output']['embed-no_player']['field_1']['name'].format(picked_player=picked_player), value=language['player_info.py']['output']['embed-no_player']['field_1']['value'], inline=False)
                return await msg.edit_original_response(content="", embed=embed)

            try:
                print(f"[player_info.py] {box_player['code']}: {box_player['message']}")
                embed = discord.Embed(title=language['player_info.py']['output']['embed-no_data']['title'], description=language['player_info.py']['output']['embed-no_data']['description'].format(code=box_player['code'], message=box_player['message']), color=colorMap['red'])
                return await msg.edit_original_response(content="", embed=embed)

            except:
                if box_player:
                    for i in range(len(box_player)):
                        player_id = box_player[i]['id']
                        player_displayed_nickname = box_player[i]['nickName']
                        player_nationality = box_player[i]['team_nationality']

                        for z in range(16):
                            if player_nationality == leagues[z]['region']:
                                player_league_id = leagues[z]['tournamentId']
                                break

                        box_players = get_team_info_by_id(tournamentId=player_league_id, teamId=box_player[i]['team_id'])
                        box_recentMatches = get_player_recent_matches_by_id(playerId=player_id)

                        try:
                            print(f"[player_info.py] {box_player['code']}: {box_player['message']}")
                            embed = discord.Embed(title=language['player_info.py']['output']['embed-no_data']['title'], description=language['player_info.py']['output']['embed-no_data']['description'].format(code=box_player['code'], message=box_player['message']), color=colorMap['red'])
                            return await msg.edit_original_response(content="", embed=embed)

                        except:
                            if box_players:
                                for j in range(len(box_players)):
                                    if box_player[i]['id'] == box_players[j]['id']:
                                        if box_player[i]['birthday'] == None: player_birth_day = language['player_info.py']['output']['string-no_player_birthday']
                                        else: player_birth_day = box_player[i]['birthday']

                                        links = f"[{emoji_esports}]({esports_op_gg_player}{box_player[i]['id']}) "
                                        if box_player[i]['stream']: links = f"{links}[{emoji_stream}]({box_player[i]['stream']}) "
                                        if box_player[i]['youtube']: links = f"{links}[{emoji_youtube}]({box_player[i]['youtube']}) "
                                        if box_player[i]['instagram']: links = f"{links}[{emoji_instagram}]({box_player[i]['instagram']}) "
                                        if box_player[i]['facebook']: links = f"{links}[{emoji_facebook}]({box_player[i]['facebook']}) "
                                        if box_player[i]['twitter']: links = f"{links}[{emoji_twitter}]({box_player[i]['twitter']}) "
                                        if box_player[i]['discord']: links = f"{links}[{emoji_discord}]({box_player[i]['discord']}) "
                                        links = links[:-1]

                                        embed = discord.Embed(title=language['player_info.py']['output']['embed-player']['title'], description="", color=colorMap['red'])
                                        embed.set_footer(text=language['player_info.py']['output']['embed-player']['footer'], icon_url=self.bot.user.display_avatar.url)
                                        # embed.set_image(url=banner_image_url)
                                        embed.set_thumbnail(url=box_player[i]['imageUrl'])
                                        if ctx.locale != "ko":
                                            embed.add_field(name=language['player_info.py']['output']['embed-player']['field_1']['name'], value=language['player_info.py']['output']['embed-player']['field_1']['value'].format(team_acronym=box_player[i]['team_acronym'], esports_team_url=esports_op_gg_team, team_id=box_player[i]['team_id'], nickname=box_player[i]['nickName'], esports_player_url=esports_op_gg_player, player_id=box_player[i]['id'], firstname=box_player[i]['firstName'], lastname=box_player[i]['lastName'], position=box_players[j]['position'].replace("탑", "Top").replace("정글", "Jungle").replace("미드", "Mid").replace("원딜", "ADC").replace("서포터", "Support")), inline=True)
                                        else:
                                            embed.add_field(name=language['player_info.py']['output']['embed-player']['field_1']['name'], value=language['player_info.py']['output']['embed-player']['field_1']['value'].format(team_acronym=box_player[i]['team_acronym'], esports_team_url=esports_op_gg_team, team_id=box_player[i]['team_id'], nickname=box_player[i]['nickName'], esports_player_url=esports_op_gg_player, player_id=box_player[i]['id'], firstname=box_player[i]['firstName'], lastname=box_player[i]['lastName'], position=box_players[j]['position']), inline=True)
                                        embed.add_field(name=language['player_info.py']['output']['embed-player']['field_2']['name'], value=links, inline=True)
                                        embed.add_field(name="\u200b", value="", inline=False)
                                        embed.add_field(name=language['player_info.py']['output']['embed-player']['field_3']['name'], value=language['player_info.py']['output']['embed-player']['field_3']['value'].format(win_ratio=box_players[j]['stat_winRate'], wins=box_players[j]['stat_wins'], loses=box_players[j]['stat_loses']), inline=False)
                                        embed.add_field(name=language['player_info.py']['output']['embed-player']['field_4']['name'], value=language['player_info.py']['output']['embed-player']['field_4']['value'].format(kda=box_players[j]['stat_kda'], kills=box_players[j]['stat_kills'], deaths=box_players[j]['stat_deaths'], assists=box_players[j]['stat_assists']), inline=False)
                                        embed.add_field(name=language['player_info.py']['output']['embed-player']['field_5']['name'], value=language['player_info.py']['output']['embed-player']['field_5']['value'].format(dpm=box_players[j]['stat_dpm']), inline=True)
                                        embed.add_field(name=language['player_info.py']['output']['embed-player']['field_6']['name'], value=language['player_info.py']['output']['embed-player']['field_6']['value'].format(dtpm=box_players[j]['stat_dtpm']), inline=True)
                                        embed.add_field(name=language['player_info.py']['output']['embed-player']['field_7']['name'], value=language['player_info.py']['output']['embed-player']['field_7']['value'].format(gpm=box_players[j]['stat_gpm']), inline=True)
                                        embed.add_field(name=language['player_info.py']['output']['embed-player']['field_8']['name'], value=language['player_info.py']['output']['embed-player']['field_8']['value'].format(cspm=box_players[j]['stat_cspm']), inline=True)
                                        embed.add_field(name=language['player_info.py']['output']['embed-player']['field_9']['name'], value=language['player_info.py']['output']['embed-player']['field_9']['value'].format(first_blood=box_players[j]['stat_firstBlood']), inline=True)
                                        embed.add_field(name=language['player_info.py']['output']['embed-player']['field_10']['name'], value=language['player_info.py']['output']['embed-player']['field_10']['value'].format(first_tower=box_players[j]['stat_firstTower']), inline=True)

                            if box_recentMatches:
                                embed.add_field(name="\u200b", value="", inline=False)

                                msg_recentMatches = ""
                                for k in range(len(box_recentMatches)):
                                    msg_recentMatches += language['player_info.py']['output']['string-recent_matches'].format(emoji_hyperlink=emoji_hyperlink, esports_match=esports_op_gg_match, match_id=box_recentMatches[k]['id'], match_name=box_recentMatches[k]['name'], match_winner=box_recentMatches[k]['winner_name'])

                                embed.add_field(name=language['player_info.py']['output']['embed-player']['field_11']['name'], value=msg_recentMatches, inline=False)

                    await msg.edit_original_response(content="", embed=embed, view=PlayerInfoView(language=language, bot=self.bot, ctx=ctx, msg=msg, origin_embed=embed, picked_match=None, picked_set=1, box_player=box_player, box_players=box_players, box_recent_matches=box_recentMatches, player_id=player_id, player_displayed_nickname=player_displayed_nickname, player_nationality=player_nationality))

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
    bot.add_cog(PlayerInfoCMD(bot))
    print("player_info.py 로드 됨")
