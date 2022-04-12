from mindsite.amazon_tr import AmazonProductFinder
from mindsite.trendyol import TrendyolProductFinder
import json

amazon_category_list = ["garden", "baby", "computers", "electronics", "home", "kitchen", "pets", "grocery",
                        "gift-cards", "stripbooks", "beauty", "mi", "office-products", "toys", "hpc", "sports", "diy"]

trendyol_product_ordering = ["PRICE_BY_ASC", "PRICE_BY_DESC", "MOST_RECENT", "BEST_SELLER", "MOST_FAVOURITE",
                             "MOST_RATED"]

trendyol_category_list = {"Cep Telefonu": ["103498"]}


class Operations:

    def __init__(self):
        self.amazon = AmazonProductFinder()
        self.trendyol = TrendyolProductFinder()

    def amazon_product_search_by_name(self, product_name: str, product_category: str):
        product_asins = self.amazon.search_product_asins(product_name, product_category)
        if product_asins == "Product not Found":
            return product_asins
        product_info = self.amazon.get_product_info(product_asins[0])
        return product_info, product_asins[0]

    def amazon_product_search_with_asin_list(self, product_asins: list):
        product_info = []
        for asin in product_asins:
            product_info.append(self.amazon.get_product_info(asin))
        return product_info

    def trendyol_product_search_by_name(self, product_name, product_ordering, product_category=""):
        product_urls = self.trendyol.search_product_url(product_name, product_category, product_ordering[0])
        if product_urls == "search_product_url":
            return "Product not Found"
        product_info = self.trendyol.get_product_info(product_urls[0])
        return product_info, product_urls

    def trendyol_category_tree(self):
        category_tree = self.trendyol.get_category_tree()
        return category_tree

    def trendyol_category_crawler(self):
        products = self.trendyol.general_category_crawler()
        return products


"""trendyol = TrendyolProductFinder()
product_name_trendyol = "iphone 13 pro max"
product_category_trendyol = "wc=1190"
product_urls = trendyol.search_product_url(product_name_trendyol, product_category_trendyol,
                                           trendyol_product_ordering[0])
product_info = trendyol.get_product_info(product_urls[0])
category_tree = trendyol.get_category_tree()
trendyol = TrendyolProductFinder()
test = trendyol.general_category_crawler()"""

"""product_name_amazon = "iphone 12"
product_category_amazon = "electronics"

amazon = AmazonProductFinder()
product_asins = amazon.search_product_asins(product_name_amazon, product_category_amazon)
Product_info = amazon.get_product_info(product_asins[0])"""

"""product_info = amazon.get_product_info("B08FF3XVVH")
{'Product_Name': 'Skechers GO RUN ELEVATE Koşu Ayakkabısı Kadın', 'Price': '', 'Asin': 'B08FF3XVVH'}
'Brand': [' Skechers'], 'Rating': '5 yıldız üzerinden 4,5', 'Review_count': '136 değerlendirme', 'Buy_box': 'No Buy Box'}"""
