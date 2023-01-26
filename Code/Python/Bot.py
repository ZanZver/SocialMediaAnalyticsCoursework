from creds import bot_username, bot_pass, bot_ID, bot_token, bot_g_type

import requests
import json
import time
import os

from py2neo import Graph, Node, Relationship

def login():
    # note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
    auth = requests.auth.HTTPBasicAuth(bot_ID, bot_token)

    # here we pass our login method (password), username, and password
    data = {'grant_type': bot_g_type,
            'username': bot_username,
            'password': bot_pass}

    # setup our header info, which gives reddit a brief description of our app
    headers = {'User-Agent': 'MyEDUBot/0.0.1'}

    # send our request for an OAuth token
    res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)

    # convert response to JSON and pull access_token value
    TOKEN = res.json()['access_token']

    # add authorization to our headers dictionary
    headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}
    return headers

def getData(headers):
    res = requests.get("https://oauth.reddit.com/r/CasualUK/new", headers=headers)
    return(res.json())  # let's see what we get
    
def formatData(outData):
    listOfDicts = []
    changeNone = lambda Myinput : Myinput if Myinput is not None else 0
    
    for post in outData["data"]["children"]:
        dictBuidler = {"selftext" : post["data"].get('selftext'),\
                        "title" : str(post["data"].get('title')).replace('''\"''', "'"),\
                        "author_fullname" : post["data"].get('author_fullname'),\
                        "author" : post["data"].get('author'),\
                        "top_awarded_type" : str(post["data"].get('top_awarded_type')),\
                        "hide_score" : str(post["data"].get('hide_score')),\
                        "name" : post["data"].get('name'),\
                        "upvote_ratio" : post["data"].get('upvote_ratio'),\
                        "ups" : post["data"].get('ups'),\
                        "total_awards_received" : post["data"].get('total_awards_received'),\
                        "user_reports" : post["data"].get('user_reports'),\
                        "category" : str(post["data"].get('category')),\
                        "all_awardings" : post["data"].get('all_awardings'),\
                        "awarders" : post["data"].get('awarders'),\
                        "locked" : str(post["data"].get('locked')),\
                        "author_flair_text" : str(post["data"].get('author_flair_text')),\
                        "num_reports" : changeNone(post["data"].get('num_reports')),\
                        "num_comments" : changeNone(post["data"].get('num_comments')),\
                        "created_utc" : time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(post["data"].get('created_utc'))),\
                        "is_video" : str(post["data"].get('is_video'))}
        listOfDicts.append(dictBuidler)
    
    return(listOfDicts)
    
def insertNeo4j():
    g = Graph('http://localhost:7474/db/data', auth=("neo4j", "password"))
    a = Node("Person", name="Bob", age=44)
    b = Node("Person", name="Bil", age=22)
    KNOWS = Relationship.type("KNOWS")
    g.merge(KNOWS(a, b), "Person", "name")

'''    
logged_headers = login()
json_data = getData(logged_headers)
someItems = formatData(json_data)
json_formatted_str = json.dumps(someItems, indent=4)
print(json_formatted_str)
'''

insertNeo4j()
