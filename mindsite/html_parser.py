# import grequests as async_request
import requests
from bs4 import BeautifulSoup
from mindsite.log import LoggingMixin
import random


class HtmlParser(LoggingMixin):

    def html_request(self, url):
        """
        All projects requests working from here.
        Most of the error logging handling in here

        :param url: url
        :return: BeautifulSoup object
        """
        proxies, header = self.avoid_detection()
        client = requests.session()
        response = client.get(url, headers=header, proxies=proxies)
        # print(response.status_code)
        if response.status_code == 200:
            return BeautifulSoup(response.text, "html.parser")
        else:
            print(response.status_code)
            self.log.info(
                f"Page not found while going to '{url}'. status_code: {response.status_code} while using header: {header}")
            return "No_Page"

    @staticmethod
    def avoid_detection():
        header = {}
        proxy = {}

        # Can be added proxies for detection avoidance.
        # In order to activate proxy: proxy_randon_selector and proxy variables need to be activated.

        # proxies = []

        # proxy_randon_selector = random.randrange(len(proxies))
        # proxy = proxies[proxy_randon_selector]

        header_list = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246,"
            "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36 OPR/85.0.4341.60",
        ]

        header_randon_selector = random.randrange(len(header_list))
        header["User-Agent"] = header_list[header_randon_selector]
        return proxy, header

    """ @staticmethod
    def exception_handler(request, exception):
    print("Request failed")
    
    def html_request_async(self, urls: list):
    # rs = (async_request.get(u) for u in urls)
    # responses = async_request.map(rs)
    reqs = []
    reqs = [async_request.get(link) for link in urls]
    for url in urls:
        reqs.append(async_request.get(url, timeout=0.001))
    
    for response in async_request.imap(reqs, size=5, exception_handler=self.exception_handler):
        print("LAKSJDLAŞSDJ")
        if response.status_code == 200:
            # print(response.status_code)
            return BeautifulSoup(response.text, "html.parser")
        else:
            print(response.status_code)
            self.log.info(f"Page not found while going to {response}. status_code: {response.status_code}")
            raise Exception("failed")"""
