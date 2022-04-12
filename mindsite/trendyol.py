import time

from mindsite.html_parser import HtmlParser
from mindsite.log import LoggingMixin
import json
import threading

trendyol_multitreded_category_pages_list = []

class TrendyolProductFinder(LoggingMixin):

    def __init__(self):
        self.html_parser = HtmlParser()

    @staticmethod
    def generate_search_url(keyword: str, category_id: str, ordering: str):
        page_number = "1"
        # en düşük fiyat, en yüksek fiyat, en yeniler, çok satanlar, en favoriler, en çok değerlendirilenler
        q = "+".join(keyword.split(" "))
        base_url = f'https://www.trendyol.com/'
        params = f"sr?wc={category_id}&q={q}&os=1&pi={page_number}&sst={ordering}"
        return f'{base_url}{params}'

    def search_product_url(self, product_name, category, order_preference):
        search_url = self.generate_search_url(product_name, category, order_preference)
        page_info = self.html_parser.html_request(f'{search_url}')
        if page_info == "No_Page":
            return "Page not Found"
        main_search_slot = page_info.find("div", class_="prdct-cntnr-wrppr")
        products_info = main_search_slot.findAll("div", class_="p-card-wrppr")
        product_urls = []
        for product in products_info:
            product_url = product.find('a')
            if len(product_url["href"]) > 1:
                product_urls.append(product_url["href"])
        return product_urls

    @staticmethod
    def generate_product_url(product_url: str):
        base_url = f'https://www.trendyol.com'
        params = f"{product_url}"
        return f'{base_url}{params}'

    def get_product_info(self, partial_product_url):
        product_url = self.generate_product_url(partial_product_url)
        product_page = self.html_parser.html_request(product_url)
        if product_page == "No_Page":
            return "Page not Found"
        product_info = product_page.find("div", class_="container-right-content")
        merchant_info = product_info.find("div", class_="merchant-box-wrapper")

        full_name = product_info.find("h1", class_="pr-new-br")
        brand = full_name.find("a")
        merchant = merchant_info.find("a")
        review_count = product_info.find("a", class_="rvw-cnt-tx")
        price = product_info.find("span", class_="prc-dsc")

        # todo: rating ve soru cevap sayısı eklenecek
        # rating_info = product_page.find("div", class_="pr-rnr-cn gnr-cnt-br")
        # rating = rating_info.find("")
        # rating = product_info.find("span", class_="tltp-avg-cnt")
        # question_count = product_info.find(class_="product-questions")

        trendyol_product_info = {
            'Product_Name': full_name.text if full_name.text is not None else "",
            'Price': price.text if price.text is not None else "",
            'Brand': brand.text if brand.text is not None else "",
            "Merchant": merchant.text if merchant is not None else "",
            'Review_count': review_count.text.split(" ")[0] if review_count is not None else "",
        }
        return trendyol_product_info

    def get_category_tree(self):
        """
        Gathering Category Info

        :return: Category tree in dict format
        """
        category_tree = {}
        main_page = self.html_parser.html_request("https://www.trendyol.com")
        if main_page == "No_Page":
            return "Page not Found"
        navigation = main_page.find("div", attrs={"data-fragment-name": "Navigation"})
        main_navigaton = navigation.find("ul", class_="main-nav")
        for main_categories in main_navigaton.findAll("li", class_="tab-link", recursive=False):
            main_category_info = main_categories.find("a", class_="category-header")
            main_category_name = main_category_info.text
            main_category_url_params = main_category_info["href"]
            category_tree[main_category_name] = {"main_category_name": main_category_name,
                                                 "main_category_url_params": main_category_url_params}

            for sub_categories in main_categories.findAll("div", class_="normal-column"):
                sub_category_info = sub_categories.find("a", class_="sub-category-header")
                sub_category_name = sub_category_info.text
                sub_category_url_params = sub_category_info["href"]
                category_tree[main_category_name][sub_category_name] = {
                    "sub_category_name": sub_category_name,
                    "sub_category_url_params": sub_category_url_params
                }
                for double_sub_category_info in sub_categories.findAll("a", attrs={"href": True}):
                    double_sub_category_name = double_sub_category_info.text
                    double_sub_category_url_params = double_sub_category_info["href"]
                    category_tree[main_category_name][sub_category_name][double_sub_category_name] = {
                        "double_sub_category_name": double_sub_category_name,
                        "double_sub_category_url_params": double_sub_category_url_params
                    }

        return category_tree

    @staticmethod
    def generate_category_search_url(category_url: str):
        """https://www.trendyol.com/sr/cocuk-giyim-x-g3-c82?gag=2-2"""
        base_url = f'https://www.trendyol.com'
        params = f"{category_url}"
        return f'{base_url}{params}'

    @staticmethod
    def category_url_extractor(category_tree: dict):
        """
        Gathering category url params for complite search

        :param category_tree: category tree
        :return: list
        """
        category_urls = []
        for main_category in category_tree:
            sub_categories = category_tree[main_category]
            for sub_category in sub_categories:
                if sub_category not in ["main_category_url_params", "main_category_name"]:
                    category_urls.append(sub_categories[sub_category]["sub_category_url_params"])
                    double_sub_categories = sub_categories[sub_category]
                    for double_sub_categoriy in double_sub_categories:
                        if double_sub_categoriy not in ["sub_category_url_params", "sub_category_name"]:
                            category_urls.append(
                                double_sub_categories[double_sub_categoriy]["double_sub_category_url_params"])
        return category_urls

    def specific_category_crawler(self, category_url: str):
        """
        Searches for only one category. Pagination will should be next future.
        :param category_url:
        :return:
        """
        products_with_specific_group = []
        category_search_url = self.generate_category_search_url(category_url)
        category_main_page = self.html_parser.html_request(category_search_url)
        product_category = category_url.split("-x-")[0].replace("/", "")
        product_main_column = category_main_page.find("div", class_="prdct-cntnr-wrppr")
        if product_main_column is not None:
            products_info = product_main_column.findAll("div", class_="p-card-wrppr")
            try:
                for product in products_info:
                    products_with_specific_group.append({
                        "product_name": product.find("span", class_="prdct-desc-cntnr-name hasRatings").text,
                        "product_price": product.find("div", class_="prc-box-dscntd").text,
                        "procut_category": product_category
                    })
            except:
                self.log.info(f"Product info not found in {product_category} category")
        return products_with_specific_group

    def category_pages(self, category_urls: list):
        """
        Looking for product data in all categories.
        With threading uses many request simultaneously in order to speed the process

        :param category_urls:
        :return:
        """
        threads = []
        total_work = len(category_urls)

        for category_url in category_urls:
            t = threading.Thread(target=self.categorier, args=(category_url, ))
            threads.append(t)
        for thread in threads:
            thread.start()
            n = threading.active_count()
            while n > 10:
                n = threading.active_count()
                thread.join()
                print("Throttling")
                print(f'{len(trendyol_multitreded_category_pages_list)/total_work*100:.3f}%')

        return trendyol_multitreded_category_pages_list

    def categorier(self, category_url, ):
        category_search_url = self.generate_category_search_url(category_url)
        category_main_page = self.html_parser.html_request(category_search_url)
        # if category_main_page:
        #     print("boş")
        #     return
        trendyol_multitreded_category_pages_list.append(category_main_page)

    def general_category_crawler(self):
        products = []
        category_tree = self.get_category_tree()
        category_urls = self.category_url_extractor(category_tree)
        print(f'There are {len(category_urls)} number of categories')
        print(f'Processing')
        category_pages1 = self.category_pages(category_urls)
        print(f'{len(category_pages1)} category product is gathered')
        print(f'Merging product data')
        for index, category_main_page in enumerate(category_pages1):
            product_category = category_urls[index].split("-x-")[0].replace("/", "")
            product_main_column = category_main_page.find("div", class_="prdct-cntnr-wrppr")
            if product_main_column is not None:
                products_info = product_main_column.findAll("div", class_="p-card-wrppr")
                try:
                    for product in products_info:
                        products.append({
                            "product_name": product.find("span", class_="prdct-desc-cntnr-name hasRatings").text,
                            "product_price": product.find("div", class_="prc-box-dscntd").text,
                            "procut_category": product_category
                        })
                except:
                    self.log.info(f"Product info not found in {product_category} category")
            else:
                self.log.info(f"Product page could not found")
        return products

    @staticmethod
    def save_results(data, file_name):
        with open(f"{file_name}.json", "w") as outfile:
            json.dump(data, outfile)
        return "Jobs Done"
