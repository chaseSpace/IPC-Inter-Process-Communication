# -*- coding: utf-8 -*-
# @Time     : 2019/4/8 15:35
# @Author   : ELI
# @IDE      : PyCharm
# @PJ_NAME  : pipe-3

# 参考https://www.cnblogs.com/shijingjing07/p/7899611.html
'''
使用FIFO（命名管道）来实现任意两个进程间的通信
特点：
    1. 和无名管道一样，半双工
    2. 每个FIFO管道都与一个路径名相关联，类似一个文件
    3. 进程间通过读写FIFO来通信

**注意：这种方式对子进程的生命周期管理并不方便，不建议在python中使用**
'''
import os, time
pipe_name = 'pipe_test'

def child():
    #子进程负责写
    pipeout = os.open(pipe_name, os.O_WRONLY)  # 必须以只写模式
    counter = 0
    while counter < 10: #不要写死循环，控制不好就是僵尸进程
        print('write Number %03d\n' % counter)
        os.write(pipeout, b'Number %03d\n' % counter)   #这里是非阻塞的
        counter +=1
        time.sleep(1)

def parent():
    #父进程负责读
    # pipein = open(pipe_name, 'r') #也可以用内置函数open，和操作文件一样
    fd = os.open(pipe_name, os.O_RDONLY)  # 必须以只读模式，获取一个file descriptor
    #fd是一个非负整数，只在单个进程中有意义，单个进程中一个fd对应一个待操作文件。
    while True:
        # line = pipein.readlines()[:-1]
        line = os.read(fd, 20)  # 每次读20个字节，读出后FIFO管道中会马上清除数据
        #open和os.read都是非阻塞的
        if line:
            print('Parent %d got "%s" at %s' % (os.getpid(), line, time.time()))
        else:
            print('Parent %d no data'% os.getpid())
        time.sleep(1)

if not os.path.exists(pipe_name):
    os.mkfifo(pipe_name)  #创建FIFO管道

pid = os.fork()  #创建子进程
if pid:
    parent()
else:
    child()

'''
这种模式允许多个进程(>=2)间通信
'''