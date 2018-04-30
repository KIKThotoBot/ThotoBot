#!/usr/bin/python3
import os, fileinput, sys, csv
import sqlite3
from datetime import datetime, timedelta
# from pathlib import Path
from flask import Flask, request, Response
from kik import KikApi, Configuration
from kik.messages import messages_from_json, TextMessage, PictureMessage, \
    SuggestedResponseKeyboard, TextResponse, StartChattingMessage

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
#
# bot must return to following messages
#    Text Messages
#    Scan Data Messages
#    Link Messages
#    Picture Messages
#    Video Messages
#    Start Chatting Messages
#    Sticker Messages

# for initialisation bot needs to be configured.
# check the configuration regularly 
# 

# security
# (receiving messages )To protect against replay attacks, the request also contains a timestamp attribute in the JSON body. Consumers can use timestamp verification to provide additional security.


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

observationPeriod = 30
# days tom keep data

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
    dbCursor.execute('SELECT count(*) FROM chatlog, users WHERE chatlog.userid = users.id AND users.id = ? AND chatlog.groupid = ? group by chatlog.userid', conditionValues)
    useraction = dbCursor.fetchone()
    dbConnection.commit()
    dbConnection.close()
    return useraction[0]

def getGroupStatistics(groupid):
    conditionValues = (groupid, )
    groupStatistic =[]
    dbConnection = sqlite3.connect('thotobot.db')
    dbCursor = dbConnection.cursor()
    for logRow in dbCursor.execute('SELECT users.username, count(*) FROM chatlog, users WHERE chatlog.userid = users.id AND chatlog.groupid = ? group by chatlog.userid', conditionValues):
        groupStatistic.append(logRow)
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
    conditionValues = (username, )
    dbConnection = sqlite3.connect('thotobot.db')
    dbCursor = dbConnection.cursor()
    dbCursor.execute('SELECT id FROM users WHERE username = ?', conditionValues)    
    chatUser  = dbCursor.fetchone()
    dbConnection.commit()
    dbConnection.close()
    return chatUser[0]

def findUserIDbyKIKUserID(userid):
    conditionValues = (userid, )
    dbConnection = sqlite3.connect('thotobot.db')
    dbCursor = dbConnection.cursor()
    dbCursor.execute('SELECT id FROM users WHERE userid = ?', conditionValues)    
    chatUser  = dbCursor.fetchone()
    dbConnection.commit()
    dbConnection.close()
    return chatUser[0]

def updateUserName(username, userID):
    conditionValues = (username, userID)
    dbConnection = sqlite3.connect('thotobot.db')
    dbCursor = dbConnection.cursor()
    chatUser = dbCursor.execute('UPDATE users SET username = ? WHERE userid = ?', conditionValues)    
    dbConnection.commit()
    dbConnection.close()

def findGroupIDbyName(groupName):
    conditionValues = (groupName, )
    dbConnection = sqlite3.connect('thotobot.db')
    dbCursor = dbConnection.cursor()
    dbCursor.execute('SELECT id FROM groups where groupname = ?', conditionValues)    
    chatGroup =  = dbCursor.fetchone()
    dbConnection.commit()
    dbConnection.close()
    return chatGroup[0]    
    
def cleanChatlog():
    conditionValues = datetime.today() - timedelta(days = 30) 
    dbConnection = sqlite3.connect('thotobot.db')
    dbCursor = dbConnection.cursor()
    chatGroup = dbCursor.execute('DELETE FROM chatlog WHERE datetime(logdate)<date(?)', conditionValues)    
    dbConnection.commit()
    dbConnection.close()

def getNumberOfUsersInGroup(groupID):
    conditionValues = (groupID, )
    dbConnection = sqlite3.connect('thotobot.db')
    dbCursor = dbConnection.cursor()
    dbCursor.execute('SELECT count(*) FROM user2group WHERE groupid = ?', conditionValues)    
    userCount = dbCursor.fetchone()
    dbConnection.commit()
    dbConnection.close()
    return userCount[0]

# output for testing
print ( datetime.today() - timedelta(days = observationPeriod) )
userStat = getGroupStatistics(1)
print ( userStat )
userCount = getNumberOfUsersInGroup(1)
print ( userCount )

class KikBot(Flask):
    def __init__(self, kik_api, import_name, static_path=None, static_url_path=None, static_folder="static",
             template_folder="templates", instance_path=None, instance_relative_config=False,
             root_path=None):

    self.kik_api = kik_api

    super(KikBot, self).__init__(import_name, static_path, static_url_path, static_folder, template_folder,
                                 instance_path, instance_relative_config, root_path)

    self.route("/incoming", methods=["POST"])(self.incoming)
    
    def incoming(self):
        
        # verify that this is a valid request
        if not self.kik_api.verify_signature(
                request.headers.get("X-Kik-Signature"), request.get_data()):
            return Response(status=403)

        messages = messages_from_json(request.json["messages"])

        response_messages = []
        
        for message in messages:
            user = self.kik_api.get_user(message.from_user)
            # Check if its the user's first message. Start Chatting messages are sent only once.
            if isinstance(message, StartChattingMessage):
                # check if User exist in DB
                # if not add
                # chat_id how to check if this is a Group chat?
                response_messages.append(TextMessage(
                    to=message.from_user,
                    chat_id=message.chat_id,
                    body="Hey {}, how are you?".format(user.first_name),
                    # keyboards are a great way to provide a menu of options for a user to respond with!
                    keyboards=[SuggestedResponseKeyboard(responses=[TextResponse("Good"), TextResponse("Bad")])]))
    
            elif isinstance(message, TextMessage):
                user = self.kik_api.get_user(message.from_user)
                message_body = message.body.lower()

                if message_body.split()[0] in ["hi", "hello"]:
                    response_messages.append(TextMessage(
                        to=message.from_user,
                        chat_id=message.chat_id,
                        body="Hey {}, how are you?".format(user.first_name),
                        keyboards=[SuggestedResponseKeyboard(responses=[TextResponse("Good"), TextResponse("Bad")])]))

                elif message_body == "good":
                    response_messages.append(TextMessage(
                        to=message.from_user,
                        chat_id=message.chat_id,
                        body="That's Great! :) Wanna see your profile pic?",
                        keyboards=[SuggestedResponseKeyboard(
                            responses=[TextResponse("Sure! I'd love to!"), TextResponse("No Thanks")])]))

                elif message_body == "bad":
                    response_messages.append(TextMessage(
                        to=message.from_user,
                        chat_id=message.chat_id,
                        body="Oh No! :( Wanna see your profile pic?",
                        keyboards=[SuggestedResponseKeyboard(
                            responses=[TextResponse("Yep! I Sure Do!"), TextResponse("No Thank You")])]))

                elif message_body in ["yep! i sure do!", "sure! i'd love to!"]:

                    # Send the user a response along with their profile picture (function definition is below)
                    response_messages += self.profile_pic_check_messages(user, message)

                elif message_body in ["no thanks", "no thank you"]:
                    response_messages.append(TextMessage(
                        to=message.from_user,
                        chat_id=message.chat_id,
                        body="Ok, {}. Chat with me again if you change your mind.".format(user.first_name)))
                else:
                    response_messages.append(TextMessage(
                        to=message.from_user,
                        chat_id=message.chat_id,
                        body="Sorry {}, I didn't quite understand that. How are you?".format(user.first_name),
                        keyboards=[SuggestedResponseKeyboard(responses=[TextResponse("Good"), TextResponse("Bad")])]))

            # If its not a text message, give them another chance to use the suggested responses
            else:

                response_messages.append(TextMessage(
                    to=message.from_user,
                    chat_id=message.chat_id,
                    body="Sorry, I didn't quite understand that. {}?".format(user.first_name),
                    keyboards=[SuggestedResponseKeyboard(responses=[TextResponse("Good"), TextResponse("Bad")])]))

            # We're sending a batch of messages. We can send up to 25 messages at a time (with a limit of
            # 5 messages per user).

            self.kik_api.send_messages(response_messages)

        return Response(status=200)

        


# how to make this as a service?

# how to handle incoming messages
# def incomingMessage(message):
    # check User 
        # if new ... add User
        # if exist update?
        # 
    # check groupid
    # check user2Group relation
    # check contenttype
        # if type = text check text
        
# how to handle wrong incoming messages
# suggest Responses with: 
# keyboards=[SuggestedResponseKeyboard(responses=[TextResponse("Good"), TextResponse("Bad")])]))

# how to send messages to admins/owners

# how to check groupactivity

# how to store individual group configuration?
# schedule of checking
# schedule of sending messages
# 


if __name__ == "__main__":
    """ Main program """
    kik = KikApi('BOT_USERNAME_HERE', 'BOT_API_KEY_HERE')
    # For simplicity, we're going to set_configuration on startup. However, this really only needs to happen once
    # or if the configuration changes. In a production setting, you would only issue this call if you need to change
    # the configuration, and not every time the bot starts.
    kik.set_configuration(Configuration(webhook='WEBHOOK_HERE'))
    app = KikBot(kik, __name__)
app.run(port=8080, host='127.0.0.1', debug=True)