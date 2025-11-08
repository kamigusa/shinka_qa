# Part 11: 実践ハンズオン - 電卓アプリ

**所要時間**: 45分
**難易度**: 初級〜中級
**前提知識**: Part 0-3完了
**使用例**: `examples/simple_calculator`

---

## 🎯 このパートで学ぶこと

1. simple_calculatorプロジェクトの完全な進化プロセス
2. 初期カバレッジ42%から90%超への改善
3. バグ検出率の向上
4. 具体的な変異戦略の効果測定

---

## 📂 プロジェクト概要

### simple_calculatorとは

基本的な算術演算を実装した電卓モジュール。Shinka QAの学習に最適な小規模サンプルです。

**機能**:
- 加算 (add)
- 減算 (subtract)
- 乗算 (multiply)
- 除算 (divide)
- べき乗 (power)
- 階乗 (factorial)
- 素数判定 (is_prime)

**ファイル構成**:
```
examples/simple_calculator/
├── calculator.py              # テスト対象コード (約100行)
├── calculator_buggy.py        # バグ版 (5つのバグ)
├── test_calculator_initial.py # 初期テスト (カバレッジ 42%)
└── quality_config.yaml        # 設定ファイル
```

---

## 🚀 ステップ1: 初期状態の確認 (5分)

### 1.1 プロジェクトディレクトリに移動

```bash
cd examples/simple_calculator
```

### 1.2 初期テストを実行

```bash
pytest test_calculator_initial.py -v
```

**期待される出力**:
```
test_calculator_initial.py::test_add_positive PASSED
test_calculator_initial.py::test_subtract_positive PASSED
test_calculator_initial.py::test_multiply PASSED
test_calculator_initial.py::test_divide_simple PASSED
test_calculator_initial.py::test_power_simple PASSED

============================== 5 passed in 0.03s ==============================
```

### 1.3 初期カバレッジを測定

```bash
pytest test_calculator_initial.py --cov=calculator --cov-report=term-missing
```

**期待される出力**:
```
Name            Stmts   Miss  Cover   Missing
---------------------------------------------
calculator.py      42     24    42%   15-18, 25-28, 35-42, 50-56
---------------------------------------------
TOTAL              42     24    42%
```

**分析**:
- ✅ 実装: 5つのテスト
- ❌ カバレッジ: わずか42%
- ❌ 未テスト: エッジケース、エラーハンドリング
- ❌ バグ検出: 不明

---

## 🧬 ステップ2: ベンチマーク実行 (5分)

### 2.1 初期性能を測定

```bash
shinka-qa benchmark --config quality_config.yaml
```

**期待される出力**:
```
🧬 Shinka Quality Benchmark
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Configuration:
  Target Module: calculator.py
  Initial Test: test_calculator_initial.py
  Seeded Bugs: calculator_buggy.py (5 bugs)

📊 Running initial benchmark...

Initial Metrics:
  Tests Passed: 5
  Tests Failed: 0
  Coverage: 42.5%

Bug Detection (against buggy version):
  Tests Passed: 3
  Tests Failed: 2
  Bugs Detected: 2/5 (40%)

Execution Time: 0.08s
Code Quality: 0.65/1.0

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Benchmark Complete!

Baseline established:
  Coverage: 42.5%
  Bug Detection: 40%
  Quality Score: 0.65
```

**重要な気づき**:
- 初期テストは5つのバグのうち2つしか検出できない
- カバレッジが低いため多くの潜在バグを見逃している

---

## ⚙️ ステップ3: 設定ファイルの確認 (5分)

### 3.1 quality_config.yamlを開く

```bash
cat quality_config.yaml
```

```yaml
# Shinka Quality 設定ファイル

# テスト対象
target:
  module_path: "calculator.py"
  test_initial_path: "test_calculator_initial.py"
  seeded_bugs_path: "calculator_buggy.py"

# 適応度関数の重み
fitness_weights:
  coverage: 0.4          # テストカバレッジ
  bug_detection: 0.35    # バグ検出率
  efficiency: 0.15       # 実行効率
  maintainability: 0.1   # コード品質

# 進化パラメータ
evolution:
  generations: 30              # 世代数
  population_size: 20          # 各島の個体数
  num_islands: 4               # 島の数
  migration_interval: 10       # 移住間隔（世代）
  migration_rate: 0.1          # 移住率
  elite_ratio: 0.3             # エリート選択比率

# 変異戦略
mutation_strategies:
  - "add_edge_cases"
  - "improve_assertions"
  - "add_parametrize"
  - "add_fixtures"
  - "add_mocks"

# 実行制限
limits:
  max_test_time: 10.0          # 単一テストの最大実行時間（秒）
  max_total_time: 300.0        # 全体の最大実行時間（秒）
  max_test_file_size: 5000     # テストファイルの最大行数

# 出力
output:
  results_dir: "results/"
  save_all_generations: true
  visualization: true
```

### 3.2 設定のポイント

**適応度の重み**:
- `coverage: 0.4` - カバレッジを最重視
- `bug_detection: 0.35` - バグ検出も重要
- 小規模プロジェクトに適したバランス

**変異戦略**:
- `add_edge_cases` - 境界値テストを追加
- `improve_assertions` - アサーションを強化
- `add_parametrize` - パラメータ化テスト

---

## 🧪 ステップ4: テスト進化の実行 (10分)

### 4.1 進化を開始

```bash
shinka-qa evolve --config quality_config.yaml --verbose
```

### 4.2 進行状況の観察

**Generation 1-5**: 初期変異
```
Generation 1/30:
  Island 0: Coverage=45.2% Bugs=2/5 Fitness=0.42
  Island 1: Coverage=48.1% Bugs=2/5 Fitness=0.51 ⭐
  Island 2: Coverage=43.7% Bugs=1/5 Fitness=0.38
  Island 3: Coverage=46.9% Bugs=2/5 Fitness=0.48
  Best: Island 1 (Fitness=0.51)
```

**Generation 5-10**: エッジケース追加
```
Generation 5/30:
  Island 0: Coverage=58.3% Bugs=3/5 Fitness=0.67
  Island 1: Coverage=62.5% Bugs=3/5 Fitness=0.71
  Island 2: Coverage=55.1% Bugs=2/5 Fitness=0.59
  Island 3: Coverage=60.2% Bugs=4/5 Fitness=0.72 ⭐
  Best: Island 3 (Fitness=0.72)

  💡 Insight: add_edge_cases strategy improved coverage by 15%
```

**Generation 10**: 島間移住
```
Generation 10/30 [Migration]:
  🔄 Migrating top solutions between islands...
  Island 0: Coverage=71.2% Bugs=4/5 Fitness=0.81
  Island 1: Coverage=68.9% Bugs=4/5 Fitness=0.78
  Island 2: Coverage=70.5% Bugs=3/5 Fitness=0.75
  Island 3: Coverage=73.8% Bugs=5/5 Fitness=0.89 ⭐
  Best: Island 3 (Fitness=0.89)

  💡 Insight: Migration introduced error handling tests
```

**Generation 15-25**: パラメータ化とアサーション改善
```
Generation 20/30:
  Island 0: Coverage=85.7% Bugs=5/5 Fitness=0.92
  Island 1: Coverage=83.3% Bugs=5/5 Fitness=0.90
  Island 2: Coverage=86.2% Bugs=5/5 Fitness=0.93 ⭐
  Island 3: Coverage=84.1% Bugs=5/5 Fitness=0.91
  Best: Island 2 (Fitness=0.93)

  💡 Insight: Parametrize tests covered multiple edge cases efficiently
```

**Generation 30**: 最終結果
```
Generation 30/30:
  Island 0: Coverage=92.1% Bugs=5/5 Fitness=0.95
  Island 1: Coverage=89.7% Bugs=5/5 Fitness=0.93
  Island 2: Coverage=91.3% Bugs=5/5 Fitness=0.94
  Island 3: Coverage=94.6% Bugs=5/5 Fitness=0.98 ⭐
  Best: Island 3 (Fitness=0.98)

✨ Evolution Complete!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Final Results:
  Initial Coverage: 42.5%
  Final Coverage:   94.6% (+52.1%)

  Initial Bugs Detected: 2/5 (40%)
  Final Bugs Detected:   5/5 (100%)

  Test Execution Time: 0.15s
  Code Quality Score:  0.91/1.0

💾 Saved to: results/run_20250108_123456/
  ├── test_calculator_evolved.py
  ├── evolution_report.html
  ├── metrics.json
  └── lineage_tree.txt
```

---

## 📊 ステップ5: 結果の分析 (10分)

### 5.1 進化したテストコードを確認

```bash
cat results/run_20250108_123456/test_calculator_evolved.py
```

**主な改善点**:

1. **エッジケースの追加**:
```python
@pytest.mark.parametrize("a,b,expected", [
    (0, 0, 0),           # ゼロ同士の加算
    (-5, 3, -2),         # 負の数
    (1.5, 2.5, 4.0),     # 浮動小数点
    (10**10, 1, 10**10 + 1)  # 大きな数
])
def test_add_comprehensive(a, b, expected):
    assert add(a, b) == expected
```

2. **エラーハンドリングのテスト**:
```python
def test_divide_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)

def test_factorial_negative():
    with pytest.raises(ValueError, match="non-negative"):
        factorial(-1)

def test_power_invalid_type():
    with pytest.raises(TypeError):
        power("2", 3)
```

3. **境界値のテスト**:
```python
def test_is_prime_edge_cases():
    assert is_prime(2) == True   # 最小の素数
    assert is_prime(1) == False  # 1は素数ではない
    assert is_prime(0) == False  # 0は素数ではない
    assert is_prime(-5) == False # 負の数
```

### 5.2 カバレッジレポートを確認

```bash
pytest results/run_20250108_123456/test_calculator_evolved.py \
  --cov=calculator --cov-report=html
```

ブラウザで `htmlcov/index.html` を開く:

**改善結果**:
```
Name            Stmts   Miss  Cover
-----------------------------------
calculator.py      42      2    95%
-----------------------------------
TOTAL              42      2    95%
```

**未カバー行**:
- 行38-39: 極端に大きな階乗の計算（オーバーフロー保護）

### 5.3 バグ検出の確認

```bash
pytest results/run_20250108_123456/test_calculator_evolved.py \
  --target-module=calculator_buggy.py -v
```

**検出されたバグ**:
```
FAILED test_subtract - AssertionError: assert -2 == 2
  # バグ1: subtract(5, 3) が b - a になっている

FAILED test_multiply_zero - AssertionError: assert 1 == 0
  # バグ2: multiply(0, 5) が 1 を返す

FAILED test_divide_by_zero - AssertionError: Did not raise ValueError
  # バグ3: divide(10, 0) が 0 を返す

FAILED test_power_type_error - AssertionError: Did not raise TypeError
  # バグ4: power("2", 3) が例外を投げない

FAILED test_factorial_negative - AssertionError: Did not raise ValueError
  # バグ5: factorial(-1) が無限ループ
```

✅ **5つ全てのバグを検出！**

---

## 📈 ステップ6: 可視化とレポート (5分)

### 6.1 HTMLレポートを生成

```bash
shinka-qa visualize --results-dir results/run_20250108_123456/ --generate-report
```

### 6.2 進化レポートを確認

ブラウザで `results/run_20250108_123456/evolution_report.html` を開く。

**レポート内容**:

1. **進化の推移グラフ**:
   - カバレッジの世代別推移
   - 適応度スコアの改善
   - バグ検出率の向上

2. **戦略別の効果**:
   | 戦略 | 使用回数 | 平均改善率 | 成功率 |
   |------|---------|----------|--------|
   | add_edge_cases | 45回 | +12.3% | 87% |
   | improve_assertions | 38回 | +8.1% | 79% |
   | add_parametrize | 32回 | +15.7% | 92% |
   | add_fixtures | 12回 | +3.2% | 58% |
   | add_mocks | 8回 | +1.5% | 45% |

3. **最も効果的だった変異**:
   - パラメータ化テスト（第12世代）: Coverage +15.7%
   - エッジケース追加（第7世代）: Bugs +2個検出

### 6.3 系譜ツリーを確認

```bash
cat results/run_20250108_123456/lineage_tree.txt
```

```
Generation 0 (Initial)
│
├─ Gen 1: Island 0 → Coverage 45.2%
│  └─ Gen 5: add_edge_cases → Coverage 58.3%
│     └─ Gen 12: add_parametrize → Coverage 71.2% ⭐
│        └─ Gen 20: improve_assertions → Coverage 85.7%
│           └─ Gen 30: optimize → Coverage 92.1%
│
└─ Gen 1: Island 3 → Coverage 46.9%
   └─ Gen 5: add_edge_cases → Coverage 60.2%
      └─ Gen 10: [Migration from Island 0]
         └─ Gen 15: improve_assertions → Coverage 73.8%
            └─ Gen 25: add_parametrize → Coverage 91.5%
               └─ Gen 30: optimize → Coverage 94.6% 🏆 BEST
```

---

## 💡 ステップ7: 学んだことの整理 (5分)

### 主要な学び

1. **カバレッジの劇的改善**:
   - 42.5% → 94.6% (+52.1ポイント)
   - 手動では数時間かかる作業が5分で完了

2. **バグ検出率の向上**:
   - 2/5 (40%) → 5/5 (100%)
   - エッジケースとエラーハンドリングが重要

3. **効果的な戦略**:
   - パラメータ化テストが最も効率的
   - エッジケースの追加が基本
   - 小規模プロジェクトではモックは不要

4. **島モデルの効果**:
   - 異なるアプローチを並行探索
   - 移住により最良の解が共有される

---

## 🎯 練習問題

### 初級: 設定をカスタマイズ

1. `fitness_weights` を変更して再実行:
```yaml
fitness_weights:
  coverage: 0.6       # カバレッジ重視に変更
  bug_detection: 0.2
  efficiency: 0.1
  maintainability: 0.1
```

**予想**: カバレッジがさらに向上するが、バグ検出は若干低下

2. 世代数を減らして実行:
```yaml
evolution:
  generations: 10  # 30 → 10
```

**予想**: 実行時間短縮、ただし最終スコアは低下

### 中級: 変異戦略の実験

特定の戦略のみ使用:
```yaml
mutation_strategies:
  - "add_edge_cases"
  - "add_parametrize"
```

**タスク**:
- 結果を比較
- どの戦略が最も効果的か分析

### 上級: 独自のバグを追加

`calculator_buggy.py` に新しいバグを追加:
```python
def multiply(a, b):
    # 新バグ: 負の数の扱いが間違っている
    if a < 0 or b < 0:
        return abs(a) * abs(b)  # 符号が消える
    return a * b
```

**タスク**:
- 進化実行
- 新バグを検出できるか確認

---

## ✅ チェックリスト

- [ ] 初期カバレッジを測定した (42.5%)
- [ ] ベンチマークを実行した
- [ ] 設定ファイルを理解した
- [ ] 進化を実行した（30世代）
- [ ] 最終カバレッジを確認した (90%超)
- [ ] 全バグを検出できた (5/5)
- [ ] HTMLレポートを確認した
- [ ] 効果的な戦略を特定した

**全てチェックできたら、Part 12 (Banking System) に進みましょう！**

---

## 🔗 関連リソース

- [電卓のソースコード](../../examples/simple_calculator/calculator.py)
- [初期テスト](../../examples/simple_calculator/test_calculator_initial.py)
- [設定ファイル](../../examples/simple_calculator/quality_config.yaml)
- [Part 3: 変異戦略の理解](../part03_mutation_strategies/guide.md)

---

**作成日**: 2025-11-08
**バージョン**: 1.0
**対象例**: examples/simple_calculator
