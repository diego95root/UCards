#!/usr/bin/env python
# - *- coding: utf- 8 - *-

import cgi
import cgitb; cgitb.enable()
import requests as r
import json
import sqlite3

debug = True
GET_req = 0

form = cgi.FieldStorage()

languages_available = {
    "eng" : u"Enter the word in English",
    "spa" : u"Introduce la palabra en Español",
    "fre" : u"Introduissez le mot en Français",
    "rus" : u"Введите слово на русском языке" #surely not accurate
}

selected_lang = 'eng-rus'

db_name = 'db/eng-rus.db'
table = 'translate'

html_start = """
<html>
<head>
    <link rel="stylesheet" href="../css/main.css">
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <script src="../js/jquery.js"></script>
    <script src="../js/main.js"></script>
</head>
<body>
<div id="main">
        <input class="input" type="text" name="eng" placeholder="{}"><br />
        <input class="input" type="text" name="rus" placeholder="{}"><br />
        <button id="sender" onclick="send_data()">hi</button>
</div>
<button onclick="google_api()">GET request</button>
""".format(languages_available[selected_lang.split('-')[0]].encode('utf-8'), languages_available[selected_lang.split('-')[1]].encode('utf-8'))

html_end = """</body>
</html>
"""

def create_table():
    db = sqlite3.connect(db_name)
    query = "create table translate(english varchar(25), russian varchar(25), image varchar(200))";
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()
    db.close()

def insert_trans(tablename, english, russian, url):
    db = sqlite3.connect(db_name)
    query = "insert into {} values('{}', '{}', '{}');".format(tablename, english, russian, url);
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()
    db.close()

def delete_trans(tablename, english='', russian=''):
    db = sqlite3.connect(db_name)
    query = "delete from {} where english='{}' or russian='{}';".format(tablename, english, russian);
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()
    db.close()

def see_all():
    db = sqlite3.connect(db_name)
    query = "select * from translate;";
    cursor = db.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print "{} : {} -- {}".format(row[0], row[1], row[2])
    db.commit()
    db.close()

def get_images(query): # CHECK IF IT'S POSSIBLE TO SEARCH AGAIN IF 403
    url = 'https://www.googleapis.com/customsearch/v1'
    json_dict = json.load(open("creds/data.json"))
    """

    DATA.JSON FORMAT:

    {"num": 1, "searchType": "image", "fileType": "png", "start": 1, "cx": "cx number here", "q":"", "key": "key here"}

    """
    json_dict["q"] = query
    jsa = json.dumps(r.get(url, params=json_dict).json())
    j = json.loads(jsa)
    return j

def build_slide(li): # CONVERT TO JS INSIDE MAIN.JS
    print '<ul class="slides">' # slider from https://codepen.io/AMKohn/pen/EKJHf (adopted to python)

    for i in range(1, 11):
        one = """
            <input type="radio" name="radio-btn" id="img-{}" checked />
            <li class="slide-container">
        		<div class="slide">
        			<img src="{}" />
                </div>
        		<div class="nav">
        			<label for="img-{}" class="prev">&#x2039;</label>
        			<label for="img-{}" class="next">&#x203a;</label>
        		</div>
            </li>
        """.format(i, li[i-1], ((i+8)%10)+1, (i % 10) + 1)
        print one

    print '<li class="nav-dots">'
    for i in range(1,11):
        print '<label for="img-{}" class="nav-dot" id="img-dot-{}"></label>'.format(i, i)
    print '</li>'

    print '<button id="button">use?</button>'

    print '</ul>'

    #imgs = get_images(orig)
    #imgli = []
    #
    #for i in range(0, len(imgs["items"])):
    #    link = imgs["items"][i]["link"]
    #    imgli.append(link)
        #print '<img src="{}" alt="flash">'.format(link)
    #build_slide(imgli)

def handle_ajax(term): # HANDLE GET AJAX - INSERT DATA
    imgs = get_images(term)
    img_list = []
    for i in range(0, len(imgs["items"])):
        link = imgs["items"][i]["link"]
        img_list.append(link)
    return json.dumps(img_list)

if form.has_key("links"):
    data = form["links"].value
    print "Content-Type: text/html" # MODIFY TO SEND JSON DATA AND THEN DESERIALIZE IN JS AND ADD TO DOM
    print
    print "1,2,3,4,5,6,7,8,9,10" #handle_ajax(data)

elif form.has_key("eng") and form.has_key("rus") and form.has_key("url"): # HANDLE POST AJAX - INSERT DATA
    d = form["eng"].value
    d2 = form["rus"].value
    d3 = form["url"].value
    insert_trans(table, d, d2, d3)

else:
    print html_start
    print html_end
