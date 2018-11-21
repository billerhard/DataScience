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
def print_figure(world_happiness_file, sheet):

    data_frame = pandas.read_excel(world_happiness_file, sheet)
    print(data_frame)


# Make a bar graph from Figure 2.2, just Country vs. Happiness
def plot_bar_graph(world_happiness_file, sheet):
    data_frame = pandas.read_excel(world_happiness_file, sheet)
    # Sheet has a lot of bloat, trim it down to countries and scores.
    data_frame = data_frame.iloc[:-1, 0:2]
    # Set index for plot
    data_frame.index = data_frame['Country']
    # Ready to plot and show!
    data_frame.plot.bar()
    matplotlib.pyplot.show()


def main():
    # Path to file
    world_happiness_file = Path("./world_happiness.xls")

    # If we don't have the report, get it into an xls.
    if not world_happiness_file.exists():
        get_and_store_report(world_happiness_file)

    # Print Figure 2.3
    print_figure(world_happiness_file, 2)

    # Make a bar graph
    plot_bar_graph(world_happiness_file, 1)

    # Create SQL Database




if __name__ == '__main__':
    main()
