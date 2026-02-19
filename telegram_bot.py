import csv
import requests
import mysql.connector
from datetime import datetime
from consts import global_consts as gc
import kbt_funtions

csv_f = gc.TELEGRAM_BOT_CSV
_date = gc.YESTERDAY_YMD  # Change to any date you need


def result_to_emoji(result):
    if not result:
        return "⏳"  # missing / not updated
    r = result.strip().lower()
    if r == "won":
        return "✅"
    elif r in ("lost", "lose"):
        return "❌"
    elif r in ("void", "refund"):
        return "♻️"
    elif r in ("pending", "Not Yet"):
        return "⏳"
    else:
        return "❔"


def connect_server():
    connection = None
    cursor = None

    try:
        connection = kbt_funtions.db_connection()

        if not connection.is_connected():
            print("Database connection failed")
            return

        cursor = connection.cursor()

        query = """
     SELECT league, fixtures, tip, odd, match_time, match_date, result, score
         FROM soccerpunt
         WHERE source = 'vip_tips_2'
           AND match_date = %s
         ORDER BY id DESC
         LIMIT 15
        """

        cursor.execute(query, (_date,))

        results = cursor.fetchall()

        if not results:
            print("No predictions found.")
            return

        headers = [col[0] for col in cursor.description]

        with open(csv_f, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(results)

        print("CSV updated:", csv_f)

    except mysql.connector.Error as err:
        print("Database error:", err)

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def post():
    tips = []

    try:
        with open(csv_f, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)  # skip header

            for row in reader:
                tips.append([
                    row[1],  # fixture
                    row[0],  # league
                    row[3],  # odd
                    row[2],  # tip
                    row[4],  # time
                    row[5],  # date
                    row[6],  # result
                    row[7]   # score
                ])

    except FileNotFoundError:
        print("CSV file not found.")
        return

    if not tips:
        print("No tips to post.")
        return

    predictions = tips[:20]

    # Calculate win rate
    total = len(predictions)
    wins = sum(1 for x in predictions if x[6] and x[6].strip().lower() == "won")
    win_rate = (wins / total) * 100 if total else 0

    # Date formatting
    raw_date = predictions[0][5]
    if not raw_date:
        print("Missing match_date")
        return

    date_obj = datetime.strptime(raw_date, "%Y-%m-%d")
    day = date_obj.day
    if 11 <= day <= 13:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
    formatted_date = f"{day}{suffix} {date_obj.strftime('%B %Y')}"

    # Celebration or try-again headline
    if win_rate >= 80:
        headline = (
            f"🎉🔥 <b>AMAZING PERFORMANCE!</b> 🔥🎉\n"
            f"✅ Win Rate: <b>{win_rate:.0f}%</b>\n\n"
        )
    else:
        headline = (
            f"😔🔄 <b>WE GO AGAIN!</b> 🔄😔\n"
            f"📊 Win Rate: <b>{win_rate:.0f}%</b>\n\n"
        )

    post_tips = headline + f"📅 <b>Date:</b> {formatted_date}\n\n"

    # Add each prediction in smaller bold format
    for x in predictions:
        emoji = result_to_emoji(x[6])
        post_tips += (
            f"{x[1]}\n"                     # League
            f"<b>{x[0]}</b>\n"             # Fixture bold
            f"Tip: <b>{x[3]}</b> | Odd: {x[2]}\n"
            f"Time: {x[4]} | Score: {x[7]}\n"
            f"Result: {emoji} <b>{x[6]}</b>\n\n"
        )

    # Message links
    message_text = "🔥 Winning KBT FREE Telegram Tips (PROOF)"
    link_1 = "👉 Subscribe: https://kingsbettingtips.com/vip-subscriptions/"
    link_2 = "💬 Need help? <a href='https://t.me/btnhelp'>Contact Support</a>"

    full_message = f"{message_text}\n\n{post_tips}{link_1}\n{link_2}"

    payload = {
        "chat_id": gc.CHANNEL_CHAT_ID,
        "text": full_message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }

    response = requests.post(
        gc.TELEGRAM_BASE_URL + "sendMessage",
        data=payload,
        timeout=10
    )

    if response.status_code == 200:
        print("Telegram message sent successfully")
    else:
        print("Telegram error:", response.text)


def run():
    connect_server()
    post()


if __name__ == "__main__":
    run()
