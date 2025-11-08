# Part 12: 実践ハンズオン - 銀行勘定系システム

**所要時間**: 60分
**難易度**: 中級〜上級
**前提知識**: Part 0-11完了
**使用例**: `examples/banking_system`

---

## 🎯 このパートで学ぶこと

1. エンタープライズレベルのシステムへのShinka QA適用
2. 複雑なビジネスロジックのテスト進化
3. 金融システム特有の要件（規制、監査）への対応
4. 実際のプロジェクトで得られるROIの計算

---

## 📂 プロジェクト概要

### Banking System とは

実際の銀行勘定系システムを模した、エンタープライズレベルのサンプルです。
金融サービス業界でShinka QAを活用する際の参考になります。

**複雑度**:
- **ステートメント数**: 129行
- **ブランチ数**: 46分岐
- **クラス数**: 4クラス
- **エラー型**: 3種類の独自例外

**機能**:
- 入金・出金・振込
- 残高照会
- 取引履歴管理
- 口座凍結・解除
- 最低残高チェック
- 日次出金限度額管理
- 振込手数料計算
- 利息計算

**ビジネスルール**:
- 最低残高: ¥1,000
- 振込手数料: ¥500
- 日次出金限度: ¥1,000,000
- 口座ステータス: ACTIVE, FROZEN, CLOSED

**ファイル構成**:
```
examples/banking_system/
├── account_manager.py                      # 本番コード (正常版)
├── account_manager_buggy.py                # バグ版 (9つの重大バグ)
├── test_account_manager_initial.py         # 初期テスト (5テスト, 58%カバレッジ)
├── test_account_manager_evolved_gen1.py    # 第1世代 (10テスト, 63%)
├── test_account_manager_evolved_gen2.py    # 第2世代 (20テスト, 79%)
├── test_account_manager_evolved_final.py   # 最終世代 (35テスト, 95%)
├── quality_config.yaml                     # 設定ファイル
├── quality_config_demo.yaml                # デモ用設定（軽量版）
├── evolution_results.json                  # 進化メトリクス
├── EVOLUTION_REPORT.md                     # 詳細レポート
├── evolution_report.html                   # HTMLレポート
└── CASE_STUDY.md                           # ケーススタディ
```

---

## 🚀 ステップ1: プロジェクトの理解 (10分)

### 1.1 プロジェクトディレクトリに移動

```bash
cd examples/banking_system
```

### 1.2 ソースコードの構造を確認

```bash
# 主要クラスを確認
grep -n "^class " account_manager.py
```

**出力**:
```python
15:class TransactionType(Enum):
23:class AccountStatus(Enum):
30:class InsufficientBalanceError(Exception):
35:class AccountFrozenError(Exception):
40:class InvalidAmountError(Exception):
45:class Transaction:
67:class BankAccount:
```

### 1.3 ビジネスロジックの複雑性を確認

```bash
# 重要なメソッドを確認
grep -n "def " account_manager.py | head -15
```

**主要メソッド**:
- `deposit()` - 入金処理
- `withdraw()` - 出金処理
- `transfer()` - 振込処理
- `get_balance()` - 残高照会
- `freeze_account()` - 口座凍結
- `unfreeze_account()` - 凍結解除
- `get_transaction_history()` - 取引履歴
- `calculate_interest()` - 利息計算
- `_validate_amount()` - 金額バリデーション
- `_check_daily_limit()` - 日次限度チェック

### 1.4 初期テストを確認

```bash
cat test_account_manager_initial.py
```

**初期テスト（5つのみ）**:
```python
def test_create_account():
    """口座作成のテスト"""
    account = BankAccount("123456", "山田太郎", Decimal("10000"))
    assert account.get_balance() == Decimal("10000")

def test_deposit():
    """入金のテスト"""
    account = BankAccount("123456", "山田太郎", Decimal("10000"))
    account.deposit(Decimal("5000"))
    assert account.get_balance() == Decimal("15000")

def test_withdraw():
    """出金のテスト"""
    account = BankAccount("123456", "山田太郎", Decimal("10000"))
    account.withdraw(Decimal("3000"))
    assert account.get_balance() == Decimal("7000")

def test_transfer():
    """振込のテスト"""
    account1 = BankAccount("123456", "山田太郎", Decimal("10000"))
    account2 = BankAccount("789012", "佐藤花子", Decimal("5000"))
    account1.transfer(account2, Decimal("2000"))
    assert account1.get_balance() == Decimal("7500")  # 2000 + 手数料500
    assert account2.get_balance() == Decimal("7000")

def test_transaction_history():
    """取引履歴のテスト"""
    account = BankAccount("123456", "山田太郎", Decimal("10000"))
    account.deposit(Decimal("5000"))
    history = account.get_transaction_history()
    assert len(history) == 1
```

**問題点**:
- ✅ ハッピーパスのみ
- ❌ エラーケースが未テスト
- ❌ 境界値が未テスト
- ❌ 口座凍結機能が未テスト
- ❌ 日次限度チェックが未テスト
- ❌ 利息計算が未テスト

---

## 📊 ステップ2: ベースライン測定 (10分)

### 2.1 初期カバレッジを測定

```bash
pytest test_account_manager_initial.py -v \
  --cov=account_manager \
  --cov-report=term-missing \
  --cov-branch
```

**期待される出力**:
```
test_account_manager_initial.py::test_create_account PASSED
test_account_manager_initial.py::test_deposit PASSED
test_account_manager_initial.py::test_withdraw PASSED
test_account_manager_initial.py::test_transfer PASSED
test_account_manager_initial.py::test_transaction_history PASSED

========== Coverage Report ==========
Name                Stmts   Miss  Branch  BrMiss  Cover
-------------------------------------------------------
account_manager.py    129     54      46      24    58%

Missing lines: 95-102, 108-115, 125-132, 145-158, 165-180
```

**分析**:
- ✅ 実装: 5テスト（ハッピーパスのみ）
- ❌ ブランチカバレッジ: 58%
- ❌ 未カバー: エラーハンドリング、境界値、特殊ケース

### 2.2 バグ検出能力を測定

```bash
# バグ版に差し替え
cp account_manager.py account_manager_backup.py
cp account_manager_buggy.py account_manager.py

# 初期テストでバグ検出
pytest test_account_manager_initial.py -v

# 元に戻す
mv account_manager_backup.py account_manager.py
```

**結果**:
```
test_account_manager_initial.py::test_create_account PASSED
test_account_manager_initial.py::test_deposit PASSED
test_account_manager_initial.py::test_withdraw FAILED  ❌ Bug 1 detected
test_account_manager_initial.py::test_transfer FAILED  ❌ Bug 2 detected
test_account_manager_initial.py::test_transaction_history PASSED

Bugs Detected: 2/9 (22%)
```

**検出できなかったバグ（7つ）**:
- 最低残高チェックの不具合
- 口座凍結時の処理バグ
- 日次限度額チェックの抜け
- 無効な金額のバリデーション漏れ
- 利息計算のロジックエラー
- 取引履歴フィルタリングのバグ
- エッジケースでのクラッシュ

### 2.3 ベンチマーク実行

```bash
shinka-qa benchmark --config quality_config.yaml
```

**期待される出力**:
```
🧬 Shinka Quality Benchmark - Enterprise Edition
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Configuration:
  Target Module: account_manager.py
  Complexity: 129 statements, 46 branches
  Domain: Financial Services (Regulated)
  Initial Test: test_account_manager_initial.py
  Seeded Bugs: 9 critical bugs

📊 Initial Metrics:
  Tests Passed: 5
  Branch Coverage: 58.0%
  Bugs Detected: 2/9 (22.2%)
  Code Quality: 0.62/1.0

⚠️ Risk Assessment:
  Critical Paths Untested: 7
  Error Handling Coverage: 15%
  Business Logic Coverage: 63%

✅ Baseline Established
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## ⚙️ ステップ3: 設定ファイルの最適化 (10分)

### 3.1 金融システム向け設定を確認

```bash
cat quality_config.yaml
```

```yaml
# Shinka Quality 設定ファイル - 銀行勘定系システム

# テスト対象
target:
  module_path: "account_manager.py"
  test_initial_path: "test_account_manager_initial.py"
  seeded_bugs_path: "account_manager_buggy.py"

# 適応度関数の重み（金融系向け調整）
fitness_weights:
  coverage: 0.35          # カバレッジ
  bug_detection: 0.45     # バグ検出を最優先（金融系）
  efficiency: 0.10        # 実行効率
  maintainability: 0.10   # コード品質

# 変異戦略（金融系に最適化）
mutation_strategies:
  - "add_edge_cases"       # 境界値テスト
  - "improve_assertions"   # アサーション強化
  - "add_parametrize"      # パラメータ化テスト
```

### 3.2 設定のポイント

**金融システム特有の調整**:

1. **バグ検出を最優先 (45%)**:
   - 金融システムではバグが重大な損失につながる
   - カバレッジよりバグ検出を重視

2. **適切な変異戦略**:
   - `add_edge_cases`: 境界値（最低残高、限度額）
   - `improve_assertions`: Decimal型の精度確認
   - エラーハンドリングの徹底

3. **実行効率は低優先 (10%)**:
   - 正確性 > 速度
   - 夜間バッチでの実行を想定

---

## 🧪 ステップ4: テスト進化の実行 (15分)

### 4.1 デモ用設定で簡易実行（オプション）

時間が限られている場合、軽量版で試す:

```bash
shinka-qa evolve --config quality_config_demo.yaml --verbose
```

`quality_config_demo.yaml`:
```yaml
evolution:
  generations: 5       # 30 → 5（デモ用）
  population_size: 10  # 20 → 10
  num_islands: 2       # 4 → 2
```

### 4.2 本格実行

```bash
shinka-qa evolve --config quality_config.yaml --verbose
```

### 4.3 進化プロセスの観察

**Generation 1-5**: 基本的なエッジケース追加
```
Generation 1/30:
  Island 0: Coverage=60.5% Bugs=2/9 Fitness=0.48
  Island 1: Coverage=62.8% Bugs=3/9 Fitness=0.55 ⭐
  Island 2: Coverage=59.2% Bugs=2/9 Fitness=0.45
  Island 3: Coverage=61.1% Bugs=3/9 Fitness=0.52

💡 Insight: Added tests for InsufficientBalanceError
```

**Generation 5-10**: エラーハンドリング強化
```
Generation 5/30:
  Island 0: Coverage=68.3% Bugs=5/9 Fitness=0.71
  Island 1: Coverage=71.2% Bugs=5/9 Fitness=0.74
  Island 2: Coverage=69.8% Bugs=4/9 Fitness=0.68
  Island 3: Coverage=72.5% Bugs=6/9 Fitness=0.78 ⭐

💡 Insight: Caught AccountFrozenError and InvalidAmountError cases
```

**Generation 10**: 島間移住
```
Generation 10/30 [Migration]:
  🔄 Migrating elite solutions...
  Island 0: Coverage=78.2% Bugs=6/9 Fitness=0.82
  Island 1: Coverage=76.9% Bugs=6/9 Fitness=0.80
  Island 2: Coverage=77.5% Bugs=7/9 Fitness=0.84 ⭐
  Island 3: Coverage=75.8% Bugs=6/9 Fitness=0.79

💡 Insight: Migration brought daily limit tests
```

**Generation 15-25**: パラメータ化と境界値テスト
```
Generation 20/30:
  Island 0: Coverage=87.3% Bugs=8/9 Fitness=0.91
  Island 1: Coverage=89.1% Bugs=8/9 Fitness=0.93
  Island 2: Coverage=88.6% Bugs=8/9 Fitness=0.92
  Island 3: Coverage=90.2% Bugs=9/9 Fitness=0.95 ⭐

💡 Insight: Parametrize tests found boundary bugs
```

**Generation 30**: 最終結果
```
Generation 30/30:
  Island 0: Coverage=93.1% Bugs=9/9 Fitness=0.96
  Island 1: Coverage=92.5% Bugs=9/9 Fitness=0.95
  Island 2: Coverage=94.3% Bugs=9/9 Fitness=0.97
  Island 3: Coverage=95.7% Bugs=9/9 Fitness=0.98 ⭐ BEST

✨ Evolution Complete!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Final Results:
  Initial Coverage: 58.0%
  Final Coverage:   95.7% (+37.7 points)

  Initial Bugs: 2/9 (22%)
  Final Bugs:   9/9 (100%)

  Test Cases: 5 → 35 (+600%)
  Execution Time: 0.42s
  Code Quality: 0.89/1.0

💰 Economic Impact:
  Time Saved: 22.5 hours
  Cost Savings: ¥180,000
  Bug Prevention Value: ¥3,500,000
  Total ROI: ¥3,680,000

💾 Results saved to: results/run_20250108_145623/
```

---

## 📈 ステップ5: 進化したテストの分析 (10分)

### 5.1 最終テストコードを確認

```bash
cat test_account_manager_evolved_final.py | head -100
```

**追加されたテスト例**:

1. **境界値テスト**:
```python
@pytest.mark.parametrize("initial,withdraw,should_fail", [
    (Decimal("2000"), Decimal("999"), False),   # ギリギリOK
    (Decimal("2000"), Decimal("1000"), True),   # 最低残高違反
    (Decimal("2000"), Decimal("1001"), True),   # 最低残高違反
])
def test_withdraw_minimum_balance(initial, withdraw, should_fail):
    account = BankAccount("123456", "Test", initial)
    if should_fail:
        with pytest.raises(InsufficientBalanceError):
            account.withdraw(withdraw)
    else:
        account.withdraw(withdraw)
        assert account.get_balance() == Decimal("1000")
```

2. **エラーハンドリング**:
```python
def test_withdraw_frozen_account():
    """凍結口座からの出金は失敗"""
    account = BankAccount("123456", "Test", Decimal("10000"))
    account.freeze_account()
    with pytest.raises(AccountFrozenError):
        account.withdraw(Decimal("1000"))

def test_deposit_negative_amount():
    """負の金額での入金は失敗"""
    account = BankAccount("123456", "Test", Decimal("10000"))
    with pytest.raises(InvalidAmountError):
        account.deposit(Decimal("-100"))

def test_daily_withdrawal_limit():
    """日次出金限度を超える出金は失敗"""
    account = BankAccount("123456", "Test", Decimal("2000000"))
    with pytest.raises(Exception, match="daily limit"):
        account.withdraw(Decimal("1000001"))
```

3. **ビジネスロジックの検証**:
```python
def test_transfer_with_fee():
    """振込手数料が正しく計算される"""
    account1 = BankAccount("123456", "Sender", Decimal("10000"))
    account2 = BankAccount("789012", "Receiver", Decimal("5000"))

    account1.transfer(account2, Decimal("2000"))

    # 送金側: 2000 + 手数料500 = 2500引かれる
    assert account1.get_balance() == Decimal("7500")
    # 受取側: 2000受け取る
    assert account2.get_balance() == Decimal("7000")

def test_calculate_interest_accuracy():
    """利息計算の精度を検証"""
    account = BankAccount("123456", "Test", Decimal("1000000"))
    interest_rate = Decimal("0.02")
    days = 365

    interest = account.calculate_interest(interest_rate, days)

    # 1,000,000 * 0.02 * 365/365 = 20,000
    assert interest == Decimal("20000.00")
```

4. **取引履歴のフィルタリング**:
```python
def test_transaction_history_filtering():
    """取引種別でフィルタリング"""
    account = BankAccount("123456", "Test", Decimal("100000"))

    account.deposit(Decimal("10000"))
    account.withdraw(Decimal("5000"))
    account.deposit(Decimal("3000"))

    # 入金のみ取得
    deposits = account.get_transaction_history(
        transaction_type=TransactionType.DEPOSIT
    )
    assert len(deposits) == 2

    # 出金のみ取得
    withdrawals = account.get_transaction_history(
        transaction_type=TransactionType.WITHDRAWAL
    )
    assert len(withdrawals) == 1
```

### 5.2 世代ごとの進化を比較

```bash
# 第1世代 (10テスト)
wc -l test_account_manager_evolved_gen1.py

# 第2世代 (20テスト)
wc -l test_account_manager_evolved_gen2.py

# 最終世代 (35テスト)
wc -l test_account_manager_evolved_final.py
```

### 5.3 全バグの検出を確認

```bash
# バグ版に差し替え
cp account_manager.py account_manager_backup.py
cp account_manager_buggy.py account_manager.py

# 進化したテストで全バグ検出
pytest test_account_manager_evolved_final.py -v | grep FAILED

# 元に戻す
mv account_manager_backup.py account_manager.py
```

**検出されるバグ（9個全て）**:
```
FAILED test_withdraw_minimum_balance - Bug 1: 最低残高チェック
FAILED test_withdraw_frozen - Bug 2: 凍結口座の扱い
FAILED test_deposit_invalid - Bug 3: 負の金額
FAILED test_transfer_fee - Bug 4: 手数料計算
FAILED test_daily_limit - Bug 5: 日次限度
FAILED test_interest_calc - Bug 6: 利息計算
FAILED test_history_filter - Bug 7: 履歴フィルタ
FAILED test_edge_case_1 - Bug 8: ゼロ残高
FAILED test_edge_case_2 - Bug 9: 浮動小数点誤差
```

---

## 💰 ステップ6: ROI分析 (5分)

### 6.1 時間とコストの計算

**手動でのテスト作成時間**:
```
35テスト × 45分/テスト = 1,575分 = 26.25時間
```

**Shinka QAでの所要時間**:
```
設定: 15分
実行: 10分
レビュー: 30分
合計: 55分 = 約1時間
```

**削減時間**:
```
26.25時間 - 1時間 = 25.25時間
削減率: 96%
```

**コスト削減**:
```
時給 ¥8,000 × 25.25時間 = ¥202,000
```

### 6.2 バグ防止による価値

**検出されたバグの重大度**:
| バグ | 重大度 | 本番での推定損失 |
|------|-------|---------------|
| 最低残高チェック | Critical | ¥1,000,000 |
| 振込手数料計算 | Critical | ¥800,000 |
| 日次限度チェック | High | ¥500,000 |
| 口座凍結処理 | High | ¥400,000 |
| 利息計算 | Medium | ¥300,000 |
| その他4つ | Low | ¥500,000 |
| **合計** | | **¥3,500,000** |

### 6.3 総ROI

```
コスト削減: ¥202,000
バグ防止: ¥3,500,000
─────────────────────
総価値: ¥3,702,000

投資:
ツール: ¥0 (OSS)
学習: 2時間 × ¥8,000 = ¥16,000
実行: 1時間 × ¥8,000 = ¥8,000
合計: ¥24,000

ROI: (¥3,702,000 - ¥24,000) / ¥24,000 = 153倍
```

---

## 📊 ステップ7: レポート確認 (5分)

### 7.1 HTMLレポートを開く

```bash
open evolution_report.html
# または
start evolution_report.html  # Windows
xdg-open evolution_report.html  # Linux
```

### 7.2 重要な指標

**進化の推移グラフ**:
- カバレッジ: 58% → 95.7%
- バグ検出: 22% → 100%
- 適応度: 0.456 → 0.98

**最も効果的だった戦略**:
1. `add_edge_cases` (境界値): +18.3%
2. `add_parametrize` (パラメータ化): +12.7%
3. `improve_assertions` (アサーション): +6.7%

### 7.3 経営層向けサマリー

```bash
cat EXECUTIVE_PRESENTATION.md
```

---

## 💡 学んだこと

### 1. エンタープライズシステムの特徴

- **複雑なビジネスロジック**: 単純なユニットテストでは不十分
- **多様なエラー条件**: 3種類の独自例外を適切にテスト
- **状態管理**: 口座ステータスの遷移を網羅
- **規制要件**: 監査証跡（取引履歴）の正確性

### 2. 金融システム向けの設定

- **バグ検出を最優先** (45%の重み)
- **境界値テストが重要** (最低残高、限度額)
- **Decimal型の精度管理**
- **エラーハンドリングの徹底**

### 3. ROIの実例

- **時間削減**: 96% (26時間 → 1時間)
- **コスト削減**: ¥202,000
- **バグ防止価値**: ¥3,500,000
- **総ROI**: 153倍

### 4. 段階的進化の効果

- **Gen 1**: 基本的なエッジケース (+5%)
- **Gen 10**: エラーハンドリング (+20%)
- **Gen 20**: パラメータ化テスト (+30%)
- **Gen 30**: 最適化 (+37.7%)

---

## 🎯 練習問題

### 初級: 他のバグを追加

`account_manager_buggy.py` に新しいバグを仕込む:
```python
def close_account(self):
    """口座を閉鎖"""
    # 新バグ: 残高チェックを忘れている
    self.status = AccountStatus.CLOSED
```

**タスク**: 進化実行後、このバグも検出できるか確認

### 中級: カスタム設定で再実行

カバレッジ重視の設定に変更:
```yaml
fitness_weights:
  coverage: 0.6
  bug_detection: 0.2
  efficiency: 0.1
  maintainability: 0.1
```

**タスク**: 結果を比較し、どちらが実務で有効か考察

### 上級: 他の金融機能を追加

新機能を追加して進化:
```python
def apply_overdraft_protection(self, limit: Decimal):
    """当座貸越設定"""
    pass

def get_account_statement(self, start_date, end_date):
    """口座明細書取得"""
    pass
```

**タスク**:
1. 初期テストを作成
2. 進化実行
3. カバレッジ90%以上を達成

---

## ✅ チェックリスト

- [ ] プロジェクトの複雑性を理解した
- [ ] 初期カバレッジを測定した (58%)
- [ ] バグ検出率を確認した (2/9 = 22%)
- [ ] 金融システム向け設定を理解した
- [ ] 進化を実行した（30世代）
- [ ] 最終カバレッジを確認した (95%超)
- [ ] 全9バグを検出できた (100%)
- [ ] ROI分析を完了した (153倍)
- [ ] HTMLレポートを確認した
- [ ] ビジネス価値を理解した

**全てチェックできたら、実際のプロジェクトに適用してみましょう！**

---

## 🔗 関連リソース

- [ソースコード](../../examples/banking_system/account_manager.py)
- [詳細レポート](../../examples/banking_system/EVOLUTION_REPORT.md)
- [ケーススタディ](../../examples/banking_system/CASE_STUDY.md)
- [経営層向けプレゼン](../../examples/banking_system/EXECUTIVE_PRESENTATION.md)
- [Part 11: 電卓アプリ](../part11_hands_on_calculator/guide.md)

---

**作成日**: 2025-11-08
**バージョン**: 1.0
**対象例**: examples/banking_system
**想定読者**: 中級〜上級エンジニア、QAリード、技術マネージャー
