# Learning world happiness
# CNA 330
# Bill Erhard, wherhard@student.rtc.edu
from typing import List, Any

import requests
from pathlib import Path
import pandas
import numpy
import matplotlib.pyplot


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


# Open and read the excel spreadsheet (specifically Figure 2.3, index *2*)
def print_figure_two_dot_three(world_happiness_file):

    data_frame = pandas.read_excel(world_happiness_file, 2)
    print(data_frame)


def main():
    # Path to file
    world_happiness_file = Path("./world_happiness.xls")

    # If we don't have the report, get it into an xls.
    if not world_happiness_file.exists():
        get_and_store_report(world_happiness_file)

    # Print Figure 2.3
    # print_figure_two_dot_three(world_happiness_file)

    # Make a boxplot TODO: fix this
    data_frame = pandas.read_excel(world_happiness_file, 1)
    print(data_frame.plot())


if __name__ == '__main__':
    main()
