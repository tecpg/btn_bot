import random
import requests
import time
import csv
import json
import logging
from bs4 import BeautifulSoup
from consts import global_consts as gc

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set date
set_date = gc.PRESENT_DAY_DATE

# Headers
headers_list = [  # shortened for brevity
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ..."}
    # ... include the rest of your headers here
]
additional_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com",
    "Connection": "keep-alive"
}
headers = {**random.choice(headers_list), **additional_headers}

# URL
base_url = (
    "https://convertbetcodes.com/c/free-predictions?"
    "team=&sports=soccer&markets%5B%5D=over_under&"
    "odds_range%5Bstart%5D=1.0&odds_range%5Bend%5D=2.0&"
    f"playing={set_date}&popularity=1&sport=1&page="
)
# Fetch & parse page
response = requests.get(base_url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# Parse predictions
predictions = []

for page in range(1, 4):  # Pages 1 to 3
    url = f"{base_url}{page}"
    headers = {**random.choice(headers_list), **additional_headers}

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        for item in soup.find_all('li', class_='list-item'):
            try:
                league = item.select_one('.media-body p:nth-of-type(1)').get_text(strip=True).split(' ', 1)[-1]
                match = item.select_one('.media-body p:nth-of-type(2)').get_text(strip=True)
                prediction_line = item.select_one('.media-body p:nth-of-type(3)').get_text(strip=True)

                if ':' in prediction_line:
                    pred_type, tip = map(str.strip, prediction_line.split(':', 1))
                else:
                    pred_type, tip = prediction_line, ''

                date_tag = item.select_one('span.badge')
                match_time = date_tag.get_text(strip=True) if date_tag else 'N/A'

                odd_tag = item.select_one('small.badge')
                odd = ''
                if odd_tag:
                    odd_text = odd_tag.get_text(strip=True)
                    odd = odd_text.replace('odd:', '').strip()

                if not odd or odd.upper() == 'N/A':
                    continue

                predictions.append({
                    'league': league,
                    'match': match,
                    'prediction_type': pred_type,
                    'tip': tip,
                    'date': match_time,
                    'odd': odd,
                })

            except Exception as e:
                logger.warning(f"Error parsing item on page {page}: {e}")

        # Sleep between page requests
        sleep_time = random.uniform(1, 3)
        logger.info(f"Sleeping for {sleep_time:.2f} seconds before next page...")
        time.sleep(sleep_time)

    except Exception as e:
        logger.error(f"Failed to fetch page {page}: {e}")
# Print results
for p in predictions:
    print(p)

# Optional: sleep to mimic human browsing (though not needed here since 1 request)
sleep_time = random.uniform(1, 3)
logger.info(f"Sleeping for {sleep_time:.2f} seconds after scraping.")
time.sleep(sleep_time)

# Export to CSV
csv_filename = f"smart_odds_{set_date}.csv"
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    fieldnames = ["league", "match", "prediction_type", "tip", "date", "odd"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(predictions)
logger.info(f"Results saved to {csv_filename}")

# Export to JSON
json_filename = f"smart_odds_{set_date}.json"
with open(json_filename, 'w', encoding='utf-8') as f:
    json.dump(predictions, f, ensure_ascii=False, indent=4)
logger.info(f"Results also saved to {json_filename}")
