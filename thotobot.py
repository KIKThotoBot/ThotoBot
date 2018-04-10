#!/usr/bin/python3
import os, fileinput, sys, csv
import sqlite3
from datetime import date
from pathlib import Path

# toDo:
# 
# process new group
#   create entry in table group
#   find Users and add entry in table users, if not already exists 
#   for each User of group add relation in table user2group
# 
# process for new logs
#   for each message find userID, groupID and add new entry in table chatlog
#   add new entry in table chatlog
# 
# process for new users
#   check if users exists, if not add users to table users and create new relation in relation in table user2group
# 
# process for group clean up
#   precondition 1: no chatlogentry exists
#   precondition 2: no relation user to group exist
#   if both preconditionsa are tru, delete group

# fields of DB: 
# users.id INTEGER NOT NULL PRIMARY KEY, 
# users.username TEXT
# users.userid TEXT
#
# groups.id INTEGER NOT NULL PRIMARY KEY
# groups.groupname TEXT
# groups.groupid TEXT 
#
# chatlog.id INTEGER NOT NULL PRIMARY KEY
# chatlog.userid INTEGER 
# chatlog.groupid INTEGER
# chatlog.messagetype TEXT
# chatlog.logdate TEXT Format YYYY-MM-DD HH:MM TEXT as ISO8601 strings ("YYYY-MM-DD HH:MM:SS.SSS")

# user2group.id INTEGER NOT NULL PRIMARY KEY
# user2group.userid INTEGER
# user2group.groupid INTEGER
# user2group.isadmin INTEGER used as boolean with 0=false, 1=true
# user2group.isowner INTEGER used as boolean with 0=false, 1=true

class logEntry(object):
    def __init__(self, logID, userID, groupID, messageType, logDate):
        self.logID = logID
        self.logDate = logDate
        self.userID = userID
        self.messagetype = mesageType
        self.groupID = groupID
        
    def __del__(self):
        print('shall be commited on deleting chatlog object?')

class chatlog(object):
    def __init__(self, logID, logDate, userID, messageType, groupID):
        # import chatlog.csv shall be done outside this class
        # list date, chatgroupID, userID
        self.logID = logID
        self.logDate = logDate
        self.userID = userID
        self.messagetype = mesageType
        self.groupID = groupID
        pass
    def __del__(self):
        print('shall be commited on deleting chatlog object?')
        
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

class chatUser(object):
    def __init__(self, userID):
        self.userID = userID

class chatGroup(object):
    def __init__(self, groupID):
        self.groupID = groupID

def addChatlogEntry(userid, groupid, messagetype, logdate):
    chatlogentry = (userid, groupid, messagetype, logdate)
    dbConnection = sqlite3.connect('thotobot.db')
    dbCursor = dbConnection.cursor()
    dbCursor.execute('INSERT INTO chatlog (userid, groupid, messagetype, logdate) VALUES(?,?,?,?)', chatlogentry)
    dbConnection.commit()
    dbConnection.close()

def getSingeleUserLogCounts(userid, groupid):
    conditionValues = (userid, groupid)
    dbConnection = sqlite3.connect('thotobot.db')
    dbCursor = dbConnection.cursor()
    useraction = dbCursor.execute('SELECT users.username, count(*) FROM chatlog, users WHERE chatlog.userid = users.id AND users.id = ? AND chatlog.groupid = ? group by chatlog.userid', conditionValues)
    dbConnection.commit()
    dbConnection.close()
    return useraction

def getGroupStatistics(groupid):
    conditionValues = (groupid)
    dbConnection = sqlite3.connect('thotobot.db')
    dbCursor = dbConnection.cursor()
    groupStatistic = dbCursor.execute('SELECT users.username, count(*) FROM chatlog, users WHERE chatlog.userid = users.id AND chatlog.groupid = ? group by chatlog.userid', conditionValues) 
    dbConnection.commit()
    dbConnection.close()
    return groupStatistic

def addUser(username, userid):
    conditionValues = (username, userid)
    dbConnection = sqlite3.connect('thotobot.db')
    dbCursor = dbConnection.cursor()
    chatUser = dbCursor.execute('INSERT INTO users (username, userid) VALUES(?,?)', conditionValues)
    dbConnection.commit()
    dbConnection.close()
    return userid

def addGroup(groupName, groupID):
    conditionValues = (groupName, groupID)
    dbConnection = sqlite3.connect('thotobot.db')
    dbCursor = dbConnection.cursor()
    chatGroup = dbCursor.execute('INSERT INTO groups (groupname, grooupid) VALUES(?,?)', conditionValues)    
    dbConnection.commit()
    dbConnection.close()
    return groupID

def addUserToGroup(userid, groupid, isAdmin, isOwner):
    conditionValues = (userid, groupid, isAdmin, isOwner)
    dbConnection = sqlite3.connect('thotobot.db')
    dbCursor = dbConnection.cursor()
    relationUser2Group = dbCursor.execute('INSERT INTO user2group (userid, groupid, isadmin, isowner) VALUES(?,?,?,?)', conditionValues)    
    dbConnection.commit()
    dbConnection.close()

def removeUserFromGroup(userid, groupid):
    conditionValues = (userid, groupid)
    dbConnection = sqlite3.connect('thotobot.db')
    dbCursor = dbConnection.cursor()
    relationUser2Group = dbCursor.execute('DELETE FROM user2group WHERE userid = ? and groupid = ?', conditionValues)    
    dbConnection.commit()
    dbConnection.close()

def findUserIDByName(username):
    conditionValues = (username)
    dbConnection = sqlite3.connect('thotobot.db')
    dbCursor = dbConnection.cursor()
    chatUser = dbCursor.execute('SELECT id FROM users WHERE username = ?', conditionValues)    
    dbConnection.commit()
    dbConnection.close()
    return chatUser

def findUserIDbyKIKUserID(userid):
    conditionValues = (userid)
    dbConnection = sqlite3.connect('thotobot.db')
    dbCursor = dbConnection.cursor()
    chatUser = dbCursor.execute('SELECT id FROM users WHERE userid = ?', conditionValues)    
    dbConnection.commit()
    dbConnection.close()
    return chatUser

def updateUserName(username, userID):
    conditionValues = (username, userID)
    dbConnection = sqlite3.connect('thotobot.db')
    dbCursor = dbConnection.cursor()
    chatUser = dbCursor.execute('UPDATE users SET username = ? WHERE userid = ?', conditionValues)    
    dbConnection.commit()
    dbConnection.close()

def findGroupIDbyName(groupName):
    conditionValues = (groupName)
    dbConnection = sqlite3.connect('thotobot.db')
    dbCursor = dbConnection.cursor()
    chatGroup = dbCursor.execute('SELECT id FROM groups where groupname = ?', conditionValues)    
    dbConnection.commit()
    dbConnection.close()
    return chatGroup    
    
def connectToDB():
    dbConnection = sqlite3.connect('thotobot.db')

