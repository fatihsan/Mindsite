#chromium solution


from requests_html import HTMLSession

url = "https://www.amazon.com.tr/s?k=iphone+13+pro+max+kılıfı+cüzdanlı&crid=13HRTL0XIZTFH&sprefix=iphone+13+pro+max+kılıfı+cüzdanlı%2Caps%2C103&ref=nb_sb_ss_ts-doa-p_1_33"

s = HTMLSession()
r = s.get(url)
r.html.render()

# print(r.html.find("title", first=True).full_text)

products = r.html.find("div[data-asin]")

for product in products:
    print(product.attrs["data-asin"])