from csv import writer
import random

import kbt_funtions
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
from datetime import datetime


date_ = gc.PRESENT_DAY_DATE
p_date = gc.YESTERDAY_DATE

csv_f = gc.CORNERS_CSV

additional_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com",
    "Connection": "keep-alive"
}

my_headers = gc.MY_HEARDER

country_name = gc.COUNTRIES

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

headers_list = [
   {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.2 Safari/605.1.15", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edg/91.0.864.59", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edg/92.0.902.55", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edg/93.0.961.38", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.818.62 Safari/537.36 Edg/90.0.818.62"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7; rv:88.0) Gecko/20100101 Firefox/88.0"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15"},
    {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0"},
    {"User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G970F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Mobile Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Android 10; Mobile; rv:88.0) Gecko/88.0 Firefox/88.0" },
    {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1" },
    {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Mobile Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"}

   
]

additional_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com",
    "Connection": "keep-alive"
}

def get_random_headers():
    return {**random.choice(headers_list), **additional_headers}

def get_country_name_from_code(img_code, countries):
    for country in countries:
        if img_code.lower() == country["2_code"].lower() or img_code.lower() == country["3_code"].lower():
            return country["name"]
    return ""

def scrape_corners_data(set_date):
    all_rows = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        headers = get_random_headers()

        context = browser.new_context(
            user_agent=headers.get("User-Agent"),
            locale="en-US",
            extra_http_headers=headers
        )

        page = context.new_page()
        page.goto(f"https://www.forebet.com/en/football-predictions/corners/{set_date}")
        page.wait_for_selector("h1.frontH", timeout=60000)
        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")
    games = soup.select(".rcnt")
    print(f"Found {len(games)} games.")

    # ✅ Limit to 50 games
    for i, game in enumerate(games):
        if i >= 50:
            break

        try:
            league = game.select_one(".shortTag")
            home = game.select_one(".homeTeam span")
            away = game.select_one(".awayTeam span")
            date_ = game.select_one(".date_bah")
            prob1 = game.select_one(".fprc span:nth-of-type(1)")
            prob2 = game.select_one(".fprc span:nth-of-type(2)")
            predict_div = game.select_one("div[class^='predict']")  # Match predict, predict_y, predict_no

            # Get prediction value
            pred = predict_div.get_text(strip=True) if predict_div else "N/A"

            # Determine result based on class name
            result = "N/A"
            if predict_div and "class" in predict_div.attrs:
                class_list = predict_div["class"]
                if "predict_y" in class_list:
                    result = "Won"
                elif "predict_no" in class_list:
                    result = "Lost"

       # ✅ Extract final score safely
            score_div = game.select_one("div.lscr_td")
            if score_div:
                score_tag = score_div.select_one("b.l_scr")
                final_score = score_tag.get_text(strip=True) if score_tag else "N/A"
            else:
                final_score = "N/A"


            avg_points = game.select_one(".avg_sc")

            img_tag = game.select_one('div.shortagDiv.tghov img')
            img_link = img_tag['src'] if img_tag else ""
            img_code = img_link.split('/')[-1].split('.')[0] if img_link else ""
            flag_name = get_country_name_from_code(img_code, country_name)


            a_tag = game.select_one("a.tnmscn")
         
            if a_tag and a_tag.has_attr("href"):
                href = a_tag["href"]
                path_parts = href.strip("/").split("/")
                league_slug = path_parts[3] if len(path_parts) > 4 else ""
                fixtures_link = f"https://www.forebet.com{href}" if href else ""
                print(league_slug)
            else:
                league_slug = ""
                fixtures_link = ""

             # Find the flag div
            short_div = game.select_one(".shortagDiv.tghov")
            league_slug = ""
            flag_name = ""

            if short_div:
                img_tag = short_div.select_one("img")
                if img_tag and img_tag.has_attr("onclick"):
                    onclick_text = img_tag["onclick"]
                    # Extract the URL part: 'football-tips-and-predictions-for-paraguay/primera-division'
                    import re
                    match = re.search(r"'football-tips-and-predictions-for-[^']*?/([^']+)'", onclick_text)
                    if match:
                        league_slug = match.group(1).strip()  # → 'primera-division'

                    # Extract the flag name from img src
                    img_link = img_tag["src"]
                    img_code = img_link.split("/")[-1].split(".")[0] if img_link else ""
                    flag_name = get_country_name_from_code(img_code, country_name)

            # ✅ Optional: also keep .shortTag text if needed
            league_tag = game.select_one(".shortTag")
            league_display = league_slug or (league_tag.text.strip() if league_tag else "")
            print(league_display)
            home = home.text.strip() if home else "N/A"
            away = away.text.strip() if away else "N/A"

            # ✅ Parse date and time safely
            date_time_str = date_.text.strip() if date_ else "N/A"
            if date_time_str != "N/A":
                try:
                    dt = datetime.strptime(date_time_str, "%d/%m/%Y %H:%M")
                    date_only = dt.strftime("%d-%m-%Y")
                    time_only = dt.strftime("%H:%M")
                except ValueError:
                    date_only = "N/A"
                    time_only = "N/A"
            else:
                date_only = "N/A"
                time_only = "N/A"

            prob1 = prob1.text.strip() if prob1 else "N/A"
            prob2 = prob2.text.strip() if prob2 else "N/A"
            avg_points = avg_points.text.strip() if avg_points else "N/A"
            code = kbt_funtions.get_code(8)

            row = [
                league_display,
                f"{home} vs {away}",
                pred,
                "",                     # odd
                time_only,              # match_time
                final_score,
                date_only,
                f"{flag_name} - {img_code}",
                result,
                code,
                "fb_cornerkicks",
                f"{prob1} - {prob2}",
                avg_points,
                final_score,
                fixtures_link,
                league_slug,
            ]

            all_rows.append(row)

        except Exception as e:
            print("Error parsing game:", e)

    print(f"✅ Returning {len(all_rows)} games (max 50).")
    return all_rows


def save_to_csv(rows):
    with open(csv_f, "w", newline="", encoding="utf-8") as f:
        writer_ = csv.writer(f)
        writer_.writerow([
            "league", "fixtures", "tip", "odd", "match_time", "score", "date",
            "flag", "result", "code", "source", "rate", "avg_point","correct_score" ,"fixtures_link, league_slug"
        ])
        writer_.writerows(rows)
    print(f"Saved {len(rows)} rows to {csv_f}")



def post_to_mysql():
    # #insert into db

    # csv_f = "oddslot_data.csv"
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
                if len(row) == 16:
                    cursor.execute(
                        'INSERT INTO corners (league, fixtures, tip, odd, match_time, score, date, flag, result, code, source,rate, avg_point,correct_score,fixtures_link, league_slug)'
                        'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                        row
                    )
                else:
                    print(f"Skipping row with incorrect number of values: {row}")

               

        print("Inserting tips now... ", time.ctime())
        print(cursor.rowcount," record(s) created==============", time.ctime())

        
        time.sleep(3) 
        print("==============Bot is taking a nap... whopps!==================== ", time.ctime())  
        print("============Bot deleting previous tips from  database:=============== ")


        cursor.execute('DELETE t1 FROM corners AS t1 INNER JOIN corners AS t2 WHERE t1.id < t2.id AND t1.fixtures = t2.fixtures AND t1.source = t2.source')

            
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


def main():
    print(p_date)
    rows = scrape_corners_data(p_date)
    if rows:
        save_to_csv(rows)
        post_to_mysql()
    else:
        print("No games found or something went wrong.")


if __name__ == "__main__":
    main()
