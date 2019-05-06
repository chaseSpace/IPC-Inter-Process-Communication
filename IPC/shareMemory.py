# -*- coding: utf-8 -*-
# @Time     : 2019/4/8 17:58
# @Author   : ELI
# @IDE      : PyCharm
# @PJ_NAME  : shareMemory


'''
进程间通信之---共享内存
特点：
    1. 最快的IPC方式
    2. 因为多个进程可以同时操作，所以需要进行同步
    3. 可通过与信号量或锁结合使用实现多个进程间同步
共享方案:
    a. 消息队列
    b. 文件映射（为了在进程间共享内存，内核专门留有一个内存区，主进程将需要共享的数据映射到这块内存中，其他进程访问这个共享内存）
'''

from multiprocessing import Process,Queue,Semaphore,current_process
from time import sleep
my_semaphore = Semaphore(2)

'''
错误的示例!
'''
global_list = list(range(5)) #进程间不共享内存，所以每个进程访问的是这个对象的副本，并不是同一个对象

def change_global_list(global_list,s):
    s.acquire()
    print('process_id:%s before change'% current_process().name, global_list)
    global_list.pop()
    sleep(1)
    s.release()
    print('process_id:%s after change'% current_process().name,global_list)


if __name__ == '__main__':
    from multiprocessing import Manager, freeze_support
    manager = Manager()
    print(dir(manager))#'address', 'connect', 'dict', 'get_server', 'join', 'list', 'register', 'shutdown', 'start'
    global_list = manager.list()

    global_list.extend(list(range(5)))

    for i in range(5):
        p = Process(target=change_global_list,args=(global_list,my_semaphore))
        p.daemon = True
        p.start()

    sleep(3)  # 等一下子进程
    print('over!')

