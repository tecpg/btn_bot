import requests
import random
from bs4 import BeautifulSoup

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



# URL of the page to scrape
url = 'https://www.ukclubsport.com/football/predictions/'

# Rotating user-agent headers
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

# Make the request
response = requests.get(url, headers=get_random_headers())
if response.status_code != 200:
    print(f"Failed to retrieve page: Status code {response.status_code}")
    exit()

# Parse HTML
soup = BeautifulSoup(response.text, 'lxml')
cards = soup.select('.prediction-card')
matches = []

for card in cards:
    try:
        title_tag = card.select_one('.prediction-card__header-match')
        match_title = title_tag.text.strip()
        match_url = 'https://www.ukclubsport.com' + title_tag['href']

        header_text = card.select_one('.prediction-card__header-text')
        date_time = header_text.contents[0].strip()
        competition = header_text.select_one('span').text.strip()

        strength_tags = card.select('.prediction-card__item')

        # Team 1 info, rate, and flag
        team1_block = strength_tags[0]
        team1_info = team1_block.text.strip()
        team1_rate = team1_block.select_one('span').text.strip()
        team1_img = team1_block.select_one('img')
        team1_flag = team1_img['src'] if team1_img else None
        if team1_flag and team1_flag.startswith('/'):
            team1_flag = 'https://www.ukclubsport.com' + team1_flag

        # Team 2 info, rate, and flag
        team2_block = strength_tags[1]
        team2_info = team2_block.text.strip()
        team2_rate = team2_block.select_one('span').text.strip()
        team2_img = team2_block.select_one('img')
        team2_flag = team2_img['src'] if team2_img else None
        if team2_flag and team2_flag.startswith('/'):
            team2_flag = 'https://www.ukclubsport.com' + team2_flag

        result_prediction = card.select_one('.prediction-card__footer-text').text.strip()
        odds = card.select_one('.ratio__count').text.strip()
        bookmaker_img = card.select_one('.ratio__logo img')
        bookmaker = bookmaker_img['alt'] if bookmaker_img else 'Unknown'

        matches.append({
            'fixture': match_title,
            'date_time': date_time,
            'competition': competition,
            'team1_rate': team1_rate,
            'team2_rate': team2_rate,
            'team1_info': team1_info,
            'team2_info': team2_info,
            'team1_flag': team1_flag,
            'team2_flag': team2_flag,
            'prediction': result_prediction,
            'odds': odds,
            'bookmaker': bookmaker,
            'url': match_url
        })

    except Exception as e:
        print(f"Error processing a card: {e}")

# Display results
for match in matches:
    print(match)


import csv

# Define CSV file name
csv_filename = 'ukclubsport_predictions.csv'

# Define the CSV column order
fieldnames = [
    'fixture',
    'date_time',
    'competition',
    'team1_rate',
    'team2_rate',
    'team1_info',
    'team2_info',
    'team1_flag',
    'team2_flag',
    'prediction',
    'odds',
    'bookmaker',
    'url'
]

# Write to CSV
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for match in matches:
        writer.writerow(match)

print(f"✅ Data has been written to '{csv_filename}' successfully.")


def post_to_mysql():
    csv_f = "ukclubsport_predictions.csv"  # Use the file from the scraping step

    try:
        connection = kbt_funtions.db_connection()
        
        if connection.is_connected():
            print("✅ Connected to MySQL Server")
            cursor = connection.cursor()

        # 🧹 Delete all previous data first
        cursor.execute("TRUNCATE TABLE top_match;")
        print("✅ All previous data removed.")

        with open(csv_f, "r", encoding="utf-8") as f:
            csv_data = csv.reader(f)
            headers = next(csv_data)  # Skip header row

            for row in csv_data:
                if len(row) == 13:
                    cursor.execute(
                        '''
                        INSERT INTO top_match (
                            fixture,
                            date_time,
                            competition,
                            team1_rate,
                            team2_rate,
                            team1_info,
                            team2_info,
                            team1_flag,
                            team2_flag,
                            prediction,
                            odds,
                            bookmaker,
                            url
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ''',
                        row
                    )
                else:
                    print(f"⚠️ Skipping row with incorrect number of values: {row}")

        print("✅ Inserting tips... ", time.ctime())
        print(f"{cursor.rowcount} record(s) inserted.", time.ctime())

    except mysql.connector.Error as err:
        print("❌ MySQL Error:", err)

    finally:
        if connection and connection.is_connected():
            connection.commit()
            cursor.close()
            connection.close()
            print("✅ MySQL connection closed.")




def main():

        post_to_mysql()


if __name__ == "__main__":
    main()
