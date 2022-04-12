from mindsite.amazon_tr import AmazonProductFinder
from mindsite.trendyol import TrendyolProductFinder


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