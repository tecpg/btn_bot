import all_betcodes
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def run():
    logging.info("Starting daily task...")
    try:
        all_betcodes.run()
        logging.info("Task completed successfully.")
    except Exception as e:
        logging.error(f"Error during task: {e}")

if __name__ == "__main__":
    run()
