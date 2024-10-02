# Camp Gear Sale

## 概要

キャンプ用品のセール情報を定期的にXにポストするアプリケーション。
Amazonからセール中の商品を取得し、その商品情報をまとめたポストを作成しXに投稿。

## 機能一覧

- Amazonでセール中のキャンプ用品の商品情報を取得
- 取得した商品情報から必要な情報を抽出、フォーマットしてポストを作成
  - ポストの文字数制限に合わせて商品タイトルを三点リーダで省略
  - 商品URLを`TinyURL`で短縮
  - 商品タイトル中のブランド名にハッシュタグをつける
- 作成したポストをXに投稿する（投稿頻度は`EventBridge Scheduler`で設定）

## 技術スタック

- Amazon ECS
- Amazon ECR
- Amazon EventBridge Scheduler
- AWS Fargate
- AWS Secrets Manager
- Python v3.11.5
- PA-API v5
- X API v2
- Docker v27.1.1

## AWS構成図

![camp-gear-sale-architecture-diagram (1) drawio](https://github.com/user-attachments/assets/18db7d0d-9de3-4c69-a866-579e6978b2ee)

## ディレクトリ構成

```tree
.
├── .dockerignore
├── .env
├── .env.local
├── .env.production
├── .gitignore
├── Dockerfile
├── README.md
├── main.py
├── requirements.txt
└── src
    ├── application
    ├── domain
    ├── infrastructure
    └── tests
```

## 実行方法

1. このリポジトリをクローン
2. 環境変数を`.env`ファイルで設定

    ```env
    # PA-API認証情報
    ACCESS_KEY = {{PA-APIのアクセスキー}}
    SECRET_KEY = {{PA-APIのシークレットキー}}
    ASSOCIATE_ID = {{AmazonアソシエイトのアソシエイトIDもしくはトラッキングID}}
    HOST = 'webservices.amazon.co.jp'
    REGION = 'us-west-2'
    
    # X API認証情報
    CONSUMER_KEY = {{X APIのコンシューマーキー}}
    CONSUMER_SECRET = {{X APIのコンシューマーシークレット}}
    ACCESS_TOKEN = {{X APIのアクセストークン}}
    ACCESS_TOKEN_SECRET = {{X APIのアクセストークンシークレット}}
    
    # ThreadsAPI認証情報
    THREADS_ACCESS_TOKEN = {{ThreadsAPIのアクセストークン}}
    ```

3. Dockerイメージをビルド

    ```bash
    docker build -t camp-gear-sale .
    ```

4. コンテナを起動

    ```bash
    docker run -v ./:/workspace  -itd --name camp-gear-sale camp-gear-sale bash
    ```

5. コンテナにアタッチ

    ```bash
    docker attach camp-gear-sale
    ```

6. プロジェクトルートで下記コマンドを実行

    ```bash
    python main.py
    ```
