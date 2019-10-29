from multiprocessing import Pipe, Process


# pipe的性能高于queue
def producer(pipe):
    pipe.send("bobby")


def consumer(pipe):
    print(pipe.recv())


if __name__ == "__main__":
    recevie_pipe, send_pipe = Pipe()
    # pipe只能适用于两个进程
    my_producer = Process(target=producer, args=(send_pipe,))
    my_consumer = Process(target=consumer, args=(recevie_pipe,))

    my_producer.start()
    my_consumer.start()
    my_producer.join()
    my_consumer.join()
