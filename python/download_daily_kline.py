import sys

from kline_downloader import KlineDownloader
from utility import get_parser


if __name__ == "__main__":
    parser = get_parser('klines')
    if len(sys.argv) < 8:
        print("""
        参数个数{}少于指定个数8，程序使用方式：
        python3 download_daily_kline.py -t um -s XRPUSDT  -i 1d -skip-monthly 1 -startDate 2024-10-01 -endDate 2024-12-06
        """.format(len(sys.argv)))
    args = parser.parse_args(sys.argv[1:])
    downloader = KlineDownloader(args)
    print(args)
    downloader.do_download_daily_klines()
