from concurrent.futures import ProcessPoolExecutor, as_completed
import urllib.request


URLS = [
    'http://www.naver.com/',
    'http://www.naver.com/',
]

def load_url(url, timeout):
    with urllib.request.urlopen(url, timeout=timeout) as conn:
        return conn.read()


def main():
    with ProcessPoolExecutor(max_workers=5) as executor:
        # future에 로드
        future_to_url = {executor.submit(load_url, url, 60): url for url in URLS}

        for future in as_completed(future_to_url):
            url = future_to_url[future]

            try:
                data = future.result()
            except Exception as e:
                print(e)
            else:
                print(f'success {url}')

if __name__ == '__main__':
    main()
