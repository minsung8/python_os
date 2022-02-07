# 프로세스 통신 구현 queue

from multiprocessing import Process, Queue, current_process, parent_process
import time
import os

def worker(id, baseNum, q):
    process_id = os.getpid()
    process_name = current_process().name

    sub_total = 0
    
    for i in range(baseNum):
        sub_total += i
    
    q.put(sub_total)

    print(f'Process ID : {process_id}, Process name : {process_name}')
    print(f'result : {sub_total}')

def main():
    parent_process_id = os.getpid()
    print(f'parent_process_id : {parent_process_id}')

    processes = []

    start_time = time.time()

    q = Queue()

    for i in range(5):
        p = Process(name=str(i), target=worker, args=(i, 10000000, q))
        processes.append(p)
        p.start()

    for process in processes:
        process.join()
    
    print('time = %s', (time.time() - start_time))

    q.put('exit')
    total = 0

    while True:
        temp = q.get()
        if temp == 'exit':
            break
        else:
            total += temp
    
    print()
    print(f'Main-Processing total count = {total}')
    print('Main-Process Done')


if __name__ == '__main__':
    main()
