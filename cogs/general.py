""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 6.1.0
"""

import platform
import random

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


class General(commands.Cog, name="general"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.context_menu_user = app_commands.ContextMenu(
            name="Grab ID", callback=self.grab_id
        )
        self.bot.tree.add_command(self.context_menu_user)
        self.context_menu_message = app_commands.ContextMenu(
            name="Remove spoilers", callback=self.remove_spoilers
        )
        self.bot.tree.add_command(self.context_menu_message)

    # Message context menu command
    async def remove_spoilers(
        self, interaction: discord.Interaction, message: discord.Message
    ) -> None:
        """
        Removes the spoilers from the message. This command requires the MESSAGE_CONTENT intent to work properly.

        :param interaction: The application command interaction.
        :param message: The message that is being interacted with.
        """
        spoiler_attachment = None
        for attachment in message.attachments:
            if attachment.is_spoiler():
                spoiler_attachment = attachment
                break
        embed = discord.Embed(
            title="Message without spoilers",
            description=message.content.replace("||", ""),
            color=0xBEBEFE,
        )
        if spoiler_attachment is not None:
            embed.set_image(url=attachment.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    # User context menu command
    async def grab_id(
        self, interaction: discord.Interaction, user: discord.User
    ) -> None:
        """
        ユーザがユーザIDを入手するコマンド

        :param interaction: アプリケーションコマンドインタラクション
        :param user: インタラクションをしたユーザ
        """
        embed = discord.Embed(
            description=f"{user.mention}のIDは`{user.id}`です。",
            color=0xBEBEFE,
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @commands.hybrid_command(
        name="help", description="Botで利用可能な全コマンドリストを取得します。"
    )
    async def help(self, context: Context) -> None:
        prefix = self.bot.config["prefix"]
        embed = discord.Embed(
            title="ヘルプ", description="有効なコマンドは、:", color=0xBEBEFE
        )
        for i in self.bot.cogs:
            if i == "owner" and not (await self.bot.is_owner(context.author)):
                continue
            cog = self.bot.get_cog(i.lower())
            commands = cog.get_commands()
            data = []
            for command in commands:
                description = command.description.partition("\n")[0]
                data.append(f"{prefix}{command.name} - {description}")
            help_text = "\n".join(data)
            embed.add_field(
                name=i.capitalize(), value=f"```{help_text}```", inline=False
            )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="botinfo",
        description="BOTの情報を取得します",
    )
    async def botinfo(self, context: Context) -> None:
        """
        ボットに関する有益な（あるいはそうでない）情報を入手する。

        :param context: ハイブリッドコマンドコンテキスト
        """
        embed = discord.Embed(
            description="Used [Krypton's](https://krypton.ninja) template",
            color=0xBEBEFE,
        )
        embed.set_author(name="Bot情報")
        embed.add_field(name="Owner:", value="DISK0401#9832", inline=True)
        embed.add_field(
            name="Python Version:", value=f"{platform.python_version()}", inline=True
        )
        embed.add_field(
            name="Prefix:",
            value=f"/ (Slash Commands) or {self.bot.config['prefix']} for normal commands",
            inline=False,
        )
        embed.set_footer(text=f"Requested by {context.author.id}")
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="serverinfo",
        description="サーバーに関する有益な（あるいはそうでない）情報を入手する",
    )
    async def serverinfo(self, context: Context) -> None:
        """
        サーバーに関する有益な（あるいはそうでない）情報を入手する

        :param context: ハイブリッドコマンドコンテキスト
        """
        roles = [role.name for role in context.guild.roles]
        if len(roles) > 50:
            roles = roles[:50]
            roles.append(f">>>> Displayin [50/{len(roles)}] Roles")
        roles = ", ".join(roles)

        embed = discord.Embed(
            title="**サーバ名:**", description=f"{context.guild}", color=0xBEBEFE
        )
        if context.guild.icon is not None:
            embed.set_thumbnail(url=context.guild.icon.url)
        embed.add_field(name="Server ID", value=context.guild.id)
        embed.add_field(name="メンバー数", value=context.guild.member_count)
        embed.add_field(
            name="テキスト•ボイスチャンネル数", value=f"{len(context.guild.channels)}"
        )
        embed.add_field(name=f"ロール ({len(context.guild.roles)})", value=roles)
        embed.set_footer(text=f"サーバ作成者: {context.guild.created_at}")
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="ping",
        description="ボットが生きているかチェックする",
    )
    async def ping(self, context: Context) -> None:
        """
        ボットが生きているかチェックする

        :param context: ハイブリッドコマンドコンテキスト
        """
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Botのレイテンシーは、**{round(self.bot.latency * 1000)}ms**です",
            color=0xBEBEFE,
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="invite",
        description="Botの招待リンクをプライベートメッセージで送信します",
    )
    async def invite(self, context: Context) -> None:
        """
        ボットの招待リンクを取得し、招待できるようにする。

        :param context: ハイブリッドコマンドコンテキスト
        """
        embed = discord.Embed(
            description=f"リンクをクリックして招待する（ [here]({self.bot.config['invite_link']}) ）",
            color=0xD75BF4,
        )
        try:
            await context.author.send(embed=embed)
            await context.send("プライベートメッセージで送信しました")
        except discord.Forbidden:
            await context.send(embed=embed)

    @commands.hybrid_command(
        name="server",
        description="Botのサポート用Discordサーバへの招待リンクをプライベートメッセージで送信する",
    )
    async def server(self, context: Context) -> None:
        """
        ボットのディスコード・サーバーの招待リンクを入手して、サポートを受けてください。

        :param context: ハイブリッドコマンドコンテキスト
        """
        embed = discord.Embed(
            description=f"リンクをクリックして、Botのサポートサーバに参加する（ [here]({self.bot.config['support_link']})）",
            color=0xD75BF4,
        )
        try:
            await context.author.send(embed=embed)
            await context.send("プライベートメッセージで送信しました")
        except discord.Forbidden:
            await context.send(embed=embed)


    @commands.hybrid_command(
        name="bitcoin",
        description="ビットコインの現在の価格を取得します。",
    )
    async def bitcoin(self, context: Context) -> None:
        """
        ビットコインの現在の価格を取得します。

        :param context: ハイブリッドコマンドコンテキスト
        """
        # こうすることで、ボットがウェブリクエストの際にすべてを停止してしまうのを防ぐことができます。 - see: https://discordpy.readthedocs.io/en/stable/faq.html#how-do-i-make-a-web-request
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"
            ) as request:
                if request.status == 200:
                    bitcoin_data = await request.json()
                    bitcoin_usd:float = float(str(bitcoin_data['bpi']['USD']['rate']).replace(",",""))
                    self.bot.logger.debug(f"bitcoin_usd:{bitcoin_usd:,}")

                    embed = discord.Embed(
                        title="**現在のBitcoin価格：**", color=0xBEBEFE
                    )
                    embed.add_field(name="USD", value=f"{bitcoin_usd:,.2f} USD")

                    async with aiohttp.ClientSession() as session:
                        async with session.get(
                            "https://api.excelapi.org/currency/rate?pair=usd-jpy"
                        ) as request:
                            if request.status == 200:
                                exchange_data:float = float(await request.text())
                                self.bot.logger.debug("為替(usd-円)",exchange_data)
                                result = exchange_data * bitcoin_usd
                                embed.add_field(name="日本円", value=f"{result:,.0f} 円")
                                embed.set_footer(text=f"為替: 1ドル {exchange_data}円")
                else:
                    embed = discord.Embed(
                        title="エラー",
                        description="APIに何か問題があるようです。",
                        color=0xE02B2B,
                    )
        await context.send(embed=embed)


async def setup(bot) -> None:
    await bot.add_cog(General(bot))
