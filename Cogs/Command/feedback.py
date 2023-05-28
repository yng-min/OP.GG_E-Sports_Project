# -*- coding: utf-8 -*-

# 패키지 라이브러리 설정
import discord
from discord.ext import commands
from discord.commands import slash_command
import sqlite3
import json
import datetime
import pytz
import traceback

from Extensions.i18n.substitution import Substitution

# config.json 파일 불러오기
try:
    with open(r"./config.json", "rt", encoding="UTF8") as configJson:
        config = json.load(configJson)
except: print("config.json이 로드되지 않음")

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

# bot.sqlite 파일 불러오기
try:
    botDB = sqlite3.connect(rf"./Database/bot.sqlite", isolation_level=None)
    botCURSOR = botDB.cursor()
    channel_feedback = botCURSOR.execute("SELECT ChannelFeedback FROM main").fetchone()[0]
    botDB.close()
except Exception as error:
    print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
    print(traceback.format_exc())

colorMap = config['colorMap']


class FeedbackModal(discord.ui.Modal):

    def __init__(self, language, bot, *args, **kwargs) -> None:
        self.language = language
        self.bot = bot
        super().__init__(*args, **kwargs)
        self.add_item(discord.ui.InputText(label=self.language['feedback.py']['output']['modal-feedback']['item-1']['label'], placeholder=self.language['feedback.py']['output']['modal-feedback']['item-1']['placeholder'], style=discord.InputTextStyle.singleline))
        self.add_item(discord.ui.InputText(label=self.language['feedback.py']['output']['modal-feedback']['item-2']['label'], placeholder=self.language['feedback.py']['output']['modal-feedback']['item-2']['placeholder'], style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        user = interaction.user
        feedback_channel = self.bot.get_channel(channel_feedback)

        embed = discord.Embed(title=self.language['feedback.py']['output']['embed-user']['title'], description=self.language['feedback.py']['output']['embed-user']['description'], color=colorMap['red'])
        embed.add_field(name=self.language['feedback.py']['output']['embed-user']['field_1']['name'], value=self.children[0].value, inline=False)
        embed.add_field(name=self.language['feedback.py']['output']['embed-user']['field_1']['name'], value=self.children[1].value, inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

        staffEmbed = discord.Embed(title="> 📪 피드백", description="아래와 같은 피드백/제안이 제출되었습니다.", color=colorMap['red'], timestamp=datetime.datetime.now(pytz.timezone("Asia/Seoul")))
        staffEmbed.set_footer(text="[개발자]", icon_url=self.bot.user.display_avatar.url)
        staffEmbed.add_field(name="> 발송자", value=f"<@{user.id}> ({user})", inline=True)
        try: staffEmbed.add_field(name="> 발송 서버", value=f"{interaction.guild.name} ({interaction.guild.id})", inline=True)
        except: staffEmbed.add_field(name="> 발송 서버", value="(DM에서 전송된 메시지)", inline=True)
        staffEmbed.add_field(name="> 제목", value=self.children[0].value, inline=False)
        staffEmbed.add_field(name="> 내용", value=self.children[1].value, inline=False)
        await feedback_channel.send(embed=staffEmbed)


class FeedbackCMD(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name=lang_en['feedback.py']['command']['name'],
        name_localizations={
            "ko": lang_ko['feedback.py']['command']['name']
        },
        description=lang_en['feedback.py']['command']['description'],
        description_localizations={
            "ko": lang_ko['feedback.py']['command']['description']
        }
    )
    async def _feedbackCMD(self, ctx):

        language = Substitution.substitution(ctx)
        modal = FeedbackModal(language=language, bot=self.bot, title=language['feedback.py']['output']['modal-feedback']['title'])
        await ctx.send_modal(modal)



def setup(bot):
    bot.add_cog(FeedbackCMD(bot))
    print("feedback.py 로드 됨")
