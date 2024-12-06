import sys

from kline_downloader import KlineDownloader
from utility import get_parser
from datetime import datetime, timedelta
from config import SYMBOL_LIST


def get_days_ago(_interval, _keep_count):
    time_diffs = {
        "3m": 180 * _keep_count,
        "5m": 300 * _keep_count,
        "15m": 900 * _keep_count,
        "4h": 14400 * _keep_count,
        "1d": 86400 * _keep_count
    }
    _time_diff = time_diffs.get(_interval, 0)
    _days_ago = int(_time_diff / 86400 + 1)
    _days_ago = _days_ago if _days_ago >= 2 else 2
    return _days_ago


if __name__ == "__main__":
    parser = get_parser('klines')
    if len(sys.argv) != 3:
        print("""
        参数个数{}少于指定个数2，程序使用方式：
        python3 download_daily_kline.py BTCUSDT 1d
        """.format(len(sys.argv) - 1))
        exit()
    else:
        symbol = sys.argv[1]
        interval = sys.argv[2]
    # 获取今天的日期
    if symbol.upper() == 'ALL':
        symbol_list = SYMBOL_LIST
    else:
        symbol_list = [symbol.upper()]
    print("symbol:{}".format(symbol))
    today = datetime.now()
    keep_count = 50
    days_ago = get_days_ago(_interval=interval, _keep_count=keep_count)
    # 获取52天前的日期
    startDate = today - timedelta(days=days_ago)
    # 将日期格式化为字符串
    startDate = startDate.strftime("%Y-%m-%d")
    endDate = today.strftime("%Y-%m-%d")
    for s in symbol_list:
        arg_list = ['-t', 'um',
                    '-s', f'{s}',
                    '-i', f'{interval}',
                    '-skip-monthly', '1',
                    '-startDate', f'{startDate}',
                    '-endDate', f'{endDate}']

        args = parser.parse_args(arg_list)
        downloader = KlineDownloader(args)
        downloader.do_download_daily_klines()
