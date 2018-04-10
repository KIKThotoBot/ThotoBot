create table users (id INTEGER NOT NULL PRIMARY KEY, username TEXT, userid TEXT);
create table groups (id INTEGER NOT NULL PRIMARY KEY, groupname TEXT, groupid TEXT);
create table user2group (id INTEGER NOT NULL PRIMARY KEY, userid INTEGER, groupid INTEGER, isadmin INTEGER, isowner INTEGER);
create table chatlog (id INTEGER NOT NULL PRIMARY KEY, userid INTEGER, groupid INTEGER, messagetype TEXT, logdate TEXT);

