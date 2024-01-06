import logging
from enum import Enum
from random import randint

logger = logging.getLogger('discord_bot').getChild(__name__)

lastExecUserTime = {}

omikuji_jp = {
    "GREAT_BLESSING": '大吉',
    "GOOD_BLESSING": '中吉',
    "MIDDLE_BLESSING": '中吉',
    "SMALL_BLESSING": '小吉',
    "UNCERTAIN_LUCK": '末吉',
    "BAD_LUCK": '凶',
    "TERRIBLE_LUCK": '大凶',
}

    
def trans_jp(Omikuji):
    return omikuji_jp.get(Omikuji.name)

class Omikuji(Enum):
    GREAT_BLESSING = 0   # 大吉
    GOOD_BLESSING = 1    # 中吉
    MIDDLE_BLESSING = 2  # 中吉
    SMALL_BLESSING = 3   # 小吉
    UNCERTAIN_LUCK =4    # 末吉
    BAD_LUCK = 5         # 凶
    TERRIBLE_LUCK = 6    # 大凶
    
    def draw() -> Enum:
        return Omikuji(randint(0, 6))


if __name__ == '__main__':
    Omikuji.draw()
