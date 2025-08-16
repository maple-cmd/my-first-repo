#!/usr/bin/env python3
import time
import psycopg2
from meilisearch import Client

# ------------------------
# PostgreSQL 接続確認
# ------------------------
try:
    conn = psycopg2.connect(
        host="host.docker.internal",  # ホスト経由で別 Compose の PostgreSQL に接続
        port=5433,                     # PostgreSQL のホスト公開ポート
        user="mm_user",
        password="mm_pass",
        database="mattermost"
    )
    cur = conn.cursor()
    cur.execute("SELECT 1;")
    print("PostgreSQL connection test passed:", cur.fetchone())
    cur.close()
    conn.close()
except Exception as e:
    print("PostgreSQL connection failed:", e)

# ------------------------
# Meilisearch 接続確認
# ------------------------
try:
    client = Client("http://meili:7700")  # Docker ネットワーク内の Meilisearch コンテナ名
    print("Meilisearch health:", client.health())

    # インデックス確認 / 作成
    index_uid = "test_index"
    indexes = client.get_indexes()
    existing_uids = [idx['uid'] if isinstance(idx, dict) else idx for idx in indexes]

    if index_uid not in existing_uids:
        client.create_index(index_uid)
        print(f"Index '{index_uid}' created.")
    else:
        print(f"Index '{index_uid}' already exists.")

    index = client.index(index_uid)

    # ドキュメント追加
    docs = [
        {"id": 1, "title": "Hello Meili"},
        {"id": 2, "title": "Test Document"}
    ]
    update = index.add_documents(docs)
    print("Documents added, update ID:", update.update_id)

    # 少し待って検索
    time.sleep(1)
    results = index.search("Hello")
    print("Search results:", results)
except Exception as e:
    print("Meilisearch connection failed:", e)