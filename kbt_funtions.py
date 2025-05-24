import random
import string
import kbt_load_env
import mysql.connector
from mysql.connector import errorcode

def db_connection():
     #open db connection
    return mysql.connector.connect(host=kbt_load_env.db_host,
                                        database=kbt_load_env.db_dbname,
                                        user=kbt_load_env.db_user,
                                        password=kbt_load_env.db_pwd)
#local mysql connection
        # connection = mysql.connector.connect(host='localhost',
        #                                  database='kingsbet_KBTdb',
        #                                  user='root',
        #                                  password='')
  

def get_code(length):
    letters = string.ascii_lowercase
    r_letters = ''.join(random.choice(letters) for i in range(length))
    numbers =   str(random.randint(2220,333000333))
    code = r_letters+numbers
    return code

def get_betcode_uid():
    numbers =   str(random.randint(2220,333000333))
    code = numbers
    return code

# Python code to remove whitespace
def remove(string):
    return string.replace("\n", "")

def get_result(pick, score):
    try:
        if ':' in score:
            # Score contains ':', indicating it's in the format 'score1:score2'
            s_list = list(map(int, score.split(":")))  # Convert scores to integers for comparison
            if pick == "1X":
                result = "Won" if s_list[0] >= s_list[1] else "Lost"
            elif pick == "2X":
                result = "Won" if s_list[0] <= s_list[1] else "Lost"
            elif pick == "X2":
                result = "Won" if s_list[0] <= s_list[1] else "Lost"
            elif pick == "1":
                result = "Won" if s_list[0] > s_list[1] else "Lost"
            elif pick == "2":
                result = "Won" if s_list[0] < s_list[1] else "Lost"
            elif pick == "12":
                result = "Won" if s_list[0] != s_list[1] else "Lost"
            else:
                result = "..."
        else:
            # Score doesn't contain ':', indicating it's not in the expected format
            result = "..."
    except Exception as e:
        print(e)  # Print the exception for debugging purposes
        result = "..."  # Default result if an exception occurs

    return result



def get_result_by_score(pick, score):
     
     try:
        if any(map(str.isdigit, score)):
            s_list = list(map(int, score.split(":")))
            s_n = sum(s_list)  # Sum of scores

            if '2.5' in pick:
                return "Won" if s_n > 2 else "Lost"
            elif '1.5' in pick:
                return "Won" if s_n >= 2 else "Lost"
            elif '3.5' in pick:
                return "Won" if s_n <= 3 else "Lost"
            elif "2DNB" in pick:
                return "Won" if s_list[0] < s_list[1] or s_list[0] == s_list[1] else "Lost"
            elif "1DNB" in pick:
                return "Won" if s_list[0] > s_list[1] or s_list[0] == s_list[1] else "Lost"
            else:
                return "..."
        else:
            return "..."
     except Exception as e:
        print(e)
        return "..."


def check_odd_range(value):
    return 1.50 <= value <= 4.0



# Function to get a random string from the list

def get_random_rate():
    # Define the list of strings
    odds = ['70', '80', '75', '55', '65', '85', '92', '87', '80', '85', '92', '87', '80']
    return random.choice(odds)

def get_random_odd():
    # Define the list of strings
    odds = ['1.20', '1.25', '1.20', '1.27', '1.30', '1.35', '1.30', '1.40', '1.45']
    return random.choice(odds)

def get_random_odd_over_15():
    # Define the list of strings
    odds = ['1.20', '1.15', '1.20', '1.10', '1.20', '1.15', '1.10', '1.10', '1.25']
    return random.choice(odds)


# Function to get a random string from the list
def get_random_odd_2():
    # Define the list of strings
    odds = ['1.40', '1.25', '1.30', '1.27', '1.40', '1.35', '1.30', '1.40', '1.45']
    return random.choice(odds)

# Function to get a random string from the list
def get_random_odd_3():
    # Define the list of strings
    odds = ['1.40', '1.55', '1.35', '1.40', '1.45', '1.65', '1.50', '1.48', '1.45']
    return random.choice(odds)

# Function to get a random string from the list
def get_random_odd_draws():
    # Define the list of strings
    odds = ['11.40', '8.55', '4.35', '6.40', '3.45', '5.65', '4.50', '3.48', '4.45']
    return random.choice(odds)

# # Example usage
# random_string = get_random_string(odds)

from datetime import datetime, timedelta

def adjust_to_gmt(time_string):
    """
    Adjusts the given time string (in HH:MM format) by subtracting 2 hours
    to convert to GMT.

    Args:
    - time_string (str): The time in "HH:MM" format.

    Returns:
    - str: The adjusted time in "HH:MM" format.
    """
    try:
        # Parse the time string into a datetime object
        original_time = datetime.strptime(time_string, "%H:%M")
        
        # Subtract 2 hours to convert to GMT
        adjusted_time = original_time - timedelta(hours=2)
        
        # Format the adjusted time back to "HH:MM" format
        return adjusted_time.strftime("%H:%M")
    
    except ValueError:
        print("Invalid time format. Please use 'HH:MM'.")
        return None


import json


def get_platforms_json(site_name=None):
    platforms = [
        {"site": "bet9ja", "img": "0xFF097E36"},
        {"site": "betking:ng", "img": "0xFF1D1592"},
        {"site": "1xbet:ng", "img": "0xFF0982EC"},
        {"site": "sportybet:ng", "img": "0xFFFA0909"},
        {"site": "22bet:ng", "img": "0xFF064146"},
        {"site": "betwinner", "img": "0xFF1A654A"},
        {"site": "paripesa", "img": "0xFF05117E"},
        {"site": "megapari", "img": "0xFF383838"},
        {"site": "melbet", "img": "0xFF151515"},
        {"site": "msport", "img": "0xFFFFCA26"},
        {"site": "linebet", "img": "0xFF2E5822"},
        {"site": "betway", "img": "0xFF000000"},
        {"site": "db_bet", "img": "0xFFFF5275"},
    ]

    if site_name:
        # Find platform matching the site_name (case insensitive substring match)
        for platform in platforms:
            if site_name.lower() in platform["site"].lower():
                return platform["img"]
        return None  # Return None if not found

    # If no site_name provided, return full JSON string
    response = {
        "data": {
            "sites": platforms
        }
    }
    return json.dumps(response, indent=4)


