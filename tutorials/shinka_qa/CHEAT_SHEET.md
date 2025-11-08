# Shinka QA チートシート

**最終更新**: 2025-11-07
**バージョン**: 1.0

このチートシートは、Shinka QAの主要なコマンド、設定、パターンを素早く参照するためのものです。

---

## 📋 目次

1. [インストール](#インストール)
2. [基本コマンド](#基本コマンド)
3. [設定ファイル](#設定ファイル)
4. [重みパターン](#重みパターン)
5. [プロジェクトサイズ別設定](#プロジェクトサイズ別設定)
6. [トラブルシューティング](#トラブルシューティング)
7. [ベストプラクティス](#ベストプラクティス)

---

## ⚡ インストール

### クイックインストール

```bash
# 1. リポジトリをクローン
git clone https://github.com/yourusername/shinka-qa.git
cd shinka-qa

# 2. インストール
pip install -e .

# 3. 確認
shinka-qa --version
```

### 仮想環境を使用

```bash
# 仮想環境を作成
python -m venv venv

# アクティベート
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# インストール
pip install -e .
```

---

## 🚀 基本コマンド

### ヘルプ

```bash
# 全体のヘルプ
shinka-qa --help

# サブコマンドのヘルプ
shinka-qa evolve --help
```

### バージョン確認

```bash
shinka-qa --version
```

### ベンチマーク実行

```bash
# 現在のテスト品質を測定
shinka-qa benchmark --config quality_config.yaml
```

### 進化実行

```bash
# 基本
shinka-qa evolve --config quality_config.yaml

# 詳細表示
shinka-qa evolve --config quality_config.yaml --verbose

# 出力先指定
shinka-qa evolve --config quality_config.yaml --output results/custom/
```

### 結果の可視化

```bash
# HTMLレポート生成
shinka-qa visualize \
  --results-dir results/run_20251107_123456/ \
  --generate-report

# レポートを開く
open results/run_20251107_123456/evolution_report.html  # Mac
start results/run_20251107_123456/evolution_report.html  # Windows
```

### 設定のバリデーション

```bash
# 設定ファイルをチェック
shinka-qa validate --config quality_config.yaml
```

---

## 📝 設定ファイル

### 最小構成

```yaml
# quality_config.yaml

target:
  module: src/

test:
  initial_file: tests/test_main.py
  framework: pytest
  coverage_tool: pytest-cov

fitness:
  weights:
    coverage: 0.4
    bug_detection: 0.3
    execution_time: 0.2
    code_quality: 0.1

evolution:
  num_generations: 5
  population_per_island: 6
  num_islands: 4

output:
  results_dir: results/
```

### 完全な設定例

```yaml
target:
  module: src/
  exclude:
    - __pycache__
    - tests/
    - migrations/
    - venv/
    - .venv/

test:
  initial_file: tests/test_comprehensive.py
  framework: pytest
  coverage_tool: pytest-cov

fitness:
  weights:
    coverage: 0.4
    bug_detection: 0.3
    execution_time: 0.2
    code_quality: 0.1

evolution:
  num_generations: 5
  population_per_island: 6
  num_islands: 4
  mutation_strategies:
    - add_edge_case
    - parameterize_test
    - add_error_handling
    - add_assertion
  early_stopping:
    enabled: true
    patience: 3
    min_improvement: 0.01

output:
  results_dir: results/
  save_intermediate: true
  generate_report: true
```

---

## ⚖️ 重みパターン

### パターン1: デフォルト（バランス型）

```yaml
fitness:
  weights:
    coverage: 0.4
    bug_detection: 0.3
    execution_time: 0.2
    code_quality: 0.1
```

**使用場面**: 特定の優先順位がない場合

**期待される結果**:
- カバレッジ: 良好
- バグ検出: 良好
- 実行時間: 適度
- コード品質: 最低限

---

### パターン2: カバレッジ重視

```yaml
fitness:
  weights:
    coverage: 0.7
    bug_detection: 0.15
    execution_time: 0.1
    code_quality: 0.05
```

**使用場面**:
- カバレッジ目標がある（例: 90%以上）
- リファクタリング前の安全網作り
- コードレビューで求められる

**期待される結果**:
- カバレッジ: 95%+
- バグ検出: やや低下
- 実行時間: 増加
- テスト数: 大幅増加

---

### パターン3: バグ検出重視

```yaml
fitness:
  weights:
    coverage: 0.2
    bug_detection: 0.6
    execution_time: 0.1
    code_quality: 0.1
```

**使用場面**:
- 本番環境でバグが頻発
- セキュリティクリティカル
- バグバウンティプログラム

**期待される結果**:
- カバレッジ: やや低下
- バグ検出: 完璧（1.00）
- エラーハンドリング: 充実
- 境界値テスト: 増加

---

### パターン4: 実行速度重視

```yaml
fitness:
  weights:
    coverage: 0.3
    bug_detection: 0.3
    execution_time: 0.3
    code_quality: 0.1
```

**使用場面**:
- CI/CDで頻繁に実行
- フィードバックループ短縮
- テスト実行が遅い

**期待される結果**:
- カバレッジ: やや低下（85%程度）
- バグ検出: 良好
- 実行時間: 半減
- テストの効率: 向上

---

### パターン5: コード品質重視

```yaml
fitness:
  weights:
    coverage: 0.3
    bug_detection: 0.3
    execution_time: 0.1
    code_quality: 0.3
```

**使用場面**:
- テストコードの保守性重視
- チームでテスト共有
- 長期メンテナンス

**期待される結果**:
- カバレッジ: やや低下
- バグ検出: 良好
- テストの可読性: 向上
- パラメータ化: 積極活用

---

## 📊 プロジェクトサイズ別設定

### 小規模（100-500行）

```yaml
evolution:
  num_generations: 3
  population_per_island: 4
  num_islands: 2

fitness:
  weights:
    coverage: 0.5      # カバレッジ重視
    bug_detection: 0.3
    execution_time: 0.1
    code_quality: 0.1
```

**実行時間**: 1分以内
**目標カバレッジ**: 95%+

---

### 中規模（500-5000行）

```yaml
evolution:
  num_generations: 5
  population_per_island: 6
  num_islands: 4

fitness:
  weights:
    coverage: 0.4      # バランス型
    bug_detection: 0.3
    execution_time: 0.2
    code_quality: 0.1
```

**実行時間**: 2-5分
**目標カバレッジ**: 85%+

---

### 大規模（5000行以上）

```yaml
evolution:
  num_generations: 10
  population_per_island: 8
  num_islands: 8

fitness:
  weights:
    coverage: 0.3
    bug_detection: 0.4  # バグ検出重視
    execution_time: 0.2
    code_quality: 0.1
```

**実行時間**: 15-30分
**目標カバレッジ**: 80%+

---

## 🔧 トラブルシューティング

### 問題: コマンドが見つからない

```
shinka-qa: command not found
```

**解決策**:

```bash
# PATHを確認
echo $PATH

# または、フルパスで実行
python -m shinka_quality.cli.main --version

# または、仮想環境を再アクティベート
source venv/bin/activate
```

---

### 問題: 重みの合計エラー

```
Error: Fitness weights must sum to 1.0 (current sum: 0.9)
```

**解決策**:

```python
# 正規化スクリプト
weights = {'coverage': 0.5, 'bug_detection': 0.3, 'execution_time': 0.2, 'code_quality': 0.1}
total = sum(weights.values())
normalized = {k: v/total for k, v in weights.items()}

# 出力
for k, v in normalized.items():
    print(f"{k}: {v:.2f}")
```

---

### 問題: 実行が遅すぎる

```
Evolution took 30 minutes...
```

**解決策1**: 世代数を減らす

```yaml
evolution:
  num_generations: 3  # 10 → 3
```

**解決策2**: 早期停止を有効化

```yaml
evolution:
  early_stopping:
    enabled: true
    patience: 3
    min_improvement: 0.01
```

---

### 問題: カバレッジが上がらない

```
Initial: 35%
Final: 38% (+3%)
```

**原因と解決策**:

1. **世代数が少ない**
   ```yaml
   evolution:
     num_generations: 10  # 5 → 10
   ```

2. **カバレッジの重みが低い**
   ```yaml
   fitness:
     weights:
       coverage: 0.7  # 0.4 → 0.7
   ```

3. **初期テストが高品質**
   - これ以上の改善が難しい場合もある
   - 目標を再評価

---

### 問題: メモリ不足

```
MemoryError: Unable to allocate...
```

**解決策**:

```yaml
evolution:
  population_per_island: 4  # 6 → 4
  num_islands: 2  # 4 → 2
```

---

## ✅ ベストプラクティス

### 1. 段階的な適用

```bash
# Step 1: コアモジュールから開始
target:
  module: src/core/

# Step 2: 全モジュールに拡大
target:
  module: src/

# Step 3: レガシーも含める
target:
  module: src/
  exclude:
    - __pycache__
```

---

### 2. バージョン管理

```bash
# 設定ファイルをGit管理
git add quality_config.yaml
git commit -m "Add Shinka QA config"

# 結果はGit管理しない
echo "results/" >> .gitignore
```

---

### 3. CI/CD統合

```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'

      - name: Install Shinka QA
        run: pip install shinka-qa

      - name: Run evolution
        run: shinka-qa evolve --config quality_config.yaml

      - name: Check coverage
        run: |
          coverage=$(python -c "import json; print(json.load(open('results/latest/metrics.json'))['final_metrics']['coverage'])")
          if (( $(echo "$coverage < 80" | bc -l) )); then
            echo "Coverage below 80%: $coverage"
            exit 1
          fi
```

---

### 4. 結果の保存

```bash
# 日付付きディレクトリにコピー
DATE=$(date +%Y%m%d)
cp -r results/run_* results/archive/${DATE}/

# または、Git LFSで管理
git lfs track "results/*.json"
git add results/metrics.json
git commit -m "Add evolution results"
```

---

### 5. チーム共有

```bash
# 設定ファイルをチーム共有
git add quality_config.yaml
git commit -m "Update Shinka QA config for Project X"
git push

# レポートをSlackに投稿
shinka-qa visualize --results-dir results/latest/
curl -F file=@results/latest/evolution_report.html \
     -F "initial_comment=Coverage improved to 92%!" \
     https://slack.com/api/files.upload
```

---

## 📌 クイックリファレンス

### よく使うコマンド

| コマンド | 用途 |
|---------|------|
| `shinka-qa --version` | バージョン確認 |
| `shinka-qa benchmark` | ベンチマーク実行 |
| `shinka-qa evolve` | 進化実行 |
| `shinka-qa visualize` | 結果可視化 |
| `shinka-qa validate` | 設定検証 |

### 設定項目

| 項目 | デフォルト | 範囲 |
|------|-----------|------|
| `num_generations` | 5 | 1-20 |
| `population_per_island` | 6 | 2-20 |
| `num_islands` | 4 | 1-16 |
| `coverage` weight | 0.4 | 0.0-1.0 |
| `bug_detection` weight | 0.3 | 0.0-1.0 |

### ショートカット

```bash
# エイリアスを設定
alias sq='shinka-qa'
alias sqb='shinka-qa benchmark --config quality_config.yaml'
alias sqe='shinka-qa evolve --config quality_config.yaml --verbose'
alias sqv='shinka-qa visualize --results-dir results/run_* --generate-report'

# 使用例
sqb  # ベンチマーク実行
sqe  # 進化実行
sqv  # 可視化
```

---

## 🔗 リンク

- **GitHub**: https://github.com/yourusername/shinka-qa
- **チュートリアル**: [tutorials/README.md](README.md)

---

## 📄 設定テンプレート集

### テンプレート1: 新規プロジェクト

```yaml
# プロジェクト開始時
target:
  module: src/

test:
  initial_file: null  # ゼロから生成
  framework: pytest
  coverage_tool: pytest-cov

fitness:
  weights:
    coverage: 0.6     # カバレッジ重視
    bug_detection: 0.25
    execution_time: 0.1
    code_quality: 0.05

evolution:
  num_generations: 3
  population_per_island: 4
  num_islands: 2
```

---

### テンプレート2: レガシープロジェクト

```yaml
# レガシーコードのテスト追加
target:
  module: src/
  exclude:
    - __pycache__
    - tests/
    - legacy/deprecated/  # 非推奨部分は除外

test:
  initial_file: tests/test_minimal.py
  framework: pytest
  coverage_tool: pytest-cov

fitness:
  weights:
    coverage: 0.4
    bug_detection: 0.35  # バグ検出も重要
    execution_time: 0.15
    code_quality: 0.1

evolution:
  num_generations: 8   # 多めに
  population_per_island: 8
  num_islands: 6
```

---

### テンプレート3: CI/CD統合

```yaml
# CI/CDで実行する設定
target:
  module: src/

test:
  initial_file: tests/test_suite.py
  framework: pytest
  coverage_tool: pytest-cov

fitness:
  weights:
    coverage: 0.4
    bug_detection: 0.3
    execution_time: 0.25  # 実行速度を考慮
    code_quality: 0.05

evolution:
  num_generations: 5
  population_per_island: 6
  num_islands: 4
  early_stopping:
    enabled: true
    patience: 2      # 早めに停止
    min_improvement: 0.02

output:
  results_dir: ci_results/
  save_intermediate: false  # ディスク節約
  generate_report: true
```

---

## 💡 最後のヒント

### 成功のための3つのルール

1. **小さく始める**: まずは小規模モジュールで試す
2. **測定する**: Before/Afterを必ず記録
3. **共有する**: チームに成果を報告

### よくある間違い

❌ **間違い**: 最初から全モジュールに適用
✅ **正解**: コアモジュールから段階的に

❌ **間違い**: デフォルト設定で満足
✅ **正解**: プロジェクトに合わせてカスタマイズ

❌ **間違い**: 生成されたテストをそのまま使用
✅ **正解**: レビューして理解してから使用

---

**このチートシートを印刷して手元に置いておきましょう！**

---

**作成日**: 2025-11-07
**更新日**: 2025-11-07
**バージョン**: 1.0
