import sched, time
from datetime import datetime, timedelta

s = sched.scheduler(time.time, time.sleep)

def do_something(sc):
    print("測試")
    # do your stuff
    sc.enter(60, 1, do_something, (sc,))

now = datetime.now()
run_at = now.replace(hour=10, minute=21, second=0)
if now > run_at:
    run_at += timedelta(days=1)
delay = (run_at - now).total_seconds()

s.enter(delay, 1, do_something, (s,))
s.run()