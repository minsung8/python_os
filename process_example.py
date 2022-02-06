from multiprocessing import Process
import time
import logging


def proc_func(name):
    print('Sub-Process {}: starting'.format(name))
    time.sleep(3)
    print('Sub-Process {}: finishing'.format(name))

def main():
    # Logging format 설정
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    p = Process(target=proc_func, args=('First', ))

    logging.info('Main-Process : before creating Process')

    # 프로세스
    p.start()

    logging.info('Main-Process : During Process')

    # 프로세스 종료
    # logging.info('Main-Process : Terminated Process')
    # p.terminate()

    logging.info('Main-Process : Joined Process')
    p.join()

    # 프로세스 상태 확인
    print(f'Process p is alive: {p.is_alive()}')

if __name__ == "__main__":
    main()
