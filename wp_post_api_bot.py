import datetime
import requests
import json
import base64
from cmath import cos
from csv import DictReader, writer
import csv
from lib2to3.pgen2 import driver
import random
import string
import requests
import time
import io
import mysql.connector
from mysql.connector import errorcode
from datetime import datetime
from datetime import timedelta
from datetime import date
import kbt_load_env
import kbt_funtions
import consts.global_consts as gc

#posting into wp
def wp_post(**post_dict):
   
    tip_category = post_dict["tips_category"]
    tip_note = post_dict["category_note"]
    source_name = post_dict["source_name"]
    more_tips_link = post_dict["more_tips_link"]
    post_title = post_dict["post_title"]

    try:
        #open db connection
        connection = kbt_funtions.db_connection()
       
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)

            cursor.execute(f'SELECT league, fixtures, tip, date FROM soccerpunt WHERE source = "{source_name}" AND date = "{gc.MYSQL_DATE}" ORDER BY id DESC LIMIT 4')
            my_results = cursor.fetchall()
            html = ''

            for key, value in enumerate(my_results):

                html += f'<tr><td>{value[3]}</td><td>{value[0]}</td><td>{value[1]}</td><td>{value[2]}</td></tr>'
            
            print(html)
    except mysql.connector.Error as err:

        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password ", err)
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print("Error while connecting to MySQL", err)

    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.commit()
            connection.close()
            
            print("MySQL connection is closed")

    post = {
    'title'    : f'{post_title}',
    'status'   : 'publish', 
    'content'  : f'{gc.WP_WELCOME_NOTE}'
    
    '<div">'
                    '<div class="table-responsive single-intro-inner style-2 text-center">'
                        '<table class="table table-striped">'
                        f'<h4 class="title">{post_title}</h4>'
                                    '<thead>'
                                    '<tr>'
                                    
                                        '<th>Date/Time</th>'
                                        '<th>League</th>'
                                        '<th>Fixtures</th>'
                                        '<th>Tip</th>'

                                    '</tr>'
                                    '</thead>'
                                    f'<tbody>{html}'
                                        
                                    '</tbody>'
                                    '</table>'
                                    f'<a class="btn btn-base" href="{more_tips_link}">Load more...<i class="fas fa-arrow-alt-circle-right ms-2"></i></a>'
                                            '</div>'
                                        '</div>'
                                        f'{gc.WP_JOIN_TELEGRAM_NOTE}'
                                        f'{tip_note}'
                                        f'{gc.WP_COMMENT_NOTE}',
                                     'date'   : f'{gc.WP_POST_DATE}',
                                    'categories' : ['4', '185', f'{tip_category}'],
                                    'tags' : ['63', '7', '66', '125', '127','53', '54', '153', '4', '16','14', '15', '51', '6', '11','52', '56', '58', '59', '57']
    }

    r = requests.post(gc.WP_LIVE_URL, headers=gc.WP_HEADER, json=post)
    print(r)