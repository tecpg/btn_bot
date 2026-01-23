import time
import logging
import all_betcodes, get_rightside_odds, oddslot

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def run_tasks():
    logging.info("Starting daily task...")
    try:
        all_betcodes.run()
        time.sleep(5)  # small delay between tasks
        oddslot.run()
        time.sleep(5)
        get_rightside_odds.run()
        time.sleep(5)

        logging.info("Task completed successfully.")
    except Exception as e:
        logging.error(f"Error during task: {e}")

if __name__ == "__main__":
    while True:
        run_tasks()
        logging.info("Sleeping for 1 hour before next run...")
        time.sleep(3600)  # wait 1 hour
