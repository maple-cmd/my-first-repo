FROM python:3.13-slim

WORKDIR /app

# 必要なパッケージをコピー＆インストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのコードをコピー
COPY . .

# 実行コマンド（例）
CMD ["python", "main.py"]