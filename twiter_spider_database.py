# -*- coding: utf-8 -*-
"""
Created on Tue Mar 08 19:18:01 2016

@author: csx
"""
import urllib
import twurl
import json
import sqlite3

twitter_url = "https://api.twitter.com/1.1/friends/list.json"

conn = sqlite3.connect("spider.sqlite3")
cur = conn.cursor()

#create table
cur.execute('''CREATE TABLE IF NOT EXISTS Twitter
            (name TEXT, retrieved INTEGER, friends INTEGER)''')
            
#enter twitter ID
while True:
    twitterID = raw_input("ID:")
    if twitterID == "quit": break
    if len(twitterID)<1:
        twitterID = cur.execute('''SELECT name FROM Twitter WHERE
            retrieved = 0 LIMIT 1''')
        try:
            twitterID = cur.fetchone()[0]
        except:
            print "No unretrieved twitter ID"
            continue #NO NEW Twitter ID

#read the twitter data using API 
url = twurl.augment(twitter_url, {'screen_name':twitterID, 'count':'20'})
print "retrieving url", url
connection = urllib.urlopen(url)
data = connection.read()
header = connection.info().dict
print header
js = json.loads(data)
print js.dumps(js,indent = 4)

cur.execute("UPDATE Twitter SET retrieved = 1 WHERE name = ?", (twitterID,))
#find all the friends
countnew = 0
countold = 0
for u in js["users"]:
    friendname = u["screen_name"]
    cur.execute('''SELECT friends FROM Twitter WHERE name = ?''', friendname)
    try:
        count = cur.fetchone()[0]
        cur.execute('''UPDATE Twitter SET friends = ? WHERE name = ?''',
                    (count+1,friendname))
    except:
        cur.execute('''INSERT INTO Twitter(name,retrieved,friends) VALUES
                    (?,0,1)''',(friendname,))
conn.commit()

cur.close()


#-----------------new version----------------------------
cur.execute('''CREATE TABLE IF NOT EXISTS people(
            id INTEGER PRIMARY KEY,name TEXT UNIQUE,retrieved INTEGER)''')
cur.execute('''CREATE TABLE IF NOT EXISTS pair(from_friend INTEGER,
               to_friend INTEGER) UNIQUE(from_friend, to_friend)''')

while True:
    twitterID = raw_input("ID:")
    if twitterID == "quit": break
    if len(twitterID)<1:
        twitterID = cur.execute('''SELECT name FROM Twitter WHERE
            retrieved = 0 LIMIT 1''')
        try:
            twitterID = cur.fetchone()[0]
        except:
            print "No unretrieved twitter ID"
    else:
        cur.execute("SELECT id FROM people WHERE name=?"(twitterID,))
        try:
            IDkey = cur.fetchone()[0]
        except:
            cur.execute("INSERT INTO people(name, retrieved) VALUES (?,0)",
                        (twitterID,))





