from cmath import cos
from csv import DictReader, writer
import csv

import datetime
from lib2to3.pgen2 import driver
import pprint
from pydoc import stripid

import traceback
from unittest import result
from urllib import request
import requests
from bs4 import BeautifulSoup as soup
import time
from wsgiref import headers
# importing webdriver from selenium
import requests
import os
import time
import io
import requests
import mysql.connector
from mysql.connector import errorcode

from lxml import etree
from datetime import datetime
from datetime import timedelta
from datetime import date
from wp_post_api_bot import wp_post
import kbt_load_env
from consts import global_consts as gc
import kbt_funtions


global csv_data
csv_f = gc.TIPSBET_CSV

session = requests.Session()
my_headers = gc.MY_HEARDER
dt = []


# taking input as the current date
# today() method is supported by date
# class in datetime module

date_ = date.today()
p_date = gc.PRESENT_DAY_DMY

x_date = date_- timedelta(days=1)
x_date = gc.YESTERDAY_DMY

# print(x_date, p_date)

bs = soup

import requests
from bs4 import BeautifulSoup as bs
from lxml import etree
import csv
import traceback
from datetime import date

def get_today_prediction(bs, set_date):
    url = f"https://tipsbet.co.uk/free-betting-tips-{set_date}/"

    try:
        # Get the web page content
        webpage = requests.get(url, headers=my_headers)
        webpage.raise_for_status()  # Raises an HTTPError for bad responses
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch the webpage: {e}")
        traceback.print_exc()
        return

    try:
        # Parse the page content with BeautifulSoup
        soup = bs(webpage.content, "html.parser")
        # Convert the BeautifulSoup object to a lxml etree
        dom = etree.HTML(str(soup))
    except Exception as e:
        print(f"Failed to parse the webpage content: {e}")
        traceback.print_exc()
        return

    try:
        # Get table row count for the tr loop
        tables = soup.findChildren('table')
        if not tables:
            print("No tables found on the page.")
            return

        # Assume the first table contains the relevant data
        web_table = tables[0]
        rows = web_table.findChildren(['tr'])
        tr_count = len(rows)
        print("Table has", tr_count - 1, "rows")
    except Exception as e:
        print(f"Failed to process the table: {e}")
        traceback.print_exc()
        return

    try:
        # Open CSV file
        with open(csv_f, "w", encoding="utf8", newline="") as f:
            thewriter = csv.writer(f)
          

            for x in range(2, tr_count - 2):
                c = x
                i = str(c)

                try:
                    league = dom.xpath(f'//*[@id="table-tipsbet"]/tbody/tr[{i}]/td[5]/strong/span/span/span/span')
                    league = league[0].text if league else ''

                    timez = dom.xpath(f'//*[@id="table-tipsbet"]/tbody/tr[{i}]/td[1]/strong/span')
                    timez = timez[0].text if timez else ''

                    match = dom.xpath(f'//*[@id="table-tipsbet"]/tbody/tr[{i}]/td[6]/strong')
                    match = match[0].text.replace("–", "VS") if match else ''

                    picks = dom.xpath(f'//*[@id="table-tipsbet"]/tbody/tr[{i}]/td[7]/strong/span')
                    picks = picks[0].text if picks else ''

                    odds = dom.xpath(f'//*[@id="table-tipsbet"]/tbody/tr[{i}]/td[8]/strong/span')
                    odds = odds[0].text if odds else ''

                    flag = dom.xpath('//*[@id="system"]/div/div/div[1]/h3/strong/span')
                    flag = flag[0].text if flag else ''

                    match_date = date.today().strftime('%Y-%m-%d')
                    match_code = kbt_funtions.get_code(8)  # Assuming this function is defined elsewhere
                    source = "tipsbet_combo_tips"
                    score = "N/A"

                    prediction = [
                        league,
                        kbt_funtions.remove(match),  # Assuming this function is defined elsewhere
                        picks,
                        odds,
                        kbt_funtions.remove(timez),  # Assuming this function is defined elsewhere
                        score,
                        match_date,
                        flag,
                        "N/A",
                        match_code,
                        source
                    ]
                    dt.append(prediction)

                except Exception as e:
                    print(f"Error processing row {i}: {e}")
                    traceback.print_exc()
                    continue  # Skip this row and continue with the next

            thewriter.writerows(dt)
            print(dt)

    except Exception as e:
        print(f"An error occurred while writing to CSV: {e}")
        traceback.print_exc()


def get_previous_prediction(nbs, set_previous_date):
    url = f"https://tipsbet.co.uk/free-betting-tips-{set_previous_date}/"

    try:
        # Get the web page content
        webpage = requests.get(url, headers=my_headers)
        webpage.raise_for_status()  # Raises an HTTPError for bad responses
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch the webpage: {e}")
        traceback.print_exc()
        return

    try:
        # Parse the page content with BeautifulSoup
        soup = nbs(webpage.content, "html.parser")
        # Convert the BeautifulSoup object to a lxml etree
        dom = etree.HTML(str(soup))
    except Exception as e:
        print(f"Failed to parse the webpage content: {e}")
        traceback.print_exc()
        return

    try:
        # Get table row count for the tr loop
        tables = soup.findChildren('table')
        if not tables:
            print("No tables found on the page.")
            return

        # Assume the first table contains the relevant data
        web_table = tables[0]
        rows = web_table.findChildren(['tr'])
        tr_count = len(rows)
        print("Table has", tr_count - 1, "rows")
    except Exception as e:
        print(f"Failed to process the table: {e}")
        traceback.print_exc()
        return

    try:
        # Open CSV file
        with open(csv_f, "w", encoding="utf8", newline="") as f:
            thewriter = csv.writer(f)
         

            for x in range(2, tr_count - 3):
                c = 1 + x
                i = str(c)
                print(i)

                try:
                    timez = dom.xpath(f'//*[@id="table-tipsbet"]/tbody/tr[{i}]/td[1]/strong/span')
                    timez = timez[0].text if timez else ''

                    leagues = dom.xpath(f'//*[@id="table-tipsbet"]/tbody/tr[{i}]/td[5]/strong/span/span/span/span')
                    leagues = leagues[0].text if leagues else ''

                    match = dom.xpath(f'//*[@id="table-tipsbet"]/tbody/tr[{i}]/td[6]/strong')
                    match = match[0].text.replace("–", "VS") if match else ''

                    picks = dom.xpath(f'//*[@id="table-tipsbet"]/tbody/tr[{i}]/td[7]/strong/span')
                    picks = picks[0].text if picks else ''

                    odds = dom.xpath(f'//*[@id="table-tipsbet"]/tbody/tr[{i}]/td[8]/strong/span')
                    odds = odds[0].text if odds else ''

                    score = dom.xpath(f'//*[@id="table-tipsbet"]/tbody/tr[{i}]/td[9]/span/strong')
                    score = score[0].text if score else ''

                    flag = dom.xpath('//*[@id="system"]/div/div/div[1]/h3/strong/span')
                    flag = flag[0].text if flag else ''

                    results = dom.xpath(f'//*[@id="table-tipsbet"]/tbody/tr[{i}]/td[9]/span//@style')
                    res = results[0] if results else ''

                    if res.find('#008000') != -1 and score != '?':
                        results = "Won"
                    elif res.find('#ff0000') != -1 and score != '?':
                        results = "Lost"
                    elif score == '?':
                        results = "..."

                    source = "tipsbet_combo_tips"
                    x_date = date.today() - timedelta(days=1)
                    match_date = x_date.strftime('%Y-%m-%d')
                    match_code = kbt_funtions.get_code(8)

                    prediction = [
                        leagues,
                        kbt_funtions.remove(match),
                        picks,
                        odds,
                        kbt_funtions.remove(timez),
                        score,
                        match_date,
                        flag,
                        results,
                        match_code,
                        source
                    ]
                    dt.append(prediction)

                except Exception as e:
                    print(f"Error processing row {i}: {e}")
                    traceback.print_exc()
                    continue  # Skip this row and continue with the next

            thewriter.writerows(dt)

        print(dt)

    except Exception as e:
        print(f"An error occurred while writing to CSV: {e}")
        traceback.print_exc()

#csv_f = "venasbet_data.csv"
def connect_server():
    #NOTE::::::::::::when i experience bad connection: 10458 (28000) in ip i browse my ip address and paste it inside cpanel add host then copy my cpanel sharedhost ip
    #and paste here as my host ip address
    try:
        connection = kbt_funtions.db_connection()

        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()

            print("You're connected to database: ", record)

        
            
        with open(csv_f, "r") as f:
        
            csv_data = csv.reader(f)
            for row in csv_data:
                print(row)
                cursor.execute('INSERT INTO soccerpunt(league,fixtures,tip,odd,match_time,score,date,flag,result,code,source)'\
                    'VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', row)

        print("Inserting tips now... ", time.ctime())
        print(cursor.rowcount," record(s) created==============", time.ctime())


        
        time.sleep(6) 
        print("==============Bot is taking a nap... whopps!==================== ", time.ctime())  
        print("============Bot deleting previous tips from  database:=============== ")
        #NOTE when i encounter Error while connecting to MySQL 1205 (HY000): Lock wait timeout exceeded; try restarting transaction;- i kill 
        #processlist from my software MYSQL WORK BENCH, I LOGIN WITH THE SHARED HOST ;-13..., tutorial from here
        #https://www.youtube.com/watch?v=xQ0z_rPPLDs thanks


        cursor.execute('DELETE t1 FROM soccerpunt AS t1 INNER JOIN soccerpunt AS t2 WHERE t1.id < t2.id AND t1.fixtures = t2.fixtures AND t1.source = t2.source')

            
        print(cursor.rowcount," record(s) deleted==============", time.ctime()) 

    

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


    post_title = 'Win 1X2 Betting Prediction For Today - Daily Free Betting Tips'
  
    tip_category = '189'
    category_note = """ <h4>What is Combo Betting Tips</h4><br>
                Combo betting, also known as multiple or accumulator betting, is a type of bet that involves combining several selections into a single wager. To win a combo bet, all of the individual selections included in the bet must be correct. Combo bets are often attractive to bettors because they offer the potential for larger payouts due to the increased risk involved in predicting the outcome of multiple events. 
                Combo betting tips refer to recommendations or suggestions for combo bets made by experts or individuals with knowledge of the sports or events being bet on. It is important to note that betting tips and recommendations are not a guarantee of success and that all forms of gambling carry inherent risks and uncertainties. 
                It is always important to gamble responsibly and to understand the risks involved. """
    source_name = 'tipsbet_combo_tips'
    more_tips_link = 'combo-betting-tips'

    wp_post(post_title = post_title,
        tips_category = tip_category,
        category_note = category_note,
        source_name  = source_name,
        more_tips_link = more_tips_link)

def run():
  
    get_today_prediction(soup,p_date)
    #time.sleep(6) 
    #print("==============Bot is taking a nap... whopps!==================== ", time.ctime())  
    get_previous_prediction(soup,x_date)
    # #print(get_result("2X","2:2"))
    # # #insert into db
    connect_server()


if __name__ == "__main__":
    run()