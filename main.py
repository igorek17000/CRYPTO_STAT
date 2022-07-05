#!/usr/bin/python
# coding:utf-8
# ---------------------------------------------------
# CRYPTO - STAT module version 0.1 for TALOS TERMINAL
# (C) 2022 Меркулов Владимир Андреевич
# Released under GNU Public License (GPL)
# Email: mr.straniks@gmail.com
# ---------------------------------------------------
from rich.traceback import install
import lib
from var import GLOSSARY
from var import SERVICE
from var import COIN_QUERY
from colorama import Fore

install(show_locals=True)


def main():
    lib.SYS_EXIT.exit_key()

    lib.UI_LOGO.print_logo()
    
    print(Fore.CYAN + "\n" + GLOSSARY.SERVER_TIME + Fore.GREEN + lib.DataExchange.get_server_time())
    
    print(Fore.MAGENTA + "\n" + GLOSSARY.DUMP_TICKERS + "...")
    lib.DataExchange.dump_ticker()
    
    while True:
        print(Fore.BLUE + "\n" + GLOSSARY.QUERY_TICKER)
        lib.GET_USER_DATA.get_ticker()
        
        print(Fore.BLUE + "\n" + GLOSSARY.QUERY_TF + "\n\n" + lib.CONVERT.list_str(convert_list=SERVICE.TimeFrameList))
        lib.GET_USER_DATA.get_time_frame()
        
        print(Fore.BLUE + "\n" + GLOSSARY.QUERY_REQUEST + " " + COIN_QUERY.ticker + "?\n")
        lib.REQUEST_LIST.printl()
        lib.GET_USER_DATA.get_number()
        
        lib.DataExchange.request_data(number_request=SERVICE.NumberRequest)
        
        lib.GET_WRITE_METHOD.get_method(number_request=SERVICE.NumberRequest)
      
        
if __name__ == "__main__":
    main()
else:
    raise SystemExit("Ejection")