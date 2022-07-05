# coding:utf-8
from dataclasses import dataclass
from rich.traceback import install
import configparser as settings
from binance.um_futures import UMFutures
from datetime import datetime
import locale
import signal
import sys
import var
import os
from colorama import Fore, Style
from art import tprint
from threading import Lock
import pathlib
from pathlib import Path
from prettytable import PrettyTable
from dataclasses import dataclass

install(show_locals=True)

futures = UMFutures()


class DataExchange:
    @staticmethod
    def dump_ticker():
        tickers = []
        
        for items in futures.exchange_info()[var.QUERY_KEY.exch_info]:
            tickers.append(items[var.QUERY_KEY.exch_info_items])
        
        var.COIN_QUERY.list_tickers = str(tickers).replace("[","").replace("]","")
        
        CONFIG.set_params(var.FILECONF.name_path, var.FILECONF.sections[1], var.FILECONF.section_keys[var.FILECONF.sections[1]][0], var.COIN_QUERY.list_tickers)

        
    @staticmethod
    def connect_exchange():
        return UMFutures(var.API_KEY.Public, var.API_KEY.Secret)
        
        
    @staticmethod
    def get_server_time():
        return str(datetime.fromtimestamp(futures.time()[var.QUERY_KEY.server_time] / 1000))[:-7]
    
    
    @staticmethod
    def request_data(number_request : int):
        RequestName = var.SERVICE.RequestName[number_request - 1]
        var.COIN_QUERY.response = RequestName(symbol = var.COIN_QUERY.ticker, period = var.COIN_QUERY.time_frame, limit = var.COIN_QUERY.limit)
    
        
class SYS_EXIT:
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

    @classmethod
    def sigint_handler(self, signal, frame):
        print("\nExit")
        sys.exit(0)

    @classmethod
    def exit_key(self):
        signal.signal(signal.SIGINT, self.sigint_handler)


class CONFIG:
    @staticmethod
    def get_params(self, conf_file: str, section: str):
        params = settings.ConfigParser()
        params.read(conf_file)

        return params[section]


    @staticmethod
    def set_params(conf_file: str, section: str, key: str, value):
        params = settings.ConfigParser()
        params.read(conf_file)
        params.set(section, key, value)
        
        with Lock():
            with open(var.FILECONF.name_path, 'w') as file_conf:
                params.write(file_conf)
                

    @classmethod        
    def set_api(self):
        var.API_KEY.Public = self.get_params(self, conf_file=var.FILECONF.name_path, section=var.FILECONF.sections[0])[var.FILECONF.section_keys[var.FILECONF.sections[0]][0]]
        var.API_KEY.Secret = self.get_params(self, conf_file=var.FILECONF.name_path, section=var.FILECONF.sections[0])[var.FILECONF.section_keys[var.FILECONF.sections[0]][1]]


    @staticmethod
    def create_folder(name_folder : str):
        folder = Path(pathlib.Path.cwd(), 'report', 'data', name_folder)
        if not os.path.isdir(folder):
            os.mkdir(folder)    
 
    
class CONVERT:
    @staticmethod
    def str_list(convert_string : str):
        return convert_string.split(",")
    
    
    @staticmethod
    def list_str(convert_list : list):
        return ' '.join(map(str, convert_list)) 
    
    
class UI_LOGO:
    @staticmethod
    def print_logo():
        print(Fore.RED + Style.BRIGHT)
        tprint(var.TERMINAL.name, font=var.TERMINAL.font)


class GET_TICKER_USER:
    @staticmethod
    def get_ticker():
        while True:            
            var.COIN_QUERY.ticker = input(Fore.CYAN + "\n" + var.GLOSSARY.INPUT_TICKER + Fore.GREEN).upper() + var.COIN_QUERY.coin_pref
            
            if var.COIN_QUERY.list_tickers.count(var.COIN_QUERY.ticker) == 1:
                return var.COIN_QUERY.ticker
                break
            else:
                print(Fore.RED + "\n" + var.GLOSSARY.ERROR_PARAM)    
                
                
class GET_TF_USER:
    @staticmethod
    def get_time_frame():
        while True:            
            var.COIN_QUERY.time_frame = input(Fore.CYAN + "\n" + var.GLOSSARY.INPUT_TF + Fore.GREEN)
            
            if var.SERVICE.TimeFrameList.count(var.COIN_QUERY.time_frame) == 1:
                return var.COIN_QUERY.time_frame
                break
            else:
                print(Fore.RED + "\n" + var.GLOSSARY.ERROR_PARAM)
                
                
class REQUEST_LIST:
    @staticmethod
    def printl():
        for index_1, index_2 in enumerate(var.SERVICE.RequestOptions):
            var.SERVICE.CountRequest += 1
            
            print("{a:d} : {b:6s}".format(a = index_1 + 1, b = index_2))
            

class GET_NUM_REQUEST:
    @staticmethod
    def get_number():
        while True:
            var.SERVICE.NumberRequest = input(Fore.CYAN + "\n" + var.GLOSSARY.INPUT_NUM_REQ + Fore.GREEN)
            number = var.SERVICE.NumberRequest
            
            if number.isdigit() and int(number) != 0 and int(number) <= var.SERVICE.CountRequest:
                var.SERVICE.NumberRequest = int(number)
                break
            else:
                print(Fore.RED + "\n" + var.GLOSSARY.ERROR_PARAM)
                

class WRITE_DATA_FILE:
    @staticmethod
    def write_taker_long_short_ratio(response : list, ticker : str, timeframe : str):        
        table = PrettyTable()
        table.field_names = ['Buy Sell Ratio', 'Buy Vol', 'Sell Vol', 'Date', 'Time', 'Ticker', 'TF']

        for items in range(len(response)-1):
            date = str(datetime.fromtimestamp(int(response[items]['timestamp']) / 1000))[:-9]
            time = str(datetime.fromtimestamp(int(response[items]['timestamp']) / 1000))[11:]

            buy_vol = locale.format('%d', int(response[items]['buyVol'][:-5]), grouping=True)
            sell_vol = locale.format('%d', int(response[items]['sellVol'][:-5]), grouping=True)

            table.add_rows(
                [
                    [response[items]['buySellRatio'], buy_vol, sell_vol, date, time, ticker, timeframe],
                ]
            )
        
        DateTime = date + " " + time + " "
        NameTicker = ticker + " "
        Timeframe = timeframe + " "
        PreName = "Taker long short ratio "
        FileName = PreName + NameTicker + DateTime + Timeframe
        
        print(Fore.GREEN+Style.BRIGHT+"\nWrite " + FileName + "\n")
        print(table)

        CONFIG.create_folder(date)
        
        with open(Path(pathlib.Path.cwd(), 'report', 'data', date, FileName), 'w') as fp:
            fp.write(str(table) + '\n')
            
            
    @staticmethod
    def write_long_short_position_ratio(response : list, ticker : str, timeframe : str):
        table = PrettyTable()
        table.field_names = ['Long Account', 'Short Account', 'Long Short Ratio', 'Date', 'Time', 'Ticker', 'TF']

        for items in range(len(response)-1):
            date = str(datetime.fromtimestamp(int(response[items]['timestamp']) / 1000))[:-9]
            time = str(datetime.fromtimestamp(int(response[items]['timestamp']) / 1000))[11:]

            table.add_rows(
                [
                    [response[items]['longAccount'], response[items]['shortAccount'], response[items]['longShortRatio'], date, time, ticker, timeframe],
                ]
            )
        
        DateTime = date + " " + time + " "
        NameTicker = ticker + " "
        Timeframe = timeframe + " "
        PreName = "Long short position ratio "
        FileName = PreName + NameTicker + DateTime + Timeframe

        print(Fore.GREEN+Style.BRIGHT+"\nWrite " + FileName + "\n")
        print(table)

        CONFIG.create_folder(date)
        
        with open(Path(pathlib.Path.cwd(), 'report', 'data', date, FileName), 'w') as fp:
            fp.write(str(table) + '\n')
            
            
    @staticmethod
    def write_long_short_account_ratio(response : list, ticker : str, timeframe : str):
        table = PrettyTable()
        table.field_names = ['Long Account', 'Short Account', 'Long Short Ratio', 'Date', 'Time', 'Ticker', 'TF']

        for items in range(len(response)-1):
            date = str(datetime.fromtimestamp(int(response[items]['timestamp']) / 1000))[:-9]
            time = str(datetime.fromtimestamp(int(response[items]['timestamp']) / 1000))[11:]

            table.add_rows(
                [
                    [response[items]['longAccount'], response[items]['shortAccount'], response[items]['longShortRatio'], date, time, ticker, timeframe],
                ]
            )
        
        DateTime = date + " " + time + " "
        NameTicker = ticker + " "
        Timeframe = timeframe + " "
        PreName = "Long short account ratio "
        FileName = PreName + NameTicker + DateTime + Timeframe

        print(Fore.GREEN+Style.BRIGHT+"\nWrite " + FileName + "\n")
        print(table)

        CONFIG.create_folder(date)
        
        with open(Path(pathlib.Path.cwd(), 'report', 'data', date, FileName), 'w') as fp:
            fp.write(str(table) + '\n')
            
            
    @staticmethod
    def write_open_interest_hist(response : list, ticker : str, timeframe : str):
        table = PrettyTable()
        table.field_names = ['Sum Open Interest', 'Sum Open Interest Value', 'Date', 'Time', 'Ticker', 'TF']

        for items in range(len(response)-1):
            date = str(datetime.fromtimestamp(int(response[items]['timestamp']) / 1000))[:-9]
            time = str(datetime.fromtimestamp(int(response[items]['timestamp']) / 1000))[11:]

            sum_oi = locale.format('%d', int(response[items]['sumOpenInterest'][:-9]), grouping=True)
            sum_oi_val = locale.format('%d', int(response[items]['sumOpenInterestValue'][:-9]), grouping=True)

            table.add_rows(
                [
                    [sum_oi, sum_oi_val, date, time, ticker, timeframe],
                ]
            )
        
        DateTime = date + " " + time + " "
        NameTicker = ticker + " "
        Timeframe = timeframe + " "
        PreName = "Open interest hist "
        FileName = PreName + NameTicker + DateTime + Timeframe

        print(Fore.GREEN+Style.BRIGHT+"\nWrite " + FileName + "\n")
        print(table)

        CONFIG.create_folder(date)
        
        with open(Path(pathlib.Path.cwd(), 'report', 'data', date, FileName), 'w') as fp:
            fp.write(str(table) + '\n')
            
    
@dataclass
class WRITE_METHOD:
    Method = [
        WRITE_DATA_FILE.write_taker_long_short_ratio,
        WRITE_DATA_FILE.write_long_short_position_ratio,
        WRITE_DATA_FILE.write_long_short_account_ratio,
        WRITE_DATA_FILE.write_open_interest_hist
    ]  
         

class GET_WRITE_METHOD:
    @staticmethod
    def get_method(number_request : int):
        write_request = WRITE_METHOD.Method[number_request - 1]
        write_request(response=var.COIN_QUERY.response, ticker=var.COIN_QUERY.ticker, timeframe=var.COIN_QUERY.time_frame)
          