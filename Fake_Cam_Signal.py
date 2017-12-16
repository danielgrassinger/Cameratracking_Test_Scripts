'''
Sends af fake signal that two tools were taken out of the toolbox and returned after a few seconds
@author Daniel Grassinger
'''

from time import sleep
import requests

SERVER_IP = 'localhost';
SERVER_PORT = 8000

REMOTE_SCRIPT_PATH = '/cgi-bin/DB_RequestHandler.py'

def takenFromToolbox(id):
    command = 'http://' + str(SERVER_IP) + ':' + str(SERVER_PORT) + str(REMOTE_SCRIPT_PATH) +'?command=takeTool&id='+ str(id)
    r = requests.get(command)
    print(r.status_code)
    print(r.text)

def returnedToToolbox(id):
    command = 'http://' + str(SERVER_IP) + ':' + str(SERVER_PORT) + str(REMOTE_SCRIPT_PATH) +'?command=returnTool&id='+ str(id)
    r = requests.get(command)
    print(r.status_code)
    print(r.text)


def main():

    takenFromToolbox(12)
    sleep(3)
    returnedToToolbox(12)

    takenFromToolbox(11)
    sleep(5)
    returnedToToolbox(11)

if __name__ == "__main__":
    main()