import datetime
import threading
import time
import logging
from random import randint
import schedule
from app.spider import Spider


def init_log(file_name='xiaoniangao.log'):
    logger = logging.getLogger('manager')
    logger.setLevel(level=logging.INFO)
    # Formatter
    formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(lineno)d] [%(levelname)s] %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')

    # FileHandler
    file_handler = logging.FileHandler(file_name)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    # StreamHandler
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)


def video_job():
    case = Spider()
    case.spider_list(randint(0, 5))
    case.analysis_list()
    case.grab()


def list_job():
    # print('start job %s' % datetime.datetime.now().strftime('%H:%M:%S'))
    for i in range(1, 10):
        if randint(1, 10) > 7:
            video_job()


def video_task():
    threading.Thread(target=list_job).start()


if __name__ == '__main__':
    init_log()
    schedule.every(20).minutes.do(video_task)
    start = datetime.time(hour=6)
    end = datetime.time(hour=21)

    while start <= datetime.datetime.now().time() <= end:
        schedule.run_pending()
        time.sleep(20*60)
    else:
        time.sleep(60*60)

