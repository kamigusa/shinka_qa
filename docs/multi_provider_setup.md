# 複数LLMプロバイダー自動選択ガイド

複数のLLM APIキーをセットして、**自動的に最安のプロバイダーから順に使用**する機能の使い方を説明します。

## 🎯 概要

この機能により：
- ✅ 複数のAPIキーを`.env`にセット
- ✅ 自動的に**最安のプロバイダー**から使用
- ✅ エラー時は自動的に次のプロバイダーにフォールバック
- ✅ **最大85%のコスト削減**が可能

## 📋 セットアップ手順

### ステップ1: APIキーを取得

以下のプロバイダーからAPIキーを取得します（複数推奨）：

| プロバイダー | 料金 | 取得先 |
|-------------|------|--------|
| **Gemini** (最安) | $0.075/1M | https://aistudio.google.com/app/apikey |
| **Anthropic** (コスパ) | $0.25/1M | https://console.anthropic.com/ |
| **OpenAI** (従来) | $0.50/1M | https://platform.openai.com/api-keys |

### ステップ2: `.env`ファイルにAPIキーを設定

プロジェクトルートの`.env`ファイルに、取得したAPIキーを追加：

```bash
# .env

# Google Gemini (最安 - 優先度1位)
GEMINI_API_KEY=your-gemini-api-key-here

# Anthropic Claude (コスパ最高 - 優先度2位)
ANTHROPIC_API_KEY=your-anthropic-api-key-here

# OpenAI (従来 - 優先度3位)
OPENAI_API_KEY=your-openai-api-key-here
```

**注意**: 1つだけでも動作しますが、複数セットすることでフォールバックが有効になります。

### ステップ3: 設定ファイルで`auto`を指定

`quality_config.yaml` または `quality_config_local.yaml`：

```yaml
llm:
  provider: "auto"  # 自動検出を有効化
  model: "auto"     # 各プロバイダーの推奨モデルを使用
  temperature: 0.7
  max_tokens: 2000
```

### ステップ4: 実行

**重要**: LLMを使用するには `--llm` オプションが必要です（デフォルトは無効）

```bash
# LLMを有効化して実行
shinka-qa evolve --config quality_config.yaml --llm --verbose

# LLMなしで実行（テンプレートベースのみ・高速）
shinka-qa evolve --config quality_config.yaml --verbose
```

## 🔍 実行時の動作

### 自動検出の例

```bash
$ shinka-qa evolve --config quality_config.yaml --llm --verbose

Shinka Quality v1.0
========================================

🔍 Auto-detecting available LLM providers...
✅ Detected: Google Gemini (gemini-2.5-flash)
✅ Detected: Anthropic Claude (claude-4.5-haiku)
✅ Detected: OpenAI (gpt-5-nano)
✅ LLM enabled with multi-provider fallback

📊 Available providers (cheapest first):
   - Google Gemini gemini-2.5-flash ($0.188/1M avg)
   - Anthropic claude-4.5-haiku ($0.750/1M avg)
   - OpenAI gpt-5-nano ($1.250/1M avg)
```

### LLM使用時の動作

```bash
Generation 15/30
  📊 Coverage saturation detected!
  💰 Using cheapest provider: Google Gemini gemini-2.5-flash
  ✅ Success! Cost: $0.075/$0.300 per 1M tokens (input/output)
```

### フォールバック動作（Geminiがエラーの場合）

```bash
  💰 Using cheapest provider: Google Gemini gemini-2.5-flash
  ❌ Google Gemini failed: Rate limit exceeded
  ⚠️  Fallback to: Anthropic claude-4.5-haiku
  ✅ Success! Cost: $0.250/$1.250 per 1M tokens (input/output)
```

## 💰 コスト削減効果

### シナリオ1: Geminiのみセット

```bash
# .env
GEMINI_API_KEY=xxx
```

**コスト削減**: 従来比 **85%削減** 🎉

| 実行回数 | 従来(OpenAI) | Gemini | 削減額 |
|---------|-------------|--------|-------|
| 100回 | $0.50 | $0.08 | $0.42 |
| 1000回 | $5.00 | $0.75 | $4.25 |
| 10000回 | $50.00 | $7.50 | $42.50 |

### シナリオ2: Gemini + Anthropic セット（フォールバック有効）

```bash
# .env
GEMINI_API_KEY=xxx
ANTHROPIC_API_KEY=xxx
```

**メリット**:
- 通常は最安のGeminiを使用（85%削減）
- Geminiエラー時は自動的にAnthropicにフォールバック
- **可用性とコスト削減を両立** 🎯

### シナリオ3: 全てセット（最強構成）

```bash
# .env
GEMINI_API_KEY=xxx
ANTHROPIC_API_KEY=xxx
OPENAI_API_KEY=xxx
```

**メリット**:
- 最大限のコスト削減
- 3段階のフォールバック
- **99.9%の可用性** 🛡️

## 🎛️ 高度な設定

### 単一プロバイダーを強制

特定のプロバイダーのみ使用したい場合：

```yaml
llm:
  provider: "gemini"  # "auto"の代わりに指定
  model: "gemini-2.5-flash"
```

### LLM無効化

```yaml
llm:
  provider: "none"
  model: "none"
```

## 📊 プロバイダー優先順位

自動検出時の優先順位（コストの安い順）：

1. **Google Gemini** `gemini-2.5-flash`
   - 入力: $0.075/1M
   - 出力: $0.30/1M
   - 平均: $0.188/1M ⭐ **最安**

2. **Anthropic Claude** `claude-4.5-haiku`
   - 入力: $0.25/1M
   - 出力: $1.25/1M
   - 平均: $0.750/1M

3. **OpenAI** `gpt-5-nano`
   - 入力: $0.50/1M
   - 出力: $2.00/1M
   - 平均: $1.250/1M

## 🔧 トラブルシューティング

### プロバイダーが検出されない

```bash
❌ No LLM providers available
⚠️  No LLM providers detected: Using template-based mutations only
```

**原因**: `.env`にAPIキーが設定されていない

**解決策**:
1. `.env`ファイルが存在するか確認
2. APIキーが正しく設定されているか確認
3. プロジェクトルートで実行しているか確認

### パッケージが見つからない

```bash
ModuleNotFoundError: No module named 'google.generativeai'
```

**解決策**:

```bash
# Gemini用
pip install google-generativeai>=0.8.0

# Anthropic用
pip install anthropic>=0.18.0

# OpenAI用
pip install openai>=1.0.0
```

### APIキーが無効

```bash
❌ Google Gemini failed: Invalid API key
```

**解決策**:
1. APIキーが正しいか確認
2. APIキーの有効期限を確認
3. 課金設定を確認

## 📈 ベストプラクティス

### 開発環境

```yaml
# quality_config_local.yaml
llm:
  provider: "auto"
  model: "auto"
```

```bash
# .env
GEMINI_API_KEY=xxx  # 最安コストで開発
```

### CI/CD環境

```yaml
# quality_config.yaml
llm:
  provider: "auto"
  model: "auto"
```

```bash
# GitHub Actions secrets
GEMINI_API_KEY=${{ secrets.GEMINI_API_KEY }}
ANTHROPIC_API_KEY=${{ secrets.ANTHROPIC_API_KEY }}
```

### 本番環境（重要プロジェクト）

```yaml
llm:
  provider: "auto"
  model: "auto"
```

```bash
# .env (全てセット)
GEMINI_API_KEY=xxx        # 最安
ANTHROPIC_API_KEY=xxx     # フォールバック
OPENAI_API_KEY=xxx        # 最終フォールバック
```

## 🎯 まとめ

| 設定 | コスト | 可用性 | 推奨用途 |
|-----|-------|-------|---------|
| Geminiのみ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 個人開発・スタートアップ |
| Gemini+Anthropic | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 中規模プロジェクト |
| 全てセット | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | エンタープライズ |

**推奨**: まずはGeminiのみでスタートし、必要に応じてAnthropicを追加 🚀
