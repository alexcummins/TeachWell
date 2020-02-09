import time
import sched

snapshots = []
s = sched.scheduler(time.time, time.sleep)

def get_snapshot(sc):
    snapshots.append()
    print ("Doing stuff...")
    # do your stuff
    s.enter(5, 1, get_snapshot, (sc,))


s.enter(5, 1, get_snapshot, (s,))
s.run()
