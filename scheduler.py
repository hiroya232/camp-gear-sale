from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler(timezone="Asia/Tokyo")


def add_job(job_function):
    scheduler.add_job(
        job_function,
        "interval",
        minutes=30,
    )


def start_scheduler(job_function):
    job_function()
    scheduler.start()
