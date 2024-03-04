import os
import discord
from discord.ext import commands
from discord.ext import tasks
import factorio_rcon
import util.factorio as factorio

class Factorio(commands.Cog, name="factorio"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.notice_done_user_list = []
        USE = bot.config["factorio"]["use"]
        IP = bot.config["factorio"]["rcon_ip"]
        PORT = bot.config["factorio"]["rcon_port"]
        PASSWORD = os.getenv("FACTORIO_RCON_PASSWORD","")
        client = factorio_rcon.RCONClient(IP, PORT, PASSWORD)
        self.bot.logger.info("[factorio] version:" + factorio.version(client))
        self.rcon_client = client
        self.check_online_user.start()


    def cog_unload(self):
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


async def setup(bot) -> None:
    await bot.add_cog(Factorio(bot))
