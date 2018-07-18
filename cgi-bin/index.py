#!/usr/bin/env python
# save as cgi-bin/index.py
# Python 2.7
import cgi
import cgitb; cgitb.enable()
import requests as r
import json
import sqlite3

form = cgi.FieldStorage()

db_name = 'db/eng-rus.db'
table = 'translate'

html_start = """
<html>
<head>
    <link rel="stylesheet" href="../css/main.css">
</head>
<body>
<form action="index.py" name="myform" method="GET">
        Enter english:  <input type="text" name="eng"><br />
        Enter russian:  <input type="text" name="rus"><br />
        <input type="submit" value="submit">
</form>"""

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

def get_images(query):
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

if (len(form.keys()) == 2):
    #print html
    """<img src="https://lumiere-a.akamaihd.net/v1/images/pr_coco_homeentertainment_digialhd_23df6b9d.png?region=0,0,400,400" alt="flash">
    <img src="http://news.miamisprings.com/wp-content/uploads/2018/05/Coco_poster.png" alt="flash">
    <img src="https://lumiere-a.akamaihd.net/v1/images/uk_coco_lg_r_02df55ea.png?region=0,0,587,306&width=294" alt="flash">
    <img src="https://cdn.watch-series.co/cover/coco-hindi.png" alt="flash">
    <img src="https://pre00.deviantart.net/f009/th/pre/i/2018/085/b/7/crash_trips_coco_by_deannart-dc71hde.png" alt="flash">
    <img src="https://lumiere-a.akamaihd.net/v1/images/pr_coco_homeentertainment_dvd_47acddd1.png?region=0,0,400,400" alt="flash">
    <img src="https://static.vix.com/en/sites/default/files/styles/large/public/c/coco-movie.png?itok=6emqdCGB" alt="flash">
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f2/Disney%27s_Coco_logo.png/1200px-Disney%27s_Coco_logo.png" alt="flash">
    <img src="https://fanart.tv/fanart/movies/354912/hdmovieclearart/coco-5a01e6ebbeda6.png" alt="flash">
    <img src="https://media.vanityfair.com/photos/5a0b835407eff7065a193c51/master/pass/coco-video-billy-elliot-spielberg.png" alt="flash">"""

    orig = form['eng'].value
    trans = form['rus'].value

    imgs = get_images(orig)

    print html_start, html_end

    for i in range(0, len(imgs["items"])):
        link = imgs["items"][i]["link"]
        print '<img src="{}" alt="flash">'.format(link)

    insert_trans(table, orig, trans, link)


else:
    print html_start
    url = "http://farm9.staticflickr.com/8072/8346734966_f9cd7d0941_z.jpg"

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

        """.format(i, url, ((i+8)%10)+1, (i % 10) + 1)
        print one

    print '<li class="nav-dots">'
    for i in range(1,11):
        print '<label for="img-{}" class="nav-dot" id="img-dot-{}"></label>'.format(i, i)
    print '</li>'

    print '</ul>'
    print html_end
    see_all()
    #delete_trans(table, "hello")
