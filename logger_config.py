import logging
import sys

logger = logging.getLogger("camp_gear_sale")
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)

app_handler = logging.FileHandler("app.log")
app_handler.setLevel(logging.DEBUG)
app_handler.addFilter(lambda record: record.levelno <= logging.INFO)
logger.addHandler(app_handler)

error_handler = logging.FileHandler("error.log")
error_handler.setLevel(logging.WARNING)
logger.addHandler(error_handler)

formatter = logging.Formatter(
    "%(levelname)-9s %(asctime)s [%(filename)s:%(lineno)d] %(message)s",
    "%Y-%d-%m %I:%M:%S",
)
stream_handler.setFormatter(formatter)
app_handler.setFormatter(formatter)
error_handler.setFormatter(formatter)
