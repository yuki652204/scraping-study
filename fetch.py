import requests                                  # ① 道具箱からrequestsを取り出す

url = "https://books.toscrape.com/"              # ② 行き先（練習用の架空の本屋さん）
response = requests.get(url, timeout=10)         # ③ ページをください、とお願いする

print("ステータス:", response.status_code)        # ④ お店の返事（200なら成功）
print("文字数:", len(response.text))              # ⑤ もらったHTMLの長さ
print(response.text[:300])                       # ⑥ HTMLの最初の300文字だけ見る