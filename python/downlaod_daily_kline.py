import sys

from kline_downloader import KlineDownloader
from utility import get_parser


if __name__ == "__main__":
    parser = get_parser('klines')
    args = parser.parse_args(sys.argv[1:])
    downloader = KlineDownloader(args)
    downloader.download_daily_klines()