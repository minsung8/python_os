# 프로세스 통신 구현 queue

from multiprocessing import Process, Pipe, current_process, parent_process
import time
import os

def worker(id, baseNum, conn):
    process_id = os.getpid()
    process_name = current_process().name

    sub_total = 0
    
    for i in range(baseNum):
        sub_total += i
    
    conn.send(sub_total)
    conn.close()

    print(f'Process ID : {process_id}, Process name : {process_name}')
    print(f'result : {sub_total}')

def main():
    parent_process_id = os.getpid()
    print(f'parent_process_id : {parent_process_id}')

    start_time = time.time()

    parent_conn, child_conn = Pipe()

    p = Process(name=str(1), target=worker, args=(1, 10000000, child_conn))
    
    p.start()

    p.join()
    
    print('time = %s', (time.time() - start_time))

    total = 0

    print()
    print(f'Main-Processing total count = {parent_conn.recv()}')
    print('Main-Process Done')


if __name__ == '__main__':
    main()
