# Part 2: 設定のカスタマイズ - チュートリアルガイド

**所要時間**: 20-25分
**難易度**: 入門〜中級
**前提知識**: Part 1完了、YAMLの基本

---

## 🎯 このパートで学ぶこと

1. 設定ファイル（quality_config.yaml）の全体構造
2. 各セクションの詳細な意味
3. 重み（weights）の調整方法
4. プロジェクトサイズ別の推奨設定
5. 実践的なカスタマイズ例

---

## 📖 ステップ1: 設定ファイルの全体像

### 1-1. 設定ファイルを開く

```bash
# Part 1で使用したサンプルディレクトリに移動
cd examples/simple_calculator

# 設定ファイルを開く
code quality_config.yaml
# または
vim quality_config.yaml
# または
cat quality_config.yaml
```

### 1-2. 設定ファイルの構造

```yaml
# quality_config.yaml の全体構造

# 1️⃣ テスト対象の指定
target:
  module: calculator.py
  exclude:
    - __pycache__
    - tests/

# 2️⃣ テストファイルの設定
test:
  initial_file: test_calculator_initial.py
  framework: pytest
  coverage_tool: pytest-cov

# 3️⃣ 評価指標の重み（最重要！）
fitness:
  weights:
    coverage: 0.4
    bug_detection: 0.3
    execution_time: 0.2
    code_quality: 0.1

# 4️⃣ 進化のパラメータ
evolution:
  num_generations: 5
  population_per_island: 6
  num_islands: 4
  mutation_strategies:
    - add_edge_case
    - parameterize_test
    - add_error_handling
    - add_assertion

# 5️⃣ 出力先の設定
output:
  results_dir: results/
  save_intermediate: true
  generate_report: true
```

**5つのセクション**:

| セクション | 役割 | 重要度 |
|-----------|------|--------|
| target | テスト対象のコード | ⭐⭐⭐ |
| test | テストファイルの場所 | ⭐⭐⭐ |
| fitness | 評価指標の重み | ⭐⭐⭐⭐⭐ |
| evolution | 進化パラメータ | ⭐⭐⭐⭐ |
| output | 結果の出力先 | ⭐⭐ |

---

## 📋 ステップ2: 各セクションの詳細

### 2-1. targetセクション

```yaml
target:
  module: calculator.py    # テスト対象のファイル or ディレクトリ
  exclude:                 # 除外するパターン（オプション）
    - __pycache__
    - tests/
    - migrations/
```

#### module の指定方法

**単一ファイル**:
```yaml
target:
  module: calculator.py
```

**ディレクトリ**:
```yaml
target:
  module: src/
```

**複数ファイル（パターンマッチ）**:
```yaml
target:
  module: src/**/*.py    # src配下の全てのPythonファイル
```

#### exclude の使い方

**デフォルトで除外すべきもの**:
```yaml
exclude:
  - __pycache__           # Pythonのキャッシュ
  - tests/                # テストコード自体
  - venv/                 # 仮想環境
  - .venv/
  - migrations/           # DBマイグレーション
  - node_modules/         # npm依存（あれば）
```

### 2-2. testセクション

```yaml
test:
  initial_file: test_calculator_initial.py  # 既存テストファイル
  framework: pytest                          # テストフレームワーク
  coverage_tool: pytest-cov                  # カバレッジツール
```

#### initial_file（既存テスト）

**既存テストがある場合**:
```yaml
test:
  initial_file: test_calculator.py
```

Shinka QAは、このファイルをベースに改善を行います。

**既存テストがない場合**:
```yaml
test:
  initial_file: null    # または、この行を削除
```

ゼロから生成されます（ただし、既存テストがある方が品質が高い）。

#### framework

**現在サポート**:
- `pytest`: Python標準（推奨）

**将来サポート予定**:
- `jest`: JavaScript/TypeScript
- `junit`: Java
- `go test`: Go

### 2-3. fitnessセクション（最重要！）

```yaml
fitness:
  weights:
    coverage: 0.4          # カバレッジの重要度
    bug_detection: 0.3     # バグ検出の重要度
    execution_time: 0.2    # 実行速度の重要度
    code_quality: 0.1      # コード品質の重要度
  # ⚠️ 合計は必ず 1.0
```

#### 各指標の意味

**coverage（カバレッジ）**:
```
何%のコードがテストされているか

高い方が良い: 100%に近いほど安心
測定方法: pytest-covで自動測定
```

**bug_detection（バグ検出）**:
```
既知のバグをどれだけ検出できるか

1.0 = 100%検出（完璧）
0.5 = 50%検出（半分見逃し）
測定方法: ミューテーションテストで自動測定
```

**execution_time（実行時間）**:
```
テストの実行速度

短い方が良い: CI/CDでのフィードバックが速い
測定方法: 実行時間を自動計測
```

**code_quality（コード品質）**:
```
テストコード自体の品質

高い方が良い: 保守しやすい
測定方法: 静的解析で自動評価
```

#### 重みのルール

**必須ルール**:
1. **合計は1.0**: `0.4 + 0.3 + 0.2 + 0.1 = 1.0`
2. **範囲は0.0〜1.0**: 負の値や1.0超えは不可
3. **全ての項目が必要**: 4つ全て指定

**検証方法**:
```bash
# 設定ファイルをチェック
shinka-qa validate --config quality_config.yaml
```

**期待される出力**:
```
Validating configuration...
✓ Weights sum to 1.0
✓ All values in range [0.0, 1.0]
✓ Configuration is valid
```

---

## ⚖️ ステップ3: 重みの調整

### 3-1. デフォルト設定（バランス型）

```yaml
fitness:
  weights:
    coverage: 0.4
    bug_detection: 0.3
    execution_time: 0.2
    code_quality: 0.1
```

**使用場面**:
- 特定の優先順位がない
- 全てをバランスよく改善したい
- 最初のテスト実行

**特徴**:
- カバレッジを最重視（0.4）
- バグ検出も重要視（0.3）
- 実行速度も考慮（0.2）
- コード品質は最低限（0.1）

### 3-2. カバレッジ重視設定

```yaml
fitness:
  weights:
    coverage: 0.7          # 大幅に引き上げ
    bug_detection: 0.15    # 半分に減らす
    execution_time: 0.1    # 半分に減らす
    code_quality: 0.05     # 半分に減らす
```

**使用場面**:
- コードカバレッジ目標がある（例: 90%以上）
- リファクタリング前の安全網を作りたい
- コードレビューでカバレッジが求められる

**期待される結果**:
```
Initial Coverage: 45%
Final Coverage: 95%
Improvement: +50pt

テストが急増します
- Before: 5個
- After: 20-25個
```

**実行例**:
```bash
# 1. 設定を編集
vim quality_config.yaml

# 2. 進化実行
shinka-qa evolve --config quality_config.yaml --verbose

# 3. 結果確認
# → カバレッジが急上昇しているはず
```

### 3-3. バグ検出重視設定

```yaml
fitness:
  weights:
    coverage: 0.2          # 最小限
    bug_detection: 0.6     # 大幅に引き上げ
    execution_time: 0.1
    code_quality: 0.1
```

**使用場面**:
- 本番環境でバグが頻発している
- バグバウンティプログラムに参加
- セキュリティクリティカルなコード

**期待される結果**:
```
Initial Bug Detection: 0.60 (60%のバグを検出)
Final Bug Detection: 1.00 (100%のバグを検出)
Improvement: +0.40

エラーハンドリングのテストが増えます
- try-except のテスト
- 境界値のテスト
- 不正入力のテスト
```

**実例**:

**Before**:
```python
def test_divide():
    assert divide(10, 2) == 5.0
```

**After**:
```python
def test_divide():
    assert divide(10, 2) == 5.0

def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)

def test_divide_invalid_input():
    with pytest.raises(TypeError):
        divide("10", 2)

def test_divide_float_overflow():
    with pytest.raises(OverflowError):
        divide(10**308, 10**-308)
```

### 3-4. 実行速度重視設定

```yaml
fitness:
  weights:
    coverage: 0.3
    bug_detection: 0.3
    execution_time: 0.3    # 引き上げ
    code_quality: 0.1
```

**使用場面**:
- CI/CDで頻繁にテストを実行
- フィードバックループを短くしたい
- テスト実行が遅すぎる（10分以上）

**期待される結果**:
```
Initial Execution Time: 5.0s
Final Execution Time: 2.5s
Improvement: -50%

効率的なテストが生成されます
- 重複テストの削減
- パラメータ化テストの活用
- モック/スタブの使用
```

**トレードオフ**:
- カバレッジは若干低下する可能性（85% → 80%）
- でも、実行時間が半分になる

### 3-5. コード品質重視設定

```yaml
fitness:
  weights:
    coverage: 0.3
    bug_detection: 0.3
    execution_time: 0.1
    code_quality: 0.3      # 大幅に引き上げ
```

**使用場面**:
- テストコードの保守性を重視
- チームでテストを共有
- 長期的なメンテナンスを考慮

**期待される結果**:
```
Initial Code Quality: 0.60
Final Code Quality: 0.95
Improvement: +0.35

読みやすいテストが生成されます
- 明確な命名
- 適切なコメント
- DRY原則の適用
```

**実例**:

**Before**:
```python
def test1():
    assert add(1, 2) == 3

def test2():
    assert add(2, 3) == 5
```

**After**:
```python
@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),  # 小さな数
    (2, 3, 5),  # 中くらいの数
])
def test_add_positive_numbers(a, b, expected):
    """正の数の加算をテスト"""
    result = add(a, b)
    assert result == expected
```

---

## 🎨 ステップ4: evolutionセクションの調整

### 4-1. evolutionセクションの全体

```yaml
evolution:
  num_generations: 5              # 世代数
  population_per_island: 6        # 島ごとの個体数
  num_islands: 4                  # 島の数
  mutation_strategies:            # 変異戦略
    - add_edge_case
    - parameterize_test
    - add_error_handling
    - add_assertion
```

### 4-2. num_generations（世代数）

**意味**: 何世代進化させるか

**推奨値**:

| プロジェクト | 世代数 | 実行時間 | 品質 |
|------------|--------|---------|------|
| 小規模（100-500行） | 3-5 | 1-2分 | 良 |
| 中規模（500-5000行） | 5-7 | 2-5分 | 非常に良 |
| 大規模（5000行以上） | 7-10 | 5-15分 | 優秀 |

**実験**: 世代数を変えて実行してみましょう

```yaml
# 実験1: 少ない世代数
evolution:
  num_generations: 3
```

```bash
shinka-qa evolve --config quality_config.yaml
```

**期待される結果**:
```
Generation 1: Coverage 55%
Generation 2: Coverage 72%
Generation 3: Coverage 82%
Final: 82% (まだ改善余地あり)
```

```yaml
# 実験2: 多い世代数
evolution:
  num_generations: 10
```

```bash
shinka-qa evolve --config quality_config.yaml
```

**期待される結果**:
```
Generation 1: Coverage 55%
Generation 2: Coverage 72%
Generation 3: Coverage 82%
Generation 4: Coverage 88%
Generation 5: Coverage 91%
Generation 6: Coverage 93%
Generation 7: Coverage 94%
Generation 8: Coverage 94.5%
Generation 9: Coverage 94.8%
Generation 10: Coverage 95%
Final: 95% (収束している)
```

**観察**:
- 世代7以降、改善が逓減
- 世代10は「やりすぎ」かもしれない
- **最適**: 世代5-7

### 4-3. population_per_island（個体数）

**意味**: 各島で何個の候補を同時に評価するか

**推奨値**:
- **小規模**: 4
- **中規模**: 6（デフォルト）
- **大規模**: 8

**トレードオフ**:
- 多い → 品質向上、時間増加
- 少ない → 時間短縮、品質低下

### 4-4. num_islands（島の数）

**意味**: 並列で何個の進化系統を実行するか

**島モデルとは**:
```
Island 1: テスト群A → 進化 → 最良A
Island 2: テスト群B → 進化 → 最良B
Island 3: テスト群C → 進化 → 最良C
Island 4: テスト群D → 進化 → 最良D

最後に、最良A, B, C, Dを統合 → 最終テスト
```

**推奨値**:
- **CPU 2コア**: 2島
- **CPU 4コア**: 4島（デフォルト）
- **CPU 8コア以上**: 8島

**確認方法**:
```bash
# CPUコア数を確認
# Mac/Linux
nproc

# Windows PowerShell
$env:NUMBER_OF_PROCESSORS
```

### 4-5. mutation_strategies（変異戦略）

**デフォルト（全て使用）**:
```yaml
mutation_strategies:
  - add_edge_case         # エッジケースの追加
  - parameterize_test     # パラメータ化
  - add_error_handling    # エラーハンドリング
  - add_assertion         # アサーション改善
```

**カスタマイズ例1: エッジケースのみ**:
```yaml
mutation_strategies:
  - add_edge_case
```

使用場面: カバレッジは十分だが、境界値テストが不足

**カスタマイズ例2: エラーハンドリング重視**:
```yaml
mutation_strategies:
  - add_error_handling
  - add_assertion
```

使用場面: バグ検出を強化したい

**詳細はPart 3で**: 各戦略の詳細な動作はPart 3で学びます

---

## 📊 ステップ5: プロジェクトサイズ別の推奨設定

### 5-1. 小規模プロジェクト（100-500行）

```yaml
# quality_config_small.yaml

target:
  module: src/calculator.py
  exclude:
    - __pycache__

test:
  initial_file: tests/test_calculator.py
  framework: pytest
  coverage_tool: pytest-cov

fitness:
  weights:
    coverage: 0.5           # カバレッジ重視
    bug_detection: 0.3
    execution_time: 0.1     # 速度は重要でない
    code_quality: 0.1

evolution:
  num_generations: 3        # 少なめ
  population_per_island: 4  # 小さめ
  num_islands: 2            # 少なめ
  mutation_strategies:
    - add_edge_case
    - parameterize_test
    - add_assertion

output:
  results_dir: results/
  save_intermediate: true
```

**理由**:
- 小規模なので、早く収束する
- カバレッジ100%近くが現実的
- 実行時間は1分以内
- エラーハンドリングは既にあると仮定

**期待される結果**:
```
Execution Time: 45秒
Initial Coverage: 40%
Final Coverage: 95%
Improvement: +55pt
```

### 5-2. 中規模プロジェクト（500-5000行）

```yaml
# quality_config_medium.yaml

target:
  module: src/
  exclude:
    - __pycache__
    - tests/
    - migrations/

test:
  initial_file: tests/test_suite.py
  framework: pytest
  coverage_tool: pytest-cov

fitness:
  weights:
    coverage: 0.4           # バランス型
    bug_detection: 0.3
    execution_time: 0.2
    code_quality: 0.1

evolution:
  num_generations: 5        # デフォルト
  population_per_island: 6  # デフォルト
  num_islands: 4            # デフォルト
  mutation_strategies:
    - add_edge_case
    - parameterize_test
    - add_error_handling
    - add_assertion

output:
  results_dir: results/
  save_intermediate: true
  generate_report: true
```

**理由**:
- デフォルト設定がちょうどいい
- バランスよく改善
- 実行時間は2-5分

**期待される結果**:
```
Execution Time: 3分
Initial Coverage: 35%
Final Coverage: 85%
Improvement: +50pt
```

### 5-3. 大規模プロジェクト（5000行以上）

```yaml
# quality_config_large.yaml

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
    coverage: 0.3           # バグ検出重視に変更
    bug_detection: 0.4      # 最重要
    execution_time: 0.2     # 考慮
    code_quality: 0.1

evolution:
  num_generations: 10       # 多め
  population_per_island: 8  # 大きめ
  num_islands: 8            # 多め（要CPUコア数）
  mutation_strategies:
    - add_edge_case
    - parameterize_test
    - add_error_handling
    - add_assertion

output:
  results_dir: results/
  save_intermediate: true
  generate_report: true
```

**理由**:
- 大規模なので徹底的に改善
- バグ検出を最優先（本番リスク大）
- 時間をかける価値がある（15-30分）

**期待される結果**:
```
Execution Time: 20分
Initial Coverage: 25%
Final Coverage: 80%
Improvement: +55pt
Bug Detection: 0.50 → 1.00
```

---

## 🔧 ステップ6: 実践演習

### 演習1: カバレッジ重視設定の作成

**タスク**: カバレッジを95%以上にする設定を作成してください

**ヒント**:
```yaml
fitness:
  weights:
    coverage: ?     # ここを調整
    bug_detection: ?
    execution_time: ?
    code_quality: ?
    # 合計 = 1.0
```

**実行**:
```bash
# 1. 設定編集
vim quality_config.yaml

# 2. 進化実行
shinka-qa evolve --config quality_config.yaml --verbose

# 3. 結果確認
# カバレッジが目標に達したか？
```

**解答例**:
```yaml
fitness:
  weights:
    coverage: 0.7
    bug_detection: 0.15
    execution_time: 0.1
    code_quality: 0.05
```

### 演習2: プロジェクトサイズに合わせた設定

**タスク**: 自分のプロジェクトに最適な設定を作成してください

**質問**:
1. プロジェクトサイズは？（行数を確認）
2. 優先順位は？（カバレッジ? バグ検出? 速度?）
3. 実行時間の制約は？（1分以内? 10分OK?）

**プロジェクトサイズの確認**:
```bash
# Pythonファイルの総行数を確認
find . -name "*.py" | xargs wc -l
```

**設定のテンプレート選択**:
- 500行未満 → 小規模プロジェクト設定
- 500-5000行 → 中規模プロジェクト設定
- 5000行以上 → 大規模プロジェクト設定

---

## 📈 ステップ7: 結果の比較

### 7-1. 複数設定の比較実験

**実験計画**:
1. デフォルト設定で実行
2. カバレッジ重視設定で実行
3. バグ検出重視設定で実行
4. 結果を比較

**実行手順**:

```bash
# 1. デフォルト設定
cp quality_config.yaml quality_config_default.yaml
shinka-qa evolve --config quality_config_default.yaml
# 結果をコピー
cp -r results/run_* results/default/

# 2. カバレッジ重視設定
# quality_config.yamlを編集（coverage: 0.7）
shinka-qa evolve --config quality_config.yaml
# 結果をコピー
cp -r results/run_* results/coverage_focused/

# 3. バグ検出重視設定
# quality_config.yamlを編集（bug_detection: 0.6）
shinka-qa evolve --config quality_config.yaml
# 結果をコピー
cp -r results/run_* results/bug_focused/
```

**結果の比較**:

| 設定 | カバレッジ | バグ検出 | 実行時間 | テスト数 |
|------|-----------|---------|---------|---------|
| デフォルト | 92% | 1.00 | 2.0分 | 15個 |
| カバレッジ重視 | 95% | 0.95 | 3.0分 | 22個 |
| バグ検出重視 | 88% | 1.00 | 2.5分 | 18個 |

**観察**:
- カバレッジ重視 → カバレッジ最高だが、時間もかかる
- バグ検出重視 → バグ検出完璧、カバレッジは若干低い
- デフォルト → バランスが良い

**結論**: プロジェクトの優先順位に応じて選択

---

## ❓ よくある質問

### Q1: 重みの合計が1.0にならない場合は？

**A**: エラーになります

```bash
Error: Fitness weights must sum to 1.0 (current sum: 0.9)
```

**解決策**:
```yaml
# NG
fitness:
  weights:
    coverage: 0.4
    bug_detection: 0.3
    execution_time: 0.2
    code_quality: 0.0   # 合計 = 0.9 ❌

# OK
fitness:
  weights:
    coverage: 0.4
    bug_detection: 0.3
    execution_time: 0.2
    code_quality: 0.1   # 合計 = 1.0 ✓
```

### Q2: 世代数は何世代が最適ですか？

**A**: プロジェクトサイズと時間制約による

**一般的な推奨**:
- 3世代: 小規模、時間制約あり
- 5世代: 中規模、バランス型（推奨）
- 7-10世代: 大規模、徹底的に改善

**判断基準**:
```
収束の兆候が見えたら停止してOK

例:
Generation 5: Coverage 92%
Generation 6: Coverage 92.5%
Generation 7: Coverage 92.8%
→ ほぼ収束（これ以上は時間の無駄）
```

### Q3: 変異戦略は全部使うべきですか？

**A**: 最初は全部使ってください

```yaml
mutation_strategies:
  - add_edge_case
  - parameterize_test
  - add_error_handling
  - add_assertion
```

慣れてきたら、選択的に使用。
詳しくはPart 3で学びます。

### Q4: 設定を変えても結果が変わらない

**A**: 以下を確認してください

1. **設定ファイルが保存されているか**
```bash
cat quality_config.yaml  # 内容を確認
```

2. **正しい設定ファイルを指定しているか**
```bash
shinka-qa evolve --config quality_config.yaml
# パスが正しいか確認
```

3. **キャッシュをクリア**
```bash
rm -rf results/
shinka-qa evolve --config quality_config.yaml
```

---

## 📝 チェックリスト

- [ ] 設定ファイルの5つのセクションを理解した
- [ ] targetセクションで除外パターンを設定した
- [ ] fitnessセクションの重みを調整した
- [ ] 重みの合計が1.0になることを確認した
- [ ] evolutionセクションのパラメータを理解した
- [ ] プロジェクトサイズに合った設定を作成した
- [ ] 複数の設定で実験して結果を比較した

全てチェックできたら、**Part 3: 変異戦略の理解**に進みましょう！

---

## 🔗 次のステップ

### Part 3で学ぶこと

**変異戦略の詳細**:
1. `add_edge_case`: どんなエッジケースが追加されるか
2. `parameterize_test`: パラメータ化の具体例
3. `add_error_handling`: エラーハンドリングのパターン
4. `add_assertion`: アサーション改善の方法

**準備**:
```bash
# Part 3のサンプルコードを見ておく
cat examples/mutation_strategies/README.md
```

準備ができたら、Part 3に進みましょう！

---

**作成日**: 2025-11-07
**更新日**: 2025-11-07
**バージョン**: 1.0
