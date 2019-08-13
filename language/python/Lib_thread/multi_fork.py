'''

多进程
进程锁

'''

from multiprocessing import Pool,Lock
from time import sleep


def get_value(value):
    print("value", value)
    sleep(5)


if __name__ == '__main__':
    values = ['value{}'.format(str(i)) for i in range(0, 5)]
    pool = Pool(processes=4)
    pool.map(get_value, values)



