# -*- coding: utf-8 -*-
# @Time     : 2019/4/8 17:54
# @Author   : ELI
# @IDE      : PyCharm
# @PJ_NAME  : Queue


from multiprocessing import Process
from multiprocessing import Queue
from time import sleep

def write(q):
    for i in range(5):
        sleep(1)
        print('put %s to queue..' % i)
        q.put(i)


def read(q):
    while 1:
        # sleep(0.5)
        v = q.get(True)
        print('get %s from queue..' % v)


if __name__ == '__main__':
    q = Queue()
    p1 = Process(target=write, args=(q,))
    p2 = Process(target=read, args=(q,))
    p1.start()
    p2.start()
    p1.join()  # 等待p1进程跑完后再往下执行
    if q.qsize() == 0:  # 待队列为空时结束p2进程
        p2.terminate()
