from mindsite.operations import Operations
import json
import pprint

amazon_category_list = ["garden", "baby", "computers", "electronics", "home", "kitchen", "pets", "grocery",
                        "gift-cards", "stripbooks", "beauty", "mi", "office-products", "toys", "hpc", "sports", "diy"]

trendyol_product_ordering = ["PRICE_BY_ASC", "PRICE_BY_DESC", "MOST_RECENT", "BEST_SELLER", "MOST_FAVOURITE",
                             "MOST_RATED"]


# trendyol_category_list = {"Cep Telefonu": ["103498"]}

def generate_dict_from_list(lst):
    categories = {}
    for i, category in enumerate(lst):
        categories[f'{i + 1}'] = category
    return categories


def amazon_product_by_name():
    print("Product name:", end=" ")
    product_name = input()
    categories = generate_dict_from_list(amazon_category_list)
    print("Product category?")
    print(f"categories: {categories}")
    category_num = input()
    return product_name, categories[category_num]


def trendyol_search_by_name():
    print("Product name:", end=" ")
    product_name = input()
    orderby = generate_dict_from_list(trendyol_product_ordering)
    print("Which order would you like to search?")
    print(f"Order by: {orderby}")
    product_ordering = input()
    return product_name, product_ordering


def saving_or_printing(decision, data, file_name):
    if decision == "1":
        with open(f"{file_name}.json", "w") as outfile:
            json.dump(data, outfile)
        return "Jobs Done"
    if decision == "2":
        pprint.pprint(data)


def menu():
    print("↓ Select the Action you want to use ↓", )
    print("1- Amazon product search with name\n"
          "2- Amazon product search with asin or asins\n"
          "3- Trendyol product search by name\n"
          "4- Gather Trendyol category tree\n"
          "5- Trendyol general product crawler\n"
          "6- Exit")


def interface():
    print("Amazon/Trendyol product finder", )
    operations = Operations()
    while True:
        menu()
        action = str(input())
        if action == "1":
            product_name, category_num = amazon_product_by_name()
            print(operations.amazon_product_search_by_name(product_name, category_num))
        if action == "2":
            print("Product asin or asins")
            product_asin = input().split(",")
            print(operations.amazon_product_search_with_asin_list(product_asin))
        if action == "3":
            product_name, product_ordering = trendyol_search_by_name()
            product_info, product_urls = operations.trendyol_product_search_by_name(product_name, product_ordering)
            """product_urls: all products' urls on first page"""
            print(product_info)
        if action == "4":
            category_tree = operations.trendyol_category_tree()
            if category_tree != "Page not Found":
                print("Category tree created")
            print("For saving output:1, For printing output:2 (json format)")
            saving_or_printing(input(), category_tree, "trendyol_category_tree")
        if action == "5":
            product_info = operations.trendyol_category_crawler()
            print("For saving output:1, For printing output:2 (json format)")
            saving_or_printing(input(), product_info, "trendyol_category_crawler")
        if action == "6":
            print("Closing")
            return
