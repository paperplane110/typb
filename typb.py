'''
Description: typb -> Tian_Yu_Progress_Bar 进度条,显示range的进度条，生成器进度条，多线程进度条，多线程偏函数进度条
version: 
Author: TianyuYuan
Date: 2021-03-26 13:44:18
LastEditors: TianyuYuan
LastEditTime: 2021-03-26 16:57:14
'''
from rich import print as rprint
from concurrent.futures import ThreadPoolExecutor,as_completed
from functools import partial
    
class ProgressBar():
    """类：进度条，可用于显示普通迭代的进度"""
    def __init__(self,task,length,batchs=50):
        """类：进度条，可用于显示迭代的进度
        - task: 任务名称，可填入·函数名·或者·字符串·,若填入函数名，则可自动获取该函数的名字描述
        - length: 任务长度，通常为可迭代对象的长度，即len(iter_files)
        - batch: 进度条的份数，默认为100个单位，以百分制显示进度
        """
        if isinstance(task,str): self.task_name = task
        else: self.task_name = task.__name__
        self.length = length
        if self.length < batchs: 
            self.batch_size=1
        else: 
            self.batchs = batchs
            self.batch_size = self.length/self.batchs

    def print_progressbar(self,i):
        """
        - i: 迭代到了第i个job
        """
        progress = int(i/self.batch_size)
        p_bar = "["+"[bold green]>[/bold green]"*(progress)+"]"
        p_propotion = "[green]{}[/green]/[red]{}[/red]".format(i,self.length)
        p_percentage = ":rocket:{}%".format(round(i/self.length*100))
        if i < self.length:
            rprint("{task}  {percentage} :{bar}  {propotion}".format(task=self.task_name,bar=p_bar,propotion=p_propotion,percentage=p_percentage),end="\r")
        else:
            rprint("{task}  {percentage} :{bar}  {propotion}".format(task=self.task_name,bar=p_bar,propotion=p_propotion,percentage=p_percentage))


# * * * * * * * * * * * * * * * * * * * * * * * #
# *            请调用这一部分的函数！             * #
# * * * * * * * * * * * * * * * * * * * * * * * #
def pb_iter(iter_files):
    """生成器，将可迭代对象填入，在生成element的同时显示迭代的进度"""
    pb = ProgressBar("iter",len(iter_files))
    i = 0
    for element in iter_files:
        i += 1
        pb.print_progressbar(i)
        yield element

def pb_range(*args):
    """可显示迭代进度的range()，功能用法与range相同
    """
    iter_files = range(*args)
    return pb_iter(iter_files)

def pb_multi_thread(workers:int,task,iter_files) -> list:
    """显示多进程进度条
    - workers: 指定多进程的max_workers
    - task: 任务函数
    - iter_files: 填入要处理的可迭代对象
    - return: 返回每个job的结果，并存入list返回
    """
    pb = ProgressBar(task,len(iter_files))
    result = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        job_list = []
        for task_input in iter_files:
            job = pool.submit(task,task_input)
            job_list.append(job)
        i = 0
        for done_job in as_completed(job_list):
            i += 1
            result.append(done_job.result())
            pb.print_progressbar(i)
    return result

def pb_multi_thread_partial(workers:int,task,iter_files,**kwargs):
    """显示多进程进度条，针对具有多参数的任务
    - workers: 指定多进程的max_workers
    - task: 任务函数
    - iter_files: 填入要处理的可迭代对象
    - **kwargs: 填入'keyword=constant_object....'
    - return: 返回每个job的结果，并存入list返回
    """
    new_task = partial(task,**kwargs)
    new_task.__name__ = task.__name__
    return pb_multi_thread(workers,new_task,iter_files)

# * * * * * * * * * * * * * * * * * * * * * * * #
# *           Test Cases & Examples           * #
# * * * * * * * * * * * * * * * * * * * * * * * #
def square_a_num(x):
    """任务函数"""
    import time
    time.sleep(0.05)
    return x*x

def multi_param_task(x,a,b,c):
    """多参数任务函数"""
    return x+a+b+c

def pb_range_testcase(*args):
    result = []
    for i in pb_range(*args):
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

def pb_multi_thread_partial_testcase(x,a,b,c):
    iter_files = range(x)
    result = pb_multi_thread_partial(5,multi_param_task,iter_files,a=a,b=b,c=c)
    # print(result)

if __name__ == "__main__":
    # Run test case
    # pb_range_testcase(3)
    # pb_simple_iter_testcase(190)
    # pb_multi_thread_testcase(30)
    # pb_multi_thread_testcase(1000)
    pb_multi_thread_partial_testcase(15,1,1,1)