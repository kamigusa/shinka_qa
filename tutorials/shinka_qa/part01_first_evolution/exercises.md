# Part 1: はじめての進化 - 演習と解答

**所要時間**: 15分
**難易度**: 入門
**形式**: 実践演習（コマンド実行と結果解釈）

---

## 📝 演習の目的

このPartは実践的な内容なので、演習は**実際にコマンドを実行して結果を確認する**ことが中心です。
理解を深めるために、手を動かして学びましょう。

---

## 問題1: インストール確認（実践）

### 質問

Shinka QAのインストールを完了し、以下の情報をレポートしてください。

```bash
# 1. バージョン確認
shinka-qa --version

# 2. ヘルプ表示
shinka-qa --help

# 3. インストール場所確認
pip show shinka-qa
```

### 解答フォーマット

```
【インストール情報】
バージョン: [表示されたバージョン]
インストールパス: [Location:]
実行可能: [Yes/No]

【ヘルプコマンド出力】
利用可能なサブコマンド:
- [コマンド1]
- [コマンド2]
- [コマンド3]

【問題の有無】
[問題があれば記載、なければ「なし」]
```

### 解答例

```
【インストール情報】
バージョン: Shinka QA v1.0
インストールパス: /home/user/shinka-qa
実行可能: Yes ✓

【ヘルプコマンド出力】
利用可能なサブコマンド:
- benchmark: 現在のテスト品質を測定
- evolve: テストを進化させる
- visualize: 結果を可視化

【問題の有無】
なし。正常にインストールされています。
```

### 評価基準

- **全て実行できた**: 優秀！次に進んでください
- **一部エラー**: トラブルシューティングセクションを参照
- **全てエラー**: 講師またはTAに相談してください

---

## 問題2: ベンチマーク結果の解釈（理解度確認）

### 質問

以下のベンチマーク結果を見て、3つの問題点を指摘してください。

```
Running benchmark...
========================================

Benchmark Results:
  Tests Passed: 5
  Tests Failed: 0
  Coverage: 42.5%
  Success: YES
```

### 解答例

1. **カバレッジが低い（42.5%）**
   - コードの半分以上がテストされていない
   - 潜在的なバグのリスクが高い
   - 目標は85%以上

2. **テスト数が少ない（5個のみ）**
   - エッジケースがカバーされていない可能性
   - エラーハンドリングのテスト不足
   - 境界値テストがない

3. **失敗テストがゼロだが安心できない**
   - テストが成功しても、カバレッジが低いため
   - テストされていない部分にバグがある可能性
   - 「Success: YES」は誤解を招く

### 解説

カバレッジが低い状態で「Success: YES」と表示されるのは、**既存のテストは全て成功している**という意味です。

しかし、これは**テストされていないコードにバグがないことを保証しません**。

**例**:
```python
def divide(a, b):
    # この関数には2つの問題がある
    if b == 0:
        raise ValueError("Cannot divide by zero")  # テストされている
    return a / b  # テストされている

def multiply(a, b):
    # この関数は全くテストされていない！
    return a + b  # バグ！本当は a * b であるべき
```

ベンチマーク結果:
- Tests Passed: 2 (divide関数のテスト)
- Coverage: 50% (divide関数のみカバー)
- Success: YES (既存テストは成功)
- **問題**: multiply関数のバグは検出されない

### 評価基準

- **3つ以上指摘**: 優秀！本質を理解している
- **2つ指摘**: 良好。基本を理解している
- **1つ以下**: ガイドのステップ3を再読してください

---

## 問題3: 進化の過程を読む（コードリーディング）

### 質問

以下の進化ログを見て、各世代で何が改善されたか説明してください。

```
Generation 1/5
  Best Fitness: 0.523
  Coverage: 58.0%
  Bug Detection: 0.60

Generation 2/5
  Best Fitness: 0.712
  Coverage: 75.0%
  Bug Detection: 0.80

Generation 3/5
  Best Fitness: 0.856
  Coverage: 88.0%
  Bug Detection: 0.90

Generation 4/5
  Best Fitness: 0.924
  Coverage: 92.0%
  Bug Detection: 1.00

Generation 5/5
  Best Fitness: 0.950
  Coverage: 92.0%
  Bug Detection: 1.00
```

### 解答

**世代1→2**:
- カバレッジ: +17pt (58% → 75%)
- バグ検出: +0.20 (0.60 → 0.80)
- 改善内容: エッジケースのテストが追加された
- 大幅な改善が見られる

**世代2→3**:
- カバレッジ: +13pt (75% → 88%)
- バグ検出: +0.10 (0.80 → 0.90)
- 改善内容: 境界値テストが追加された
- 引き続き良い改善

**世代3→4**:
- カバレッジ: +4pt (88% → 92%)
- バグ検出: +0.10 (0.90 → 1.00)
- 改善内容: 残りのバグを全て検出
- バグ検出が完璧に

**世代4→5**:
- カバレッジ: 変化なし (92% → 92%)
- バグ検出: 変化なし (1.00 → 1.00)
- 改善内容: フィットネスのみ微改善
- **収束した**（これ以上の改善が難しい）

### 解説

#### 典型的な進化曲線

```
改善率
  │
  │  ┌─ 大幅改善フェーズ (Gen 1-2)
  │ ╱
  │╱
  ├──── 逓減フェーズ (Gen 3-4)
  │──── 収束フェーズ (Gen 5)
  └─────────────> 世代
```

**大幅改善フェーズ（世代1-2）**:
- 明らかなギャップを埋める
- カバレッジが急上昇
- 簡単なテストが追加される

**逓減フェーズ（世代3-4）**:
- 残りのギャップを埋める
- 改善幅が減少
- 難しいケースに取り組む

**収束フェーズ（世代5）**:
- ほぼ最適化完了
- これ以上の改善が困難
- 停止時期の判断

### なぜ100%にならないか？

カバレッジが92%で止まった理由:
1. **デッドコード**: 実際には使われないコード
2. **到達不能**: 特定条件でしか実行されないコード
3. **防御的プログラミング**: 起こり得ないエラー処理

**推奨**: 85-95%で十分。100%を目指すのはコスト対効果が悪い

---

## 問題4: Before/Afterテストの比較（コードリーディング）

### 質問

以下のBeforeとAfterのテストコードを比較して、どのような改善がされたか詳しく説明してください。

#### Before
```python
def test_add():
    assert add(2, 3) == 5

def test_subtract():
    assert subtract(5, 3) == 2

def test_multiply():
    assert multiply(4, 5) == 20

def test_divide():
    assert divide(10, 2) == 5.0

def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)
```

#### After
```python
import pytest

@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
    (1.5, 2.5, 4.0),
])
def test_add_comprehensive(a, b, expected):
    assert add(a, b) == expected

def test_add_large_numbers():
    assert add(10**10, 10**10) == 2 * 10**10

def test_divide_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)

@pytest.mark.parametrize("a,b,expected", [
    (-10, 2, -5.0),
    (10, -2, -5.0),
    (-10, -2, 5.0),
])
def test_divide_negative(a, b, expected):
    assert divide(a, b) == expected

def test_subtract_edge_cases():
    assert subtract(0, 0) == 0
    assert subtract(-5, -3) == -2
    assert subtract(5, -3) == 8

@pytest.mark.parametrize("a,b,expected", [
    (0, 5, 0),
    (5, 0, 0),
    (-1, 5, -5),
])
def test_multiply_edge_cases(a, b, expected):
    assert multiply(a, b) == expected
```

### 解答例

#### 1. パラメータ化テストの導入

**Before**:
```python
def test_add():
    assert add(2, 3) == 5  # 1ケースのみ
```

**After**:
```python
@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5),      # 正の数
    (0, 0, 0),      # ゼロ
    (-1, 1, 0),     # 負の数と正の数
    (1.5, 2.5, 4.0),  # 小数点
])
def test_add_comprehensive(a, b, expected):
    assert add(a, b) == expected  # 4ケースを効率的にテスト
```

**効果**:
- テストケース数: 1個 → 4個
- 保守性: 新しいケースの追加が容易
- 可読性: テストデータが一目瞭然

#### 2. エッジケースの追加

**新しく追加されたエッジケース**:
- ゼロとの演算 (`0, 0`, `0, 5`, `5, 0`)
- 負の数 (`-1, 1`, `-10, 2`, `-10, -2`)
- 大きな数 (`10**10`)
- 小数点 (`1.5, 2.5`)

**Before**: 基本的な正の数のみ
**After**: 包括的なカバー

#### 3. エラーメッセージの検証

**Before**:
```python
with pytest.raises(ValueError):
    divide(10, 0)  # 例外の型のみチェック
```

**After**:
```python
with pytest.raises(ValueError, match="Cannot divide by zero"):
    divide(10, 0)  # 例外の型とメッセージをチェック
```

**効果**:
- より厳密な検証
- エラーメッセージの変更を検出
- ユーザーへのエラー表示を保証

#### 4. テスト数の増加

| 指標 | Before | After | 変化 |
|------|--------|-------|------|
| テスト数 | 5個 | 15個以上 | +200% |
| カバレッジ | 42.5% | 92.0% | +49.5pt |
| エッジケース | 1個 | 10個以上 | +900% |

#### 5. テストの命名改善

**Before**: `test_add()` - 抽象的
**After**: `test_add_comprehensive()`, `test_add_large_numbers()` - 具体的

**効果**:
- テストの意図が明確
- 失敗時の原因特定が容易
- ドキュメントとしての価値

### 評価基準

- **5つ以上の改善点**: 優秀！細部まで理解している
- **3-4つの改善点**: 良好。実践に十分
- **1-2つの改善点**: 基本的な理解。さらに学習推奨

---

## 問題5: トラブルシューティング（シナリオ）

### 質問

以下のエラーメッセージが表示されました。原因と解決策を答えてください。

#### シナリオA
```
$ shinka-qa evolve --config quality_config.yaml

Error: Configuration file not found: quality_config.yaml
```

#### シナリオB
```
$ shinka-qa benchmark --config quality_config.yaml

ModuleNotFoundError: No module named 'pytest'
```

#### シナリオC
```
Evolution Complete!
Final Coverage: 45.0% (improved by +3.0%)

Warning: Limited improvement. Consider:
- Increasing num_generations
- Adjusting mutation strategies
```

### 解答

#### シナリオA: 設定ファイルが見つからない

**原因**:
1. カレントディレクトリが間違っている
2. ファイル名のタイポ
3. ファイルが存在しない

**解決策**:
```bash
# 1. カレントディレクトリを確認
pwd

# 2. ファイルの存在を確認
ls -la quality_config.yaml

# 3. 正しいディレクトリに移動
cd examples/simple_calculator

# 4. 再実行
shinka-qa evolve --config quality_config.yaml
```

**または、フルパス指定**:
```bash
shinka-qa evolve --config /full/path/to/quality_config.yaml
```

#### シナリオB: pytestがインストールされていない

**原因**:
依存関係がインストールされていない

**解決策**:
```bash
# 依存関係を全てインストール
pip install -e .

# または、pytestのみインストール
pip install pytest pytest-cov

# インストール確認
pytest --version
```

**予防策**:
```bash
# 仮想環境を使用
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e .
```

#### シナリオC: 改善幅が小さい

**原因**:
1. 初期テストが既に高品質
2. 世代数が少なすぎる
3. 設定が適切でない

**解決策1**: 世代数を増やす
```yaml
# quality_config.yaml
evolution:
  num_generations: 10  # 5から10に増やす
```

**解決策2**: 変異戦略を調整
```yaml
evolution:
  mutation_strategies:
    - add_edge_case
    - parameterize_test
    - add_error_handling
```

**解決策3**: 重みを調整
```yaml
fitness:
  weights:
    coverage: 0.5  # カバレッジを重視
    bug_detection: 0.3
    execution_time: 0.1
    code_quality: 0.1
```

**判断基準**:
- 改善幅 +3%: 再実行を検討
- 改善幅 +10%以上: 正常
- 改善幅 +30%以上: 優秀

---

## 問題6: 結果の活用（実践計画）

### 質問

進化実行が完了し、以下の結果が得られました。
次に何をすべきか、3つのステップで計画を立ててください。

```
Final Results:
  Best Fitness: 0.950
  Final Coverage: 92.0%
  Final Bug Detection: 1.00

Results saved to: results/run_20251107_123456/
  - evolved_test.py
  - metrics.json
  - best_test_gen1.py ~ gen5.py
```

### 解答例

#### ステップ1: 生成されたテストをレビュー（30分）

**タスク**:
```bash
# 1. 最終テストを確認
cat results/run_20251107_123456/evolved_test.py

# 2. エディタで開く
code results/run_20251107_123456/evolved_test.py
```

**レビュー観点**:
- [ ] テストは意図が明確か？
- [ ] アサーションは適切か？
- [ ] エッジケースは妥当か？
- [ ] コードスタイルは統一されているか？
- [ ] 不要なテストはないか？

**アクション**:
- 良いテスト → マージ候補
- 不明確なテスト → コメント追加
- 不要なテスト → 削除

#### ステップ2: 既存テストとマージ（15分）

**マージ方法**:

```bash
# 1. バックアップ作成
cp test_calculator_initial.py test_calculator_backup.py

# 2. 新しいテストファイルを作成
cat test_calculator_initial.py > test_calculator.py
cat results/run_20251107_123456/evolved_test.py >> test_calculator.py

# 3. 重複を削除
# エディタで手動削除、または
python scripts/deduplicate_tests.py test_calculator.py
```

**重複削除の例**:
```python
# Before
def test_add():  # 既存
    assert add(2, 3) == 5

def test_add():  # 進化後（重複）
    assert add(2, 3) == 5

# After
def test_add():  # 1つに統合
    assert add(2, 3) == 5
```

#### ステップ3: 実行して確認（10分）

**実行**:
```bash
# 1. 全テストを実行
pytest test_calculator.py -v

# 2. カバレッジを確認
pytest test_calculator.py --cov=calculator --cov-report=html

# 3. HTMLレポートを開く
open htmlcov/index.html  # Mac
start htmlcov/index.html  # Windows
```

**期待される結果**:
```
=================== test session starts ===================
collected 15 items

test_calculator.py::test_add_comprehensive[2-3-5] PASSED
test_calculator.py::test_add_comprehensive[0-0-0] PASSED
...
test_calculator.py::test_divide_negative[-10--2-5.0] PASSED

=================== 15 passed in 0.15s ===================

Coverage: 92%
```

**もし失敗したら**:
1. エラーメッセージを確認
2. 該当テストを修正
3. 再実行

### 発展課題

**CI/CDに統合**（Part 5で詳しく学習）:
```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: pytest test_calculator.py --cov=calculator
```

---

## 問題7: メトリクスの解釈（応用）

### 質問

以下の2つのプロジェクトで進化実行を行いました。
どちらがより成功したと言えますか？理由と共に答えてください。

#### プロジェクトA
```
Initial Metrics:
  Coverage: 30.0%
  Bug Detection: 0.40
  Execution Time: 0.10s
  Fitness: 0.25

Final Metrics:
  Coverage: 85.0%
  Bug Detection: 0.95
  Execution Time: 0.50s
  Fitness: 0.82

Improvement:
  Coverage: +55.0pt
  Bug Detection: +0.55
  Fitness: +0.57
```

#### プロジェクトB
```
Initial Metrics:
  Coverage: 70.0%
  Bug Detection: 0.80
  Execution Time: 0.20s
  Fitness: 0.68

Final Metrics:
  Coverage: 92.0%
  Bug Detection: 1.00
  Execution Time: 0.35s
  Fitness: 0.89

Improvement:
  Coverage: +22.0pt
  Bug Detection: +0.20
  Fitness: +0.21
```

### 解答

**結論**: **プロジェクトAの方がより成功している**

### 理由

#### 1. 改善幅が大きい

| 指標 | プロジェクトA | プロジェクトB |
|------|--------------|--------------|
| カバレッジ改善 | +55pt | +22pt |
| バグ検出改善 | +0.55 | +0.20 |
| フィットネス改善 | +0.57 | +0.21 |

**プロジェクトA**:
- カバレッジが30%から85%へ（**2.8倍**）
- バグ検出が0.40から0.95へ（**2.4倍**）
- 大幅な品質向上

**プロジェクトB**:
- カバレッジが70%から92%へ（1.3倍）
- バグ検出が0.80から1.00へ（1.25倍）
- 良い改善だが、A程ではない

#### 2. 投資対効果（ROI）が高い

**プロジェクトA**:
```
投資: 実行時間が0.10s → 0.50s (+0.40s, 5倍)
リターン: フィットネスが0.25 → 0.82 (+0.57, 3.3倍)
ROI: 優秀
```

**プロジェクトB**:
```
投資: 実行時間が0.20s → 0.35s (+0.15s, 1.75倍)
リターン: フィットネスが0.68 → 0.89 (+0.21, 1.3倍)
ROI: 良好だが、Aより低い
```

#### 3. ビジネスインパクトが大きい

**プロジェクトA**:
- 初期状態が低品質（カバレッジ30%）
- **本番バグのリスクが高かった**
- 進化後、安全なレベルに到達
- **クリティカルな改善**

**プロジェクトB**:
- 初期状態が中品質（カバレッジ70%）
- ある程度安全だった
- 進化後、さらに安全に
- **追加の安心**

### ただし、両方とも成功

**絶対値で見ると**:
- プロジェクトBの最終カバレッジ（92%）はAの85%より高い
- プロジェクトBのバグ検出は完璧（1.00）

**相対値で見ると**:
- プロジェクトAの改善率が圧倒的に高い

### 実務での判断

**優先順位**:
1. **低品質プロジェクト（A型）**: すぐに対処すべき
2. **中品質プロジェクト（B型）**: 余裕があれば改善

**推奨アプローチ**:
```
Phase 1: A型プロジェクトを全てB型レベルに引き上げる
Phase 2: B型プロジェクトをさらに改善
Phase 3: 新規プロジェクトは最初から高品質を維持
```

---

## 📊 演習の総括

### 採点基準

| 問題 | 配点 | あなたの得点 |
|------|------|--------------:|
| 問題1 | 10点 | ___ |
| 問題2 | 15点 | ___ |
| 問題3 | 15点 | ___ |
| 問題4 | 20点 | ___ |
| 問題5 | 15点 | ___ |
| 問題6 | 15点 | ___ |
| 問題7 | 10点 | ___ |
| **合計** | **100点** | ___ |

### 評価

- **90点以上**: 完璧！Part 2に進んでください
- **70-89点**: 良好。実践で学びながらPart 2へ
- **50-69点**: 基本は理解。もう一度実行してみてください
- **49点以下**: ガイドを再読し、講師に質問してください

---

## 🎯 実践チェックリスト

全て実行しましたか？

### 基本操作
- [ ] Shinka QAをインストールした
- [ ] バージョン確認ができた
- [ ] サンプルプロジェクトに移動した
- [ ] ベンチマークを実行した
- [ ] 結果を解釈できた

### 進化実行
- [ ] evolveコマンドを実行した
- [ ] 進化の過程を観察した
- [ ] 最終結果を確認した
- [ ] カバレッジの改善を確認した

### 結果の活用
- [ ] evolved_test.pyを確認した
- [ ] metrics.jsonを読んだ
- [ ] HTMLレポートを生成した
- [ ] Before/Afterを比較した

### トラブルシューティング
- [ ] エラーに遭遇した（あれば）
- [ ] エラーを解決できた
- [ ] 解決方法を理解した

**全てチェックできたら、Part 2に進みましょう！**

---

## 💡 発展課題（オプション）

時間がある方は、以下にも挑戦してみてください：

### 課題1: 独自プロジェクトで試す

自分のプロジェクトで進化を実行してみましょう。

```bash
# 1. 自分のプロジェクトに移動
cd /path/to/your/project

# 2. 設定ファイルをコピー
cp /path/to/shinka-qa/examples/simple_calculator/quality_config.yaml .

# 3. 設定を編集
vim quality_config.yaml

# 4. 実行
shinka-qa evolve --config quality_config.yaml
```

### 課題2: 世代数を変えて実験

世代数を変えて、結果の違いを観察しましょう。

```yaml
# 実験1: 少ない世代数
evolution:
  num_generations: 3

# 実験2: 多い世代数
evolution:
  num_generations: 10

# 実験3: 非常に多い世代数
evolution:
  num_generations: 20
```

**仮説**:
- 世代数が多いほど、カバレッジは向上する？
- しかし、収穫逓減が起こる？

**実験して確かめてください！**

### 課題3: 世代別テストを比較

```bash
# 世代1のテストを見る
cat results/run_20251107_123456/best_test_gen1.py

# 世代3のテストを見る
cat results/run_20251107_123456/best_test_gen3.py

# 世代5のテストを見る
cat results/run_20251107_123456/best_test_gen5.py
```

**質問**:
- 各世代でどんなテストが追加されましたか？
- どのようなパターンがありますか？

---

## 🔗 次のステップ

### Part 2で学ぶこと

**Part 2: 設定のカスタマイズ**では、以下を学びます：

1. **設定ファイルの詳細**
   - 各パラメータの意味
   - デフォルト値
   - 推奨値

2. **重みの調整**
   - カバレッジ重視
   - バグ検出重視
   - 実行速度重視
   - バランス型

3. **プロジェクトに合わせた最適化**
   - 小規模プロジェクト
   - 中規模プロジェクト
   - 大規模プロジェクト
   - レガシーコード

4. **変異戦略の選択**
   - 戦略の種類
   - 使い分け
   - カスタム戦略

### 準備

Part 2に進む前に：
```bash
# 設定ファイルをエディタで開いておく
code quality_config.yaml

# または
vim quality_config.yaml
```

準備ができたら、Part 2に進みましょう！

---

## 💬 フィードバック

この演習について、感想や改善提案があればお聞かせください：

```
【良かった点】


【難しかった点】


【もっと知りたいこと】

```

---

**作成日**: 2025-11-07
**更新日**: 2025-11-07
**バージョン**: 1.0
