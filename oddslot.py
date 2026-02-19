from cmath import cos
from csv import DictReader, writer
import csv
import datetime
from lib2to3.pgen2 import driver
import random
import string
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
from datetime import date
from lxml import etree
import kbt_funtions
from consts import global_consts as gc


date_ = gc.PRESENT_DAY_YMD
p_date =  gc.PRESENT_DAY_YMD




csv_f = gc.VIP_CSV

import re
from datetime import datetime, time


def is_allowed_match_time(time_str):
    """
    Allow ONLY 05:30 → 22:29
    Input may contain 'GMT'
    """

    if not time_str:
        return False

    # 🔹 Extract HH:MM ONLY (strip GMT or any text)
    match = re.search(r'(\d{1,2}:\d{2})', time_str)
    if not match:
        return False

    try:
        match_time = datetime.strptime(match.group(1), "%H:%M").time()
    except ValueError:
        return False

    # ❌ BLOCK 22:30 → 05:29
    if match_time >= time(22, 30) or match_time < time(5, 30):
        return False

    return True



def post_tips():
    session = requests.Session()
    my_headers = gc.MY_HEARDER
    url = "https://oddslot.com/tips/?page="
    dt = []
    first_item = True  # Only the first match across all pages gets 'free'
    free_limit = 2  # how many items should be marked as 'free'

    for page in range(1, 10):
        webpage = requests.get(url + str(page), headers=my_headers)
        spider = soup(webpage.content, "html.parser")
        dom = etree.HTML(str(spider))

        for x in range(0, 10):
            i = str(1 + x)

            try:
                league = dom.xpath(f'/html/body/div[2]/div[4]/div/div/div/div/div[2]/div/table/tbody/tr[{i}]/td[4]/strong')[0].text
                timez = dom.xpath(f'/html/body/div[2]/div[4]/div/div/div/div/div[2]/div/table/tbody/tr[{i}]/td[1]/strong')[0].text
             
                # ⏱ Allow only matches between 05:00 – 22:00
                if not is_allowed_match_time(timez):
                    continue


                picks = dom.xpath(f'/html/body/div[2]/div[4]/div/div/div/div/div[2]/div/table/tbody/tr[{i}]/td[7]/strong')[0].text
                home_teams = dom.xpath(f'/html/body/div[2]/div[4]/div/div/div/div/div[2]/div/table/tbody/tr[{i}]/td[2]/div/div/a/h4/strong')[0].text
                away_teams = dom.xpath(f'/html/body/div[2]/div[4]/div/div/div/div/div[2]/div/table/tbody/tr[{i}]/td[3]/div/div/a/h4/strong')[0].text
                odds = float(dom.xpath(f'/html/body/div[2]/div[4]/div/div/div/div/div[2]/div/table/tbody/tr[{i}]/td[6]/a/strong')[0].text)
                rates = dom.xpath(f'/html/body/div[2]/div[4]/div/div/div/div/div[2]/div/table/tbody/tr[{i}]/td[5]/strong')[0].text

                result_text = dom.xpath(f'/html/body/div[2]/div[4]/div/div/div/div/div[2]/div/table/tbody/tr[{i}]/td[8]/a')[0].text
                if result_text.find("NOT STARTED") == -1:
                    continue
                else:
                    results = "?"
                    score = "?:?"
                # Assign 'free' to the first two items
                
                protip = 'free' if free_limit > 0 else 'premium'
                if free_limit > 0:
                    free_limit -= 1

                source = "vip_tips"
                flag = ""
                league_logo = ""
                league_flag = ""
                home_flag = ""
                away_flag = ""
                match_date = p_date
                _date = p_date
                match_code = kbt_funtions.get_code(8)

                prediction = [
                    league,
                    home_teams + ' vs ' + away_teams,
                    picks,
                    odds,
                    timez,
                    score,
                    match_date,
                    _date,
                    flag,
                     league_logo ,
                league_flag ,
                home_flag ,
                away_flag ,
                    results,
                    match_code,
                    source,
                    protip
                ]
                dt.append(prediction)

            except Exception as e:
                print(f"Error on item {i}: {e}")
                continue

    # Shuffle and select
    random.shuffle(dt)
    selected_list = dt[:20]


    # Write to CSV
    with open(csv_f, "w", encoding="utf-8", newline="") as f:
        thewriter = writer(f)
        free_assigned = 0  # Counter for how many 'free' tags we've used

        for sublist in selected_list:
            if kbt_funtions.check_odd_range(sublist[3]):
                if free_assigned <= 2:
                    sublist[12] = 'free'
                    free_assigned += 1
                else:
                    sublist[12] = 'premium'

                sublist[3] = round(sublist[3] + 0.04, 2)
                match_list = [str(value) for value in sublist]
                thewriter.writerow(match_list)
                print(match_list)




def run():
    post_tips()



if __name__ == "__main__":
     run()
