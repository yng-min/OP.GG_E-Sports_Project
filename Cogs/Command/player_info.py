print("player_info.py 로드 됨")

# # -*- coding: utf-8 -*-

# # 패키지 라이브러리 설정
# import discord
# from discord.ext import commands
# from discord.commands import SlashCommandGroup, option
# import random
# import json
# import datetime
# import pytz
# import traceback

# from Extensions.Process.league import get_player_info
# from Extensions.Process.search import get_search_player

# # config.json 파일 불러오기
# try:
#     with open(r"./config.json", "rt", encoding="UTF8") as configJson:
#         config = json.load(configJson)
# except: print("config.json이 로드되지 않음")

# # league.json 파일 불러오기
# try:
#     with open(r"./league.json", "rt", encoding="UTF8") as leagueJson:
#         leagues = json.load(leagueJson)['leagues']
# except: print("league.json이 로드되지 않음")

# # emoji.json 파일 불러오기
# try:
#     with open(r"./emoji.json", "rt", encoding="UTF8") as emojiJson:
#         emoji = json.load(emojiJson)
# except: print("emoji.json 파일이 로드되지 않음")

# esports_op_gg_player = "https://esports.op.gg/players/"
# esports_op_gg_team = "https://esports.op.gg/teams/"
# time_difference = config['time_difference']
# colorMap = config['colorMap']
# emoji_youtube = emoji['YouTube']
# emoji_instagram = emoji['Instagram']
# emoji_facebook = emoji['Facebook']
# emoji_discord = emoji['Discord']
# emoji_twitter = emoji['Twitter']
# emoji_esports = emoji['Esports']
# emoji_website = emoji['Website']


# async def search_player(ctx: discord.AutocompleteContext):

#     keyword = ctx.options['이름']
#     box_search_data = get_search_player(keyword=keyword)
#     player_name = box_search_data['data'][0]['player_name']

#     try:
#         # print(f"[player_info.py] {box_search_data['code']}: {box_search_data['message']}")
#         ...

#     except:
#         return [ player_name ]


# class PlayerInfoCMD(commands.Cog):

#     def __init__(self, bot):
#         self.bot = bot

#     _search = SlashCommandGroup(name="검색", description="검색 명령어", guild_only=False)

#     @_search.command(
#         name="선수",
#         description="리그 오브 레전드 e스포츠의 선수 정보를 검색할 수 있어요.",
#     )
#     @option("이름", description="e스포츠 선수를 선택해주세요.", required=True, autocomplete=discord.utils.basic_autocomplete(search_player))
#     async def _playerCMD(self, ctx: discord.AutocompleteContext, 이름: str):

#         picked_player = 이름
#         links = ""
#         search_id = ""
#         box_player = []
#         banner_image_url = random.choice(config['banner_image_url'])

#         embed = discord.Embed(title="", description="⌛ 정보를 불러오는 중...", color=colorMap['red'])
#         msg = await ctx.respond(embed=embed)

#         try:
#             search_player_id = get_search_player(keyword=picked_player)

#             try:
#                 print(f"[player_info.py] {search_player_id['code']}: {search_player_id['message']}")
#                 embed = discord.Embed(title="> ⚠️ 오류", description=f"Code: `{search_player_id['code']}`\nMessage: {search_player_id['message']}", color=colorMap['red'])
#                 return await msg.edit_original_response(content="", embed=embed)

#             except:
#                 if search_player_id:
#                     search_id = search_player_id['data']['player_id']
#                     box_player = get_player_info(playerId=[search_id])
#                     # print(box_player)

#                     try:
#                         print(f"[player_info.py] {box_player['code']}: {box_player['message']}")
#                         embed = discord.Embed(title="> ⚠️ 오류", description=f"Code: `{box_player['code']}`\nMessage: {box_player['message']}", color=colorMap['red'])
#                         return await msg.edit_original_response(content="", embed=embed)

#                     except:
#                         if box_player:
#                             for i in range(len(box_player)):
#                                 links = f"[{emoji_esports}]({esports_op_gg_player}{box_player[i]['id']}) "
#                                 if box_player[i]['stream']: links = f"{links}[{emoji_website}]({box_player[i]['stream']}) "
#                                 if box_player[i]['youtube']: links = f"{links}[{emoji_youtube}]({box_player[i]['youtube']}) "
#                                 if box_player[i]['instagram']: links = f"{links}[{emoji_instagram}]({box_player[i]['instagram']}) "
#                                 if box_player[i]['facebook']: links = f"{links}[{emoji_facebook}]({box_player[i]['facebook']}) "
#                                 if box_player[i]['twitter']: links = f"{links}[{emoji_twitter}]({box_player[i]['twitter']}) "
#                                 if box_player[i]['discord']: links = f"{links}[{emoji_discord}]({box_player[i]['discord']}) "
#                                 links = links[:-1]

#                                 embed = discord.Embed(title=f"> 🔍 선수 정보", description="리그 오브 레전드 e스포츠의 선수 정보입니다.", color=colorMap['red'])
#                                 embed.set_footer(text="TIP: ", icon_url=self.bot.user.display_avatar.url)
#                                 embed.set_image(url=banner_image_url)
#                                 embed.set_thumbnail(url=box_player[i]['imageUrl'])
#                                 embed.add_field(name="인적 정보", value=f"닉네임: [{box_player[i]['team_acronym']}]({esports_op_gg_team}{box_player[i]['team_id']}) [{box_player[i]['nickName']}]({esports_op_gg_player}{box_player[i]['id']})\n본명: {box_player[i]['firstName']} {box_player[i]['lastName']}\n생일: {box_player[i]['birthday']}", inline=True)
#                                 embed.add_field(name="SNS 플랫폼", value=links, inline=True)
#                             await msg.edit_original_response(content="", embed=embed)

#         except Exception as error:
#             print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
#             print(traceback.format_exc())



# def setup(bot):
#     bot.add_cog(PlayerInfoCMD(bot))
#     print("player_info.py 로드 됨")
