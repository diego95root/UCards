#!/usr/bin/env python
# - *- coding: utf- 8 - *-

import sqlite3

def create_table(db_name):
    db = sqlite3.connect(db_name)
    query = "create table translate(english varchar(25), russian varchar(25), image varchar(200))";
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()
    db.close()

def insert_trans(db_name, tablename, english, russian, url):
    db = sqlite3.connect(db_name)
    query = "insert into {} values('{}', '{}', '{}');".format(tablename, english, russian, url);
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()
    db.close()

def delete_trans(db_name, tablename, english='', russian=''):
    db = sqlite3.connect(db_name)
    query = "delete from {} where english='{}' or russian='{}';".format(tablename, english, russian);
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()
    db.close()

def see_all(db_name):
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
