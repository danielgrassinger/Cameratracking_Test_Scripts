'''
Sends af fake signal that two tools were taken out of the toolbox and returned after a few seconds
@author Daniel Grassinger
'''
from time import sleep
import requests

def takenFromToolbox(id):
    command = 'http://localhost:8000/cgi-bin/DB_RequestHandler.py?command=takeTool&id='+ str(id)
    r = requests.get(command)
    print(r.status_code)
    print(r.text)

def retrunedToToolbox(id):
    command = 'http://localhost:8000/cgi-bin/DB_RequestHandler.py?command=returnTool&id=' + str(id)
    r = requests.get(command)
    print(r.status_code)
    print(r.text)


def main():

    takenFromToolbox(12)
    sleep(3)
    retrunedToToolbox(12)

    takenFromToolbox(11)
    sleep(5)
    retrunedToToolbox(11)

if __name__ == "__main__":
    main()