Amazon/Trendyol Product Finder

to start the program run: --> `python3 main.py

Genel kullanım

1-  Ürün ismi ile amazonda ürün arattırmak. Yüzde 30 çalışıyor. Amazon request i engelliyor genellikle.
    Kategori seçerken içinde bulunan key value larına girmezseniz hata veriyor. O kısımını düzeltmeye zamanım kalmadı.

2-  Asin değerleri ile ürün arattırmak. Genelde request doğru dönüyor amazon tarafından.
    Asin ile aramayı denemek için örnek asin değeri: B09HKMCD9D

3-  Ürün ismi ile trendyolda ürün arattırmak.
    Sıralama ölçütü seçerken yanlış key girildiğinde hata veriyor.

4-  Otomatik bir işlem. Aslında ilk düşüncem trendyolun içinde tek bir kategoriyi tamamen taratmaktı ancak 5. seçenekte
multithread i çalıştırmam uzun sürdüğü için vaktim kalmadı. Şuan için kategori ağacını alıyor sadece trendyoldan.

5-  Trendyoldaki bütün kategorileri çekip sonrasında her kategorinin ilk sayfasındaki ürünleri tarıyor. Sonrasında json
olarak kaydedebiliyorsunuz.
    Multithread ayarlamadan öncesinde zaman tutmadım ancak her istek yaklaşık 1 sn sürüyordu.
Şuan toplam 594 kategoriyi 1 dk 10 sn civarlarında tarıyor.
Ortalama 590 kategorinin requesti doğru geliyor. 7800 civarında ürün verisi almış oluyor.


trendyol.py ın içinde "general_category_crawler" fonksiyonu bu işlemi çalıştırıyor. Onun içinde requestler multitred
işlenmesi için "category_pages" fonksiyonuna gidiyor. Şuan aynı anda 10 işlem yapacak şekilde ayarlandı. Istenir ise
"max_thread_number" değişkeni değiştirilebilir.


