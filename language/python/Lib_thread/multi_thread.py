'''

    多线程 ：
           传参
           同步 锁

'''

from time import sleep, ctime
import _thread as thread
import random

lock = thread.allocate_lock()


def fun1(a, b):
    lock.acquire()
    print(str(a))
    sleep(random.randint(1, 5))
    print(b)
    lock.release()


def fun2():
    print("开始fun2")
    sleep(random.randint(1, 5))
    print("结束fun2")


def main():
    print("开始main")
    for i in range(10):
        print(i)
        thread.start_new_thread(fun1, (i + 1, '*' * (i + 1)))
    ##thread.start_new_thread(fun2,())
    print("结束main")


main()
input()
# if __name__ == '__main__':
#    main()
