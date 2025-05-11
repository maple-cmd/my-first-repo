import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# 注文数
num_orders = 10000
# 顧客数（少し少なめにして、結合ミスも含めて練習できるように）
num_customers = 8000

# マスタ候補
categories = ['家電', '食品', '衣類', '書籍', '家具']
payment_methods = ['クレジットカード', '現金', 'PayPay', '楽天ペイ', '銀行振込']
regions = ['東京', '大阪', '名古屋', '札幌', '福岡']
genders = ['男性', '女性', 'その他']

# ランダム日付
def random_date(start_days_ago=365):
    start = datetime.now() - timedelta(days=start_days_ago)
    return start + timedelta(days=random.randint(0, start_days_ago))

### DataFrame①：注文データ（orders_df）
orders_df = pd.DataFrame({
    '注文ID': range(1, num_orders + 1),
    '顧客ID': np.random.randint(1000, 1000 + num_customers, size=num_orders),
    '注文日': [random_date().date() for _ in range(num_orders)],
    '商品ID': np.random.randint(100, 999, size=num_orders),
    'カテゴリ': [random.choice(categories) for _ in range(num_orders)],
    '単価': np.random.randint(500, 20000, size=num_orders),
    '個数': np.random.randint(1, 5, size=num_orders),
    '支払い方法': [random.choice(payment_methods) for _ in range(num_orders)],
    '地域': [random.choice(regions) for _ in range(num_orders)],
})

# 合計金額列を計算
orders_df['合計金額'] = orders_df['単価'] * orders_df['個数']

### DataFrame②：顧客データ（customers_df）
customers_df = pd.DataFrame({
    'customer_id': range(1000, 1000 + num_customers),
    '名前': ['顧客_' + str(i) for i in range(num_customers)],
    '性別': [random.choice(genders) for _ in range(num_customers)],
    '年齢': np.random.randint(18, 70, size=num_customers),
    '登録日': [random_date(730).date() for _ in range(num_customers)],  # 過去2年以内
    '住所_地域': [random.choice(regions) for _ in range(num_customers)],
})

customers_df.to_csv("customers_df.csv", index=False)