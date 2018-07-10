# -*- coding: utf-8 -*-

# @Time     : 2018/4/17
# @Author   : WangL
# @File     : Tools.py
import queue
import threading


StopEvent = object()


class ThreadPool(object):
    """
    实现一个线程池
    """
    def __init__(self, max_num=4):
        self.MAX_THREAD_NUM = max_num
        self.task_queue = queue.Queue()
        self.lock = threading.Lock()
        self.free_list = []
        self.generate_list = []
        
    def generate_thread(self):
        t = threading.Thread(target=self.execute_task)
        t.start()
        
    def add_task(self, func, arg):
        if len(self.free_list) == 0 and len(self.generate_list) < self.MAX_THREAD_NUM:
            self.generate_thread()
        task = (func, arg)
        self.task_queue.put(task)
    
    def execute_task(self):
        cur_thread = threading.currentThread().getName()
        self.lock.acquire()
        self.generate_list.append(cur_thread)
        print('current list is {}'.format(str(self.generate_list)))
        self.lock.release()

        task = self.task_queue.get()
        while True:
            if task == StopEvent:
                print('thread {} exit'.format(cur_thread))
                break
            
            func, arg = task
            if callable(func):
                print('thread {} execute url {}'.format(cur_thread, arg))
                func(arg)
            
            self.lock.acquire()
            self.free_list.append(cur_thread)
            self.lock.release()
            
            task = self.task_queue.get()
            
            self.lock.acquire()
            self.free_list.remove(cur_thread)
            self.lock.release()

    def terminate(self):
        for _ in self.generate_list:
            self.task_queue.put(StopEvent)
