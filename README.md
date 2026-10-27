# scraping-study

Python で Web スクレイピングの基本を学んだ記録です。
練習用サイト [Books to Scrape](https://books.toscrape.com/) を対象にしています。

## 学んだこと

- 取得（requests）→ 解析（BeautifulSoup）→ 保存（CSV）の基本の型
- next リンクをたどって複数ページを巡回
- robots.txt の自動チェック
- 通信エラー・404 の再試行と、取得済みデータの保護

## ファイル構成

| ファイル | 内容 |
|---|---|
| fetch.py | HTML を取得して表示 |
| parse.py | 題名と値段を抜き出す |
| save_csv.py | 1ページ分を CSV に保存 |
| crawl.py | 複数ページを巡回 |
| crawl_v2.py | 関数に分けて整理＋robots.txt チェック |
| crawl_v3.py | エラー対策を追加（最新版） |
| check_robots.py | robots.txt の読み取り練習 |

## 動かし方（Windows / PowerShell）

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python crawl_v3.py
```

`books_all.csv` が作られます（CSV は Git 管理外）。

## マナー

- 練習用サイト以外では、利用規約と robots.txt を必ず確認する
- 1ページごとに 1 秒以上待つ
- 必要以上のページを取らない（`MAX_PAGES` で制限）
