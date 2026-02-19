import time
import logging
import all_betcodes, get_rightside_odds, oddslot, prima_tips,  primalow, over1_5goals, get_vip_2, get_btn_match_results, api_call, api_call_result, add_flags_to_matches, update_btn_results

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
        api_call.run()
        time.sleep(5)
        api_call_result.run()
        time.sleep(5)
        get_vip_2.run()
        time.sleep(5)
        get_btn_match_results.run()
        time.sleep(5)
        prima_tips.run()
        time.sleep(5)
        primalow.run()
        time.sleep(5)
        over1_5goals.run()
        time.sleep(5)
        add_flags_to_matches.run()
        time.sleep(5)
        update_btn_results.run()
        logging.info("Task completed successfully.")
    except Exception as e:
        logging.error(f"Error during task: {e}")

if __name__ == "__main__":
    while True:
        run_tasks()
        logging.info("Sleeping for 1 hour before next run...")
        time.sleep(3600)  # wait 1 hour
