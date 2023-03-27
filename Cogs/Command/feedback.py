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

# config.json 파일 불러오기
try:
    with open(r"./config.json", "rt", encoding="UTF8") as configJson:
        config = json.load(configJson)
except: print("config.json이 로드되지 않음")

# bot.sqlite 파일 불러오기
try:
    botDB = sqlite3.connect(rf"./Data/bot.sqlite", isolation_level=None)
    botCURSOR = botDB.cursor()
    channel_feedback = botCURSOR.execute("SELECT ChannelFeedback FROM main").fetchone()[0]
    botDB.close()
except Exception as error:
    print("\n({})".format(datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%y/%m/%d %H:%M:%S")))
    print(traceback.format_exc())

colorMap = config['colorMap']


class FeedbackModal(discord.ui.Modal):

    def __init__(self, bot, *args, **kwargs) -> None:
        self.bot = bot
        super().__init__(*args, **kwargs)
        self.add_item(discord.ui.InputText(label="간략한 주제나 제목을 입력해 주세요.", placeholder="(피드백은 개발에 큰 도움이 됩니다.)", style=discord.InputTextStyle.singleline))
        self.add_item(discord.ui.InputText(label="피드백 내용을 자세히 서술해 주세요.", placeholder="(비속어와 인종차별 등 혐오 발언은 처벌 대상이 될 수 있습니다.)", style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        user = interaction.user
        feedbackChannel = self.bot.get_channel(channel_feedback)

        embed = discord.Embed(title="> 💌 피드백", description="아래와 같이 피드백/제안을 전송하였습니다. 이용 감사드립니다. 🙏", color=colorMap['red'])
        embed.add_field(name="> 제목", value=self.children[0].value, inline=False)
        embed.add_field(name="> 내용", value=self.children[1].value, inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

        staffEmbed = discord.Embed(title="> 📪 피드백", description="아래와 같은 피드백/제안이 제출되었습니다.", color=colorMap['red'], timestamp=datetime.datetime.now(pytz.timezone("Asia/Seoul")))
        staffEmbed.set_footer(text="[개발자]", icon_url=self.bot.user.display_avatar.url)
        staffEmbed.add_field(name="> 발송자", value=f"<@{user.id}> ({user})", inline=True)
        try: staffEmbed.add_field(name="> 발송 서버", value=f"{interaction.guild.name} ({interaction.guild.id})", inline=True)
        except: staffEmbed.add_field(name="> 발송 서버", value="(DM에서 전송된 메시지)", inline=True)
        staffEmbed.add_field(name="> 제목", value=self.children[0].value, inline=False)
        staffEmbed.add_field(name="> 내용", value=self.children[1].value, inline=False)
        await feedbackChannel.send(embed=staffEmbed)


class FeedbackCMD(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="피드백",
        description="[Beta] 서비스 개선을 위한 피드백을 제출할 수 있어요.",
    )
    async def _feedbackCMD(self, ctx):

        modal = FeedbackModal(self.bot, title="OP.GG Esports 디스코드 봇 피드백")
        await ctx.send_modal(modal)



def setup(bot):
    bot.add_cog(FeedbackCMD(bot))
    print("feedback.py 로드 됨")
