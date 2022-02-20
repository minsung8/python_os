import concurrent.futures
import threading
import requests
import time

# 각 스레드에 할당되는 객체 (독립된 네임스페이스)
thread_local = threading.local()

def get_session():
    if not hasattr(thread_local, 'session'):
        thread_local.session = requests.Session()
    return thread_local.session

def request_site(url):
    session = get_session()

    with session.get(url) as response:
        print(f'[read content : {len(response.content)}, status code : {response.status_code}] from {url}') 

def request_all_sites(urls):
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(request_site, urls)

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
