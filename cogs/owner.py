""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 6.1.0
"""

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


class Owner(commands.Cog, name="owner"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(
        name="sync",
        description="スラッシュコマンドを同期します",
    )
    @app_commands.describe(scope="同期対象のスコープを入力してください。(global or guild)")
    @commands.is_owner()
    async def sync(self, context: Context, scope: str) -> None:
        """
        スラッシュコマンドを同期する

        :param context: コマンドコンテキスト
        :param scope: 同期対象のスコープ(global or guild)
        """

        if scope == "global":
            await context.bot.tree.sync()
            embed = discord.Embed(
                description="スラッシュコマンドがグローバルに同期されました",
                color=0xBEBEFE,
            )
            await context.send(embed=embed)
            return
        elif scope == "guild":
            context.bot.tree.copy_global_to(guild=context.guild)
            await context.bot.tree.sync(guild=context.guild)
            embed = discord.Embed(
                description="スラッシュコマンドがギルドに同期されました",
                color=0xBEBEFE,
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            description="指定するスコープは「global」又は「guild」である必要があります。", color=0xE02B2B
        )
        await context.send(embed=embed)

    @commands.command(
        name="unsync",
        description="スラッシュコマンドをクリアします。",
    )
    @app_commands.describe(
        scope="クリアする対象のスコープを入力してください。(global or guild)"
    )
    @commands.is_owner()
    async def unsync(self, context: Context, scope: str) -> None:
        """
        スラッシュコマンドをクリアする。

        :param context: コマンドコンテキスト
        :param scope: クリア対象のスコープ(global or guild)
        """

        if scope == "global":
            context.bot.tree.clear_commands(guild=None)
            await context.bot.tree.sync()
            embed = discord.Embed(
                description="スラッシュコマンドがグローバルからクリアされました。",
                color=0xBEBEFE,
            )
            await context.send(embed=embed)
            return
        elif scope == "guild":
            context.bot.tree.clear_commands(guild=context.guild)
            await context.bot.tree.sync(guild=context.guild)
            embed = discord.Embed(
                description="スラッシュコマンドがこのギルドからクリアされました",
                color=0xBEBEFE,
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            description="scopeは「global」又は「guild」を指定してください", color=0xE02B2B
        )
        await context.send(embed=embed)

    @commands.command(
        name="load",
        description="特定のcogを読み込みます",
    )
    @app_commands.describe(cog="読み込むcogの名前")
    @commands.is_owner()
    async def load(self, context: Context, cog: str) -> None:
        """
        botに指定したcogを読み込む

        :param context: ハイブリッドコマンドコンテキスト
        :param cog: 読み込むcogの名前
        """
        try:
            await self.bot.load_extension(f"cogs.{cog}")
        except Exception:
            embed = discord.Embed(
                description=f"`{cog}` cogを読み込むことができませんでした。", color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            description=f"`{cog}` cogの読み込みに成功しました。", color=0xBEBEFE
        )
        await context.send(embed=embed)

    @commands.command(
        name="unload",
        description="特定のcogをアンロードします",
    )
    @app_commands.describe(cog="アンロードするcogの名前")
    @commands.is_owner()
    async def unload(self, context: Context, cog: str) -> None:
        """
        botから指定したcogをアンロードする

        :param context: ハイブリッドコマンドコンテキスト
        :param cog: アンロードするcogの名前
        """
        try:
            await self.bot.unload_extension(f"cogs.{cog}")
        except Exception:
            embed = discord.Embed(
                description=f"`{cog}` cogのアンロードに失敗しました。", color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            description=f"`{cog}` cogのアンロードに成功しました。", color=0xBEBEFE
        )
        await context.send(embed=embed)

    @commands.command(
        name="reload",
        description="特定のcogをリロードする",
    )
    @app_commands.describe(cog="リロードするcogの名前")
    @commands.is_owner()
    async def reload(self, context: Context, cog: str) -> None:
        """
        botから指定したcogをリロードする

        :param context: ハイブリッドコマンドコンテキスト
        :param cog: リロードする対象のcogファイル名
        """
        try:
            await self.bot.reload_extension(f"cogs.{cog}")
        except Exception:
            embed = discord.Embed(
                description=f"Could not reload the `{cog}` cog.", color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            description=f"Successfully reloaded the `{cog}` cog.", color=0xBEBEFE
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="shutdown",
        description="Botを停止させる",
    )
    @commands.is_owner()
    async def shutdown(self, context: Context) -> None:
        """
        Botを停止させる

        :param context: ハイブリッドコマンドコンテキスト
        """
        embed = discord.Embed(description="Shutting down. Bye! :wave:", color=0xBEBEFE)
        await context.send(embed=embed)
        await self.bot.close()

    @commands.hybrid_command(
        name="say",
        description="Botに指定した文言を発言させる",
    )
    @app_commands.describe(message="Botに発言させるメッセージ")
    @commands.is_owner()
    async def say(self, context: Context, *, message: str) -> None:
        """
        Botはあなたの望むことを何でも言う。

        :param context: ハイブリッドコマンドコンテキスト
        :param message: Botに発言させるメッセージ
        """
        await context.send(message)

    @commands.hybrid_command(
        name="say_embed",
        description="Botに指定した文言を埋め込み形式で発現させる",
    )
    @app_commands.describe(message="Botに発現させるメッセージ")
    @commands.is_owner()
    async def embed(self, context: Context, *, message: str) -> None:
        """
        Botに指定した文言を埋め込み形式で発現させる

        :param context: ハイブリッドコマンドコンテキスト
        :param message: Botに発現させるメッセージ
        """
        embed = discord.Embed(description=message, color=0xBEBEFE)
        await context.send(embed=embed)

    @commands.hybrid_group(
        name="blacklist",
        description="ブラックリストに関連するコマンド",
    )
    @commands.is_owner()
    async def blacklist(self, context: Context) -> None:
        """
        ブラックリストに関連するコマンド

        :param context: ハイブリッドコマンドコンテキスト
        """
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                description="サブコマンドを指定する必要があります。\n\n**サブコマンド:**\n`add` - ユーザーをブラックリストに追加する.\n`remove` - ブラックリストからユーザーを削除する。",
                color=0xE02B2B,
            )
            await context.send(embed=embed)

    @blacklist.command(
        base="blacklist",
        name="show",
        description="ブラックリストに登録されているユーザーのリストを表示します。",
    )
    @commands.is_owner()
    async def blacklist_show(self, context: Context) -> None:
        """
        ブラックリストに登録されているユーザーのリストを表示します。

        :param context: ハイブリッドコマンドコンテキスト
        """
        blacklisted_users = await self.bot.database.get_blacklisted_users()
        if len(blacklisted_users) == 0:
            embed = discord.Embed(
                description="現在、ブラックリストに登録されているユーザーはいません。", color=0xE02B2B
            )
            await context.send(embed=embed)
            return

        embed = discord.Embed(title="ブラックリスト ユーザリスト", color=0xBEBEFE)
        users = []
        for bluser in blacklisted_users:
            user = self.bot.get_user(int(bluser[0])) or await self.bot.fetch_user(
                int(bluser[0])
            )
            users.append(f"• {user.mention} ({user}) - ブラックリスト入り <t:{bluser[1]}>")
        embed.description = "\n".join(users)
        await context.send(embed=embed)

    @blacklist.command(
        base="blacklist",
        name="add",
        description="ボットを使用できないユーザーを追加します",
    )
    @app_commands.describe(user="ブラックリストに追加するユーザー")
    @commands.is_owner()
    async def blacklist_add(self, context: Context, user: discord.User) -> None:
        """
        ボットを使用できないユーザーを追加する

        :param context: ハイブリッドコマンドコンテキスト
        :param user: ブラックリストに追加するユーザー
        """
        user_id = user.id
        if await self.bot.database.is_blacklisted(user_id):
            embed = discord.Embed(
                description=f"**{user.name}** は既にブラックリストに追加されています",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
            return
        total = await self.bot.database.add_user_to_blacklist(user_id)
        embed = discord.Embed(
            description=f"**{user.name}** はブラックリストに正常に追加されました",
            color=0xBEBEFE,
        )
        embed.set_footer(
            text=f"ブラックリストには、合計{total}人が登録されています。"
        )
        await context.send(embed=embed)

    @blacklist.command(
        base="blacklist",
        name="remove",
        description="Botを使用できないユーザーから外す",
    )
    @app_commands.describe(user="ブラックリストから削除するユーザ")
    @commands.is_owner()
    async def blacklist_remove(self, context: Context, user: discord.User) -> None:
        """
        Botを使用できないユーザーから外す

        :param context: ハイブリッドコマンドコンテキスト
        :param user: ブラックリストから削除するユーザ
        """
        user_id = user.id
        if not await self.bot.database.is_blacklisted(user_id):
            embed = discord.Embed(
                description=f"**{user.name}** はブラックリストに入っていません", color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        total = await self.bot.database.remove_user_from_blacklist(user_id)
        embed = discord.Embed(
            description=f"**{user.name}** はブラックリストから正常に削除されました。",
            color=0xBEBEFE,
        )
        embed.set_footer(
            text=f"ブラックリストには、合計{total}人が登録されています。"
        )
        await context.send(embed=embed)


async def setup(bot) -> None:
    await bot.add_cog(Owner(bot))
