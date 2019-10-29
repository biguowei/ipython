from multiprocessing import Manager, Process


def add_data(p_dict, key, value):
    p_dict[key] = value


if __name__ == "__main__":
    progress_dict = Manager().dict()
    from queue import PriorityQueue

    first_progress = Process(target=add_data, args=(progress_dict, "bobby1", 22))
    second_progress = Process(target=add_data, args=(progress_dict, "bobby2", 23))

    first_progress.start()
    second_progress.start()
    first_progress.join()
    second_progress.join()

    print(progress_dict)
