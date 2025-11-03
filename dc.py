from cmath import cos
from csv import DictReader, writer
import csv
import datetime
from lib2to3.pgen2 import driver
import pprint
from pydoc import stripid
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
import kbt_load_env
from consts import global_consts as gc
import kbt_funtions
import requests
from bs4 import BeautifulSoup as soup
from csv import writer
import logging


global csv_data
csv_f = gc.SAFE_BET_DC_CSV

session = requests.Session()
my_headers = gc.MY_HEARDER
dt = []

p_date = gc.PRESENT_DAY_DMY
# calculating end date by adding 4 days
x_date = gc.YESTERDAY_DATE

country_list = gc.COUNTRIES

print(p_date)



# Set up logging to capture errors
logging.basicConfig(filename='error_log.txt', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


# Define headers for the request (ensure this is correctly set in your environment)
my_headers = gc.MY_HEARDER


# Set your headers and CSV file name here
MY_HEADER = {"User-Agent": "Mozilla/5.0"}



def get_today_prediction(set_date):
    url = "https://www.safertip.com/double-chance"
 

    try:
        # Fetch the webpage content
        webpage = requests.get(url, headers=my_headers)
        webpage.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch the webpage: {e}")
        return  # Exit the function if we can't fetch the webpage

    try:
        # Parse the webpage content with BeautifulSoup
        bs = soup(webpage.content, "html.parser")
    except Exception as e:
        logging.error(f"Failed to parse the webpage content: {e}")
        return  # Exit the function if parsing fails

    try:
        # Find all div elements with class 'tableBox'
        tables = bs.find_all("div", {"class": "col-md-9"})
        limited_tables = tables[:4]  # Limit to first four divs containing tables

        # Check if any tables were found
        if not limited_tables:
            print("No 'col-md-9' divs found.")
            return

        # Loop through the first four 'tableBox' divs
        for index, table_box in enumerate(limited_tables):
            print(f"\nExtracting data from table {index + 1}:")

            # Find the table within the div
            table = table_box.find('table')

            # Check if a table is found inside the current div
            if not table:
                print("No table found within this tableBox.")
                continue

            # Find all rows in the table
            rows = table.find_all('tr')

            # Loop through each row and extract specific columns
            for row_index, row in enumerate(rows[:10]):
                # Find all cells in the current row (both <td> and <th>)
                cells = row.find_all(['td', 'th'])

                # Check if the row contains the expected number of cells (at least 7)
                if len(cells) >= 4:
                    # Extract the specific columns by index
                    
                    league_value = cells[0].get_text(strip=True)
                    league_prefix = league_value [:3].upper()  # Extract first 3 letters and convert to uppercase
                    # Find matching country
                    matching_country = next((c for c in country_list if c["2_code"] == league_prefix or c["3_code"] == league_prefix), None)
                    if matching_country:
                        league = matching_country["name"] 
                        flag = matching_country["2_code"] 

                    else:
                        league = league_value
                        flag = ''




                    time = cells[1].get_text(strip=True)
                    adjusted_time = kbt_funtions.adjust_to_gmt(time)
                    fixtures = cells[2].get_text(strip=True).replace("Vs", " vs ")
                    tip = cells[3].get_text(strip=True)
                    odd_text = cells[4].get_text(strip=True)

                    try:
                        # Convert odd to float and filter by odds >= 1.20
                        odd = float(odd_text)
                        if odd >= 1.15:
                            score = 'N/A'
                            result = 'N/A'
                            source = 'safertip_dc'
                            match_date = set_date
                            
                            match_code = kbt_funtions.get_code(8)
                            final_odd = odd_text

                            # Append the data to the list
                            prediction = [
                                league, fixtures, tip, final_odd, adjusted_time,
                                score, match_date, flag, result, match_code, source
                            ]
                            dt.append(prediction)
                    except ValueError:
                        print(f"Skipping row with invalid odd value: {odd_text}")

    except Exception as e:
        logging.error(f"Failed to find match elements on the page: {e}")
        return  # Exit the function if we can't find match elements

    try:
        # Write the extracted data to a CSV file
        with open(csv_f, "w", encoding="utf8", newline="") as f:
            thewriter = writer(f)
            thewriter.writerows(dt)
    except Exception as e:
        logging.error(f"Error writing to CSV file: {e}")

    # Print the collected data
    print(dt)

def connect_server():
    #NOTE::::::::::::when i experience bad connection: 10458 (28000) in ip i browse my ip address and paste it inside cpanel add host then copy my cpanel sharedhost ip
    # and paste here as my host ip address
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


        cursor.execute('DELETE t1 FROM soccerpunt AS t1 INNER JOIN soccerpunt AS t2 WHERE t1.id < t2.id AND t1.fixtures = t2.fixtures AND t1.tip = t2.tip AND t1.source = t2.source')

            
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



    
def run():
    get_today_prediction(p_date)

   
    connect_server()


if __name__ == "__main__":
    run()