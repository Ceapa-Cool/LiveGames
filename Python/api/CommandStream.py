import io
import threading
import time



class Command:
    def __init__(self, p, t, d):
        self.p = p
        self.t = t
        self.d = d

class CommandStream:
    def __init__(self):
        self.list = []
        self.lock = threading.Lock()
        self.loaded = threading.Event()

    def write(self, p, t, d=None):

        com = Command(p, t, d)

        self.lock.acquire()
        self.list.append(com)
        if len(self.list) == 1:
            self.loaded.set()
        self.lock.release()

    def read(self):

        #nonblocking wait
        while not self.loaded.wait(0.02):
            pass

        self.lock.acquire()

        com = self.list.pop(0)
        if len(self.list) == 0:
            self.loaded.clear()

        self.lock.release()

        return com
