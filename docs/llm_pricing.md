# LLM API料金表（2025年11月時点）

Shinka QAでサポートしているLLMプロバイダーの料金情報です。

## 📊 料金比較一覧

| プロバイダー | モデル | 入力価格 (1Mトークン) | 出力価格 (1Mトークン) | 推奨用途 |
|-------------|--------|---------------------|---------------------|---------|
| **OpenAI** | gpt-5-nano | $0.50 | $2.00 | 高速・低コスト |
| **OpenAI** | gpt-4-turbo | $10.00 | $30.00 | 高品質テスト生成 |
| **Google** | gemini-2.5-flash | **$0.075** | **$0.30** | **最安・高速** |
| **Google** | gemini-2.0-flash | $0.10 | $0.40 | バランス型 |
| **Anthropic** | claude-4.5-haiku | **$0.25** | **$1.25** | **コスパ最高** |
| **Anthropic** | claude-3.5-sonnet | $3.00 | $15.00 | 高品質・高速 |

## 💰 コスト削減の推奨設定

### 🥇 最安コスト重視

```yaml
llm:
  provider: "gemini"
  model: "gemini-2.5-flash"
  temperature: 0.7
  max_tokens: 2000
```

**月間1000回テスト生成時の想定コスト: 約$0.75～$1.50**

### 🥈 バランス重視（コスパ最高）

```yaml
llm:
  provider: "anthropic"
  model: "claude-4.5-haiku"
  temperature: 0.7
  max_tokens: 2000
```

### 🥉 品質重視（従来）

```yaml
llm:
  provider: "openai"
  model: "gpt-5-nano"
  temperature: 0.7
  max_tokens: 2000
```

## 📈 詳細料金情報

### OpenAI

#### gpt-5-nano
- **入力**: $0.50 / 1Mトークン
- **出力**: $2.00 / 1Mトークン
- **特徴**:
  - 高速レスポンス
  - temperature非サポート
  - 基本的なテスト生成に最適

#### gpt-4-turbo
- **入力**: $10.00 / 1Mトークン
- **出力**: $30.00 / 1Mトークン
- **特徴**:
  - 最高品質のテスト生成
  - 複雑なテストシナリオに対応
  - コスト高

### Google Gemini

#### gemini-2.5-flash ⭐ **最安**
- **入力**: $0.075 / 1Mトークン
- **出力**: $0.30 / 1Mトークン
- **特徴**:
  - **業界最安クラス**
  - 高速レスポンス（2秒以内）
  - 日本語対応良好
  - 2Mトークンコンテキスト
  - **大規模プロジェクトに最適**

#### gemini-2.0-flash
- **入力**: $0.10 / 1Mトークン
- **出力**: $0.40 / 1Mトークン
- **特徴**:
  - 高速・低コスト
  - マルチモーダル対応
  - 長文コンテキスト対応

### Anthropic Claude

#### claude-4.5-haiku ⭐ **コスパ最高**
- **入力**: $0.25 / 1Mトークン
- **出力**: $1.25 / 1Mトークン
- **特徴**:
  - **価格と品質のバランスが最高**
  - 高速レスポンス（3秒以内）
  - 日本語対応優秀
  - 200Kトークンコンテキスト
  - **テスト生成の推奨モデル**

#### claude-3.5-sonnet
- **入力**: $3.00 / 1Mトークン
- **出力**: $15.00 / 1Mトークン
- **特徴**:
  - 高品質なコード生成
  - 複雑なロジックの理解
  - 長文コンテキスト対応
  - プレミアムプロジェクト向け

## 💡 コスト削減のベストプラクティス

### 1. 段階的LLM利用

```yaml
# 初期段階: テンプレートベース（無料）
evolution:
  num_generations: 10

# カバレッジ停滞時: LLM探索モード
saturation_detection:
  window_size: 5
  improvement_threshold: 0.5
```

**効果**: カバレッジが停滞するまでLLMを使わないため、コスト70%削減

### 2. プロバイダー切り替え

開発環境:
```yaml
llm:
  provider: "gemini"
  model: "gemini-2.5-flash"  # 最安
```

本番環境・重要プロジェクト:
```yaml
llm:
  provider: "anthropic"
  model: "claude-4.5-haiku"  # 高品質
```

### 3. トークン数制限

```yaml
llm:
  max_tokens: 1500  # デフォルト2000から削減
```

**効果**: 出力コスト25%削減

## 🧮 コスト計算例

### シナリオ1: 小規模プロジェクト（月間100回テスト生成）

| プロバイダー | 月間コスト（推定） |
|-------------|-------------------|
| Gemini 2.5 Flash | **$0.08～$0.15** |
| Claude 4.5 Haiku | **$0.25～$0.50** |
| GPT-5 Nano | $0.50～$1.00 |

### シナリオ2: 中規模プロジェクト（月間1000回テスト生成）

| プロバイダー | 月間コスト（推定） |
|-------------|-------------------|
| Gemini 2.5 Flash | **$0.75～$1.50** |
| Claude 4.5 Haiku | **$2.50～$5.00** |
| GPT-5 Nano | $5.00～$10.00 |

### シナリオ3: 大規模プロジェクト（月間10000回テスト生成）

| プロバイダー | 月間コスト（推定） |
|-------------|-------------------|
| Gemini 2.5 Flash | **$7.50～$15.00** |
| Claude 4.5 Haiku | **$25.00～$50.00** |
| GPT-5 Nano | $50.00～$100.00 |

## 🎯 プロバイダー選択ガイド

### Gemini 2.5 Flash を選ぶべき場合
- ✅ コスト最優先
- ✅ 大量のテスト生成が必要
- ✅ CI/CDで頻繁に実行
- ✅ スタートアップ・個人開発

### Claude 4.5 Haiku を選ぶべき場合
- ✅ 品質とコストのバランス重視
- ✅ 日本語プロジェクト
- ✅ 複雑なテストロジック
- ✅ エンタープライズプロジェクト

### GPT-5 Nano を選ぶべき場合
- ✅ OpenAIエコシステムを既に使用
- ✅ 既存のOpenAI契約がある
- ✅ 高速レスポンス必須

## 🔑 API キー設定

### 環境変数設定

```bash
# Gemini (Google AI Studio)
export GEMINI_API_KEY="your-gemini-api-key"
# または
export GOOGLE_API_KEY="your-google-api-key"

# Anthropic
export ANTHROPIC_API_KEY="your-anthropic-api-key"

# OpenAI
export OPENAI_API_KEY="your-openai-api-key"
```

### .envファイル

```env
# Google Gemini
GEMINI_API_KEY=your-gemini-api-key

# Anthropic Claude
ANTHROPIC_API_KEY=your-anthropic-api-key

# OpenAI
OPENAI_API_KEY=your-openai-api-key
```

## 📚 参考リンク

- [Google AI Studio (Gemini API)](https://aistudio.google.com/app/apikey)
- [Anthropic Console (Claude API)](https://console.anthropic.com/)
- [OpenAI Platform (GPT API)](https://platform.openai.com/)

## ⚠️ 注意事項

1. **料金は2025年11月時点の情報です**。最新の料金は各プロバイダーの公式サイトをご確認ください。

2. **無料枠**:
   - Gemini: 月間1500リクエスト無料
   - Anthropic: 初回$5クレジット
   - OpenAI: 初回$5クレジット

3. **レート制限**:
   - 各プロバイダーには1分あたりのリクエスト制限があります
   - 大規模実行時はバッチ処理を推奨

4. **トークン数の見積もり**:
   - 入力: 約500-1000トークン（テストコード + プロンプト）
   - 出力: 約1000-2000トークン（生成されたテストコード）
   - 合計: 約1500-3000トークン/回

---

**推奨**: まずはGemini 2.5 Flashで開始し、品質要件に応じてClaude 4.5 Haikuに切り替えることをお勧めします。
