# -*- coding: utf-8 -*-
# @Time     : 2019/4/8 11:38
# @Author   : ELI
# @IDE      : PyCharm
# @PJ_NAME  : pipe-2

'''
#标准库提供的管道是普通管道，单工的，读写方向固定
特点：只允许具有亲缘关系的两个进程通信
'''
import os, sys

print("The child will write text to a pipe and ")
print("the parent will read the text written by child...")

# file descriptors r, w for reading and writing
r, w = os.pipe()

processid = os.fork() #fork 方法仅能在linux系统上运行,跨平台就用multiprocess

print(processid)

if processid:
    # This is the paunameent process
    # Closes file descriptor w
    os.close(w)
    r = os.fdopen(r)
    print("Parent reading")
    str = r.read()
    print("text =", str)
    sys.exit(0)
else:
    # This is the child process
    os.close(r)
    w = os.fdopen(w, 'w')
    print("Child writing")
    w.write("Text written by child...")
    w.close()
    print("Child closing")
    sys.exit(0)