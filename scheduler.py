from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler(timezone="Asia/Tokyo")


def add_job(job_function, amazon_api, twitter_auth):
    scheduler.add_job(
        job_function, "interval", minutes=30, args=[amazon_api, twitter_auth]
    )


def start_scheduler(job_function, amazon_api, twitter_auth):
    job_function(amazon_api, twitter_auth)
    scheduler.start()
