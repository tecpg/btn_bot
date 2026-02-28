import time
import logging
import signal
import sys
from datetime import datetime

import all_betcodes
import get_rightside_odds
import oddslot
import prima_tips
import primalow
import over1_5goals
import get_vip_2
import get_btn_match_results
import api_call
import api_call_result
import add_flags_to_matches
import update_btn_results


# ==================================================
# LOGGING
# ==================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ==================================================
# INTERVALS
# ==================================================
DEFAULT_INTERVAL = 3600        # 1 hour
LONG_INTERVAL = 18 * 3600     # 18 hours
TASK_DELAY = 5                # seconds between tasks

running = True


# ==================================================
# GRACEFUL SHUTDOWN
# ==================================================
def shutdown_handler(signum, frame):
    global running
    logging.warning("🛑 Shutdown signal received. Stopping scheduler...")
    running = False


signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)


# ==================================================
# SLEEP LOGIC
# ==================================================
from datetime import datetime, timedelta
import logging

def get_next_sleep_interval():
    now = datetime.now()
    hour = now.hour

    # -------------------------
    # Night / hourly window
    # 00:00 → 06:59
    # -------------------------
    if 0 <= hour < 7:
        logging.info("🌙 Night window → running hourly")
        return 3600  # 1 hour

    # -------------------------
    # Evening warm-up
    # 22:00 → 23:59
    # -------------------------
    if hour >= 22:
        target = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        seconds = (target - now).total_seconds()
        logging.info(f"🌆 Evening detected → waiting until midnight ({seconds/3600:.2f}h)")
        return int(seconds)

    # -------------------------
    # Day sleep mode
    # 07:00 → 01:59
    # -------------------------
    target = now.replace(hour=2, minute=0, second=0, microsecond=0)
    if hour >= 7:
        target += timedelta(days=1)

    seconds = (target - now).total_seconds()
    logging.info(f"☀️ Day mode → sleeping until {target.strftime('%Y-%m-%d %H:%M')}")
    return int(seconds)

def safe_sleep(seconds):
    """Sleep in small chunks to allow instant shutdown"""
    global running
    slept = 0
    while running and slept < seconds:
        time.sleep(1)
        slept += 1


# ==================================================
# TASK RUNNER
# ==================================================
def run_tasks():
    logging.info("🚀 Starting bot pipeline")

    tasks = [
        all_betcodes.run,
        oddslot.run,
        get_rightside_odds.run,
        api_call.run,
        api_call_result.run,
        get_vip_2.run,
        get_btn_match_results.run,
        prima_tips.run,
        primalow.run,
        over1_5goals.run,
        add_flags_to_matches.run,
        update_btn_results.run,
    ]

    for task in tasks:
        if not running:
            break

        try:
            logging.info(f"▶ Running {task.__module__}.run()")
            task()
            safe_sleep(TASK_DELAY)

        except Exception:
            logging.exception(f"❌ Failure in {task.__module__}")

    logging.info("✅ Bot cycle completed")


# ==================================================
# MAIN LOOP
# ==================================================
def run():
    logging.info("🚀 Scheduler started")

    while True:
        now = datetime.now()

        # Only run tasks during night window
        if 0 <= now.hour < 7:
            logging.info("▶ Running tasks (night window)")
            run_tasks()
        else:
            logging.info("⏸ Outside night window → skipping task run")

        sleep_seconds = get_next_sleep_interval()
        logging.info(f"🕒 Sleeping for {sleep_seconds/3600:.2f} hours")
        time.sleep(sleep_seconds)

# ==================================================
# ENTRY POINT
# ==================================================
if __name__ == "__main__":
    run()