# Learning world happiness
# CNA 330
# Bill Erhard, wherhard@student.rtc.edu
import requests


# returns xls as binary from website
def fetch_xls():

    query = "https://s3.amazonaws.com/happiness-report/2018" \
            "/WHR2018Chapter2OnlineData.xls"
    request = requests.get(query)
    binary = request.content

    return binary


def main():
    fetch_xls()


if __name__ == '__main__':
    main()
