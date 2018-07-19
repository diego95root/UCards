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
    <script src="../js/main.js"></script>
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

def build_slide(li):
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

    print '<button>hi</button>'

    print '</ul>'

if (len(form.keys()) == 2):
    orig = form['eng'].value
    trans = form['rus'].value

    imgs = get_images(orig)
    imgli = []

    for i in range(0, len(imgs["items"])):
        link = imgs["items"][i]["link"]
        imgli.append(link)
        #print '<img src="{}" alt="flash">'.format(link)

    print html_start
    build_slide(imgli)
    print html_end

    #insert_trans(table, orig, trans, link)


else:
    print html_start
    print """

        <ul class="slides">

                <input type="radio" name="radio-btn" id="img-1" checked />
                <li class="slide-container">
            		<div class="slide">
            			<img src="https://staticz.womenalia.com/images/avatar/blogs/post/8755/el-papel-del-abuelo-en-la-relacion-abuelo-nieto_1523460007.png" />
                    </div>
            		<div class="nav">
            			<label for="img-10" class="prev">&#x2039;</label>
            			<label for="img-2" class="next">&#x203a;</label>
            		</div>
                </li>



                <input type="radio" name="radio-btn" id="img-2" checked />
                <li class="slide-container">
            		<div class="slide">
            			<img src="https://prod.media.larepublica.pe/720x405/larepublica/imagen/2018/05/30/noticia-donald-trump-eeuu-abuelo.png" />
                    </div>
            		<div class="nav">
            			<label for="img-1" class="prev">&#x2039;</label>
            			<label for="img-3" class="next">&#x203a;</label>
            		</div>
                </li>



                <input type="radio" name="radio-btn" id="img-3" checked />
                <li class="slide-container">
            		<div class="slide">
            			<img src="https://blog.panasonic.es/wp-content/uploads/2014/07/ABUELOS.png" />
                    </div>
            		<div class="nav">
            			<label for="img-2" class="prev">&#x2039;</label>
            			<label for="img-4" class="next">&#x203a;</label>
            		</div>
                </li>



                <input type="radio" name="radio-btn" id="img-4" checked />
                <li class="slide-container">
            		<div class="slide">
            			<img src="https://i.blogs.es/9f06c5/abuelo-uci/450_1000.png" />
                    </div>
            		<div class="nav">
            			<label for="img-3" class="prev">&#x2039;</label>
            			<label for="img-5" class="next">&#x203a;</label>
            		</div>
                </li>



                <input type="radio" name="radio-btn" id="img-5" checked />
                <li class="slide-container">
            		<div class="slide">
            			<img src="http://www.revolucionmama.com/wp-content/uploads/2016/10/d%C3%ADa-del-abuelo.png" />
                    </div>
            		<div class="nav">
            			<label for="img-4" class="prev">&#x2039;</label>
            			<label for="img-6" class="next">&#x203a;</label>
            		</div>
                </li>



                <input type="radio" name="radio-btn" id="img-6" checked />
                <li class="slide-container">
            		<div class="slide">
            			<img src="https://prod.media.larepublica.pe/720x405/larepublica/imagen/2018/03/16/noticia-whatsapp-abuelo.png" />
                    </div>
            		<div class="nav">
            			<label for="img-5" class="prev">&#x2039;</label>
            			<label for="img-7" class="next">&#x203a;</label>
            		</div>
                </li>



                <input type="radio" name="radio-btn" id="img-7" checked />
                <li class="slide-container">
            		<div class="slide">
            			<img src="https://prod.media.wapa.pe/670x376/wapa/imagen/2018/03/09/noticia-abueloteextrano.png" />
                    </div>
            		<div class="nav">
            			<label for="img-6" class="prev">&#x2039;</label>
            			<label for="img-8" class="next">&#x203a;</label>
            		</div>
                </li>



                <input type="radio" name="radio-btn" id="img-8" checked />
                <li class="slide-container">
            		<div class="slide">
            			<img src="https://www.vista-laser.com/wp-content/uploads/revslider/portada/abuelo-nieto.png" />
                    </div>
            		<div class="nav">
            			<label for="img-7" class="prev">&#x2039;</label>
            			<label for="img-9" class="next">&#x203a;</label>
            		</div>
                </li>



                <input type="radio" name="radio-btn" id="img-9" checked />
                <li class="slide-container">
            		<div class="slide">
            			<img src="https://pbs.twimg.com/profile_images/2790294881/51e9b8b1aec8761a3460ad9c6a5f6090_400x400.png" />
                    </div>
            		<div class="nav">
            			<label for="img-8" class="prev">&#x2039;</label>
            			<label for="img-10" class="next">&#x203a;</label>
            		</div>
                </li>



                <input type="radio" name="radio-btn" id="img-10" checked />
                <li class="slide-container">
            		<div class="slide">
            			<img src="https://www.dolcacatalunya.com/wp-content/uploads/2016/01/captura-de-pantalla-2016-01-17-a-las-10-22-35.png" />
                    </div>
            		<div class="nav">
            			<label for="img-9" class="prev">&#x2039;</label>
            			<label for="img-1" class="next">&#x203a;</label>
            		</div>
                </li>


        <li class="nav-dots">
        <label for="img-1" class="nav-dot" id="img-dot-1"></label>
        <label for="img-2" class="nav-dot" id="img-dot-2"></label>
        <label for="img-3" class="nav-dot" id="img-dot-3"></label>
        <label for="img-4" class="nav-dot" id="img-dot-4"></label>
        <label for="img-5" class="nav-dot" id="img-dot-5"></label>
        <label for="img-6" class="nav-dot" id="img-dot-6"></label>
        <label for="img-7" class="nav-dot" id="img-dot-7"></label>
        <label for="img-8" class="nav-dot" id="img-dot-8"></label>
        <label for="img-9" class="nav-dot" id="img-dot-9"></label>
        <label for="img-10" class="nav-dot" id="img-dot-10"></label>
        </li>
        </ul>
        <button onclick="add_img_link()">hi</button>
    """
    print html_end
    see_all()
    #delete_trans(table, "hello")
