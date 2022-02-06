import logging
from concurrent.futures import ThreadPoolExecutor
import time


def task(name):
    logging.info('Sub-Thread %s: starting', name)
    res = 0
    for i in range(10001):
        res += i
    logging.info('Sub-Thread %s: finishing result %d', name, res)
    return res

def main():
    # Logging format 설정
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    logging.info('Main-Thread : before creating and running thread')

    # 실행 방법 1
    # max_workers : 작업의 개수가 넘어가면 직접 설정이 유리
    # excutor = ThreadPoolExecutor(max_workers=3)

    # task1 = excutor.submit(task, ('first', ))
    # task2 = excutor.submit(task, ('second', ))

    # print(task1.result())
    # print(task2.result())

    # 실행 방법 2
    with ThreadPoolExecutor(max_workers=3) as excutor:
        tasks = excutor.map(task, ['first', 'second'])

        # 결과 확인
        print(list(tasks))

if __name__ == "__main__":
    main()
