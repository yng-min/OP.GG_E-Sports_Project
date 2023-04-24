# -*- coding: utf-8 -*-

# 패키지 라이브러리 설정
import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup, option
import random
import json
import datetime
import pytz
import traceback

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

esports_op_gg_player = "https://esports.op.gg/players/"
esports_op_gg_team = "https://esports.op.gg/teams/"
esports_op_gg_match = "https://esports.op.gg/matches/"
esports_op_gg_champion = "https://esports.op.gg/champions/"
op_gg_player = "https://www.op.gg/summoners/"
time_difference = config['time_difference']
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

    player_displayed_nickname = ""
    try: keyword = ctx.options['이름'].split(" ")[1]
    except: keyword = ctx.options['이름']

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


def make_game_info_embed(picked_match, picked_set, box_player, box_players, box_recent_matches, player_id, player_displayed_nickname, player_nationality):

    picked_match = box_recent_matches[picked_match - 1]
    match_date = datetime.datetime.strptime(picked_match['beginAt'].split("T")[0], "%Y-%m-%d").strftime("X%Y년 X%m월 X%d일").replace("X0", "").replace("X", "")

    game_info = get_game_info_by_id(match_id=picked_match['id'], match_set=str(picked_set))

    # msg_ban_1 = f"🚫) {game_info['teams'][0]['bans'][0]} {game_info['teams'][0]['bans'][1]} {game_info['teams'][0]['bans'][2]} {game_info['teams'][0]['bans'][3]} {game_info['teams'][0]['bans'][4]}"
    msg_ban_1 = f"🚫) [⬜]({esports_op_gg_champion}{game_info['teams'][0]['bans'][0]}) [⬜]({esports_op_gg_champion}{game_info['teams'][0]['bans'][1]}) [⬜]({esports_op_gg_champion}{game_info['teams'][0]['bans'][2]}) [⬜]({esports_op_gg_champion}{game_info['teams'][0]['bans'][3]}) [⬜]({esports_op_gg_champion}{game_info['teams'][0]['bans'][4]})" # 챔피언 이모티콘 적용될 때까지만 임시
    # msg_ban_2 = f"🚫) {game_info['teams'][1]['bans'][0]} {game_info['teams'][1]['bans'][1]} {game_info['teams'][1]['bans'][2]} {game_info['teams'][1]['bans'][3]} {game_info['teams'][1]['bans'][4]}"
    msg_ban_2 = f"🚫) [⬜]({esports_op_gg_champion}{game_info['teams'][1]['bans'][0]}) [⬜]({esports_op_gg_champion}{game_info['teams'][1]['bans'][1]}) [⬜]({esports_op_gg_champion}{game_info['teams'][1]['bans'][2]}) [⬜]({esports_op_gg_champion}{game_info['teams'][1]['bans'][3]}) [⬜]({esports_op_gg_champion}{game_info['teams'][1]['bans'][4]})"  # 챔피언 이모티콘 적용될 때까지만 임시

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
                msg_kda_1 += f"\n`{game_info['players'][k]['kills']}/{game_info['players'][k]['deaths']}/{game_info['players'][k]['assists']}` _{game_info['players'][k]['kda']}_ 평점"
            elif game_info['players'][k]['kda'] == max(most_kda):
                msg_kda_1 += f"\n`{game_info['players'][k]['kills']}/{game_info['players'][k]['deaths']}/{game_info['players'][k]['assists']}` __**{game_info['players'][k]['kda']}**__ 평점"
            elif game_info['players'][k]['kda'] >= 3:
                msg_kda_1 += f"\n`{game_info['players'][k]['kills']}/{game_info['players'][k]['deaths']}/{game_info['players'][k]['assists']}` **{game_info['players'][k]['kda']}** 평점"
            else:
                msg_kda_1 += f"\n`{game_info['players'][k]['kills']}/{game_info['players'][k]['deaths']}/{game_info['players'][k]['assists']}` {game_info['players'][k]['kda']} 평점"

            msg_damage_1 += f"\n`{game_info['players'][k]['totalDamageDealtToChampions']:,}`"

        else:
            if game_info['players'][k]['id'] == player_id:
                # msg_player_2 += f"\n{game_info['players'][k]['championId']} **{game_info['players'][k]['nickName']}**"
                msg_player_2 += f"\n⬜ **[{game_info['players'][k]['team_acronym']}]({esports_op_gg_team}{game_info['players'][k]['team_id']}) [{game_info['players'][k]['nickName']}]({esports_op_gg_player}{game_info['players'][k]['id']})**" # 챔피언 이모티콘 적용될 때까지만 임시
            else:
                # msg_player_2 += f"\n{game_info['players'][k]['championId']} {game_info['players'][k]['nickName']}"
                msg_player_2 += f"\n⬜ [{game_info['players'][k]['team_acronym']}]({esports_op_gg_team}{game_info['players'][k]['team_id']}) [{game_info['players'][k]['nickName']}]({esports_op_gg_player}{game_info['players'][k]['id']})" # 챔피언 이모티콘 적용될 때까지만 임시

            if game_info['players'][k]['kda'] == "Perfect":
                msg_kda_2 += f"\n`{game_info['players'][k]['kills']}/{game_info['players'][k]['deaths']}/{game_info['players'][k]['assists']}` _{game_info['players'][k]['kda']}_ 평점"
            elif game_info['players'][k]['kda'] == max(most_kda):
                msg_kda_2 += f"\n`{game_info['players'][k]['kills']}/{game_info['players'][k]['deaths']}/{game_info['players'][k]['assists']}` __**{game_info['players'][k]['kda']}**__ 평점"
            elif game_info['players'][k]['kda'] >= 3:
                msg_kda_2 += f"\n`{game_info['players'][k]['kills']}/{game_info['players'][k]['deaths']}/{game_info['players'][k]['assists']}` **{game_info['players'][k]['kda']}** 평점"
            else:
                msg_kda_2 += f"\n`{game_info['players'][k]['kills']}/{game_info['players'][k]['deaths']}/{game_info['players'][k]['assists']}` {game_info['players'][k]['kda']} 평점"

            msg_damage_2 += f"\n`{game_info['players'][k]['totalDamageDealtToChampions']:,}`"

    embed = discord.Embed(title="> 📊 경기 정보", description="", color=colorMap['red'])
    embed.add_field(name=f"{picked_match['name']} ({picked_set}세트)", value=f"└ (**{match_date}**에 진행된 경기)", inline=False)

    if game_info['winner_name'] == game_info['teams'][0]['name']:
        embed.add_field(name=f"> {emoji_blueside} {game_info['teams'][0]['name']} (승리)", value=f"{msg_ban_1}ㅤ{msg_object_1}", inline=False)
        embed.add_field(name="챔피언", value=msg_player_1, inline=True)
        embed.add_field(name="KDA 정보", value=msg_kda_1, inline=True)
        embed.add_field(name="가한 데미지", value=msg_damage_1, inline=True)
        embed.add_field(name=f"> {emoji_redside} {game_info['teams'][1]['name']} (패배)", value=f"{msg_ban_2}ㅤ{msg_object_2}", inline=False)
        embed.add_field(name="챔피언", value=msg_player_2, inline=True)
        embed.add_field(name="KDA 정보", value=msg_kda_2, inline=True)
        embed.add_field(name="가한 데미지", value=msg_damage_2, inline=True)
    else:
        embed.add_field(name=f"> {emoji_blueside} {game_info['teams'][0]['name']} (패배)", value=f"{msg_ban_1}ㅤ{msg_object_1}", inline=False)
        embed.add_field(name="챔피언", value=msg_player_1, inline=True)
        embed.add_field(name="KDA 정보", value=msg_kda_1, inline=True)
        embed.add_field(name="가한 데미지", value=msg_damage_1, inline=True)
        embed.add_field(name=f"> {emoji_redside} {game_info['teams'][1]['name']} (승리)", value=f"{msg_ban_2}ㅤ{msg_object_2}", inline=False)
        embed.add_field(name="챔피언", value=msg_player_2, inline=True)
        embed.add_field(name="KDA 정보", value=msg_kda_2, inline=True)
        embed.add_field(name="가한 데미지", value=msg_damage_2, inline=True)

    return embed


class MatchInfoSelect(discord.ui.Select):

    def __init__(self, bot, ctx, msg, origin_embed, picked_match, picked_set, box_player, box_players, box_recent_matches, player_id, player_displayed_nickname, player_nationality):
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
        options.append(discord.SelectOption(emoji="↩️", label="선수 프로필로 돌아가기", value="back", description=""))

        super().__init__(
            placeholder="경기 선택하기",
            min_values=1,
            max_values=1,
            options=options,
            row=0
        )

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id: return await interaction.response.send_message("> 자신의 메시지에서만 이용할 수 있어요. 😢", ephemeral=True)

        if self.values[0] != "back":
            self.picked_match = int(self.values[0]) + 1
            self.picked_set = 1
        else:
            self.picked_match = None
            self.picked_set = 1
            return await interaction.response.edit_message(content="", embed=self.origin_embed, view=PlayerInfoView(bot=self.bot, ctx=self.ctx, msg=self.msg, origin_embed=self.origin_embed, picked_match=self.picked_match, picked_set=self.picked_set, box_player=self.box_player, box_players=self.box_players, box_recent_matches=self.box_recent_matches, player_id=self.player_id, player_displayed_nickname=self.player_displayed_nickname, player_nationality=self.player_nationality))

        embed = make_game_info_embed(picked_match=self.picked_match, picked_set=self.picked_set, box_player=self.box_player, box_players=self.box_players, box_recent_matches=self.box_recent_matches, player_id=self.player_id, player_displayed_nickname=self.player_displayed_nickname, player_nationality=self.player_nationality)

        try:
            await interaction.response.edit_message(content="", embed=embed, view=PlayerInfoView(bot=self.bot, ctx=self.ctx, msg=self.msg, origin_embed=self.origin_embed, picked_match=self.picked_match, picked_set=self.picked_set, box_player=self.box_player, box_players=self.box_players, box_recent_matches=self.box_recent_matches, player_id=self.player_id, player_displayed_nickname=self.player_displayed_nickname, player_nationality=self.player_nationality))
        except discord.NotFound:
            pass


class PlayerInfoView(discord.ui.View):

    def __init__(self, bot, ctx, msg, origin_embed, picked_match, picked_set, box_player, box_players, box_recent_matches, player_id, player_displayed_nickname, player_nationality):
        super().__init__(timeout=60)
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

        self.add_item(MatchInfoSelect(bot=self.bot, ctx=self.ctx, msg=self.msg, origin_embed=self.origin_embed, picked_match=self.picked_match, picked_set=self.picked_set, box_player=self.box_player, box_players=self.box_players, box_recent_matches=self.box_recent_matches, player_id=self.player_id, player_displayed_nickname=self.player_displayed_nickname, player_nationality=self.player_nationality))
        self.add_button()

        if picked_match == None:
            self.add_item(discord.ui.Button(label="OP.GG E-Sports에서 보기", url=f"{esports_op_gg_player}{self.player_id}", row=2))
            self.add_item(discord.ui.Button(label="OP.GG에서 보기", url=f"{op_gg_player}{self.player_nationality.lower()}/{self.player_displayed_nickname}", disabled=True, row=2))
        else:
            self.add_item(discord.ui.Button(label="OP.GG E-Sports에서 보기", url=f"{esports_op_gg_match}{self.box_recent_matches[self.picked_match - 1]['id']}", row=2))

    def add_button(self):
        if self.picked_match == None: return

        for i in range(1, 6):
            if i == 1: emoji = "1️⃣"
            elif i == 2: emoji = "2️⃣"
            elif i == 3: emoji = "3️⃣"
            elif i == 4: emoji = "4️⃣"
            elif i == 5: emoji = "5️⃣"

            try:
                get_game_info_by_id(match_id=self.box_recent_matches[self.picked_match - 1]['id'], match_set=str(i))
 
                if self.picked_set == i:
                    self.box_button.append(discord.ui.Button(emoji=emoji, style=discord.ButtonStyle.blurple, custom_id=f"{i}", row=1))
                elif self.picked_set != i:
                    self.box_button.append(discord.ui.Button(emoji=emoji, style=discord.ButtonStyle.gray, custom_id=f"{i}", row=1))

            except:
                self.box_button.append(discord.ui.Button(emoji=emoji, style=discord.ButtonStyle.gray, custom_id=f"{i}", row=1, disabled=True))

        async def button_callback(interaction: discord.Interaction):
            if interaction.user.id != self.ctx.author.id: return await interaction.response.send_message("> 자신의 메시지에서만 이용할 수 있어요. 😢", ephemeral=True)

            self.picked_set = int(interaction.data['custom_id'])

            embed = make_game_info_embed(picked_match=self.picked_match, picked_set=self.picked_set, box_player=self.box_player, box_players=self.box_players, box_recent_matches=self.box_recent_matches, player_id=self.player_id, player_displayed_nickname=self.player_displayed_nickname, player_nationality=self.player_nationality)

            try:
                await interaction.response.edit_message(content="", embed=embed, view=PlayerInfoView(bot=self.bot, ctx=self.ctx, msg=self.msg, origin_embed=self.origin_embed, picked_match=self.picked_match, picked_set=self.picked_set, box_player=self.box_player, box_players=self.box_players, box_recent_matches=self.box_recent_matches, player_id=self.player_id, player_displayed_nickname=self.player_displayed_nickname, player_nationality=self.player_nationality))
            except discord.NotFound:
                pass

        for j in range(len(self.box_button)):
            self.box_button[j].callback = button_callback
            self.add_item(self.box_button[j])


    async def on_timeout(self):
        try:
            return await self.msg.edit_original_response(content="", view=DisabledButton(picked_match=self.picked_match, picked_set=self.picked_set, box_recent_matches=self.box_recent_matches, player_id=self.player_id, player_displayed_nickname=self.player_displayed_nickname, player_nationality=self.player_nationality))
        except discord.NotFound:
            pass
        except TypeError:
            pass


class DisabledButton(discord.ui.View):

    def __init__(self, picked_match, picked_set, box_recent_matches, player_id, player_displayed_nickname, player_nationality):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Select(placeholder="경기 선택하기", options=[discord.SelectOption(label="asdf", value="1", description="asdf")], disabled=True, row=0))
        if (picked_match == None) and (picked_set == None):
            self.add_item(discord.ui.Button(label="OP.GG E-Sports에서 보기", url=f"{esports_op_gg_player}{player_id}", row=2))
            self.add_item(discord.ui.Button(label="OP.GG에서 보기", url=f"{op_gg_player}{player_nationality.lower()}/{player_displayed_nickname}", disabled=True, row=2))
        elif picked_set != None:
            self.add_item(discord.ui.Button(emoji="1️⃣", disabled=True, row=1))
            self.add_item(discord.ui.Button(emoji="2️⃣", disabled=True, row=1))
            self.add_item(discord.ui.Button(emoji="3️⃣", disabled=True, row=1))
            self.add_item(discord.ui.Button(emoji="4️⃣", disabled=True, row=1))
            self.add_item(discord.ui.Button(emoji="5️⃣", disabled=True, row=1))
            self.add_item(discord.ui.Button(label="OP.GG E-Sports에서 보기", url=f"{esports_op_gg_match}{box_recent_matches[picked_match - 1]['id']}", row=2))
        else:
            self.add_item(discord.ui.Button(label="OP.GG E-Sports에서 보기", url=f"{esports_op_gg_match}{box_recent_matches[picked_match - 1]['id']}", row=2))


class PlayerInfoCMD(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    _search = SlashCommandGroup(name="선수", description="검색 명령어", guild_only=False)

    @_search.command(
        name="검색",
        description="리그 오브 레전드 e스포츠의 선수 프로필을 검색할 수 있어요.",
    )
    @option("이름", description="검색할 e스포츠 선수를 입력해주세요.", required=True, autocomplete=search_player)
    async def _playerCMD(self, ctx: discord.AutocompleteContext, 이름: str):

        try: picked_player = 이름.split(" ")[1]
        except: picked_player = 이름
        links = ""
        box_player = []
        box_players = []
        player_id = ""
        player_displayed_nickname = ""
        player_nationality = ""
        player_league_id = ""
        player_birth_day = ""
        banner_image_url = random.choice(config['banner_image_url'])

        embed = discord.Embed(title="", description="⌛ 정보를 불러오는 중...", color=colorMap['red'])
        msg = await ctx.respond(embed=embed)

        try:
            try:
                box_player = get_player_info_by_nickname(playerNickname=picked_player)

            except:
                embed = discord.Embed(title="> 🔍 선수 프로필", description="", color=colorMap['red'])
                embed.set_footer(text="TIP: 선수는 영문 닉네임으로만 검색할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
                embed.set_image(url=banner_image_url)
                embed.add_field(name=f"검색어: '{picked_player}'", value="> 선수 프로필을 불러올 수 없습니다.\n> 검색어가 정확한지 다시 확인해주세요.", inline=False)
                return await msg.edit_original_response(content="", embed=embed)

            try:
                print(f"[player_info.py] {box_player['code']}: {box_player['message']}")
                embed = discord.Embed(title="> ⚠️ 오류", description=f"Code: `{box_player['code']}`\nMessage: {box_player['message']}", color=colorMap['red'])
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
                            embed = discord.Embed(title="> ⚠️ 오류", description=f"Code: `{box_player['code']}`\nMessage: {box_player['message']}", color=colorMap['red'])
                            return await msg.edit_original_response(content="", embed=embed)

                        except:
                            if box_players:
                                for j in range(len(box_players)):
                                    if box_player[i]['id'] == box_players[j]['id']:
                                        if box_player[i]['birthday'] == None: player_birth_day = "정보 없음"
                                        else: player_birth_day = box_player[i]['birthday']

                                        links = f"[{emoji_esports}]({esports_op_gg_player}{box_player[i]['id']}) "
                                        if box_player[i]['stream']: links = f"{links}[{emoji_stream}]({box_player[i]['stream']}) "
                                        if box_player[i]['youtube']: links = f"{links}[{emoji_youtube}]({box_player[i]['youtube']}) "
                                        if box_player[i]['instagram']: links = f"{links}[{emoji_instagram}]({box_player[i]['instagram']}) "
                                        if box_player[i]['facebook']: links = f"{links}[{emoji_facebook}]({box_player[i]['facebook']}) "
                                        if box_player[i]['twitter']: links = f"{links}[{emoji_twitter}]({box_player[i]['twitter']}) "
                                        if box_player[i]['discord']: links = f"{links}[{emoji_discord}]({box_player[i]['discord']}) "
                                        links = links[:-1]

                                        embed = discord.Embed(title=f"> 🔍 선수 프로필", description="", color=colorMap['red'])
                                        embed.set_footer(text="TIP: SNS 아이콘을 클릭하면 해당 선수의 SNS로 바로 이동할 수 있어요.", icon_url=self.bot.user.display_avatar.url)
                                        # embed.set_image(url=banner_image_url)
                                        embed.set_thumbnail(url=box_player[i]['imageUrl'])
                                        embed.add_field(name="인적 정보", value=f"닉네임: [{box_player[i]['team_acronym']}]({esports_op_gg_team}{box_player[i]['team_id']}) [{box_player[i]['nickName']}]({esports_op_gg_player}{box_player[i]['id']})\n본명: {box_player[i]['firstName']} {box_player[i]['lastName']}\n포지션: {box_players[j]['position']}", inline=True)
                                        embed.add_field(name="SNS 플랫폼", value=links, inline=True)
                                        embed.add_field(name="\u200b", value="", inline=False)
                                        embed.add_field(name="승률", value=f"__{box_players[j]['stat_winRate']}__% (__{box_players[j]['stat_wins']:,}__승 __{box_players[j]['stat_loses']:,}__패)", inline=False)
                                        embed.add_field(name="KDA 정보", value=f"{box_players[j]['stat_kda']} 평점 `({box_players[j]['stat_kills']}/{box_players[j]['stat_deaths']}/{box_players[j]['stat_assists']})`", inline=False)
                                        embed.add_field(name="가한 피해량", value=f"분당 {box_players[j]['stat_dpm']:,}데미지", inline=True)
                                        embed.add_field(name="입은 피해량", value=f"분당 {box_players[j]['stat_dtpm']:,}데미지", inline=True)
                                        embed.add_field(name="골드 획득", value=f"분당 {box_players[j]['stat_gpm']:,}골드", inline=True)
                                        embed.add_field(name="CS", value=f"분당 {box_players[j]['stat_cspm']:,}개", inline=True)
                                        embed.add_field(name="첫 킬률", value=f"{box_players[j]['stat_firstBlood']}%", inline=True)
                                        embed.add_field(name="첫 타워 파괴율", value=f"{box_players[j]['stat_firstTower']}%", inline=True)

                            if box_recentMatches:
                                embed.add_field(name="\u200b", value="", inline=False)

                                msg_recentMatches = ""
                                for k in range(len(box_recentMatches)):
                                    msg_recentMatches += f"[{emoji_hyperlink}]({esports_op_gg_match}{box_recentMatches[k]['id']}) **{box_recentMatches[k]['name']}** (||__{box_recentMatches[k]['winner_name']}__|| 승)\n"

                                embed.add_field(name="최근 5경기", value=msg_recentMatches, inline=False)

                    # await msg.edit_original_response(content="", embed=embed, view=DisabledButton(player_id=player_id, player_displayed_nickname=player_displayed_nickname, player_nationality=player_nationality))
                    await msg.edit_original_response(content="", embed=embed, view=PlayerInfoView(bot=self.bot, ctx=ctx, msg=msg, origin_embed=embed, picked_match=None, picked_set=1, box_player=box_player, box_players=box_players, box_recent_matches=box_recentMatches, player_id=player_id, player_displayed_nickname=player_displayed_nickname, player_nationality=player_nationality))

        except Exception as error:
            print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
            print(traceback.format_exc())



def setup(bot):
    bot.add_cog(PlayerInfoCMD(bot))
    print("player_info.py 로드 됨")
