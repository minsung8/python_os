import concurrent.futures
from email import message
import logging
import queue
import random
from re import T
import threading
import time



"""

pytonh Event 객체
1. Flag 초기값 = 0
2. Set() -> 1
3. Clear() -> 0
4. Wait(1 -> return, 0 -> 대기)
5. isSet() -> 현재 flag 상태 
 
"""
# 생산자
def producer(queue, event):
    """ 네트워크 대기 상태라 가정 (서버) """
    while not event.is_set():
        message = random.randint(1, 11)
        logging.info('Producer got message : %s', message)
        queue.put(message)
    
    logging.info('Producer received event Exiting')

# 소비자
def consumer(queue, event):
    """ 응답 받고 소비하는 것으로 가정 or DB 저장 """
    while not event.is_set() or not queue.empty():
        message = queue.get()
        logging.info(
            'Consumer storing message : %s (size=%d)', message, queue.qsize()
        )

    logging.info('Consumer received event exiting')


if __name__ == '__main__':
    # Logging format 설정
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    # queue 사이즈 중요
    pipeline = queue.Queue(maxsize=10)

    # 이벤트 플래그 초기값 0
    event = threading.Event()

    # with context 시작
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(producer, pipeline, event)
        executor.submit(consumer, pipeline, event)

        # 실행 시간 조정
        time.sleep(0.1)

        logging.info('Main : about to set event')

        # 프로그램 종료
        event.set()
