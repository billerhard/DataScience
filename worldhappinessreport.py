# Learning world happiness
# CNA 330
# Bill Erhard, wherhard@student.rtc.edu

from pathlib import Path
from matplotlib import pyplot
import sqlite3
import pandas
import requests


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
    return


# Open and read the excel spreadsheet, specifically Figure 2.3
def print_figure(world_happiness_file, sheet):

    data_frame = pandas.read_excel(world_happiness_file, sheet)
    print(data_frame)
    return


# Make a bar graph from Figure 2.2, just Country vs. Happiness
def plot_bar_graph(world_happiness_file, sheet):

    data_frame = pandas.read_excel(world_happiness_file, sheet)

    # Sheet has a lot of bloat, trim it down to countries and scores.
    data_frame = data_frame.iloc[:-1, 0:2]

    # Set index for plot
    data_frame.index = data_frame['Country']

    # Ready to plot and show!
    data_frame.plot.bar()
    pyplot.show()
    return


def create_database(database):
    connection = sqlite3.connect(database)
    return connection


def clear_table(cursor):
    sql = '''DROP TABLE happiness;'''
    cursor.execute(sql)


def create_table(cursor, data_frame):
    columns = list(data_frame.columns)
    sql = '''CREATE TABLE happiness(id INTEGER PRIMARY KEY'''
    for column in columns:
        sql = sql + ''', "%s" TEXT''' % column
    sql = sql + ''');'''
    cursor.execute(sql)


def insert_data(cursor, data_frame):
    i = 0
    for row in data_frame.values:
        sql = '''INSERT INTO happiness VALUES(%s, ''' % i
        for value in row:
            sql += '''"%s", ''' % value
        sql = sql[:-2]
        sql += ''');'''
        cursor.execute(sql)
        i += 1


def populate_database(cursor, world_happiness_file):
    data_frame = pandas.read_excel(world_happiness_file, 2)
    # clear_table(cursor) # in case you want to get rid of old data
    create_table(cursor, data_frame)
    insert_data(cursor, data_frame)


def print_database(cursor):
    sql = "SELECT * FROM happiness"
    cursor.execute(sql)
    response = cursor.fetchall()
    for row in response:
        print(row)


def main():
    # Setup Files (xls and sql)
    world_happiness_file = Path("./world_happiness.xls")
    database = Path("./world_happiness.sql")

    # If we don't have the report, get it into an xls.
    if not world_happiness_file.exists():
        get_and_store_report(world_happiness_file)

    # Print Figure 2.3
    print_figure(world_happiness_file, 2)

    # Make a bar graph from Figure 2.2
    plot_bar_graph(world_happiness_file, 1)

    # Create SQL Database
    connection = create_database(database)
    cursor = connection.cursor()
    populate_database(cursor, world_happiness_file)
    # print_database(cursor) # for debugging purposes
    connection.commit()


if __name__ == '__main__':
    main()
