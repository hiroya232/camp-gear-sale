from apscheduler.events import EVENT_JOB_EXECUTED, JobExecutionEvent
from apscheduler.schedulers.blocking import BlockingScheduler

import time
import datetime
from zoneinfo import ZoneInfo


scheduler_list = {}
target_product_index_list = {}


def finished_scheduler(target_date, asin_list):
    target_product_index_list[target_date] += 1
    if target_product_index_list[target_date] >= len(asin_list):
        return target_date


def completed_scheduler_listener(event: JobExecutionEvent):
    completed_scheduler = event.retval
    if completed_scheduler is not None:
        scheduler_list[completed_scheduler].shutdown(wait=True)


def create_scheduler(asin_list, short_url_list, target_date, job_function):
    target_product_index_list[target_date] = 0

    scheduler_list[target_date] = BlockingScheduler(timezone="Asia/Tokyo")
    scheduler_list[target_date].add_listener(
        completed_scheduler_listener, EVENT_JOB_EXECUTED
    )
    scheduler_list[target_date].add_job(
        job_function,
        "interval",
        seconds=3,
        args=[asin_list, short_url_list, target_date],
    )


def start_scheduler(asin_list, short_url_list, target_date, job_function):
    for date, scheduler in scheduler_list.items():
        exec_date = datetime.datetime.strptime(date, "%Y-%m-%d").astimezone(
            ZoneInfo("Asia/Tokyo")
        )
        now_datetime = datetime.datetime.now(ZoneInfo("Asia/Tokyo"))
        if exec_date.date() == now_datetime.date():
            job_function(asin_list, short_url_list, target_date)
            scheduler.start()
        else:
            delta = exec_date.replace(hour=7, minute=0, second=0) - now_datetime
            time.sleep(delta.total_seconds())
            scheduler.start()
