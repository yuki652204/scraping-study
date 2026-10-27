from urllib.robotparser import RobotFileParser       # ① 張り紙を読む係

books = RobotFileParser("https://books.toscrape.com/robots.txt")   # ② どの張り紙か
books.read()                                          # ③ 実際に読みに行く
print("books 2ページ目:", books.can_fetch("*", "https://books.toscrape.com/catalogue/page-2.html"))   # ④

amazon = RobotFileParser("https://www.amazon.co.jp/robots.txt")
amazon.read()
print("amazon ほしい物リスト:", amazon.can_fetch("*", "https://www.amazon.co.jp/gp/wishlist/"))