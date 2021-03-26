'''
Description: 
version: 
Author: TianyuYuan
Date: 2021-03-26 15:25:13
LastEditors: TianyuYuan
LastEditTime: 2021-03-26 16:23:49
'''
from typb import pb_iter,pb_multi_thread,pb_range

def square_a_num(x):
    """任务函数"""
    import time
    time.sleep(0.05)
    return x*x

def pb_range_testcase(x):
    result = []
    for i in pb_range(x):
        result.append(square_a_num(i))
    # print(result)

def pb_simple_iter_testcase(x):
    result = []
    for i in pb_iter(range(x)):
        result.append(square_a_num(i))
    # print(result)
    
def pb_multi_thread_testcase(x):
    iter_files = range(x)
    result = pb_multi_thread(5,square_a_num,iter_files)
    # print(result)

if __name__ == "__main__":
    # Run test case
    # pb_range_testcase(3)
    # pb_simple_iter_testcase(190)
    pb_multi_thread_testcase(15)
    pb_multi_thread_testcase(30)