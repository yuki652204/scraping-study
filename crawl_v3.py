import csv
import time
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup

START_URL = "https://books.toscrape.com/"
ROBOTS_URL = "https://books.toscrape.com/robots.txt"
MAX_PAGES = 3
OUTPUT_FILE = "books_all.csv"


def is_allowed(url):
    """門番：robots.txt で取得してよいか確認する"""
    robots = RobotFileParser(ROBOTS_URL)
    robots.read()
    return robots.can_fetch("*", url)


def fetch_soup(url, retries=3):
    """① 取得：失敗したら少し待って再挑戦。全部ダメなら None を返す"""
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            response.encoding = "utf-8"
            return BeautifulSoup(response.text, "html.parser")
        except requests.RequestException as e:
            print(f"  失敗 {attempt}/{retries}回目: {e}")
            if attempt < retries:
                time.sleep(2)
    return None


def parse_books(soup, page):
    """② 解析：1ページ分の本を [ページ, 題名, 値段] のリストで返す"""
    rows = []
    for book in soup.select("article.product_pod"):
        link = book.select_one("h3 a")
        price_tag = book.select_one("p.price_color")
        if link is None or price_tag is None:
            print("  形の違う本があったのでスキップ")
            continue
        title = link["title"]
        price = price_tag.text.replace("£", "")
        rows.append([page, title, price])
    return rows


def find_next_url(soup, current_url):
    """次ページの完全なURLを返す。なければ None"""
    next_link = soup.select_one("li.next a")
    if next_link:
        return urljoin(current_url, next_link["href"])
    return None


def save_csv(rows, path):
    """③ 保存：CSVに書き出す"""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["page", "title", "price_gbp"])
        writer.writerows(rows)


def main():
    """現場監督：部品を順番に呼ぶ"""
    if not is_allowed(START_URL):
        print("robots.txt で禁止されているので中止します")
        return

    url = START_URL
    page = 1
    all_rows = []

    while url and page <= MAX_PAGES:
        print(f"{page}ページ目を取得中: {url}")
        soup = fetch_soup(url)
        if soup is None:
            print("取得できなかったので、ここまでの分で終了します")
            break
        all_rows.extend(parse_books(soup, page))
        url = find_next_url(soup, url)
        page += 1
        time.sleep(1)

    if all_rows:
        save_csv(all_rows, OUTPUT_FILE)
        print(len(all_rows), "件を", OUTPUT_FILE, "に保存しました")
    else:
        print("1件も取れなかったので保存しません")


main()