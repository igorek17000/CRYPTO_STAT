# coding:utf-8
from rich.traceback import install
from binance.um_futures import UMFutures
from datetime import datetime
import locale
import signal
import sys
import var
import os
from colorama import Fore, Style
from art import tprint
import pathlib
from pathlib import Path
from prettytable import PrettyTable
from dataclasses import dataclass

install(show_locals=True)

futures = UMFutures()


class ServerGetData:
    @staticmethod
    def get_server_time():
        return str(datetime.fromtimestamp(futures.time()[var.QueryKey.server_time] / 1000))[:-7]

    @staticmethod
    def request_data(number_request: int) -> None:
        request_name = var.Service.RequestName[number_request - 1]

        ticker = var.CoinQuery.ticker
        tf = var.CoinQuery.time_frame
        limit = var.CoinQuery.limit

        var.CoinQuery.response = request_name(symbol=ticker, period=tf, limit=limit)

    @staticmethod
    def dump_ticker() -> None:
        for items in futures.exchange_info()[var.QueryKey.exch_info]:
            var.CoinQuery.list_tickers.append(items[var.QueryKey.exch_info_items])


class SysExit:
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

    @classmethod
    def sigint_handler(cls, signal, frame) -> None:
        print("\nExit")
        sys.exit(0)

    @classmethod
    def exit_key(cls) -> None:
        signal.signal(signal.SIGINT, cls.sigint_handler)


class Patch:
    @staticmethod
    def create_folder(name_folder: str) -> None:
        folder = Path(pathlib.Path.cwd(), 'report', 'data', name_folder)
        if not os.path.isdir(folder):
            os.mkdir(folder)    
 
    
class Covert:
    @staticmethod
    def list_str(convert_list: list):
        return ' '.join(map(str, convert_list)) 
    
    
class LogoPrint:
    @staticmethod
    def logo() -> None:
        print(Fore.RED + Style.BRIGHT)
        tprint(var.ModuleName.name, font=var.ModuleName.font)


class UserInput:
    @staticmethod
    def get_ticker():
        while True:
            msg = var.GlossaryOutput.INPUT_TICKER

            var.CoinQuery.ticker = input(Fore.CYAN + "\n" + msg + Fore.GREEN).upper() + var.CoinQuery.coin_pref
            
            if var.CoinQuery.list_tickers.count(var.CoinQuery.ticker) == 1:
                break
            else:
                print(Fore.RED + "\n" + var.GlossaryOutput.ERROR_PARAM)

        return var.CoinQuery.ticker

    @staticmethod
    def get_time_frame():
        while True:            
            var.CoinQuery.time_frame = input(Fore.CYAN + "\n" + var.GlossaryOutput.INPUT_TF + Fore.GREEN)
            
            if var.Service.TimeFrameList.count(var.CoinQuery.time_frame) == 1:
                break
            else:
                print(Fore.RED + "\n" + var.GlossaryOutput.ERROR_PARAM)

        return var.CoinQuery.time_frame

    @staticmethod
    def get_number() -> None:
        while True:
            var.Service.NumberRequest = input(Fore.CYAN + "\n" + var.GlossaryOutput.INPUT_NUM_REQ + Fore.GREEN)
            number = var.Service.NumberRequest
            
            if number.isdigit() and int(number) != 0 and int(number) <= var.Service.CountRequest:
                var.Service.NumberRequest = int(number)
                break
            else:
                print(Fore.RED + "\n" + var.GlossaryOutput.ERROR_PARAM)
    
                
class RequestList:
    @staticmethod
    def printl() -> None:
        for index_1, index_2 in enumerate(var.Service.RequestOptions):
            var.Service.CountRequest += 1
            
            print("{a:d} : {b:6s}".format(a=index_1 + 1, b=index_2))

                
class WriteDataFile:
    @staticmethod
    def write_taker_long_short_ratio(response: list, ticker: str, timeframe: str) -> None:
        date = ""
        time = ""
        table = PrettyTable()
        table.field_names = ['Buy Sell Ratio', 'Buy Vol', 'Sell Vol', 'Date', 'Time', 'Ticker', 'TF']

        for items in range(len(response)-1):
            date = str(datetime.fromtimestamp(int(response[items]['timestamp']) / 1000))[:-9]
            time = str(datetime.fromtimestamp(int(response[items]['timestamp']) / 1000))[11:]

            buy_vol = locale.format_string('%d', int(response[items]['buyVol'][:-5]), grouping=True)
            sell_vol = locale.format_string('%d', int(response[items]['sellVol'][:-5]), grouping=True)

            table.add_rows(
                [
                    [response[items]['buySellRatio'], buy_vol, sell_vol, date, time, ticker, timeframe],
                ]
            )
        
        date_time = date + " " + time + " "
        name_ticker = ticker + " "
        time_frame = timeframe + " "
        pre_name = "Taker long short ratio "
        file_name = pre_name + name_ticker + date_time + time_frame
        
        print(Fore.GREEN+Style.BRIGHT+"\nWrite " + file_name + "\n")
        print(table)

        Patch.create_folder(date)
        
        with open(Path(pathlib.Path.cwd(), 'report', 'data', date, file_name), 'w') as fp:
            fp.write(str(table) + '\n')

    @staticmethod
    def write_long_short_position_ratio(response: list, ticker: str, timeframe: str) -> None:
        date = ""
        time = ""
        table = PrettyTable()
        table.field_names = ['Long Account', 'Short Account', 'Long Short Ratio', 'Date', 'Time', 'Ticker', 'TF']

        for items in range(len(response)-1):
            date = str(datetime.fromtimestamp(int(response[items]['timestamp']) / 1000))[:-9]
            time = str(datetime.fromtimestamp(int(response[items]['timestamp']) / 1000))[11:]

            table.add_rows(
                [
                    [
                        response[items]['longAccount'],
                        response[items]['shortAccount'],
                        response[items]['longShortRatio'],
                        date, time, ticker, timeframe],
                ]
            )
        
        date_time = date + " " + time + " "
        name_ticker = ticker + " "
        time_frame = timeframe + " "
        pre_name = "Long short position ratio "
        file_name = pre_name + name_ticker + date_time + time_frame

        print(Fore.GREEN+Style.BRIGHT+"\nWrite " + file_name + "\n")
        print(table)

        Patch.create_folder(date)
        
        with open(Path(pathlib.Path.cwd(), 'report', 'data', date, file_name), 'w') as fp:
            fp.write(str(table) + '\n')

    @staticmethod
    def write_long_short_account_ratio(response: list, ticker: str, timeframe: str) -> None:
        date = ""
        time = ""
        table = PrettyTable()
        table.field_names = ['Long Account', 'Short Account', 'Long Short Ratio', 'Date', 'Time', 'Ticker', 'TF']

        for items in range(len(response)-1):
            date = str(datetime.fromtimestamp(int(response[items]['timestamp']) / 1000))[:-9]
            time = str(datetime.fromtimestamp(int(response[items]['timestamp']) / 1000))[11:]

            table.add_rows(
                [
                    [
                        response[items]['longAccount'],
                        response[items]['shortAccount'],
                        response[items]['longShortRatio'],
                        date, time, ticker, timeframe],
                ]
            )
        
        date_time = date + " " + time + " "
        name_ticker = ticker + " "
        time_frame = timeframe + " "
        pre_name = "Long short account ratio "
        file_name = pre_name + name_ticker + date_time + time_frame

        print(Fore.GREEN+Style.BRIGHT+"\nWrite " + file_name + "\n")
        print(table)

        Patch.create_folder(date)
        
        with open(Path(pathlib.Path.cwd(), 'report', 'data', date, file_name), 'w') as fp:
            fp.write(str(table) + '\n')

    @staticmethod
    def write_open_interest_hist(response: list, ticker: str, timeframe: str):
        date = ""
        time = ""
        table = PrettyTable()
        table.field_names = ['Sum Open Interest', 'Sum Open Interest Value', 'Date', 'Time', 'Ticker', 'TF']

        for items in range(len(response)-1):
            date = str(datetime.fromtimestamp(int(response[items]['timestamp']) / 1000))[:-9]
            time = str(datetime.fromtimestamp(int(response[items]['timestamp']) / 1000))[11:]

            sum_oi = locale.format_string('%d', int(response[items]['sumOpenInterest'][:-9]), grouping=True)
            sum_oi_val = locale.format_string('%d', int(response[items]['sumOpenInterestValue'][:-9]), grouping=True)

            table.add_rows(
                [
                    [sum_oi, sum_oi_val, date, time, ticker, timeframe],
                ]
            )
        
        date_time = date + " " + time + " "
        name_ticker = ticker + " "
        time_frame = timeframe + " "
        pre_name = "Open interest hist "
        file_name = pre_name + name_ticker + date_time + time_frame

        print(Fore.GREEN+Style.BRIGHT+"\nWrite " + file_name + "\n")
        print(table)

        Patch.create_folder(date)
        
        with open(Path(pathlib.Path.cwd(), 'report', 'data', date, file_name), 'w') as fp:
            fp.write(str(table) + '\n')
            
    
@dataclass
class WriteMethod:
    Method = [
        WriteDataFile.write_taker_long_short_ratio,
        WriteDataFile.write_long_short_position_ratio,
        WriteDataFile.write_long_short_account_ratio,
        WriteDataFile.write_open_interest_hist
    ]  
         

class GetWriteMethod:
    @staticmethod
    def get_method(number_request: int):
        write_request = WriteMethod.Method[number_request - 1]
        write_request(response=var.CoinQuery.response, ticker=var.CoinQuery.ticker, timeframe=var.CoinQuery.time_frame)
          