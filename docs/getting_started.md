# Getting Started with Shinka QA

このガイドでは、Shinka QAの基本的な使い方を学びます。

## インストール

### 必須要件

- Python 3.11以上
- pip（Pythonパッケージマネージャー）

### インストール方法

```bash
# ソースからインストール
git clone git@github.com:kamigusa/shinka_qa.git
cd shinka-qa
pip install -e .


# PyPIからインストール（公開準備中）
# pip install shinka-qa

```

## クイックスタート

### 1. サンプルプロジェクトで試す

Shinka Qualityには電卓モジュールのサンプルが含まれています。

```bash
# サンプルプロジェクトに移動
cd examples/simple_calculator

# 設定ファイルを確認
cat quality_config.yaml

# テストを評価
shinka-qa evolve --config quality_config.yaml

# 結果を確認
shinka-qa visualize --results-dir results/run_YYYYMMDD_HHMMSS/ --generate-report
```

### 2. あなたのプロジェクトに適用

#### ステップ1: 設定ファイルを作成

プロジェクトのルートディレクトリに`quality_config.yaml`を作成：

```yaml
# テスト対象
target:
  module_path: "src/mymodule.py"
  test_initial_path: "tests/test_mymodule.py"
  seeded_bugs_path: "tests/mymodule_buggy.py"  # オプション

# 適応度関数の重み
fitness_weights:
  coverage: 0.4          # テストカバレッジ
  bug_detection: 0.35    # バグ検出率
  efficiency: 0.15       # 実行効率
  maintainability: 0.1   # コード品質

# 変異戦略
mutation_strategies:
  - "add_edge_cases"
  - "improve_assertions"
  - "add_parametrize"
```

#### ステップ2: ベンチマークを実行

```bash
shinka-qa benchmark --config quality_config.yaml
```

出力例：
```
Running benchmark...
========================================

Benchmark Results:
  Tests Passed: 5
  Tests Failed: 0
  Coverage: 42.5%
  Success: YES
```

#### ステップ3: テストを進化させる

```bash
shinka-qa evolve --config quality_config.yaml --verbose
```

#### ステップ4: 結果を可視化

```bash
shinka-qa visualize --results-dir results/run_YYYYMMDD_HHMMSS/ --generate-report
```

HTMLレポートが生成されます：
- `evolution_report.html` - 詳細なメトリクスレポート
- `lineage_tree.txt` - 進化の系譜
- `metrics.json` - 生データ

## コマンドリファレンス

### evolve

テストスイートを進化させます。

```bash
shinka-qa evolve [OPTIONS]

Options:
  --config PATH          設定ファイルのパス（必須）
  --output-dir PATH      出力ディレクトリ（デフォルト: results/）
  --verbose              詳細ログを表示
  --llm / --no-llm       LLMを使用するかどうか（デフォルト: 無効）
```

**使用例:**
```bash
# テンプレートベースのみ（高速・無料）
shinka-qa evolve --config quality_config.yaml

# LLM使用（高品質なテスト生成）
shinka-qa evolve --config quality_config.yaml --llm
```

### benchmark

初期テストの性能を測定します。

```bash
shinka-qa benchmark [OPTIONS]

Options:
  --config PATH          設定ファイルのパス（必須）
```

### visualize

進化の結果を可視化します。

```bash
shinka-qa visualize [OPTIONS]

Options:
  --results-dir PATH     結果ディレクトリのパス（必須）
  --generate-report      HTMLレポートを生成
```

### validate

テストファイルの妥当性を検証します。

```bash
shinka-qa validate TEST_FILE TARGET_MODULE
```

## 設定ファイルの詳細

### target セクション

```yaml
target:
  module_path: "path/to/module.py"        # テスト対象モジュール
  test_initial_path: "path/to/test.py"    # 初期テストファイル
  seeded_bugs_path: "path/to/buggy.py"    # バグ版（オプション）
```

### fitness_weights セクション

各指標の重みを設定します（合計1.0）：

```yaml
fitness_weights:
  coverage: 0.4          # テストカバレッジの重み
  bug_detection: 0.35    # バグ検出率の重み
  efficiency: 0.15       # 実行効率の重み
  maintainability: 0.1   # コード品質の重み
```

### mutation_strategies セクション

使用する変異戦略のリスト：

```yaml
mutation_strategies:
  - "add_edge_cases"       # エッジケースの追加
  - "improve_assertions"   # アサーションの改善
  - "add_parametrize"      # パラメータ化テストの追加
  - "add_fixtures"         # フィクスチャの追加
  - "add_mocks"            # モックの追加
```

## ベストプラクティス

### 1. バグシーディング

テストの効果を測定するため、意図的にバグを含むバージョンを作成：

```python
# original.py
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

# buggy.py（バグ版）
def divide(a, b):
    # バグ: ゼロチェックが不完全
    if b == 0:
        return 0  # 本来は例外を投げる
    return a / b
```

### 2. 段階的な改善

最初は基本的なテストから始め、徐々に拡張：

1. まず基本機能のテストを作成
2. `shinka-qa benchmark`でベースラインを確認
3. `evolve`コマンドで改善
4. 結果を確認し、必要に応じて設定を調整

### 3. CI/CDとの統合

`.github/workflows/shinka-qa.yml`を追加：

```yaml
name: Quality Check

on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install shinka-qa
      - run: shinka-qa benchmark --config quality_config.yaml
```

## トラブルシューティング

### カバレッジが0%と表示される

- `module_path`が正しいか確認
- テストファイルが`pytest`で実行可能か確認
- `pytest-cov`がインストールされているか確認

### LLMを使用したい場合

```bash
# OpenAI APIキーを設定
export OPENAI_API_KEY="your-api-key"

# LLMクライアントをインストール
pip install "shinka-qa[llm]"
```

設定ファイルに追加：

```yaml
llm:
  provider: "gemini"
  model: "gemini-2.5-flash"
  temperature: 0.7
```

## 次のステップ

- [APIリファレンス](api_reference.md) - 詳細なAPI仕様
- [サンプルプロジェクト](../examples/) - 追加のサンプル
- [コントリビューションガイド](../CONTRIBUTING.md) - 開発に参加

## サポート

問題が発生した場合：

1. [GitHubのIssues](https://github.com/yourusername/shinka-qa/issues)で既存の問題を確認
2. 新しいIssueを作成
3. 以下の情報を含める：
   - Pythonバージョン
   - Shinka Qualityバージョン
   - エラーメッセージ
   - 再現手順
