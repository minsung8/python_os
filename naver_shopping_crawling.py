import requests
import json
import lxml.html
from time import sleep
import re
from typing import Optional, List
from requests import Response
from abc import ABCMeta, abstractmethod
from typing import Optional, List
from requests import Session, Response
from json import JSONDecodeError
import csv


def get_review(keyword, page):
    review_list = []

    # 1. 상품 ID 리스트 구하기
    naver_shopping_url = 'https://search.shopping.naver.com/search/all?query=' + keyword
    smart_store_product_url_list = []
    naver_shopping_product_id_list = []

    params = {}
    for i in range(1, page + 1):
        params['pagingIndex'] = i
        html = requests.get(naver_shopping_url, params=params).text
        root_element = lxml.html.document_fromstring(html)

        s = root_element.xpath('//script[@id="__NEXT_DATA__"]')[0].text_content().strip()
        json_data = json.loads(s)

        product_list = json_data['props']['pageProps']['initialState']['products']['list']
        for product in product_list:
            if product['item']['purchaseConditionInfos']:
                if len(product['item']['mallProductUrl']) > 0:
                    smart_store_product_url_list.append([product['item']['mallProductId'], product['item']['mallPcUrl'].split('/')[-1]])
                else:
                    naver_shopping_product_id_list.append(product['item']['parentId'])
        sleep(1)

    r = SmartstoreRequester()
    # 스마트 스토어
    print(f'smart_store_product_url_list size = {len(smart_store_product_url_list)}')

    for url in smart_store_product_url_list:
        try:
            res = r.request_product(url[1], url[0])
            raw_json = rx_find_single_group(
                res, r'window\.__PRELOADED_STATE__=([\S\n\t\v ]*)}<\/script>', str
            )
            data = json.loads(raw_json + '}')
    
            origin_product_id = int(data['product']['A']['productNo'])
            merchant_no = int(data['product']['A']['channel']['naverPaySellerNo'])

            for i in range(1, 101):
                try:
                    res = r.request_review(origin_product_id, merchant_no, i)
                    temp_review_list = json.loads(res)
                    for review in temp_review_list['contents']:
                        try:
                            temp = {}
                            temp['productNo'] = review['productNo']
                            temp['createDate'] = review['createDate']
                            temp['writerMemberId'] = review['writerMemberId']
                            temp['id'] = review['id']
                            temp['reviewContent'] = review['reviewContent']
                            temp['reviewScore'] = review['reviewScore']
                            review_list.append(temp)
                        except:
                            pass
                except:
                    pass
                sleep(0.1)
        except:
            pass

    r2 = NaverShoppingRequester()

    # 네이버 쇼핑
    print(f'naver_shopping_product_id_list size = {len(naver_shopping_product_id_list)}')

    for id in naver_shopping_product_id_list:
        for i in range(1, 101):
            try:
                res = r2.request_review(id, i)
                data = json.loads(res)
                for review in data['reviews']:
                    try:
                        temp = {}
                        temp['productNo'] = id
                        temp['createDate'] = review['registerDate']
                        temp['writerMemberId'] = review['userId']
                        temp['id'] = review['mallReviewId']
                        temp['reviewContent'] = review['content']
                        temp['reviewScore'] = review['starScore']
                        review_list.append(temp)
                    except:
                        pass
            except:
                pass
            sleep(0.1)

    print(len(review_list))

    f = open(keyword + '_crawling_data.csv', 'w', newline='')
    wr = csv.writer(f)
    wr.writerow([1, 'productNo', 'createDate', 'writerMemberId', 'id', 'reviewContent', 'reviewScore'])

    for i in range(len(review_list)):
        wr.writerow([i + 2, review_list[i]['productNo'], review_list[i]['createDate'], review_list[i]['writerMemberId'],
        review_list[i]['id'], review_list[i]['reviewContent'], review_list[i]['reviewScore']])

    f.close()
    return


# 
"""
파싱을 위한 라이브러리 (regex 등) 에 대한 유틸리티성 메서드를 제공합니다.
"""

def __try_to_convert(value: str, convert_type: Optional[type], ignore_fail_to_none: bool):
    """
    입력값과 type을 바탕으로 명시적 형변환을 시도합니다.
    """
    if convert_type:
        try:
            return convert_type(value)
        except ValueError as e:
            if ignore_fail_to_none:
                return None
            else:
                raise e
    else:
        return value


def rx_find_single_group(
        source: str, regex: str, convert_type: Optional[type] = None, ignore_fail_to_none: bool = False
) -> Optional:
    """
    re.search (단일 검사) 실행으로 일치하는 데이터의 단일 그룹을 지정한 타입으로 변환합니다.

    @source: 파싱 대상 문서
    @regex: 파싱 regex
    @convert_type: 추출한 문자의 변환 타입. 변환하지 않을 경우 None 입니다.
    @ignore_fail_to_none: 추출이 실패했을 경우, True 라면 오류를 무시하고 None을 입력합니다.
    """
    match = re.search(regex, source)
    return __try_to_convert(match.groups()[0], convert_type, ignore_fail_to_none) if match else None


def rx_find_multiple_group(
        source: str, regex: str, convert_groups: List[Optional[type]], ignore_fail_to_none: bool = False
) -> Optional[List]:
    """
    re.search (단일 검사) 실행으로 일치하는 데이터의 다중 그룹을 지정한 타입으로 변환합니다.

    @source: 파싱 대상 문서
    @regex: 파싱 regex
    @convert_type: 추출한 문자의 변환 타입. 변환하지 않을 경우 None 입니다.
    @ignore_fail_to_none: 추출이 실패했을 경우, True 라면 오류를 무시하고 None을 입력합니다.
    """
    extract_group_size = len(convert_groups)
    assert extract_group_size, "추출 그룹이 지정되어야 합니다."

    match = re.search(regex, source)
    if not match:
        return None
    
    results = []
    groups = match.groups()
    for idx in range(extract_group_size):
        value = groups[idx]
        convert_type = convert_groups[idx]
        results.append(__try_to_convert(value, convert_type, ignore_fail_to_none))

    return results


def rx_findall_single_group(
        source: str, regex: str, convert_type: Optional[type] = None, ignore_fail_to_none: bool = False
) -> List:
    """
    re.findall(전체 검사) 실행으로 일치하는 데이터들의 단일 그룹을 지정한 타입으로 변환합니다.

    @source: 파싱 대상 문서
    @regex: 파싱 regex
    @convert_type: 추출한 문자의 변환 타입. 변환하지 않을 경우 None 입니다.
    @ignore_fail_to_none: 추출이 실패했을 경우, True 라면 오류를 무시하고 None을 입력합니다.
    """
    results = []
    matches = re.findall(regex, source)
    for match in matches:
        results.append(__try_to_convert(match, convert_type, ignore_fail_to_none))

    return results


def rx_findall_multiple_groups(
        source: str, regex: str, convert_groups: List[Optional[type]], ignore_fail_to_none: bool = False
) -> List[List]:
    """
    re.findall(전체 검사) 실행으로 일치하는 데이터들의 다중 그룹을 지정한 타입으로 변환합니다.

    @source: 파싱 대상 문서
    @regex: 파싱 regex
    @convert_groups: 추출한 문자의 각 그룹별 변환 타입. 변환하지 않을 경우 None 입니다.
    @ignore_fail_to_none: 추출이 실패했을 경우, True 라면 오류를 무시하고 None을 입력합니다.
    """
    extract_group_size = len(convert_groups)
    assert extract_group_size, "추출 그룹이 지정되어야 합니다."

    # N개 이상의 그룹 파싱을 시도하면, 해당 N개와 매칭되지 않은 경우 findall 결과에 포함되지 않음에 유의한다.

    results = []
    matches = re.findall(regex, source)
    for match in matches:  # type: Tuple
        bucket = []
        for idx in range(extract_group_size):
            value = match[idx]
            convert_type = convert_groups[idx]
            bucket.append(__try_to_convert(value, convert_type, ignore_fail_to_none))

        results.append(bucket)

    return results


class RequesterBase(metaclass=ABCMeta):
    """
    requests.Session 라이브러리를 기반으로 한 요청을 위한 클래스 베이스입니다.
    """

    # 외부 데이터 요청에 필요한 세션 인스턴스입니다.
    session = None  # type: Session

    # 전체 URL 제공을 위한 schema://domain 의 형태를 작성합니다.
    URL_HOME = None  # type Optional[str]

    def __init__(self, sess: Optional[Session] = None):
        self.session = sess if sess else Session()

    def __get_full_url(self, url: str, full_url: Optional[str]) -> str:
        """
        사용자 코드 작성 편의를 위해 지정된 규칙에 따라 요청 URL을 빌드합니다.
        """
        if full_url:
            return full_url
        else:
            assert self.URL_HOME, "full_url이 제공되지 않은 경우, url_home (schema://domain) 이 제공되어야 합니다."
            assert url.startswith('/'), 'url은 \'/\'로 시작해야 합니다.'
            return f'{self.URL_HOME}{url}'

    def get(
            self, url: str, full_url: Optional[str] = None, check_expected_response: bool = True, **kwargs
    ) -> Response:
        _url = self.__get_full_url(url, full_url)
        response = self.session.get(url=_url, **kwargs)

        if check_expected_response:
            self.check_abnormal_response_routine(response)
        return response

    def post(
            self, url: str, full_url: Optional[str] = None, check_expected_response: bool = True, **kwargs
    ) -> Response:
        _url = self.__get_full_url(url, full_url)
        response = self.session.post(url=_url, **kwargs)

        if check_expected_response:
            self.check_abnormal_response_routine(response)
        return response

    @abstractmethod
    def check_abnormal_response_routine(self, response: Response):
        """
        반환된 데이터가 사용 가능한 데이터인지 확인합니다
        포맷 자체의 오류는 검증하지 않으며, 인증, 스로들링 등의 문제가 발생했는지 확인합니다.

        잘못된 응답을 수신했을 경우, RequesterException 또는 상속 오류를 발생합니다.
        """
        pass


class SmartstoreRequester(RequesterBase):

    URL_HOME = "https://smartstore.naver.com"

    def check_abnormal_response_routine(self, response: Response):
        pass

    def __init__(self):
        super(SmartstoreRequester, self).__init__()
        self.session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4775.0 Safari/537.36'

    def request_product(self, seller_id: str, product_no: int) -> str:
        url = "/%s/products/%s" % (seller_id, product_no)
        return self.get(url).text

    def request_review(self, origin_product_id, merchant_no, page: int = 1) -> str:
        url = '/i/v1/reviews/paged-reviews'
        params = {
            'page': page, 'pageSize': 20, 'merchantNo': merchant_no, 'originProductNo': origin_product_id,
            'sortType': 'REVIEW_RANKING'
        }
        return self.get(url=url, params=params).text


class NaverShoppingRequester(RequesterBase):

    URL_HOME = "https://search.shopping.naver.com"

    def check_abnormal_response_routine(self, response: Response):
        pass

    def __init__(self):
        super(NaverShoppingRequester, self).__init__()
        self.session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4775.0 Safari/537.36'

    def request_product(self, product_no: str) -> str:
        url = "/catalog/%s" % product_no
        return self.get(url).text

    def request_review(self, product_no: str, page: int = 1) -> str:
        url = '/api/review?nvMid=%s&reviewType=ALL&sort=QUALITY&isNeedAggregation=N&isApplyFilter=N&page=%d&pageSize=20' % (product_no, page)
        return self.get(url=url).text


if __name__ == '__main__':
    keyword = input('keyword : ')
    page = int(input('page : '))

    get_review(keyword, page)
