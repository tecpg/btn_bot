import csv
import requests
import mysql.connector
from datetime import datetime
from consts import global_consts as gc
import kbt_funtions

csv_f = gc.TELEGRAM_VIP_BOT_CSV
_date = gc.PRESENT_DAY_YMD  


# =========================
# FETCH VIP TIPS TO CSV
# =========================
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

        print("✅ VIP CSV updated:", csv_f)

    except mysql.connector.Error as err:
        print("Database error:", err)

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


# =========================
# POST TO TELEGRAM VIP CHANNEL
# =========================
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
                ])

    except FileNotFoundError:
        print("CSV file not found.")
        return

    if not tips:
        print("No tips to post.")
        return

    predictions = tips[:15]

    # Date formatting
    raw_date = predictions[0][5]
    date_obj = datetime.strptime(raw_date, "%Y-%m-%d")
    day = date_obj.day
    suffix = "th" if 11 <= day <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
    formatted_date = f"{day}{suffix} {date_obj.strftime('%B %Y')}"

    # Post header
    post_tips = (
        "👑 <b>KBT VIP MATCH PREDICTIONS</b>\n"
        "🎯 <i>Premium selections for serious bettors</i>\n\n"
        f"📅 <b>Date:</b> {formatted_date}\n\n"
    )

    # Predictions
    for x in predictions:
        post_tips += (
            f"🏆 <b>{x[1]}</b>\n"
            f"⚽ <b>{x[0]}</b>\n"
            f"📌 Tip: <b>{x[3]}</b>  |  💰 Odd: <b>{x[2]}</b>\n"
            f"⏰ Time: {x[4]} \n\n"
        )

    # Footer with support link
    footer = (
        "✅ <i>Stake responsibly</i>\n"
        "🔥 <b>Let’s cash out together!</b> 💸\n\n"

        f"💬 Last Result: https://t.me/betipsnetwork\n"
        "💬 Need help? <a href='https://t.me/btnhelp'>Contact Support</a>"
    )

    full_message = f"{post_tips}{footer}"

    payload = {
        "chat_id": gc.CHANNEL_CHAT_VIP_ID,
        "text": full_message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }

    response = requests.post(
        gc.TELEGRAM_VIP_BASE_URL + "sendMessage",
        data=payload,
        timeout=10
    )

    if response.status_code == 200:
        print("✅ VIP Telegram message sent successfully")
    else:
        print("❌ Telegram error:", response.text)


# =========================
# RUN
# =========================
def run():
    connect_server()
    post()


if __name__ == "__main__":
    run()
