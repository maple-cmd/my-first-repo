FROM ubuntu:22.04

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    wget unzip ca-certificates && \
    apt-get clean

# Tableau CLI のバイナリをダウンロード・展開・配置
RUN wget https://downloads.tableau.com/esdalt/tableau-cli/tableau-cli-1.20.0-linux.zip && \
    unzip tableau-cli-1.20.0-linux.zip && \
    mv tableau /usr/local/bin/ && \
    chmod +x /usr/local/bin/tableau

# CLIが動作するか確認用（起動時に --version を表示）
CMD ["tableau", "--version"]