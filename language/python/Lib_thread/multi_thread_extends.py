'''

thread 继承

'''

import threading
from time import ctime, sleep

lock = threading.Lock()


class MyThread(threading.Thread):

    def __init__(self, name):
        super().__init__(name=name)
        self.name = name

    def run(self):
        lock.acquire()
        print("线程", self.name, "已经运行")
        sleep(2)
        print("线程", self.name, "已经停止")
        lock.release()


thread1 = MyThread("one")
thread1.start()

thread2 = MyThread("two")
thread2.start()

thread1.join()
thread2.join()
