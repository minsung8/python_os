from multiprocessing import Process, current_process
import os
import random
import time


def square(n):
    time.sleep(random.randint(1,3))
    process_id = os.getpid()
    process_name = current_process().name
    res = n * n

    print(f'Process ID : {process_id}, Process name : {process_name}')
    print(f'res : {res}')

if __name__ == "__main__":
    # 부모 프로세스 아이디
    parent_process_id = os.getpid()
    print('Parent process ID {parent_process_id}')

    processes = []

    for i in range(1, 10):
        t = Process(name=str(i), target=square, args=(i, ))
        processes.append(t)
        t.start()
    
    for process in processes:
        process.join()

    print('Main-Processing Done!')
