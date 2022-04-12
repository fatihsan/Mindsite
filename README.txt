Amazon/Trendyol Product Finder

environment: Linux Ubunutu 20.04
to start the program run: --> `python3 main.py

General Usage

1 - Amazon product search with name
About 30% of times is working. Usually amazon does not allow to use search bar.
Be careful to choose valid key value for category dict (1-17). Otherwise, program will crash.

2-  Amazon product search with asin or asins
Usually works. Example product asin : B09HKMCD9D

3-  Trendyol product search by name
Be carefully to use valid key for order dict(1-6). Otherwise, program will crash.

4-  Gather Trendyol category tree
Automated process. Only gathers category tree from Trendyol / save or print. First idea was to make another mechanism
for searching all products in single category by pagination but operation 5 is working just fine with using threading.

5-  Trendyol general product crawler
Gathers all category urls from Trendyol's main page. After it sends a request to each category and gathers all products
in first pages for each category / save or print.

Did not time it before using multithread, but I assume each category took about 1 to 0.8 sec.
After adding threading, total process is taken approximately 1 min 10 sec.
It is looking for 594 category and usually 590 category request returns successfully. (About 7800 product)

In trendyol.py "category_pages" function is operating multithreading. With current setting, there can be 10 thread max.
It may change by changing "max_thread_number" variable.
