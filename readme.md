# AI開発者向け　ニュースサマライズ

## 📝 目的
AIに関するニュースは日々目まぐるしくアップデートと新たな追加がなされています。
その中で、AIの開発担当者や開発のマネジメント・コンサルタントをしている人にとって重要な情報とそうでない情報が入り交ざっています。今回のAIでAI開発やマネジメント、コンサルティングをする人に向けた最新情報を定期的に更新し、わかりやすく届けるAPIを構築します。

## 🎯 要求・ゴール
* **定期収集（バッチ）**: 指定したサイトからAIに関する最新のニュースを毎日自動収集し、DBへ蓄積する。
* **データ管理**: 収集したデータを一元管理し、過去のニュースも含めて期間指定で取り出せるようにする。
* **分類とサマライズ**: AIのニュースをカテゴリ分けし、サマリーを作成。
* **優先度決定**: 多くのニュースからAI開発担当やマネジメント担当の役に立つ情報のみをピックアップ。
* **要約文作成**: ピックアップした情報を整理し、文章として返却。


## ⚙️ 要件定義

システムの処理を「データ収集（日次）」と「データ配信（APIリクエスト時）」の2フェーズに分割します。

| 項目 | 内容 |
| :--- | :--- |
| **1. データ収集フェーズ** | **毎日定期実行 (Batch/Cron)** |
| **データソース** | AI関連のニュースを配信しているサイト (RSS/Web) |
| **収集ロジック** | 毎日RSS/サイトを確認し、新規記事を最大10件/サイト程度ピックアップ |
| **前処理** | データ定義の整理、HTMLタグ除去、日付フォーマット統一、重複チェック |
| **格納先** | DynamoDB (時系列でクエリ可能な状態で保存) |
| | |
| **2. データ配信フェーズ** | **ユーザーからのAPIリクエスト時** |
| **ユーザー入力** | 直近何日間のニュースを利用するか (N日) |
| **データ取得** | DynamoDBから、現在日時〜指定日数前までの記事データをクエリ取得 |
| **LLMカテゴライズ** | LLMでタイトル情報からカテゴリ分けと優先順位(スコア)を判定 |
| **情報をサマライズ** | 優先度が高い記事のみURLへアクセスし、情報をLLMでサマライズする |
| **出力形式** | JSON。サマリー、対象記事をカテゴリごとに提示 |


## 🏗️ システムアーキテクチャ

### フェーズ1: 定期データ収集 (Daily Batch)
```text
[CloudWatch Events / Cron]
│ 1日1回トリガー
▼
[収集用 Lambda]
│ 1. 各RSS/サイトから最新記事をFetch (上限10件/サイト)
│ 2. 前処理 (フォーマット統一)
│ 3. 重複チェック (既にDBにあるURLはスキップ)
▼
[DynamoDB] 🗄️ (蓄積)
│ 保存データ: { URL(ID), タイトル, 概要, 公開日時, サイト名 }

ユーザー (APIクライアント)
│
│ リクエスト: "直近利用日数 (N日)"
▼
[配信重 API Lambda]
│ 1. DynamoDBへクエリ (PublishedAt > Now - N days)
│ → 該当期間の記事リストを取得
│
│ 2. [LLM処理] カテゴリ分類 & 優先度判定
│ → 開発者/コンサル視点でスコアリング
│
│ 3. [スクレイピング & 要約]
│ → 高スコア記事のURLへアクセスし本文取得
│ → LLMで要約作成
▼
[出力モジュール]
JSON形式で「カテゴリごとのサマリーと対象記事」を提示

```

## RSSデータソース定義

各ソースの特性に基づき、収集の重み付けや解析優先度を最適化するためのマスターリストです。

| ID | サイト名 / 運営組織 | カテゴリ | RSSフィードURL |
| :--- | :--- | :--- | :--- |
| 01 | OpenAI News | Model Provider | `https://openai.com/news/rss.xml` |
| 02 | Google Cloud Blog | Cloud Platform | `https://cloudblog.withgoogle.com/rss/` |
| 03 | AWS News Blog (JP) | Cloud Platform | `https://aws.amazon.com/jp/blogs/aws/feed/` |
| 04 | Google Developers Japan | Engineering | `https://developers-jp.googleblog.com/atom.xml` |
| 05 | Mercari Engineering | Tech Blog (Domestic) | `https://engineering.mercari.com/blog/feed.xml` |
| 06 | CyberAgent Developers | Tech Blog (Domestic) | `https://developers.cyberagent.co.jp/blog/feed/` |
| 07 | AI Shift Tech Blog | Tech Blog (Domestic) | `https://www.ai-shift.co.jp/techblog/feed` |
| 08 | Recruit Tech Blog | Tech Blog (Domestic) | `https://recruit-tech.co.jp/blog/feed/` |
| 09 | BrainPad Platinum Data Blog | Tech Blog (Consulting) | `https://blog.brainpad.co.jp/rss` |
| 10 | Zenn (Topic: LLM) | Community | `https://zenn.dev/topics/llm/feed` |
| 11 | ITmedia AI+ | Media | `https://rss.itmedia.co.jp/rss/2.0/aiplus.xml` |
| 12 | ＠IT (Build IT) | Media | `https://atmarkit.itmedia.co.jp/rss/rss.xml` |
| 13 | Medium (@kyakuno) | Expert Blog | `https://medium.com/feed/@kyakuno` |
| 14 | Hugging Face Daily Papers | Research (OSS) | `https://rsshub.app/huggingface/daily-papers` |
| 15 | Preferred Networks Research | Research (Domestic) | `https://research.preferred.jp/feed/` |
| 16 | Google Search Central Blog | SEO/Marketing | `https://feeds.feedburner.com/blogspot/gJZg` |
| 17 | PyTorch Blog | Library/Framework | `https://pytorch.org/feed.xml` |
| 18 | DeepLearning.AI (The Batch) | Education/Trend | `https://www.deeplearning.ai/the-batch/rss` |
| 19 | MIT Technology Review (JP) | Scientific Media | `https://www.technologyreview.jp/feed/` |


### RSSフィードの参考URL
https://note.com/manyamam/n/n05fc8f66886a<br>
https://note.com/eurekachan/n/n0c1c1b8793e2

### やりたいけどRSSがない
https://ai-media-bsg.com/

### アップデート手順
- 修正箇所を修正し、本Gitのmainブランチへデプロイ。すると、各種テストやAWSでのリソース作成などが自動実行される
- 作成したLambda関数のIPアドレスを起動したECSタスクへ変更する
- Lambda関数をデプロイし、テストを実行。問題なければ完了