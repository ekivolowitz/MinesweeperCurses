from threading import Thread, Lock

class Clock():
    def __init__(self):
        self.time = 0
        self.clock_lock = Lock()
        self.kill = False
        self.kill_lock = Lock()

    def updateTime(self):
        with self.clock_lock:
            self.time += 1

    def getTime(self):
        t = None
        with self.clock_lock:
            t = self.time
        return t
    def killClock(self):
        with self.kill_lock:
            self.kill = True
    def getKill(self):
        kill = False
        with self.kill_lock:
            kill = self.kill
        return kill
