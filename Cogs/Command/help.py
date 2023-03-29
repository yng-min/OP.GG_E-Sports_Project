# -*- coding: utf-8 -*-

# 패키지 라이브러리 설정
import discord
from discord.ext import commands
from discord.commands import slash_command
import random
import json
import uuid

# config.json 파일 불러오기
try:
    with open(r"./config.json", "rt", encoding="UTF8") as configJson:
        config = json.load(configJson)
except:
    print("config.json이 로드되지 않음")

colorMap = config['colorMap']


def embed_setup(bot, banner, page):

    if page == 1:
        embed = discord.Embed(title="> 📌 OP.GG Esports 봇 서비스 가이드", description="```서비스 소개 페이지```", color=colorMap['red'])
        embed.add_field(name="▫️ 소개", value=" 본 디스코드 봇은 [OP.GG Esports](https://esports.op.gg/) 서비스의 공식 디스코드 봇이며, **리그 오브 레전드**의 e스포츠 리그 관련 기능을 제공합니다.", inline=False)
        embed.add_field(name="▫️ 기능", value=" 기본적으로 리그 오브 레전드의 e스포츠 일정 조회, 경기 알림 등을 제공하지만 더욱 재밌게 승부 예측 미니게임도 즐길 수 있어요.", inline=False)
        embed.add_field(name="▫️ 서포트 서버", value=" [OP.GG 서비스 서포트 서버](https://discord.com/invite/opgg/)에 입장하여 유저들과 소통하고 OP.GG Esports 봇과 다른 서비스들의 정보를 확인해보세요!", inline=False)

    elif page == 2:
        embed = discord.Embed(title="> 📌 OP.GG Esports 봇 서비스 가이드", description="```기본 명령어 페이지```", color=colorMap['red'])
        embed.add_field(name="/가이드", value="OP.GG Esports 봇의 가이드를 전송해요.", inline=False)
        embed.add_field(name="/서비스 가입", value="서비스를 이용을 위한 기본 설정을 진행해요.", inline=False)
        embed.add_field(name="/서비스 탈퇴", value="서비스를 탈퇴하고 데이터를 삭제해요.", inline=False)
        embed.add_field(name="/프로필", value="서비스 내의 유저 프로필 정보를 조회해요.", inline=False)
        embed.add_field(name="/경기 일정", value="리그 오브 레전드 e스포츠 리그 일정을 확인할 수 있어요.", inline=False)
        embed.add_field(name="/리그 순위", value="리그 오브 레전드 e스포츠 리그 팀 순위를 보여줘요.", inline=False)
        embed.add_field(name="/베스트 플레이어", value="리그 오브 레전드 e스포츠의 MVP는 누구인지 찾아보세요!", inline=False)
        embed.add_field(name="/피드백", value="[Beta] OP.GG Esports 봇의 피드백 또는 의견 제안을 제출할 수 있어요.", inline=False)

    elif page == 3:
        embed = discord.Embed(title="> 📌 OP.GG Esports 봇 서비스 가이드", description="```관리자 명령어 페이지```", color=colorMap['red'])
        embed.add_field(name="/설정 셋업", value="서비스를 이용을 위한 기본 서버 설정을 진행해요.", inline=False)
        embed.add_field(name="/설정 변경", value="서비스 설정의 옵션을 변경할 수 있어요.", inline=False)
        embed.add_field(name="/설정 리그", value="원하는 리그만 알림을 받도록 설정할 수 있어요.", inline=False)

    elif page == 4:
        embed = discord.Embed(title="> 📌 OP.GG Esports 봇 서비스 가이드", description="```승부 예측 미니게임 페이지```", color=colorMap['red'])
        embed.add_field(name="▫️ 승부 예측 게임이 뭔가요?", value=" 리그 경기의 승패를 예측하여 자신의 포인트를 베팅하여 리그를 더욱 즐길 수 있어요.\n\n자신이 좋아하는 팀을 응원한다는 것을 엄청난 베팅을 통해 표현하거나, 냉정하게 분석하여 유리한 베팅 등을 진행해 보세요!", inline=False)
        embed.add_field(name="▫️ 어떻게 즐길 수 있나요?", value=" 승부 예측은 각 경기가 시작되면 베팅 필드가 열리고, 15분 뒤 베팅이 마감돼요.\n\n그리고 해당 경기 종료 후 경기 결과와 함께 승부 예측 결과도 전송됩니다.\n\n※ 단, 주의해야 할 점은 승부 예측은 총 경기 승패와 관계 없이 1세트 결과만 유효해요.(변경 예정)")

    embed.set_footer(text="TIP: 아래 버튼을 눌러 페이지를 넘길 수 있어요.", icon_url=bot.user.display_avatar.url)
    embed.set_image(url=banner)
    return embed


class HelpBUTTON(discord.ui.View):

    def __init__(self, bot, banner, page):
        super().__init__(timeout=None)
        self.bot = bot
        self.banner = banner
        self.page = page
        self.min_page = 1
        self.max_page = 4
        self.add_button()

    def add_button(self):
        button_uuid = uuid.uuid4().hex
        _prev = discord.ui.Button(label="◀️", style=discord.ButtonStyle.blurple, custom_id=f"prev-{button_uuid}")
        _next = discord.ui.Button(label="▶️", style=discord.ButtonStyle.blurple, custom_id=f"next-{button_uuid}")
        _page = discord.ui.Button(label=f"{self.page} / {self.max_page}", style=discord.ButtonStyle.gray, custom_id="page", disabled=True)

        self.add_item(_prev)
        self.add_item(_page)
        self.add_item(_next)

        async def _prev_callback(interaction: discord.Interaction):
            self.page -= 1
            if self.page < self.min_page:
                self.page = self.max_page

            embed = embed_setup(self.bot, self.banner, self.page)

            self.remove_item(_prev)
            self.remove_item(_page)
            self.remove_item(_next)
            self.add_button()
            await interaction.response.edit_message(content="", embed=embed, view=self)

        async def _next_callback(interaction: discord.Interaction):
            self.page += 1
            if self.page > self.max_page:
                self.page = self.min_page

            embed = embed_setup(self.bot, self.banner, self.page)

            self.remove_item(_prev)
            self.remove_item(_page)
            self.remove_item(_next)
            self.add_button()
            await interaction.response.edit_message(content="", embed=embed, view=self)

        _next.callback = _next_callback
        _prev.callback = _prev_callback


class HelpCMD(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.banner = random.choice(config['banner_image_url'])
        self.page = 1

    @slash_command(
        name="가이드",
        description="OP.GG Esports 봇의 가이드를 확인해보세요.",
    )
    async def _helpCMD(self, ctx):

        banner_image_url = random.choice(config['banner_image_url'])

        embed = embed_setup(self.bot, self.banner, self.page)
        await ctx.respond(embed=embed, view=HelpBUTTON(self.bot, banner_image_url, self.page))



def setup(bot):
    bot.add_cog(HelpCMD(bot))
    print("help.py 로드 됨")
