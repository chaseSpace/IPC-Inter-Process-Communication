# -*- coding: utf-8 -*-
# @Time     : 2019/4/8 17:47
# @Author   : ELI
# @IDE      : PyCharm
# @PJ_NAME  : semaphore

'''

进程间通信之---信号量
特点：不传输数据，用于多进程的同步
参考： https://blog.csdn.net/sinat_27864123/article/details/78490164
'''

import multiprocessing
import time

def consumer(s):
    s.acquire() #信号量的使用与互斥量类似
    print(multiprocessing.current_process().name+' 正在执行')
    time.sleep(2) #执行时会发现同一时刻只有2个进程在执行
    s.release()
    print(multiprocessing.current_process().name+' release')


if __name__ == '__main__':
    s = multiprocessing.Semaphore(5) #把信号量值设置为2，一次提供给两个消费者服务
    for i in range(5): #启5个进程
        p = multiprocessing.Process(target=consumer,args=(s,))
        p.daemon = True #跟随主进程死亡,如果生产环境使用，最好加上这个，否则主进程结束时，子进程还在运行的话，就会造成孤儿进程（内存泄露）
        p.start()

    time.sleep(3) #等一下子进程
    print('main end')
