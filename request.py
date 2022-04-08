import random
import requests
from bs4 import BeautifulSoup


URL = f"https://www.amazon.com.tr/s?k=iphone+13+pro+max+kılıfı+cüzdanlı&crid=13HRTL0XIZTFH&sprefix=iphone+13+pro+max+kılıfı+cüzdanlı%2Caps%2C103&ref=nb_sb_ss_ts-doa-p_1_33"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
}

response = requests.get(URL, headers=headers)

print(response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

# print(soup.find_all(attrs={"data-asin" : "B09DGDB7DT"}))

a = soup.find("div",class_="s-main-slot s-result-list s-search-results sg-row")

scriptTags = a.findAll('div', attrs={'data-asin':True})

for i in scriptTags:
    print(i["data-asin"])

# proper usage:

asin_data = soup.findAll('div', attrs={'data-asin':True})
product_asin = []
for asin in asin_data:
    if len(asin["data-asin"]) > 1:
        product_asin.append(asin["data-asin"])
print(product_asin)

