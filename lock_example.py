import logging
from concurrent.futures import ThreadPoolExecutor
import time

class FakeDataStore:
    # 공유 변수
    def __init__(self):
        self.value = 0
    
    # 변수 업데이트 함수
    def update(self, n):
        logging.info('Thread %s : starting update', n)

        #mutex or lock 등 Thread synchronization 필요
        local_copy = self.value
        local_copy += 1
        time.sleep(0.1)
        self.value = local_copy

        logging.info('Thread %s : finishing update', n)


if __name__ == "__main__":
    # Logging format 설정
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    # 클래스 인스턴스화
    store = FakeDataStore()

    logging.info('Testing update. Starting value is %d', store.value)

    # with context 시작
    with ThreadPoolExecutor(max_workers=2) as executor:
        for n in ['first', 'second', 'third']:
            executor.submit(store.update, n)
    
    logging.info('Testing update. ending value is %d', store.value)
