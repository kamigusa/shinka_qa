# Part 3: 変異戦略の理解 - 演習と解答

**所要時間**: 20分
**難易度**: 中級

---

## 問題1: 戦略の識別

以下のBefore/Afterを見て、どの戦略が使われたか答えてください。

### ケースA
```python
# Before
def test_withdraw():
    account = BankAccount(1000)
    account.withdraw(500)
    assert account.balance == 500

# After
@pytest.mark.parametrize("initial,amount,expected", [
    (1000, 500, 500),
    (1000, 1000, 0),
    (1000, 0, 1000),
])
def test_withdraw(initial, amount, expected):
    account = BankAccount(initial)
    account.withdraw(amount)
    assert account.balance == expected
```

**解答**: `parameterize_test`

---

### ケースB
```python
# Before
def test_divide():
    assert divide(10, 2) == 5.0

# After
def test_divide():
    assert divide(10, 2) == 5.0

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)
```

**解答**: `add_error_handling`

---

### ケースC
```python
# Before
def test_user():
    user = create_user("Alice")
    assert user is not None

# After
def test_user():
    user = create_user("Alice")
    assert user is not None
    assert user.name == "Alice"
    assert isinstance(user, User)
```

**解答**: `add_assertion`

---

## 問題2: 戦略の選択

以下のコードに最適な戦略を選んでください。

### コードA
```python
def calculate_tax(income):
    if income <= 0:
        return 0
    elif income <= 10000:
        return income * 0.05
    elif income <= 50000:
        return income * 0.10
    else:
        return income * 0.20
```

**解答**: `add_edge_case`

**理由**: 0, 10000, 50000の境界値テストが必要

**生成されるテスト例**:
```python
@pytest.mark.parametrize("income,expected_rate", [
    (0, 0.0),       # 境界値
    (1, 0.05),      # 0超の境界
    (10000, 0.05),  # 10000以下の境界
    (10001, 0.10),  # 10000超の境界
    (50000, 0.10),  # 50000以下の境界
    (50001, 0.20),  # 50000超の境界
])
def test_calculate_tax_boundaries(income, expected_rate):
    result = calculate_tax(income)
    assert result == income * expected_rate
```

---

## 問題3: 設定の作成

自分のプロジェクトに合った戦略設定を作成してください。

**プロジェクト情報**:
- 数学計算ライブラリ
- if文での境界チェックが多数
- 外部APIは使用しない
- エラーハンドリングが不足

**解答例**:
```yaml
mutation_strategies:
  - add_edge_case       # 境界値が多い
  - add_error_handling  # エラー処理不足
  - parameterize_test   # 効率化
  - add_assertion       # 詳細検証
```

---

## 📊 採点

| 問題 | 配点 | 得点 |
|------|------|------|
| 問題1 | 30点 | ___ |
| 問題2 | 30点 | ___ |
| 問題3 | 40点 | ___ |
| **合計** | **100点** | ___ |

**80点以上**: Part 4へ進んでください
**80点未満**: ガイドを再読してください

---

**作成日**: 2025-11-07
**バージョン**: 1.0
