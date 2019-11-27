import datetime
import threading
import time
from random import randint
import schedule
from spider import Spider


def video_job():
    case = Spider()
    case.spider_list(randint(0, 6))
    case.analysis_list()
    case.grab()


def list_job():
    print('start job %s' % datetime.datetime.now().strftime('%H:%M:%S'))
    for i in range(1, 10):
        if randint(1, 10) > 7:
            video_job()


def video_task():
    threading.Thread(target=list_job).start()


if __name__ == '__main__':
    schedule.every(30).minutes.do(video_task)
    while True:
        print()
        print('-------start one loop------ %s' % datetime.datetime.now().strftime('%H:%M:%S'))
        start = datetime.time(hour=6)
        end = datetime.time(hour=21)
        if start <= datetime.datetime.now().time() <= end:
            schedule.run_pending()
            time.sleep(30*30)
        else:
            time.sleep(60*60)

