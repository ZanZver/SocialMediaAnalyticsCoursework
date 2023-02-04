from creds import bot_username, bot_pass, bot_ID, bot_token, bot_g_type

import requests
import json
import time
import os

from py2neo import Graph, Node, Relationship
from py2neo.bulk import create_nodes

def login():
    auth = requests.auth.HTTPBasicAuth(bot_ID, bot_token)
    data = {'grant_type': bot_g_type,
            'username': bot_username,
            'password': bot_pass}
    
    headers = {'User-Agent': 'MyEDUBot/0.0.1'}
    res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)
    TOKEN = res.json()['access_token']

    headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}
    return headers

def getData(headers):
    res = requests.get("https://oauth.reddit.com/r/CasualUK/new", headers=headers)
    return(res.json())
    
def replace_chars(text):
    myDict = {  
                "\u2019"  : "'", 
                "\u200b" : "",
                "\u00a3" : "",
                "\u201d" : "",
                "\u201c" : "",
                "\u2018" : "",
                "\u2026" : "",
                "\n" : "",
                '''"''' : "'",
                "\\" : "'"
            }
    return "".join([myDict.get(c, c) for c in text])    
    
def formatData(outData):
    listOfDicts = []
    changeNone = lambda Myinput : Myinput if Myinput is not None else 0
    
    
    for post in outData["data"]["children"]:
        dictBuidler = {
                        "author" : post["data"].get('author'),\
                        "selftext" : replace_chars(str(post["data"].get('selftext'))),\
                        "title" : replace_chars(str(post["data"].get('title'))),\
                        #"author_fullname" : post["data"].get('author_fullname'),\
                        #"top_awarded_type" : str(post["data"].get('top_awarded_type')),\
                        #"hide_score" : str(post["data"].get('hide_score')),\
                        #"name" : post["data"].get('name'),
                        #"upvote_ratio" : post["data"].get('upvote_ratio'),\
                        "ups" : post["data"].get('ups'),
                        #"total_awards_received" : post["data"].get('total_awards_received'),\
                        #"user_reports" : post["data"].get('user_reports'),\
                        #"category" : str(post["data"].get('category')),\
                        #"all_awardings" : post["data"].get('all_awardings'),\
                        #"awarders" : post["data"].get('awarders'),\
                        #"locked" : str(post["data"].get('locked')),\
                        #"author_flair_text" : str(post["data"].get('author_flair_text')),\
                        #"num_reports" : changeNone(post["data"].get('num_reports')),\
                        #"num_comments" : changeNone(post["data"].get('num_comments')),\
                        #"created_utc" : time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(post["data"].get('created_utc'))),\
                        #"is_video" : str(post["data"].get('is_video'))
                        }
        listOfDicts.append(dictBuidler)
    
    return(listOfDicts)
    
def insertNeo4jSample():
    g = Graph('http://localhost:7474/db/data', auth=("neo4j", "password"))
    a = Node("Person", name="Test", age=44)
    b = Node("Person", name="Bil", age=22)
    KNOWS = Relationship.type("KNOWS")
    g.merge(KNOWS(a, b), "Person", "name")
    
def insertNeo4j3(label, dataDict, keys):
    g = Graph('http://localhost:7474/db/data', auth=("neo4j", "password"))
    create_nodes(g.auto(), dataDict, labels={label}, keys=keys)
    
def insertNeo4j2(myDict):
    for item in myDict:
        g = Graph('http://localhost:7474/db/data', auth=("neo4j", "password"))
        create_nodes(g.auto(), [list(item.values())], labels={"RedditData3"}, keys=list(item.keys()))
        #print(list(item.keys()))
        #print(list(item.values()))
        #insertNeo4j3("RedditData2",\
        #             [list(item.values())],\
        #             list(item.keys())
        #)


logged_headers = login()
json_data = getData(logged_headers)
someItems = formatData(json_data)
json_formatted_str = json.dumps(someItems, indent=4)
print(json_formatted_str)

#insertNeo4j()

insertNeo4j2(someItems)