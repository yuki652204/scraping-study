import requests
from bs4 import BeautifulSoup                    # ① 解析ロボットを取り出す

url = "https://books.toscrape.com/"
response = requests.get(url, timeout=10)
response.encoding = "utf-8"                      # ② 文字化け防止（下で説明）

soup = BeautifulSoup(response.text, "html.parser")   # ③ HTMLをロボットに渡す

books = soup.select("article.product_pod")       # ④ 本の箱を全部集める
print("見つかった本の数:", len(books))

for book in books:                               # ⑤ 箱を1つずつ開ける
    title = book.select_one("h3 a")["title"]     # ⑥ 題名
    price = book.select_one("p.price_color").text   # ⑦ 値段
    print(price, title)