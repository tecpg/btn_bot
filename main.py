import time
import logging

import all_betcodes
import get_rightside_odds
import oddslot

# Logging config (Heroku captures stdout)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

TASK_DELAY = 5  # seconds between tasks


def run_task(task, index, total):
    """Run a single task with timing, logging, and error handling."""
    task_name = task.__name__
    start_msg = f"▶ [{index}/{total}] Starting {task_name}..."
    logging.info(start_msg)
    print(start_msg)

    start_time = time.time()

    try:
        task.run()
        duration = time.time() - start_time

        success_msg = (
            f"✅ [{index}/{total}] {task_name} completed "
            f"in {duration:.2f}s"
        )
        logging.info(success_msg)
        print(success_msg)

    except Exception as e:
        error_msg = f"❌ [{index}/{total}] {task_name} failed: {e}"
        logging.exception(error_msg)
        print(error_msg)

    time.sleep(TASK_DELAY)


def run_tasks():
    logging.info("📅 Daily Heroku scheduled job started")
    print("📅 Daily Heroku scheduled job started")

    tasks = [
        all_betcodes,
        oddslot,
        get_rightside_odds,
    ]

    total_tasks = len(tasks)

    for index, task in enumerate(tasks, start=1):
        run_task(task, index, total_tasks)

    logging.info("🏁 All scheduled tasks finished")
    print("🏁 All scheduled tasks finished")


if __name__ == "__main__":
    run_tasks()
