#!/usr/bin/env python3
from meilisearch import Client
import time

# Meilisearch に接続
client = Client("http://meili:7700")

# ヘルスチェック
health = client.health()
print("Health:", health)

# インデックス確認 / 作成
index_uid = "test_index"
indexes = client.get_indexes()

# indexes がリストで UID が文字列の場合もあるので、str として判定
existing_uids = [idx['uid'] if isinstance(idx, dict) else idx for idx in indexes]

if index_uid not in existing_uids:
    client.create_index(index_uid)
    print(f"Index '{index_uid}' created.")
else:
    print(f"Index '{index_uid}' already exists.")

# インデックスオブジェクト取得
index = client.index(index_uid)

# ドキュメント追加
docs = [
    {"id": 1, "title": "Hello Meili"},
    {"id": 2, "title": "Test Document"},
    {"id": 3, "title": "Another example"}
]

# ドキュメント追加（非同期）
update = index.add_documents(docs)
# print("Documents added, update ID:", update.update_id)

# 簡易待機
time.sleep(1)

# 検索テスト
results = index.search("Hello")
print("Search results:", results)