import unittest
from unittest.mock import patch

from mindsite.html_parser import HtmlParser
from mindsite.amazon_tr import AmazonProductFinder


class TestAmazonTr(unittest.TestCase):

    @patch("mindsite.html_parser.requests")
    def test_html_request_failed(self, mock_requests):
        url = "https://www.amazon.com.tr/s?k=iphone+13+pro+max"
        p = HtmlParser()
        # mock_requests.get.return_value = ""
        mock_requests.get.return_value.status_code = 404
        with self.assertRaises(Exception) as cm:
            p.html_request(url)
        self.assertEqual(str(cm.exception), "failed")

    @patch("mindsite.html_parser.requests")
    def test_html_request_success(self, mock_requests):
        url = "https://www.amazon.com.tr/s?k=iphone+13+pro+max"
        p = HtmlParser()
        mock_requests.get.return_value.text = open("./tests/dummy_files/dummy_amazon_search_page.html")
        mock_requests.get.return_value.status_code = 200
        page_info = p.html_request(url)
        self.assertIn("B09G9PQ132", str(page_info))
        self.assertNotIn("foo-bar-baz", str(page_info))

    def test_generate_search_url(self):
        keyword = "Macbook Pro"
        category = "electronics"

        url = AmazonProductFinder.generate_search_url(keyword, category)
        self.assertEqual(url, f'https://www.amazon.com.tr/s?k={"+".join(keyword.split(" "))}&i={category}')



