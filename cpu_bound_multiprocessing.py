
import time
from multiprocessing import current_process, Array, Value, Manager, Process, freeze_support
import os 

def cpu_bound(number, total_list):
    process_id = os.getpid()
    process_name = current_process().name
    print(f'process_id = {process_id}, process_name = {process_name}')
    total_list.append(sum(i * i for i in range(number)))

def main():
    numbers = [3_000_000 + x for x in range(30)]

    processes = list()
    manager = Manager()
    total_list = manager.list()

    start_time = time.time()

    for i in numbers:
        t = Process(name=str(i), target=cpu_bound, args=(i, total_list,))
        processes.append(t)
        t.start()

    for process in processes:
        process.join()

    print(f'total list : {total_list}')
    print(f'sum : {sum(total_list)}')

    duration = time.time() - start_time

    print(f'duration : {duration}')

if __name__ == '__main__':
    main()
