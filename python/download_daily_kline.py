import sys

from kline_downloader import KlineDownloader
from utility import get_parser
from datetime import datetime, timedelta


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
    today = datetime.now()
    # 获取52天前的日期
    startDate = today - timedelta(days=52)
    # 将日期格式化为字符串
    endDate = today.strftime("%Y-%m-%d")
    startDate = startDate.strftime("%Y-%m-%d")
    arg_list = ['-t', 'um',
                '-s', f'{symbol}',
                '-i', f'{interval}',
                '-skip-monthly', '1',
                '-startDate', f'{startDate}',
                '-endDate', f'{endDate}']

    args = parser.parse_args(arg_list)
    downloader = KlineDownloader(args)
    downloader.do_download_daily_klines()
