# from concurrent.futures import ThreadPoolExecutor
#
# pool = ThreadPoolExecutor()
# task = pool.submit(函数名，（参数）) #此方法不会阻塞，会立即返回
# task.done()#查看任务执行是否完成
# task.result()#阻塞的方法，查看任务返回值
# task.cancel()#取消未执行的任务，返回True或False,取消成功返回True
# task.add_done_callback()#回调函数
# task.running()#是否正在执行     task就是一个Future对象
#
# for data in pool.map(函数，参数列表):#返回已经完成的任务结果列表，根据参数顺序执行
#     print(返回任务完成得执行结果data)
#
# from concurrent.futures import as_completed
# as_completed(任务列表)#返回已经完成的任务列表，完成一个执行一个
#
# wait(任务列表,return_when=条件)#根据条件进行阻塞主线程，有四个条件