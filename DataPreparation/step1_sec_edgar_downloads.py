import pandas as pd
import time
import requests
import re
import os
import csv
from sec_edgar_downloader import Downloader

def downloadSECFile(tickerSymbol):
    pathDownload = fileTypePath
    dl = Downloader(pathDownload)
    number_of_file = dl.get(fileType, tickerSymbol, after="2018-01-01", before="2023-03-27")
    return number_of_file

def download_group_of_companies(read_path, write_path, read_col_name, write_col_name, start_index, end_index):
    csvOutput = open(write_path, "a+", newline="")
    csvWriter = csv.writer(csvOutput, quoting=csv.QUOTE_NONNUMERIC)
    count_number_of_Files = 0 
    symbol_list = []
    # READ FROM SELECTED INDUSTRIAL FROM CSV
    with open(read_path, encoding="utf8") as f:
        csv_reader = csv.DictReader(f, read_col_name)
        with open(write_path, "w", encoding='UTF8') as w:
            csv_writer = csv.writer(w)
            csv_writer.writerow(write_col_name)
            next(csv_reader)
            for i, line in enumerate(csv_reader):
                # time.sleep(60)
                if i < start_index:
                    continue
                if i >= end_index:
                    break
                Symbol = line["Symbol"]
                # print("Symbol:", Symbol)
                Name = line["Security"]
                Sec = line["GICS Sector"]
                try:
                    number_of_Files = downloadSECFile(Symbol)
                    csv_writer.writerow([Symbol, Name, Sec, number_of_Files])
                    count_number_of_Files += number_of_Files
                    symbol_list.append(Symbol)
                    print("Symbol: ",Symbol)
                except:
                    print(f"unable to download {Symbol}")
                    csv_writer.writerow([Symbol, Name, Sec, "unable to download"])
                    
    print("total downloads file:", count_number_of_Files)
    print("symbol_list", symbol_list)



#######################
#    Run Function     #
#######################
# 0(2) - 10(11),
# start_index = 0
# end_index = 100

start_index = 400
end_index = 503

fileType = "10-K"
fileTypePath = "10K"
read_path = "SP500_20230317.csv"
write_path = "SP500" + "_" + "Summary" + fileType + '_'+ str(start_index) + '_'+ str(end_index) + '.csv'
read_col_name = ["Symbol", "Security", "GICS Sector", "GICS Sub-Industry", "Headquarters Location", "Date added", "CIK Founded"]
write_col_name = ["Symbol", "Security", "Sector", "number_of_Files"] 

download_group_of_companies(read_path, write_path, read_col_name, write_col_name, start_index, end_index)




