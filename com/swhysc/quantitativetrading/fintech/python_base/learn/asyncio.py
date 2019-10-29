# future=asyncio.ensure_future(协程)  等于后面的方式  future=loop.create_task(协程)
# future.add_done_callback()添加一个完成后的回调函数
# loop.run_until_complete(future)
# future.result()查看写成返回结果
#
# asyncio.wait()接受一个可迭代的协程对象
# asynicio.gather(*可迭代对象,*可迭代对象）    两者结果相同，但gather可以批量取消，gather对象.cancel()
#
# 一个线程中只有一个loop
#
# 在loop.stop时一定要loop.run_forever()否则会报错
# loop.run_forever()可以执行非协程
# 最后执行finally模块中 loop.close()
#
# asyncio.Task.all_tasks()拿到所有任务 然后依次迭代并使用任务.cancel()取消
#
# 偏函数partial(函数，参数)把函数包装成另一个函数名  其参数必须放在定义函数的前面
#
# loop.call_soon(函数,参数)
# call_soon_threadsafe()线程安全
# loop.call_later(时间,函数,参数)
# 在同一代码块中call_soon优先执行，然后多个later根据时间的升序进行执行
#
# 如果非要运行有阻塞的代码
# 使用loop.run_in_executor(executor,函数，参数)包装成一个多线程，然后放入到一个task列表中，通过wait(task列表)来运行
#
# 通过asyncio实现http
# reader,writer=await asyncio.open_connection(host,port)
# writer.writer()发送请求
# async for data in reader:
#     data=data.decode("utf-8")
#     list.append(data)
# 然后list中存储的就是html
#
# as_completed(tasks)完成一个返回一个,返回的是一个可迭代对象
#
# 协程锁
# async with Lock():