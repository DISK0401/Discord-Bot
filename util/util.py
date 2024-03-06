from datetime import timedelta


def format_timedelta(time:timedelta) -> str:
    """
    引数timeに与えられた時間の値を「HH:MM:SS」形式の文字列として返す関数です。 
    """
    total_sec:float = time.total_seconds()
    # hours
    hours:float = total_sec // 3600 
    # remaining seconds
    remain:float = total_sec - (hours * 3600)
    # minutes
    minutes:float = remain // 60
    # remaining seconds
    seconds:float = remain - (minutes * 60)
    # total time
    return '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))