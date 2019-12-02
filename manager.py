import datetime
import threading
import time
import os
from random import randint
import schedule
import logging
from spider import Spider


def init_log(file_name='data/sp_xiaoniangao.log'):
    if not os.path.exists(file_name):
        os.mkdir(file_name)
        logging.basicConfig(filename=file_name, level=logging.INFO)


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
    while True:
        # print()
        # print('-------start one loop------ %s' % datetime.datetime.now().strftime('%H:%M:%S'))
        start = datetime.time(hour=6)
        end = datetime.time(hour=21)
        if start <= datetime.datetime.now().time() <= end:
            schedule.run_pending()
            time.sleep(20*60)
        else:
            time.sleep(40*60)

