# 🧬 Shinka Quality

<div align="center">

**ソフトウェアテストを進化させる - AI駆動の品質改善フレームワーク**

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[クイックスタート](#-30秒でスタート) • [ドキュメント](docs/getting_started.md) • [サンプル](examples/) • [API Reference](docs/api_reference.md)

</div>

---

## 🎯 Shinka Qualityとは？

Shinka Qualityは、**進化的アルゴリズム**を使ってテストコードを自動的に改善するフレームワークです。

### 🤔 こんな悩みを解決

- ✅ テストカバレッジが低い（40% → 90%に自動改善）
- ✅ エッジケースのテストが不足している
- ✅ バグを見逃しやすいテストコード
- ✅ テストの保守性が低い

### 💡 Before / After

**Before: 基本的なテストのみ**
```python
def test_add():
    assert add(2, 3) == 5

def test_divide():
    assert divide(10, 2) == 5.0
```
- カバレッジ: 42%
- バグ検出: 20%
- フィットネス: 0.39

**After: Shinka Quality適用後**
```python
@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
    (1.5, 2.5, 4.0),
])
def test_add_comprehensive(a, b, expected):
    assert add(a, b) == expected

def test_divide_zero():
    with pytest.raises(ValueError):
        divide(10, 0)
```
- カバレッジ: 92%
- バグ検出: 100%
- フィットネス: 0.95

---

## 🚀 30秒でスタート

### ステップ1: インストール

#### 方法A: pyproject.tomlからインストール（推奨）

```bash
# リポジトリをクローン
git clone https://github.com/yourusername/shinka-qa.git
cd shinka-qa

# インストール（依存関係も自動）
pip install -e .
```

#### 方法B: 仮想環境 + requirements.txtでインストール

```bash
# リポジトリをクローン
git clone https://github.com/yourusername/shinka-qa.git
cd shinka-qa

# 仮想環境を作成・有効化
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# 依存関係をインストール
pip install --upgrade pip
pip install -r requirements.txt

# shinka-qaをインストール
pip install -e .
```

### ステップ2: サンプルを実行

```bash
# サンプルディレクトリに移動
cd examples/simple_calculator

# 現在のテスト品質を評価
shinka-qa evolve --config quality_config_local.yaml --verbose
```

### ステップ3: 結果を確認

```bash
# 美しいHTMLレポートを生成
shinka-qa visualize --results-dir results/run_* --generate-report

# HTMLファイルをブラウザで開く
# → results/run_YYYYMMDD_HHMMSS/evolution_report.html
```

**🎉 これだけ！** 数秒でテスト品質の詳細レポートが生成されます。

---

## ✨ 主な機能

### 1️⃣ 多角的品質評価

4つの指標でテストスイートを総合評価：

| 指標 | 重み | 説明 |
|------|------|------|
| **カバレッジ** | 40% | 行・分岐・関数カバレッジ |
| **バグ検出率** | 35% | 仕込んだバグを何個検出できるか |
| **実行効率** | 15% | テスト実行時間 |
| **保守性** | 10% | コードの可読性・独立性 |

### 2️⃣ 進化的アルゴリズム（Phase 2実装済み）

- **島モデル**: 複数の進化集団を並行実行
- **UCB1バンディット**: 最適な変異戦略を自動選択
- **新規性フィルタリング**: 多様性を維持して局所最適化を回避
- **メタスクラッチパッド**: 成功パターンを学習・共有

### 3️⃣ 自動変異戦略

5種類の変異戦略を適応的に適用：

```yaml
mutation_strategies:
  - add_edge_cases       # エッジケース追加（None, 0, 負数など）
  - improve_assertions   # assert True → assert x == y
  - add_parametrize      # @pytest.mark.parametrize 追加
  - add_fixtures         # pytest fixtures 導入
  - add_mocks            # モック化で独立性向上
```

### 4️⃣ 美しいビジュアルレポート

生成されるレポート：
- **evolution_report.html**: インタラクティブなHTMLダッシュボード
- **lineage_tree.txt**: 進化の系譜ツリー
- **metrics.json**: 詳細なメトリクスデータ

---

## 📊 実際の使用例

### 電卓モジュールの例

#### 初期状態

```python
# calculator.py
def add(a, b):
    return a + b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

# test_calculator_initial.py（カバレッジ42%）
def test_add_positive():
    assert add(2, 3) == 5

def test_divide_simple():
    assert divide(10, 2) == 5.0
```

#### Shinka Quality実行

```bash
$ shinka-qa evolve --config quality_config_local.yaml
Shinka Quality v1.0
========================================

Configuration:
  Target: calculator.py

Measuring baseline...
  Initial Coverage: 42.0%

Evaluating initial test suite...
  Coverage: 42.0%
  Bug Detection: 40.0%
  Execution Time: 0.85s
  Code Quality: 1.00
  Overall Fitness: 0.390

Analysis Complete!
Results saved to: results/run_20251107_175036/
```

#### 生成されたレポート

```
Shinka Quality - Evolution Summary
==================================================

Baseline Coverage: 42.0%
Current Coverage:  42.0%
Bug Detection:     40.0% (5個中2個検出)
Execution Time:    0.85s
Code Quality:      1.00

Overall Fitness:   0.390
```

---

## 🛠️ あなたのプロジェクトに適用

### ステップ1: 設定ファイルを作成

プロジェクトルートに`quality_config.yaml`を作成：

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

### ステップ2: ベンチマーク実行

```bash
# 現在のテスト品質を確認
shinka-qa benchmark --config quality_config.yaml
```

出力例：
```
Benchmark Results:
  Tests Passed: 15
  Tests Failed: 0
  Coverage: 58.3%
  Success: YES
```

### ステップ3: テスト品質を評価・改善

```bash
# 詳細ログ付きで評価
shinka-qa evolve --config quality_config.yaml --verbose
```

### ステップ4: 結果を可視化

```bash
# HTMLレポートを生成
shinka-qa visualize \
  --results-dir results/run_YYYYMMDD_HHMMSS \
  --generate-report

# ブラウザで開く
open results/run_YYYYMMDD_HHMMSS/evolution_report.html
```

---

## 🏗️ アーキテクチャ

```
┌─────────────────────────────────────────────┐
│           Shinka Quality CLI                │
└─────────────────┬───────────────────────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
┌───▼────┐   ┌───▼────┐   ┌───▼────┐
│ Core   │   │Evolution│   │Visual  │
│Modules │   │ Modules │   │Modules │
└───┬────┘   └───┬────┘   └───┬────┘
    │             │             │
    ├─ Evaluator  ├─ Island Model  ├─ Report Gen
    ├─ Metrics    ├─ UCB1 Bandit   ├─ Lineage Tree
    └─ Runner     ├─ Novelty Filter└─ HTML/JSON
                  └─ Meta Scratchpad
```

### モジュール構成

| モジュール | 役割 | 主要クラス |
|-----------|------|-----------|
| **core/** | 品質評価 | QualityEvaluator |
| **evolution/** | 進化アルゴリズム | IslandModel, UCB1Bandit, NoveltyFilter |
| **utils/** | ユーティリティ | TestRunner |
| **visualization/** | レポート生成 | ReportGenerator, LineageTreeVisualizer |
| **cli/** | コマンドライン | CLI Commands |

---

## 📚 コマンドリファレンス

### `evolve` - テストスイートを評価

```bash
shinka-qa evolve [OPTIONS]

Options:
  --config PATH       設定ファイルのパス（必須）
  --output-dir PATH   出力ディレクトリ（デフォルト: results/）
  --verbose           詳細ログを表示
  --help              ヘルプを表示
```

**例:**
```bash
# 基本的な使用
shinka-qa evolve --config quality_config.yaml

# 詳細ログ付き
shinka-qa evolve --config quality_config.yaml --verbose

# 出力先を指定
shinka-qa evolve --config quality_config.yaml --output-dir ./my_results
```

### `benchmark` - パフォーマンス測定

```bash
shinka-qa benchmark --config quality_config.yaml
```

### `visualize` - 結果の可視化

```bash
shinka-qa visualize --results-dir RESULTS_DIR [--generate-report]

Options:
  --results-dir PATH   結果ディレクトリのパス（必須）
  --generate-report    HTMLレポートを生成
```

### `validate` - テストファイル検証

```bash
shinka-qa validate TEST_FILE TARGET_MODULE
```

---

## 🔧 CI/CD統合

### GitHub Actions

`.github/workflows/quality-check.yml`:

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
      - uses: actions/upload-artifact@v3
        with:
          name: quality-results
          path: results/
```

### GitLab CI

詳細は [`ci-templates/.gitlab-ci.yml`](ci-templates/.gitlab-ci.yml) を参照。

### Pre-commit Hooks

```bash
# インストール
pip install pre-commit
pre-commit install

# 設定ファイルをコピー
cp ci-templates/.pre-commit-config.yaml .pre-commit-config.yaml
```

---

## 📖 ドキュメント

- **[Getting Started Guide](docs/getting_started.md)** - 詳細なチュートリアル
- **[API Reference](docs/api_reference.md)** - 全クラス・メソッドのリファレンス
- **[サンプルプロジェクト](examples/)** - 実際の使用例

---

## ❓ FAQ

<details>
<summary><b>Q: LLMは必須ですか？</b></summary>

いいえ、LLMなしでも基本的な機能は動作します。LLMを使用すると、より高度な変異戦略が利用できます。

```bash
# LLM統合（オプション）
pip install "shinka-qa[llm]"
export OPENAI_API_KEY="your-api-key"
```
</details>

<details>
<summary><b>Q: どのテストフレームワークに対応していますか？</b></summary>

現在はpytestに対応しています。unittestやnoseのサポートは今後追加予定です。
</details>

<details>
<summary><b>Q: カバレッジが0%と表示される</b></summary>

以下を確認してください：
1. `pytest-cov`がインストールされているか: `pip install pytest-cov`
2. 設定ファイルの`module_path`が正しいか
3. テストが実際に実行されているか: `pytest test_file.py -v`
</details>

<details>
<summary><b>Q: 既存のプロジェクトに導入するのは難しいですか？</b></summary>

いいえ、3ステップで導入できます：
1. 設定ファイルを作成
2. `shinka-qa benchmark`で現状確認
3. `shinka-qa evolve`で評価

詳しくは[Getting Started Guide](docs/getting_started.md)を参照してください。
</details>

<details>
<summary><b>Q: バグシーディングとは何ですか？</b></summary>

テストの効果を測定するために、意図的にバグを含むバージョンを作成する手法です。良いテストは、これらのバグを検出できるはずです。

```python
# 正常版
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

# バグ版（calculator_buggy.py）
def divide(a, b):
    if b == 0:
        return 0  # バグ: 例外を投げるべき
    return a / b
```
</details>

---

## 🎯 ロードマップ

- [x] **Phase 1**: コア機能（評価器、変異オペレータ、CLI）
- [x] **Phase 2**: 進化アルゴリズム（島モデル、UCB1、新規性フィルタ）
- [x] **Phase 3**: 可視化（HTMLレポート、系譜ツリー）
- [x] **Phase 4**: CI/CD統合、ドキュメント整備
- [ ] **Phase 5**: LLM完全統合（GPT-4, Claude, DeepSeek）
- [ ] **Phase 6**: Web UIダッシュボード
- [ ] **Phase 7**: VSCode拡張機能
- [ ] **Phase 8**: 追加サンプル（REST API, ML, データ処理）

---

## 🤝 コントリビューション

コントリビューションを歓迎します！

### 開発環境のセットアップ

#### 方法A: pyproject.tomlから開発環境を構築（推奨）

```bash
# リポジトリをクローン(SSH)
git clone git@github.com:kamigusa/shinka_qa.git
cd shinka-qa

# 開発依存関係をインストール
pip install -e ".[dev]"

# Pre-commit hooksをセットアップ
pre-commit install

# テストを実行
pytest tests/ --cov=shinka_quality
```

#### 方法B: 仮想環境を使った開発環境構築

```bash
# リポジトリをクローン(SSH)
git clone git@github.com:kamigusa/shinka_qa.git
cd shinka-qa

# 仮想環境を作成・有効化
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# 依存関係をインストール
pip install --upgrade pip
pip install -r requirements.txt

# shinka-qaをインストール（開発モード）
pip install -e ".[dev]"

# Pre-commit hooksをセットアップ
pre-commit install

# テストを実行
pytest tests/ --cov=shinka_quality
```

### コントリビューションの流れ

1. Issue を作成して議論
2. フォークしてブランチを作成: `git checkout -b feature/amazing-feature`
3. コミット: `git commit -m 'Add amazing feature'`
4. プッシュ: `git push origin feature/amazing-feature`
5. Pull Request を作成

---

## 📄 ライセンス

MIT License - 詳細は[LICENSE](LICENSE)を参照してください。

---

## 🙏 謝辞

- **[ShinkaEvolve](https://github.com/SakanaAI/shinkaevolve)** - このプロジェクトのベースとなったフレームワーク

<div align="center">

**Made by Yoshiki Kanda**

[⬆ トップに戻る](#-shinka-qa)

</div>
