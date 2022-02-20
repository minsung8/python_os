import requests
import time

def request_site(url, session):
    with session.get(url) as response:
        print(f'[read content : {len(response.content)}, status code : {response.status_code}] from {url}') 

def request_all_sites(urls):
    with requests.Session() as session:
        for url in urls:
            request_site(url, session)

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
