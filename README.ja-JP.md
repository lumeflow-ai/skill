# Lumeflow Skill Hub

OpenClaw プラットフォーム向けの AI Agent スキルパッケージ。自然言語でやりたいことを伝えるだけで、プロフェッショナルな動画や画像を生成できます——手動操作不要、学習コストゼロ。

本スキルは Agent Skills 仕様に準拠し、対応する AI コーディングアシスタント（Cursor、Claude Code など）で利用できます。

**言語**: [English](README.md) | [中文](README.zh-CN.md) | [日本語](README.ja-JP.md) | [한국어](README.ko-KR.md)

## インストール

OpenClaw で AI にスキルのインストールを依頼してください：

```
このスキルをインストールして：https://github.com/lumeflow-ai/skill
```

## 何ができるの？

スキルをインストールしたら、AI に必要なことを伝えるだけです。以下は例です：

### 一言で创作

| あなたが言うと…… | 得られるもの…… |
|-----------------|---------------|
| "5枚の異なるスタイルの商品写真を生成して" | AI が生成した5枚の画像、バッチ並列生成 |
| "夕焼けのビーチを歩く猫の10秒動画を作って" | AI が生成した動画クリップ |
| "この写真を使って動画を作って" | 画像を参考にした動画生成 |
| "この水筒をファッションモデルに持たせて" | モデルが商品を持つ合成画像 |
| "オレンジ色の猫を描いて、9:16 縦版" | AI が生成した画像 |
| "この商品写真の背景を消して" | きれいな切り抜き PNG |
| "この写真の背景をトロピカルビーチに変えて" | AI が編集した画像 |
| "この参考動画のスタイルを真似た新しい動画を作って" | スタイル転送動画 |

### 使い方

OpenClaw で AI Agent と自然言語で対話するだけです：

- **動画生成** — 「猫がキッチンで料理する動画を生成して、Pixverse C1で、720P、5秒で」
- **画像生成** — 「GPT Image 2でオレンジ色の猫を描いて、9:16縦向き、2K解像度で」
- **画像→動画 / 画像→画像** — 参考画像を送信または説明すると、Agentが自動的にアップロードして入力として使用
- **残高確認** — 「クレジット残高はあとどのくらい？」
- **履歴確認** — 「以前の生成タスクを見せて」

生成前にAgentがパラメータ概要と予想クレジット消費量を表示し、確認後にのみタスクを送信します。

**想像力が唯一の制限です** — 上の例はほんの始まりに過ぎません。画像生成、動画作成などを自由に組み合わせて、想像できるあらゆるワークフローを構築できます。自分の言葉でクリエイティブなビジョンを伝えてください、AIが実現方法を考えます。

## 対応モデル

### 動画モデル

Current catalog: [33 supported video models and parameter rules](references/video-model-catalog.md). Inspect locally with `python scripts/generate.py --action models`.

| モデル | バージョン | 長さ | 解像度 |
|--------|-----------|------|--------|
| Kling | 1.6 / 2.5 / 3.0 | 5/10s; 3.0: 3-15s | 3.0: 720P / 1080P / 4K; others use mode |
| LumeFlow / Pixverse | pix6 (4.0) / pix5 (3.0) / pix4.5 / V5.5 / C1 | 5/8/10s by version; pix6/C1: 2-15s | 360P / 540P / 720P / 1080P by duration |
| Hailuo | 02 / 2.3 / 2.3 Fast | 6/10s | 768P; 6s also 1080P |
| Google Veo | 3.1 / 3.1 Fast | 8s | No resolution parameter |
| Wan | 2.5 / 2.6 / 2.7 | 2.5: 5/10s; 2.6/2.7: 2-15s | 480P / 720P / 1080P by version |
| Seedance | 1.5 Pro / 2.0 / Fast / VIP / VIP Fast / Mini / 2.5 | 1.5: 4-12s; 2.0: 4-15s; 2.5: 4-30s | 480P / 720P; 1.5/2.0/VIP also 1080P |
| Vidu | Q1 / Q2 / Q2 Turbo | Q1: no duration parameter; Q2/Turbo: 5/10s | Q1: no resolution parameter; Q2/Turbo: 540P / 720P / 1080P |
| Sora | 2 / 2 Pro | 10/15s; Pro also 25s | 2: 720P; Pro: 1080P |
| Happy Horse | 1.0 / 1.1 | 3-15s | 720P / 1080P |
| Grok Imagine | 1.5 (image-to-video) | 10/15s | 720P |
| Gemini Omni | Text / single image | 6/8/10s | 720P / 1080P |
| MiniMax | H3 | 4-15s | 768P / 2K |

### 画像モデル

| モデル | バージョン | 解像度 |
|--------|-----------|--------|
| Nano Banana | V1 / V2 / Pro | V1: omitted; V2/Pro: 1K / 2K / 4K by mode |
| Seedream | 4.0 / 5.0 Lite / 5.0 Pro | 4.0: 1K/2K/4K; Lite: 2K/3K; Pro: 1K/2K |
| Kling O1 Image | Image-to-image (38) | 1K / 2K |
| GPT Image | 2 / 2.5 Flare / 2.5 Sunburst | 1K / 2K / 4K; selectable quality |

Image rules: [current image catalog](references/image-model-catalog.md). Inspect with `python scripts/generate.py --action image-models`.

## プロジェクト構成

```
lumeflow-video/
├── SKILL.md                  # スキルマニフェスト (v1.0.0)
├── capabilities/             # 機能定義（ワークフロー、ルール、モデルパラメータ）
│   ├── workflow.md           # 必須7ステップワークフロー
│   ├── rules.md              # 出力フォーマットと対話ルール
│   ├── video.md              # 動画モデルとパラメータ制約
│   ├── image.md              # 画像モデルとパラメータ制約
│   ├── request-templates.md  # JSONリクエストテンプレート
│   ├── result-handling.md    # 結果処理と自動リトライ
│   ├── parameter-flow.md     # パラメータ収集フロー
│   └── upload.md             # ファイルアップロード形式とmedia://プロトコル
├── references/
│   ├── api_reference.md      # APIエンドポイントリファレンスとエラーコード
│   └── ai_models_analysis.md # モデルパラメータの詳細分析
└── scripts/
    ├── image_catalog.py      # Image IDs and request validation
    ├── model_catalog.py      # Current website model IDs and request validation
    ├── generate.py           # メインエントリスクリプト（生成、検索、アップロード、残高）
    ├── login.py              # ブラウザログインフロー
    ├── sign.py               # APIリクエスト署名（MD5）
    ├── write_body.py         # JSONボディライター（UTF-8 BOMなし）
    ├── task_store.py         # ローカルタスクストレージ
    └── product_config.py     # ランタイム設定リゾルバー
```

## 動作環境

- Python 3.10+
- サードパーティーライブラリ不要、標準ライブラリのみ

## License

[Apache-2.0](LICENSE)
