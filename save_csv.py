import csv                                       # ① CSVを書く道具（Python標準装備）
import requests
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/"
response = requests.get(url, timeout=10)
response.encoding = "utf-8"
soup = BeautifulSoup(response.text, "html.parser")

books = soup.select("article.product_pod")

rows = []                                        # ② 空のカゴを用意
for book in books:
    title = book.select_one("h3 a")["title"]
    price = book.select_one("p.price_color").text.replace("£", "")   # ③ £を外す
    rows.append([title, price])                  # ④ 1冊ぶんをカゴに入れる

with open("books.csv", "w", newline="", encoding="utf-8") as f:   # ⑤ ファイルを開く
    writer = csv.writer(f)
    writer.writerow(["title", "price_gbp"])      # ⑥ 見出し
    writer.writerows(rows)                       # ⑦ カゴの中身をまとめて書く

print(len(rows), "件を books.csv に保存しました")