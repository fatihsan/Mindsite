from mindsite.html_parser import HtmlParser
from mindsite.log import LoggingMixin


class AmazonProductFinder(LoggingMixin):

    def __init__(self):
        self.html_parser = HtmlParser()

    @staticmethod
    def generate_search_url(keyword: str, product_category: str):
        k = "+".join(keyword.split(" "))
        base_url = f'https://www.amazon.com.tr/'
        params = f"s?k={k}&i={product_category}&creative=380333&creativeASIN=B07ZL57W9S&linkCode=asn&tag=cimritr1-21"
        return f'{base_url}{params}'

    def search_product_asins(self, product_name, product_category):
        """
        Creating search url and finding product asins for getting product info

        :param product_name: Product name
        :param product_category: Product Category
        :return: product asins
        """

        search_url = self.generate_search_url(product_name, product_category)


        page_info = self.html_parser.html_request(f'{search_url}')
        if page_info == "No_Page":
            return "Product not Found"
        main_search_slot = page_info.find("div", class_="s-main-slot s-result-list s-search-results sg-row")
        asin_data = main_search_slot.findAll('div', attrs={'data-asin': True}, recursive=False)
        product_asins = []
        for asin in asin_data:
            """Removing advert or sponsored products"""
            if "AdHolder" not in asin["class"]:
                if len(asin["data-asin"]) > 1:
                    product_asins.append(asin["data-asin"])
        return product_asins

    @staticmethod
    def generate_product_url(product_asin: str):
        base_url = f'https://www.amazon.com.tr/'
        params = f"dp/{product_asin}"
        return f'{base_url}{params}'

    # https://www.amazon.com.tr/gp/product/ajax/ref=dp_aod_unknown_mbc?asin=B000A0BSCY&m=&qid=1649526944&experienceId=aodAjaxMain

    @staticmethod
    def generate_no_buy_box_url(product_asin: str):

        base_url = f"https://www.amazon.com.tr/gp/product/ajax"
        params = f'?asin={product_asin}&experienceId=aodAjaxMain'
        return f'{base_url}{params}'

    def get_product_info(self, product_asin: str):
        """
        Generating product info

        :param product_asin: product asin
        :return: amazon product info
        """
        # product_asin = "B0974NF1T3"
        buy_box = "No Buy Box"
        product_url = self.generate_product_url(product_asin)
        product_page = self.html_parser.html_request(product_url)
        if product_page == "No_Page":
            return "Product not Found"
        center_column = product_page.find("div", id="centerCol")
        buy_box_column = product_page.find("div", id="rightCol")

        full_name = center_column.find("span", id="productTitle")
        buy_box_info = buy_box_column.find("div", id="buybox")
        brand = center_column.find("a", id="bylineInfo")
        rating = center_column.find("span", class_="reviewCountTextLinkedHistogram noUnderline")["title"]
        review_count = center_column.find("span", id="acrCustomerReviewText")

        if buy_box_info.findAll("div", id="qualifiedBuybox"):
            # id='priceblock_ourprice'
            price = f'{center_column.find("span", class_="a-price-whole").text}{center_column.find("span", class_="a-price-fraction").text} {center_column.find("span", class_="a-price-symbol").text}'
            buy_box = "Has Buy Box"
        else:
            price = "No price tag"

            # todo: buy box olmaması durumunda fiyat alanı gelmiyor
            # generate_no_buy_box_url(product_asin)
            # no_buy_box_page = HtmlParser.html_request(product_url)
            # all_offers = no_buy_box_page.find("div", id="all-offers-display", class_="a-section")
            # offers = no_buy_box_page.find("div", id="aod-offer-list")
            # offer_list = offers.findAll("div", id="aod-offer", recursive=False)

        amazon_product_info = {
            'Product_Name': str(full_name.text).strip() if full_name.text is not None else "",
            'Price': price,
            'Asin': product_asin,
            'Brand': str(brand.text).split(":")[1:] if brand.text is not None else "",
            "Rating": rating if rating is not None else "",
            'Review_count': review_count.text if review_count is not None else "",
            'Buy_box': buy_box
        }

        return amazon_product_info
