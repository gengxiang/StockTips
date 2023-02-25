import sched
import time
from datetime import datetime

schedule = sched.scheduler(time.time, time.sleep)


def task(inc):
    now = datetime.now()
    ts = now.strftime("%Y-%m-%d %H:%M:%S")
    print(ts)
    schedule.enter(inc, 0, task, (inc,))


def func(inc=3):
    schedule.enter(0, 0, task, (inc,))
    schedule.run()


func()
