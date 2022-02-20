import multiprocessing
from re import L
import requests
import time

# 각 프로세스 메모리 영역에 생성되는 객체
# 함수 실행 할 때 마다 객체 생성은 비효율적 => 각 프로세스마다 할당

session = None

def set_global_session():
    global session
    if not session:
        session = requests.Session()

def request_site(url):

    with session.get(url) as response:
        name = multiprocessing.current_process().name
        print(f'name : {name} => [read content : {len(response.content)}, status code : {response.status_code}] from {url}') 

def request_all_sites(urls):
    # 멀티프로세싱 실행
    with multiprocessing.Pool(initializer=set_global_session, processes=4) as pool:
        pool.map(request_site, urls)

def main():
    urls = [
        'https://www.jython.org',
        'http://olympus.realpython.org/dice',
        'https://realpython.com'
    ] * 5

    start_time = time.time()

    request_all_sites(urls)

    duration = time.time() - start_time

    print(f'Download {len(urls)} sites in {duration} seconds')

if __name__ == '__main__':
    main()
