from multiprocessing import Process, current_process, parent_process
import os

# 프로세스 메모리 공유 X Case
# 실행 함수
def generate_update_number(v: int):
    for _ in range(50):
        v += 1
    print(current_process().name, "data", v)

def main():
    # 부모 프로세스 아이디
    parent_process_id = os.getpid()
    print(f'Parent process ID {parent_process_id}')

    processes = list()
    
    share_value = 0

    for _ in range(1, 10):
        p = Process(target=generate_update_number, args=(share_value,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    print(f'share_value : {share_value}')
if __name__ == '__main__':
    main()
