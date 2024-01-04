from discord.member import Member,VoiceState
from enum import Enum
import datetime
import logging

logger = logging.getLogger('discord_bot').getChild(__name__)

lastExecUserTime = {}

def isIntervalTimePassed(user:Member, interval:int) -> bool:
    """
    対象のユーザがインターバル時間を経過しているかを判定する。

    Args:
        user (Member): チェック対象のMemberオブジェクト
        interval (int): インターバル時間(second)

    Returns:
        bool: インターバル時間が経過した場合にTrue
    """
    logger.debug(lastExecUserTime)

    now = datetime.datetime.now()
    if user.id in lastExecUserTime:
        lastExecTime = lastExecUserTime[user.id]
        if (now - lastExecTime).total_seconds() < interval:
            lastExecUserTime[user.id] = now
            return False
    lastExecUserTime[user.id] = now
    return True


class Action(Enum):
    CHANNEL_JOIN = 1
    CHANNEL_EXIT = 2
    CHANNEL_MOVE = 3
    MUTE = 4
    UNMUTE = 5
    DEAF = 6
    UNDEAF = 7
    STREAM_START = 8
    STREAM_END = 9
    VIDEO_ON = 10
    VIDEO_OFF = 11
    OTHER = 12

    def checkAction(member:Member, after:VoiceState, before:VoiceState) -> int:
        """
        対象のユーザが実行したアクションを判定する

        Args:
            member (Member): 対象ユーザ
            after (VoiceState): 操作前のボイスチャンネルでのステータス
            before (VoiceState): 操作後のボイスチャンネルでのステータス

        Returns:
            int: 対象操作ID
        """
        if before.channel is None:
            ## チャンネルに参加した
            logger.info(f'{member.name} が {after.channel.name} に参加しました。')
            return Action.CHANNEL_JOIN
        elif after.channel is None:
            ## チャンネルから退出した
            logger.info(f'{member.name} が {before.channel.name} から退出しました。')
            return Action.CHANNEL_EXIT
        elif before.channel.id != after.channel.id:
            ## チャンネルを移動した
            logger.info(f'{member.name} が {before.channel.name} から {after.channel.name} に移動しました。')
            return Action.CHANNEL_MOVE
        elif before.self_mute is False and after.self_mute is True:
            ## ミュートした
            logger.info(f'{member.name} が {after.channel.name} でミュートしました。')
            return Action.MUTE
        elif before.self_mute is True and after.self_mute is False:
            ## ミュート解除した
            logger.info(f'{member.name} が {after.channel.name} でミュート解除しました。')
            return Action.UNMUTE
        elif before.self_deaf is False and after.self_deaf is True:
            ## スピーカーを切った
            logger.info(f'{member.name} が {after.channel.name} でスピーカーを切りました。')
            return Action.DEAF
        elif before.self_deaf is True and after.self_deaf is False:
            ## スピーカーをつけた
            logger.info(f'{member.name} が {after.channel.name} でスピーカーをつけました。')
            return Action.UNDEAF
        elif before.channel.id != after.channel.id:
            ## チャンネルを移動した
            logger.info(f'{member.name} が {before.channel.name} から {after.channel.name} に移動しました。')
            return Action.CHANNEL_MOVE
        elif before.self_stream is False and after.self_stream is True:
            ## 配信を開始した
            logger.info(f'{member.name} が {after.channel.name} で配信を開始しました。')
            return Action.STREAM_START
        elif before.self_stream is True and after.self_stream is False:
            ## 配信を終了した
            logger.info(f'{member.name} が {after.channel.name} で配信を終了しました。')
            return Action.STREAM_END
        elif before.self_video is False and after.self_video is True:
            ## カメラをオンにした
            logger.info(f'{member.name} が {after.channel.name} でカメラをオンにしました。')
            return Action.VIDEO_ON
        elif before.self_video is True and after.self_video is False:
            ## カメラをオフにした
            logger.info(f'{member.name} が {after.channel.name} でカメラをオフにしました。')
            return Action.VIDEO_OFF
        else:
            ## その他
            logger.info("不明な操作です。")
            return Action.OTHER
