# Learning world happiness
# CNA 330
# Bill Erhard, wherhard@student.rtc.edu
from typing import List, Any

import requests
from pathlib import Path
import pandas
import xlrd


# Fetches 2018 world happiness report from aws s3 in xls binary format
def fetch_xls():

    query = "https://s3.amazonaws.com/happiness-report/2018" \
            "/WHR2018Chapter2OnlineData.xls"
    request = requests.get(query)
    binary = request.content

    return binary


# Uses fetch_xls to get 2018 world happiness report and stores it in
# "world_happiness.xls" (only need to run once)
def get_and_store_report(path):

    with open(path, "wb") as f:
        f.write(fetch_xls())


def main():

    # If we don't have the report, get it.
    world_happiness_file = Path("./world_happiness.xls")
    if not world_happiness_file.exists():
        get_and_store_report(world_happiness_file)

    # Open and read the excel spreadsheet (specifically Figure 2.3, index *2*)
    data_frame = pandas.read_excel(world_happiness_file, 2)
    print(data_frame)


if __name__ == '__main__':
    main()
