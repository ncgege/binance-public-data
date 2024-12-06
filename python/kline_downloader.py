#!/usr/bin/env python

import pandas as pd
from enums import *
from utility import download_file, get_all_symbols, get_start_end_date_objects, convert_to_date_object, \
    get_path


class KlineDownloader:
    def __init__(self, args):
        self.args = args
        self.symbols = self.get_symbols()
        self.num_symbols = len(self.symbols)
        self.start_date, self.end_date = get_start_end_date_objects(self.args.startDate, self.args.endDate)

    def get_symbols(self):
        if not self.args.symbols:
            print("Fetching all symbols from exchange")
            return get_all_symbols(self.args.type)
        return self.args.symbols

    def download_monthly_klines(self):
        for symbol in self.symbols:
            self.print_progress(symbol, "monthly")
            for interval in self.args.intervals:
                for year in self.args.years:
                    for month in self.args.months:
                        current_date = convert_to_date_object(f'{year}-{month}-01')
                        if self.start_date <= current_date <= self.end_date:
                            self.download_kline(symbol, interval, year, month, "monthly")

    def download_daily_klines(self, dates):
        for symbol in self.symbols:
            self.print_progress(symbol, "daily")
            for interval in self.args.intervals:
                if interval in DAILY_INTERVALS:
                    for _date in dates:
                        current_date = convert_to_date_object(_date)
                        if self.start_date <= current_date <= self.end_date:
                            self.download_kline(symbol, interval, _date, None, "daily")

    def download_kline(self, symbol, interval, year_or_date, month=None, kline_type="monthly"):
        path = get_path(self.args.type, "klines", kline_type, symbol, interval)
        if kline_type == "monthly":
            file_name = f"{symbol.upper()}-{interval}-{year_or_date}-{month:02d}.zip"
        else:
            file_name = f"{symbol.upper()}-{interval}-{year_or_date}.zip"
        print("download file now, path:{}, file_name:{}".format(path, file_name))
        download_file(path, file_name, self.args.startDate + " " + self.args.endDate, self.args.folder)

        if self.args.checksum == 1:
            checksum_file_name = file_name + ".CHECKSUM"
            download_file(path, checksum_file_name, self.args.startDate + " " + self.args.endDate, self.args.folder)

    def print_progress(self, symbol, kline_type):
        current = self.symbols.index(symbol) + 1
        print(f"[{current}/{self.num_symbols}] - start download {kline_type} {symbol} klines")

    def do_download_daily_klines(self):
        dates = self.get_dates()

        if self.args.skip_monthly == 0:
            self.download_monthly_klines()

        if self.args.skip_daily == 0:
            self.download_daily_klines(dates)

    def get_dates(self):
        if self.args.dates:
            return self.args.dates
        period = convert_to_date_object(datetime.today().strftime('%Y-%m-%d')) - convert_to_date_object(
            PERIOD_START_DATE)
        dates = pd.date_range(end=datetime.today(), periods=period.days + 1).to_pydatetime().tolist()
        return [_date.strftime("%Y-%m-%d") for _date in dates]
