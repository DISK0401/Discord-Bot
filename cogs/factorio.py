import discord
from discord.ext import commands
from discord.ext import tasks
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
import util.factorio as factorio

class Factorio(commands.Cog, name="factorio"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.notice_done_user_list = []
        USE = bot.config["factorio"]["use"]
        self.use_factorio_notice = USE
        if USE:
            client = factorio.create_client(self.bot)
            self.bot.logger.info("[factorio] version:" + factorio.version(client))
            self.rcon_client = client
            self.check_online_user.start()


    def cog_unload(self):
        if self.use_factorio_notice:
            self.check_online_user.cancel()


    @tasks.loop(seconds=5)
    async def check_online_user(self):
        self.bot.logger.debug("[factorio] check_online_user実行開始")
        online_user_list:list = factorio.online_player_list(self.rcon_client)
        if online_user_list:
            for user_name in online_user_list:
                if user_name in self.notice_done_user_list:
                    # 通知済みリストにいる = 既知のログイン
                    self.bot.logger.debug("[factorio] 「" + user_name + "さん」はログイン通知済み")
                    continue
                else:
                    # 通知済みリストにいない = 新規ログイン
                    self.notice_done_user_list.append(user_name)
                    message = "「" + user_name+"さん」がログインしました。"
                    self.bot.logger.info("[factorio] " + message)
                    await self.channel.send(message)
                    continue
        if self.notice_done_user_list:
            # 通知済みリストにいるのに、オンラインユーザにいない = 新規ログアウト
            diff_list = list(set(self.notice_done_user_list) - set(online_user_list))
            if diff_list:
                message = ""
                for user_name in diff_list:
                    self.notice_done_user_list.remove(user_name)
                    message += "「"+user_name+"さん」"
                message += "がログアウトしました。"
                self.bot.logger.info("[factorio] " + message)
                await self.channel.send(message)
        self.bot.logger.debug("[factorio] check_online_user実行終了")


    @check_online_user.before_loop
    async def before_check_online_user(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(self.bot.config["factorio"]["notice_channel"])
        self.channel = channel
        # 起動段階でオンラインのユーザを通知
        online_user_list:list = factorio.online_player_list(self.rcon_client)
        if online_user_list:
            message = ""
            for user_name in online_user_list:
                self.notice_done_user_list.append(user_name)
                message += "「"+user_name+"さん」"
            message += "がログイン中です。"
            self.bot.logger.info("[factorio] " + message)
            await self.channel.send(message)


    @commands.hybrid_command(
        name="factorio_notice_stop",
        description="Factorio入退出通知をストップする",
    )
    async def factorio_notice_stop(self, context: Context) -> None:
        """
        Factorioの入退出通知をストップします

        :param context: ハイブリッドコマンドコンテキスト
        """
        if not self.use_factorio_notice:
            # すでに停止済み
            embed = discord.Embed(
                description=f"Factorio入退室通知機能は起動していませんでした", color=0xE02B2B
            )
            await context.send(embed=embed)
            return

        # 停止させる
        self.use_factorio_notice = False
        self.notice_done_user_list = []
        self.check_online_user.cancel()
        embed = discord.Embed(
            description=f"Factorio入退室通知機能を停止しました。", color=0xBEBEFE
        )
        await context.send(embed=embed)
        

    @commands.hybrid_command(
        name="factorio_notice_start",
        description="Factorio入退出通知を起動する",
    )
    async def factorio_notice_start(self, context: Context) -> None:
        """
        Factorioの入退出通知を起動します

        :param context: ハイブリッドコマンドコンテキスト
        """
        if self.use_factorio_notice:
            # すでに起動済み
            embed = discord.Embed(
                description=f"Factorio入退室通知機能は起動済みです", color=0xE02B2B
            )
            await context.send(embed=embed)
            return

        # 起動させる
        client = factorio.create_client(self.bot)
        self.bot.logger.info("[factorio] version:" + factorio.version(client))
        self.rcon_client = client
        self.check_online_user.start()
        embed = discord.Embed(
            description=f"Factorio入退室通知機能を起動しました。", color=0xBEBEFE
        )
        await context.send(embed=embed)


    @commands.hybrid_command(
        name="factorio_status",
        description="Factorioステータス取得",
    )
    @app_commands.describe(show_players="プレイヤー情報を表示するか否か(True/False)")
    async def factorio_status(self, context: Context, *, show_players: bool=False) -> None:
        """
        Factorioステータスを確認する

        :param context: ハイブリッドコマンドコンテキスト
        """
        if not self.use_factorio_notice:
            # 停止中
            embed = discord.Embed(
                description=f"Factorio入退室通知機能が起動していません。", color=0xBEBEFE
            )
            await context.send(embed=embed)
            return

        # 起動中
        embed = discord.Embed(
            description=f"Factorioが起動中です", color=0xBEBEFE
        )
        embed.set_author(name="Factorioサーバ情報")

        ## サーバシード値
        embed.add_field(
            name="シード値:",
            value=f"{factorio.seed(self.rcon_client)}",
            inline=True,
        )
        ## サーバ内経過時間
        embed.add_field(
            name="サーバ内経過時間:",
            value=f"{factorio.time(self.rcon_client)}",
            inline=True,
        )
        ## エイリアン進化ファクター
        embed.add_field(
            name="エイリアン進化ファクター:",
            value=f"{factorio.evolution(self.rcon_client)}",
            inline=False,
        )
        ## オンラインプレイヤー情報
        online_player_list = factorio.online_player_list(self.rcon_client)
        embed.add_field(
            name="現在オンラインユーザ数:",
            value=f"{len(online_player_list)} 人",
            inline=True,
        )
        if show_players:
            online_player_name = ""
            if online_player_list:
                for index, player_name in enumerate(online_player_list):
                    if index >=1 :
                        online_player_name += ", "
                    online_player_name += player_name
            embed.add_field(
                name="現在オンラインのユーザ:",
                value=f"{online_player_name}",
                inline=False,
            )
        ## 参加ユーザ情報
        player_list = factorio.player_list(self.rcon_client)
        embed.add_field(
            name="参加ユーザ数:",
            value=f"{len(player_list)} 人",
            inline=True,
        )
        if show_players:
            player_name = ""
            if player_list:
                for index, player_name in enumerate(player_list):
                    if index >=1 :
                        player_name += ", "
                    player_name += player_name
            embed.add_field(
                name="参加ユーザ:",
                value=f"{player_name}",
                inline=False,
            )
        embed.set_footer(text=f"Factorio_version: {factorio.version(self.rcon_client)}")
        await context.send(embed=embed)


async def setup(bot) -> None:
    await bot.add_cog(Factorio(bot))
