# -*- coding: utf-8 -*-

"""
@author: Mr_zhang
@software: PyCharm
@file: hh.py
@time: 2022/1/21 09:57
"""
import time

import requests
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from multiprocessing import cpu_count


class ThreadRequest:
    """推送抽象基类"""
    """
        ⡖⠒⠒⠤⢄⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   ⢸⠁⠀⠀⠀⡼⠀⠀⠀⠀ ⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢶⣲⡴⣗⣲⡦⢤⡏⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠋⠉⠉⠓⠛⠿⢷⣶⣦⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠇⠀⠀⠀⠀⠀⠀⠘⡇⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡞⠀⠀⠀⠀⠀⠀⠀⢰⠇⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⡴⠊⠉⠳⡄⠀⢀⣀⣀⡀⠀⣸⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⢸⠃⠀⠰⠆⣿⡞⠉⠀⠀⠉⠲⡏⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠈⢧⡀⣀⡴⠛⡇⠀⠈⠃⠀⠀⡗⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣱⠃⡴⠙⠢⠤⣀⠤⡾⠁⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⢀⡇⣇⡼⠁⠀⠀⠀⠀⢰⠃⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⣸⢠⣉⣀⡴⠙⠀⠀⠀⣼⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⡏⠀⠈⠁⠀⠀⠀⠀⢀⡇⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⢸⠃⠀⠀⠀⠀⠀⠀⠀⡼⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⣰⠃⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⣀⠤⠚⣶⡀⢠⠄⡰⠃⣠⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⢀⣠⠔⣋⣷⣠⡞⠀⠉⠙⠛⠋⢩⡀⠈⠳⣄⠀⠀⠀⠀⠀⠀⠀
        ⠀⡏⢴⠋⠁⠀⣸ 在你代码里⣹⢦⣶⡛⠳⣄⠀⠀⠀⠀⠀
        ⠀⠙⣌⠳⣄⠀⡇⠀⠀里拉屎⠀⠀⡏⠀⠀⠈⠳⡌⣦⠀⠀⠀⠀
        ⠀⠀⠈⢳⣈⣻⡇⠀⠀⠀⠀⠀⠀⢰⣇⣀⡠⠴⢊⡡⠋⠀⠀⠀⠀
        ⠀⠀⠀⠀⠳⢿⡇⠀⠀⠀⠀⠀⠀⢸⣻⣶⡶⠊⠁⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⢠⠟⠙⠓⠒⠒⠒⠒⢾⡛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⣠⠏⠀⣸⠏⠉⠉⠳⣄⠀⠙⢆⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⡰⠃⠀⡴⠃⠀⠀⠀⠀⠈⢦⡀⠈⠳⡄⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⣸⠳⣤⠎⠀⠀⠀💩⠀⠀⠀⠙⢄⡤⢯⡀⠀⠀⠀⠀⠀⠀
        ⠀⠐⡇⠸⡅⠀⠀⠀⠀💩⠀⠀⠀⠀⠀⠹⡆⢳⠀⠀⠀⠀⠀⠀
        ⠀⠀⠹⡄⠹⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣇⠸⡆⠀⠀⠀⠀⠀
        ⠀⠀⠀⠹⡄⢳⡀⠀⠀ 💩⠀⠀⠀ ⠀⠀⢹⡀⣧⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⢹⡤⠳⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣷⠚⣆⠀⠀⠀⠀
        ⠀⠀⠀⡠⠊⠉⠉⢹⡀⠀💩⠀⠀⠀⠀⠀⢸⡎⠉⠀⠙⢦⡀⠀
        ⠀⠀⠾⠤⠤⠶⠒⠊⠀💩💩⠀⠀⠀ ⠀⠉⠙⠒⠲⠤⠽

    """

    def __init__(self):
        self.TIMEOUT = 0.8
        self.base_url_list = [
            "http://47.104.240.15:9001/market/index.html",
            "http://47.104.240.15/admin/",
            "http://47.104.240.15/admin/#/admin/api/datastatistics/",
            "http://47.104.240.15/admin/#/admin/api/report/",
            "http://47.104.240.15/admin/#/admin/api/checkidfa/",
            "http://47.104.240.15/admin/#/admin/api/channel/",
        ]
        
    def process_task(self):
        """多进程回调函数"""
        for base_url in self.base_url_list:
            res = requests.get(base_url, timeout=self.TIMEOUT)
            print(res.url, res.status_code)
    
    def thread_task(self):
        """多线程回调函数"""
        for base_url in self.base_url_list:
            res = requests.get(base_url, timeout=self.TIMEOUT)
            print(res.url, res.status_code)

    def process_execute(self, process_pool_count=4, process_nums=10):
        """
        :param process_pool_count: 进程池个数
        :param process_nums: 进程池数量
        :return:
        """
        process_pool = ProcessPoolExecutor(max_workers=process_pool_count)
        targets = []
        for _ in range(process_nums):
            targets.append(process_pool.submit(self.process_task))
        process_pool.shutdown()
        
    def thread_execute(self, thread_pool_count=10, thread_nums=10):
        """
        :param thread_pool_count: 线程池个数
        :param thread_nums: 线程数量
        :return:
        """
        thread_pool = ThreadPoolExecutor(max_workers=thread_pool_count)
        for _ in range(thread_nums):
            _ = thread_pool.submit(self.thread_task)
        thread_pool.shutdown()


if __name__ == '__main__':
    start_time = time.time()
    thread_request = ThreadRequest()
    # thread_request.process_execute(process_pool_count=cpu_count(), process_nums=100000)
    thread_request.thread_execute(thread_pool_count=1000, thread_nums=100000)
    print(time.time() - start_time)
    