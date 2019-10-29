from multiprocessing import Queue, Process
import time


def producer(queue):
    queue.put("a")
    time.sleep(2)


def consumer(queue):
    time.sleep(2)
    data = queue.get()
    print(data)


if __name__ == "__main__":
    queue = Queue(10)
    my_producer = Process(target=producer, args=(queue,))
    my_consumer = Process(target=consumer, args=(queue,))
    my_producer.start()
    my_consumer.start()
    my_producer.join()
    my_consumer.join()
