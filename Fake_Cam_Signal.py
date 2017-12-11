from time import sleep
import datetime
import requests

def takenFromToolbox(id, time):
    r = requests.get('https://github.com/')
    print(r.status_code)

def retrunedToToolbox(id, time):
    pass


def main():



    takenFromToolbox(12,datetime.datetime.now())
    sleep(3)
    retrunedToToolbox(12, datetime.datetime.now())

    takenFromToolbox(11, datetime.datetime.now())
    sleep(5)
    retrunedToToolbox(11, datetime.datetime.now())

if __name__ == "__main__":
    main()