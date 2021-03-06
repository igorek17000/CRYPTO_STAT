# coding:utf-8
from rich.traceback import install
from dataclasses import dataclass
from binance.um_futures import UMFutures

install(show_locals=True)

futures = UMFutures()
    
    
@dataclass
class CoinQuery:
    ticker: str
    time_frame: str
    response: list
    list_tickers = []
    coin_pref: str = "USDT"
    limit: int = 30


@dataclass
class Service:
    TimeFrameList = [
        '5m',
        '15m',
        '30m',
        '1h',
        '2h',
        '4h',
        '6h',
        '12h',
        '1d'
    ]
    RequestOptions = [
        'Taker long short ratio',
        'Long short position ratio',
        'Long short account ratio',
        'Open interest hist'
    ]
    RequestName = [
        futures.taker_long_short_ratio,
        futures.top_long_short_position_ratio,
        futures.top_long_short_account_ratio,
        futures.open_interest_hist
    ]
    CountRequest: int = 0
    NumberRequest: int = 0
    CountInParams: int = 0

    
@dataclass
class ModuleName:
    name: str = "CRYPTO - STAT"
    font: str = "bulbhead"


@dataclass
class QueryKey:
    server_time: str = "serverTime"
    exch_info: str = "symbols"
    exch_info_items: str = "symbol"
 
    
@dataclass
class GlossaryOutput:
    SERVER_TIME: str = "Binance server time: "
    DUMP_TICKERS: str = "Update database tickers from Binance"
    ERROR_PARAM: str = "Invalid parameter, please try again."
    INPUT_TICKER: str = "Enter symbol ticker : "
    INPUT_TF: str = "Enter time frame : "
    INPUT_NUM_REQ: str = "Enter number request : "
    QUERY_TF: str = "What time frame search?"
    QUERY_TICKER: str = "What ticker search?"
    QUERY_REQUEST: str = "What data to request for"
     