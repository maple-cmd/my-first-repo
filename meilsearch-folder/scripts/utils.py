import os

def fetch_new_posts(cur, last_ts, batch_size=1000):
    cur.execute("""
        SELECT id, user_id, channel_id, message, create_at
        FROM posts
        WHERE create_at > %s
        ORDER BY create_at ASC
        LIMIT %s
    """, (last_ts, batch_size))
    return cur.fetchall()

def format_posts_for_meili(rows):
    docs = []
    for row in rows:
        docs.append({
            "id": row[0],
            "user_id": row[1],
            "channel_id": row[2],
            "message": row[3],
            "create_at": row[4]
        })
    return docs

def load_last_ts(filename="last_ts.txt"):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return int(f.read().strip())
    return 0

def save_last_ts(ts, filename="last_ts.txt"):
    with open(filename, "w") as f:
        f.write(str(ts))

def send_to_meili(index, docs):
    if not docs:
        print("差分なし")
        return
    res = index.add_documents(docs)
    print(f"追加ドキュメント数: {len(docs)}, updateId: {res['updateId']}")