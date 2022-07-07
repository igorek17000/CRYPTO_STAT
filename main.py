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
from var import GlossaryOutput
from var import Service
from var import CoinQuery
from colorama import Fore

install(show_locals=True)


def main():
    lib.SysExit.exit_key()

    lib.LogoPrint.logo()
    
    print(Fore.CYAN + "\n" + GlossaryOutput.SERVER_TIME + Fore.GREEN + lib.ServerGetData.get_server_time())
    
    print(Fore.MAGENTA + "\n" + GlossaryOutput.DUMP_TICKERS + "...")
    lib.ServerGetData.dump_ticker()
    
    while True:
        print(Fore.BLUE + "\n" + GlossaryOutput.QUERY_TICKER)
        lib.UserInput.get_ticker()

        tf = lib.Covert.list_str(convert_list=Service.TimeFrameList)

        print(Fore.BLUE + "\n" + GlossaryOutput.QUERY_TF + "\n\n" + tf)
        lib.UserInput.get_time_frame()
        
        print(Fore.BLUE + "\n" + GlossaryOutput.QUERY_REQUEST + " " + CoinQuery.ticker + "?\n")
        lib.RequestList.printl()
        lib.UserInput.get_number()
        
        lib.ServerGetData.request_data(number_request=Service.NumberRequest)
        
        lib.GetWriteMethod.get_method(number_request=Service.NumberRequest)
      
        
if __name__ == "__main__":
    main()
else:
    raise SystemExit("Ejection")
