# -*- coding: utf-8 -*-
#
# Discord API ( OP.GG e스포츠 ex. QWER.GG [Python] )
#
# 테스트가 끝난 뒤에는 꼭 토큰 값을 변경할 것.

# 패키지 라이브러리 설정
import discord
from discord.ext import commands
import json
import traceback
import os

import requests
import datetime
import pytz

# config.json 파일 불러오기
try:
    with open(r"./config.json", "rt", encoding="UTF8") as configJson:
        config = json.load(configJson)
    print("config.json 로드 됨")
except: print("config.json 파일이 로드되지 않음")

token_key = config['token_key']
prefix_developer = config['prefix_developer']
webhook_url = config['all_log_webhook_url']

intents = discord.Intents().all()
bot = commands.AutoShardedBot(command_prefix=prefix_developer, intents=intents, shard_count=2)
# bot = commands.Bot(command_prefix=prefix_developer, intents=intents)
bot.remove_command("help")


# Event Code 파일 불러오기
try:
    for cog_files in os.listdir(r"./Cogs/Event"):
        if cog_files.endswith(".py"):
            bot.load_extension("Cogs.Event." + cog_files[:-3])
except Exception as error:
    print("./Cogs/Event 폴더에 접근할 수 없음")
    print(traceback.format_exc())
    print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
    webhook_headers = { "Content-Type": "application/json" }
    webhook_data = {
        "username": "OP.GG E-Sports Log",
        "content": f"``` ```\n>>> `({datetime.datetime.now(pytz.timezone('Asia/Seoul')).strftime('%y/%m/%d %H:%M:%S')})`\n./Cogs/Event 폴더에 접근할 수 없음\n{traceback.format_exc()}"
    }
    webhook_result = requests.post(url=webhook_url, json=webhook_data, headers=webhook_headers)
    if 200 <= webhook_result.status_code < 300: pass
    else: print(f'- [LOG] Not sent with {webhook_result.status_code}, response:\n{webhook_result.json()}')

# Command Code 파일 불러오기
try:
    for cog_files in os.listdir(r"./Cogs/Command"):
        if cog_files.endswith(".py"):
            bot.load_extension("Cogs.Command." + cog_files[:-3])
except Exception as error:
    print("./Cogs/Command 폴더에 접근할 수 없음")
    print(traceback.format_exc())
    webhook_headers = { "Content-Type": "application/json" }
    webhook_data = {
        "username": "OP.GG E-Sports Log",
        "content": f"``` ```\n>>> `({datetime.datetime.now(pytz.timezone('Asia/Seoul')).strftime('%y/%m/%d %H:%M:%S')})`\n./Cogs/Event 폴더에 접근할 수 없음\n{traceback.format_exc()}"
    }
    webhook_result = requests.post(url=webhook_url, json=webhook_data, headers=webhook_headers)
    if 200 <= webhook_result.status_code < 300: pass
    else: print(f'- [LOG] Not sent with {webhook_result.status_code}, response:\n{webhook_result.json()}')

# # View Code 파일 불러오기
# try:
#     for cog_files in os.listdir(r"./Cogs/View"):
#         if cog_files.endswith(".py"):
#             bot.load_extension("Cogs.View." + cog_files[:-3])
# except Exception as error:
#     print("./Cogs/View 폴더에 접근할 수 없음")
#     print(traceback.format_exc())
#     webhook_headers = { "Content-Type": "application/json" }
#     webhook_data = {
#         "username": "OP.GG E-Sports Log",
#         "content": f"``` ```\n>>> `({datetime.datetime.now(pytz.timezone('Asia/Seoul')).strftime('%y/%m/%d %H:%M:%S')})`\n./Cogs/Event 폴더에 접근할 수 없음\n{traceback.format_exc()}"
#     }
#     webhook_result = requests.post(url=webhook_url, json=webhook_data, headers=webhook_headers)
#     if 200 <= webhook_result.status_code < 300: pass
#     else: print(f'- [LOG] Not sent with {webhook_result.status_code}, response:\n{webhook_result.json()}')



bot.run(token_key)
