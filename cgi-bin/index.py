#!/usr/bin/env python
# - *- coding: utf- 8 - *-

import cgi
import cgitb; cgitb.enable()
import requests as r
import json
import sys

sys.path.append('cgi-bin')

from my_functions import *

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
    <div id="overlay-back"></div>
    <div id="saved">Flashcard image set</div>
    <div id="main">
            <input class="input" id="first-input" type="text" name="eng" placeholder="{}"><br />
            <input class="input" id="second-input" type="text" name="rus" placeholder="{}"><br />
            <button id="sender" onclick="send_data()">Create Flashcard</button>
    </div>
    <button onclick="api_caller()">GET request</button>
    """.format(languages_available[selected_lang.split('-')[0]].encode('utf-8'), languages_available[selected_lang.split('-')[1]].encode('utf-8'))

html_end = """
    </body>
    </html>"""

if form.has_key("links"):
    data = form["links"].value
    print "Content-Type: text/html" # MODIFY TO SEND JSON DATA AND THEN DESERIALIZE IN JS AND ADD TO DOM
    print
    print "1,2,3,4,5,6,7,8,9,10" #handle_ajax(data)

elif form.has_key("eng") and form.has_key("rus") and form.has_key("url"): # HANDLE POST AJAX - INSERT DATA
    d = form["eng"].value
    d2 = form["rus"].value
    d3 = form["url"].value
    insert_trans(db_name, table, d, d2, d3)

else:
    print html_start
    print html_end
