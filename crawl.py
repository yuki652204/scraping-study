import csv
import time                                   # 休憩用
from urllib.parse import urljoin              # 住所の組み立て用

import requests
from bs4 import BeautifulSoup

START_URL = "https://books.toscrape.com/"
MAX_PAGES = 3                                 # 練習なので3ページで止める

url = START_URL
rows = []
page = 1

while url and page <= MAX_PAGES:              # ① 行き先があって、3ページ以内の間くり返す
    print(f"{page}ページ目を取得中: {url}")

    response = requests.get(url, timeout=10)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")

    for book in soup.select("article.product_pod"):
        title = book.select_one("h3 a")["title"]
        price = book.select_one("p.price_color").text.replace("£", "")
        rows.append([page, title, price])     # 何ページ目の本かも記録

    next_link = soup.select_one("li.next a")  # ② nextボタンを探す
    if next_link:
        url = urljoin(url, next_link["href"]) # ③ 次の完全な住所を作る
    else:
        url = None                            # 最終ページなので行き先なし

    page += 1
    time.sleep(1)                             # ④ 1秒休む

with open("books_all.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["page", "title", "price_gbp"])
    writer.writerows(rows)

print(len(rows), "件を books_all.csv に保存しました")