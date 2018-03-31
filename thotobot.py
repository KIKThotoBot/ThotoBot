#!/usr/bin/python3
import os, fileinput, sys, csv
from datetime import date
from pathlib import Path


class chatlog(object):
    def __init__(self):
        # import chatlog.csv
        # list date, chatgroupID, userID
    pass
    def addLogDate(self, logDate):
        # add date of log entry
        pass
    def addLogChatgroupID(self, chatgroupID):
        # add grouid of log entry
        pass
    def addUserID(self, userID):
        # add userid of log entry
        pass
    def addLogID(self, logID):
        # add id of log entry
        pass
    def getLogDate(self, logID):
        # return value of log entry
        pass
    def getLogChatgroupID(self, logID):
        # return value of log entry
        pass
    def getUserID(self, logID):
        # return value of log entry
        pass
    def getLogID(self, userID):
        # return value of log entry
        # ist this function necessary?
        pass
    def commitLog():
        # save log to file
        with open('chatstats_temp.csv', "w") as csvfile:
            chatlogwrite = csv.writer(csvfile, delimiter=',', quotechar='|')
            chatlogwrite.writerow(['aplha', 'beta', 'dings'])
            chatlogwrite.writerows()
        # chatstats.csv delete
        # rename chatstats_temp.csv -> chatstats.csv
        pass


def initThotoBot():
    chatlogfile = Path('chatstats.csv')
    if not chatlogfile.is_file():
        print("Chatlog needs to be installed first. trying to create...")
        os.system('touch chatstats.csv')
    elif chatlogfile.is_file():
        print("try to read chatlog")
        #csvinit here
        with open('chatstats.csv') as csvfile:
            chatlog = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in chatlog:
                print(', '.join(row))
    else:
        print("nothing to do?")
def addChatlogEntry():
    daten = ({'123234', '1', '12'},{'123234', '1', '12'},{'123234', '1', '12'})
    with open('chatstats_temp.csv', "w") as csvfile:
        chatlogwrite = csv.writer(csvfile, delimiter=',', quotechar='|')
        chatlogwrite.writerow(['aplha', 'beta', 'dings'])
        chatlogwrite.writerows()
initThotoBot()
print(chatlog)
addChatlogEntry()
