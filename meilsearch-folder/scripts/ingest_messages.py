import psycopg2
from meilisearch import Client
import os
from utils import fetch_new_posts, format_posts_for_meili, load_last_ts, save_last_ts, send_to_meili

# PostgreSQL 接続設定
POSTGRES_CONFIG = {
    "host": "postgres",
    "port": 5432,
    "dbname": "mattermost",
    "user": "mm_user",
    "password": "mm_pass"
}

# Meilisearch 接続
MEILI_URL = "http://meilisearch:7700"
MEILI_API_KEY = ""
INDEX_NAME = "messages"

# 差分管理ファイル
LAST_TS_FILE = "last_ts.txt"

# PostgreSQL 接続
conn = psycopg2.connect(**POSTGRES_CONFIG)
cur = conn.cursor()

# Meilisearch 接続
client = Client(MEILI_URL, MEILI_API_KEY)
index = client.index(INDEX_NAME)

# 最終更新タイムスタンプ読み込み
last_ts = load_last_ts(LAST_TS_FILE)

# PostgreSQL から差分取得
rows = fetch_new_posts(cur, last_ts)

# Meilisearch 形式に変換
docs = format_posts_for_meili(rows)

# Meilisearch に投入
send_to_meili(index, docs)

# 最終タイムスタンプ更新
if rows:
    save_last_ts(rows[-1][4], LAST_TS_FILE)

cur.close()
conn.close()