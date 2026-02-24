import time
import logging
import signal
import sys

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

# -----------------------------
# Logging setup
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

RUN_INTERVAL = 3600  # 1 hour

running = True

# -----------------------------
# Graceful shutdown
# -----------------------------
def shutdown_handler(signum, frame):
    global running
    logging.warning("Shutdown signal received. Exiting gracefully...")
    running = False

signal.signal(signal.SIGINT, shutdown_handler)   # Ctrl+C
signal.signal(signal.SIGTERM, shutdown_handler)  # Server stop

# -----------------------------
# Task Runner
# -----------------------------
def run_tasks():
    logging.info("🚀 Starting daily task pipeline...")

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
        try:
            logging.info(f"▶ Running {task.__module__}.run()")
            task()
            time.sleep(5)
        except Exception as e:
            logging.exception(f"❌ Error in {task.__module__}: {e}")

    logging.info("✅ Task cycle completed successfully")

# -----------------------------
# Main loop
# -----------------------------
def run():
    global running
    while running:
        run_tasks()
        if not running:
            break
        logging.info(f"🕒 Sleeping for {RUN_INTERVAL // 60} minutes...")
        time.sleep(RUN_INTERVAL)

    logging.info("🛑 Scheduler stopped")
    sys.exit(0)

# -----------------------------
# Entry point
# -----------------------------
if __name__ == "__main__":
    run()
