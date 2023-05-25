# -*- coding: utf-8 -*-

# 패키지 라이브러리 설정
import discord
from discord.ext import commands
from discord.commands import slash_command
import random
import json
import uuid

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


colorMap = config['colorMap']
inviteURL = config['invite_code']


def embed_setup(language, bot, banner, page):

    if page == 1:
        embed_title = language['guide.py']['output']['embed-page_1']['title']
        embed_description = language['guide.py']['output']['embed-page_1']['description']
        embed_field_1_name = language['guide.py']['output']['embed-page_1']['field_1']['name']
        embed_field_1_value = language['guide.py']['output']['embed-page_1']['field_1']['value']
        embed_field_2_name = language['guide.py']['output']['embed-page_1']['field_2']['name']
        embed_field_2_value = language['guide.py']['output']['embed-page_1']['field_2']['value']
        embed_field_3_name = language['guide.py']['output']['embed-page_1']['field_3']['name']
        embed_field_3_value = language['guide.py']['output']['embed-page_1']['field_3']['value']
        embed_field_4_name = language['guide.py']['output']['embed-page_1']['field_4']['name']
        embed_field_4_value = language['guide.py']['output']['embed-page_1']['field_4']['value'].format(url=inviteURL)

        embed = discord.Embed(title=embed_title, description=embed_description, color=colorMap['red'])
        embed.add_field(name=embed_field_1_name, value=embed_field_1_value, inline=False)
        embed.add_field(name=embed_field_2_name, value=embed_field_2_value, inline=False)
        embed.add_field(name=embed_field_3_name, value=embed_field_3_value, inline=False)
        embed.add_field(name=embed_field_4_name, value=embed_field_4_value, inline=False)

    elif page == 2:
        embed_title = language['guide.py']['output']['embed-page_2']['title']
        embed_description = language['guide.py']['output']['embed-page_2']['description']
        embed_field_1_name = language['guide.py']['output']['embed-page_2']['field_1']['name']
        embed_field_1_value = language['guide.py']['output']['embed-page_2']['field_1']['value']
        embed_field_2_name = language['guide.py']['output']['embed-page_2']['field_2']['name']
        embed_field_2_value = language['guide.py']['output']['embed-page_2']['field_2']['value']
        embed_field_3_name = language['guide.py']['output']['embed-page_2']['field_3']['name']
        embed_field_3_value = language['guide.py']['output']['embed-page_2']['field_3']['value']
        embed_field_4_name = language['guide.py']['output']['embed-page_2']['field_4']['name']
        embed_field_4_value = language['guide.py']['output']['embed-page_2']['field_4']['value']
        embed_field_5_name = language['guide.py']['output']['embed-page_2']['field_5']['name']
        embed_field_5_value = language['guide.py']['output']['embed-page_2']['field_5']['value']

        embed = discord.Embed(title=embed_title, description=embed_description, color=colorMap['red'])
        embed.add_field(name=embed_field_1_name, value=embed_field_1_value, inline=False)
        embed.add_field(name=embed_field_2_name, value=embed_field_2_value, inline=False)
        embed.add_field(name=embed_field_3_name, value=embed_field_3_value, inline=False)
        embed.add_field(name=embed_field_4_name, value=embed_field_4_value, inline=False)
        embed.add_field(name=embed_field_5_name, value=embed_field_5_value, inline=False)

    elif page == 3:
        embed_title = language['guide.py']['output']['embed-page_3']['title']
        embed_description = language['guide.py']['output']['embed-page_3']['description']
        embed_field_1_name = language['guide.py']['output']['embed-page_3']['field_1']['name']
        embed_field_1_value = language['guide.py']['output']['embed-page_3']['field_1']['value']
        embed_field_2_name = language['guide.py']['output']['embed-page_3']['field_2']['name']
        embed_field_2_value = language['guide.py']['output']['embed-page_3']['field_2']['value']
        embed_field_3_name = language['guide.py']['output']['embed-page_3']['field_3']['name']
        embed_field_3_value = language['guide.py']['output']['embed-page_3']['field_3']['value']
        embed_field_4_name = language['guide.py']['output']['embed-page_3']['field_4']['name']
        embed_field_4_value = language['guide.py']['output']['embed-page_3']['field_4']['value']
        embed_field_5_name = language['guide.py']['output']['embed-page_3']['field_5']['name']
        embed_field_5_value = language['guide.py']['output']['embed-page_3']['field_5']['value']

        embed = discord.Embed(title=embed_title, description=embed_description, color=colorMap['red'])
        embed.add_field(name=embed_field_1_name, value=embed_field_1_value, inline=False)
        embed.add_field(name=embed_field_2_name, value=embed_field_2_value, inline=False)
        embed.add_field(name=embed_field_3_name, value=embed_field_3_value, inline=False)
        embed.add_field(name=embed_field_4_name, value=embed_field_4_value, inline=False)
        embed.add_field(name=embed_field_5_name, value=embed_field_5_value, inline=False)

    elif page == 4:
        embed_title = language['guide.py']['output']['embed-page_4']['title']
        embed_description = language['guide.py']['output']['embed-page_4']['description']
        embed_field_1_name = language['guide.py']['output']['embed-page_4']['field_1']['name']
        embed_field_1_value = language['guide.py']['output']['embed-page_4']['field_1']['value']
        embed_field_2_name = language['guide.py']['output']['embed-page_4']['field_2']['name']
        embed_field_2_value = language['guide.py']['output']['embed-page_4']['field_2']['value']
        embed_field_3_name = language['guide.py']['output']['embed-page_4']['field_3']['name']
        embed_field_3_value = language['guide.py']['output']['embed-page_4']['field_3']['value']

        embed = discord.Embed(title=embed_title, description=embed_description, color=colorMap['red'])
        embed.add_field(name=embed_field_1_name, value=embed_field_1_value, inline=False)
        embed.add_field(name=embed_field_2_name, value=embed_field_2_value, inline=False)
        embed.add_field(name=embed_field_3_name, value=embed_field_3_value, inline=False)

    elif page == 5:
        embed_title = language['guide.py']['output']['embed-page_5']['title']
        embed_description = language['guide.py']['output']['embed-page_5']['description']
        embed_field_1_name = language['guide.py']['output']['embed-page_5']['field_1']['name']
        embed_field_1_value = language['guide.py']['output']['embed-page_5']['field_1']['value']
        embed_field_2_name = language['guide.py']['output']['embed-page_5']['field_2']['name']
        embed_field_2_value = language['guide.py']['output']['embed-page_5']['field_2']['value']

        embed = discord.Embed(title=embed_title, description=embed_description, color=colorMap['red'])
        embed.add_field(name=embed_field_1_name, value=embed_field_1_value, inline=False)
        embed.add_field(name=embed_field_2_name, value=embed_field_2_value, inline=False)

    embed_footer = language['guide.py']['output'][f'embed-page_{page}']['footer']
    embed.set_footer(text=embed_footer, icon_url=bot.user.display_avatar.url)
    embed.set_image(url=banner)
    return embed


class HelpBUTTON(discord.ui.View):

    def __init__(self, language, bot, banner, page):
        super().__init__(timeout=None)
        self.language = language
        self.bot = bot
        self.banner = banner
        self.page = page
        self.min_page = 1
        self.max_page = 5
        self.add_button()

    def add_button(self):
        button_uuid = uuid.uuid4().hex
        _prev = discord.ui.Button(label="◀️", style=discord.ButtonStyle.gray, custom_id=f"prev-{button_uuid}")
        _next = discord.ui.Button(label="▶️", style=discord.ButtonStyle.gray, custom_id=f"next-{button_uuid}")
        _page = discord.ui.Button(label=f"{self.page} / {self.max_page}", style=discord.ButtonStyle.gray, custom_id="page", disabled=True)

        self.add_item(_prev)
        self.add_item(_page)
        self.add_item(_next)


        async def _prev_callback(interaction: discord.Interaction):
            self.page -= 1
            if self.page < self.min_page:
                self.page = self.max_page

            embed = embed_setup(language=self.language, bot=self.bot, banner=self.banner, page=self.page)

            self.remove_item(_prev)
            self.remove_item(_page)
            self.remove_item(_next)
            self.add_button()
            await interaction.response.edit_message(content="", embed=embed, view=self)


        async def _next_callback(interaction: discord.Interaction):
            self.page += 1
            if self.page > self.max_page:
                self.page = self.min_page

            embed = embed_setup(language=self.language, bot=self.bot, banner=self.banner, page=self.page)

            self.remove_item(_prev)
            self.remove_item(_page)
            self.remove_item(_next)
            self.add_button()
            await interaction.response.edit_message(content="", embed=embed, view=self)

        _next.callback = _next_callback
        _prev.callback = _prev_callback


class GuideCMD(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.page = 1

    @slash_command(
        name=lang_en['guide.py']['command']['name'],
        name_localizations={
            "ko": lang_ko['guide.py']['command']['name'],
        },
        description=lang_en['guide.py']['command']['description'],
        description_localizations={
            "ko": lang_ko['guide.py']['command']['description'],
        }
    )
    async def _helpCMD(self, ctx):

        language = Substitution.substitution(ctx)
        banner_image_url = random.choice(config['banner_image_url'])
        embed = embed_setup(language=language, bot=self.bot, banner=banner_image_url, page=self.page)
        await ctx.respond(embed=embed, view=HelpBUTTON(language=language, bot=self.bot, banner=banner_image_url, page=self.page))



def setup(bot):
    bot.add_cog(GuideCMD(bot))
    print("guide.py 로드 됨")
