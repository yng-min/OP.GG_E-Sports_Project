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

from Extensions.Process.player import get_player_info_by_nickname, get_team_info_by_id
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
op_gg_player = "https://www.op.gg/summoners/"
time_difference = config['time_difference']
colorMap = config['colorMap']
emoji_discord = emoji['Discord']
emoji_esports = emoji['Esports']
emoji_facebook = emoji['Facebook']
emoji_instagram = emoji['Instagram']
emoji_stream = emoji['LiveStream']
emoji_twitter = emoji['Twitter']
emoji_youtube = emoji['YouTube']


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


class DisabledButton(discord.ui.View):

    def __init__(self, player_id: str, player_displayed_nickname: str, player_nationalty: str):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Button(label="OP.GG Esports에서 보기", url=f"{esports_op_gg_player}{player_id}", row=0))
        self.add_item(discord.ui.Button(label="OP.GG에서 보기", url=f"{op_gg_player}{player_nationalty.lower()}/{player_displayed_nickname}", disabled=True, row=0))


class PlayerInfoCMD(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    _search = SlashCommandGroup(name="검색", description="검색 명령어", guild_only=False)

    @_search.command(
        name="선수",
        description="리그 오브 레전드 e스포츠의 선수 정보를 검색할 수 있어요.",
    )
    @option("이름", description="검색할 e스포츠 선수를 입력해주세요.", required=True, autocomplete=search_player)
    async def _playerCMD(self, ctx: discord.AutocompleteContext, 이름: str):

        picked_player = 이름.split(" ")[1]
        tournament_id = ""
        team_id = ""
        links = ""
        box_player = []
        box_players = []
        player_id = ""
        player_displayed_nickname = ""
        player_nationalty = ""
        player_league_id = ""
        player_birth_day = ""
        banner_image_url = random.choice(config['banner_image_url'])

        embed = discord.Embed(title="", description="⌛ 정보를 불러오는 중...", color=colorMap['red'])
        msg = await ctx.respond(embed=embed)

        try:
            box_player = get_player_info_by_nickname(playerNickname=picked_player)

            try:
                print(f"[player_info.py] {box_player['code']}: {box_player['message']}")
                embed = discord.Embed(title="> ⚠️ 오류", description=f"Code: `{box_player['code']}`\nMessage: {box_player['message']}", color=colorMap['red'])
                return await msg.edit_original_response(content="", embed=embed)

            except:
                if box_player:
                    for i in range(len(box_player)):
                        player_id = box_player[i]['id']
                        player_displayed_nickname = box_player[i]['nickName']
                        player_nationalty = box_player[i]['nationality']

                        for k in range(16):
                            if box_player[i]['nationality'] == leagues[k]['region']:
                                player_league_id = leagues[k]['tournamentId']
                                break

                        box_players = get_team_info_by_id(tournamentId=player_league_id, teamId=box_player[i]['team_id'])

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

                                        embed = discord.Embed(title=f"> 🔍 선수 정보", description="", color=colorMap['red'])
                                        embed.set_footer(text="TIP: 아래 버튼을 눌러 자세한 정보를 살펴볼 수 있어요.", icon_url=self.bot.user.display_avatar.url)
                                        # embed.set_image(url=banner_image_url)
                                        embed.set_thumbnail(url=box_player[i]['imageUrl'])
                                        embed.add_field(name="인적 정보", value=f"닉네임: [{box_player[i]['team_acronym']}]({esports_op_gg_team}{box_player[i]['team_id']}) [{box_player[i]['nickName']}]({esports_op_gg_player}{box_player[i]['id']})\n본명: {box_player[i]['firstName']} {box_player[i]['lastName']}\n생일: {player_birth_day}", inline=True)
                                        embed.add_field(name="SNS 플랫폼", value=links, inline=True)
                                        embed.add_field(name="승률", value=f"__{box_players[j]['stat_winRate']}__% (__{box_players[j]['stat_wins']:,}__승 __{box_players[j]['stat_loses']:,}__패)", inline=False)
                                        embed.add_field(name="KDA 정보", value=f"{box_players[j]['stat_kda']} 평점 `({box_players[j]['stat_kills']} / {box_players[j]['stat_deaths']} / {box_players[j]['stat_assists']})`", inline=False)
                                        embed.add_field(name="가한 피해량(분당)", value=f"{box_players[j]['stat_dpm']:,}데미지", inline=True)
                                        embed.add_field(name="입은 피해량(분당)", value=f"{box_players[j]['stat_dtpm']:,}데미지", inline=True)
                                        embed.add_field(name="골드 획득(분당)", value=f"{box_players[j]['stat_gpm']:,}골드", inline=True)
                                        embed.add_field(name="CS(분당)", value=f"{box_players[j]['stat_cspm']:,}개", inline=True)
                                        embed.add_field(name="첫 킬률", value=f"{box_players[j]['stat_firstBlood']}%", inline=True)
                                        embed.add_field(name="첫 타워 파괴율", value=f"{box_players[j]['stat_firstTower']}%", inline=True)

                    await msg.edit_original_response(content="", embed=embed, view=DisabledButton(player_id=player_id, player_displayed_nickname=player_displayed_nickname, player_nationalty=player_nationalty))

        except Exception as error:
            print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
            print(traceback.format_exc())



def setup(bot):
    bot.add_cog(PlayerInfoCMD(bot))
    print("player_info.py 로드 됨")
