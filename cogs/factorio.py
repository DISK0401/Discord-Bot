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
        print(IP)
        print(PORT)
        print(PASSWORD)
        self.rcon_client = factorio_rcon.RCONClient(IP, PORT, PASSWORD)
        self.check_online_user.start()


    def cog_unload(self):
        self.check_online_user.cancel()


    @tasks.loop(seconds=5)
    async def check_online_user(self):
        online_user_list:list = factorio.online_player_list(self.rcon_client)
        if online_user_list:
            for user_name in online_user_list:
                if user_name in self.notice_done_user_list:
                    # 通知済みリストにいる = 既知のログイン
                    self.bot.logger.debug("ログイン通知済み")
                    continue
                else:
                    # 通知済みリストにいない = 新規ログイン
                    self.bot.logger.debug("新規ログイン")
                    continue
            # 通知済みリストにいるのに、オンラインユーザにいない = 新規ログアウト
            diff_list = set(online_user_list) ^ set (self.notice_done_user_list)
            if diff_list:
                text = ""
                for user_name in diff_list:
                    text += user_name+"さん、"
                text+="がログアウトしました。"
                self.bot.logger.debug(text)


    @check_online_user.before_loop
    async def before_check_online_user(self):
        self.bot.logger.debug("bot起動待ち...")
        await self.bot.wait_until_ready()


async def setup(bot) -> None:
    await bot.add_cog(Factorio(bot))
