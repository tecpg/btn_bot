import all_betcodes
import logging
import get_rightside_odds
import tips_combo
import oddslot
import time as _time


_runtime = 5
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def run():
    logging.info("Starting daily task...")
    try:
        all_betcodes.run()
        _time.sleep(_runtime)
        oddslot.run()
        _time.sleep(_runtime)
        get_rightside_odds.run()
        _time.sleep(_runtime)
        tips_combo.run()
        logging.info("Task completed successfully.")
    except Exception as e:
        logging.error(f"Error during task: {e}")

if __name__ == "__main__":
    run()
