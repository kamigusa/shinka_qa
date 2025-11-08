# Part 3: 変異戦略の理解 - チュートリアルガイド

**所要時間**: 25-30分
**難易度**: 中級
**前提知識**: Part 2完了

---

## 🎯 このパートで学ぶこと

1. 8つの変異戦略の詳細
2. 各戦略のBefore/After
3. 戦略の使い分け方
4. 実践的な設定例

---

## 📚 8つの変異戦略

### 戦略1: add_edge_case（境界値テスト）

**目的**: 境界値の前後をテスト

**Before**:
```python
def test_calculate_discount():
    assert calculate_discount(30) == 0.1
```

**After**:
```python
@pytest.mark.parametrize("age,expected", [
    (17, 0.0),   # 18未満の境界（17歳）
    (18, 0.1),   # 境界値（18歳）
    (19, 0.1),   # 18以上の境界（19歳）
    (64, 0.1),   # 65未満の境界（64歳）
    (65, 0.3),   # 境界値（65歳）
    (66, 0.3),   # 65以上の境界（66歳）
])
def test_calculate_discount_boundaries(age, expected):
    assert calculate_discount(age) == expected
```

**適用場面**:
- if文の条件分岐が多い
- 数値の範囲チェックがある
- 日付・時刻の処理がある

---

### 戦略2: parameterize_test（パラメータ化）

**目的**: 同じパターンのテストを効率化

**Before**:
```python
def test_add_positive():
    assert add(1, 2) == 3

def test_add_negative():
    assert add(-1, -2) == -3

def test_add_zero():
    assert add(0, 0) == 0
```

**After**:
```python
@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (-1, -2, -3),
    (0, 0, 0),
])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

**メリット**:
- コード量: 15行 → 7行
- 保守性: ケース追加が1行
- 可読性: パターンが明確

---

### 戦略3: add_error_handling（エラーハンドリング）

**目的**: 異常系のテストを追加

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
    with pytest.raises(ValueError, match="division by zero"):
        divide(10, 0)

def test_divide_invalid_type():
    with pytest.raises(TypeError):
        divide("10", 2)

def test_divide_none():
    with pytest.raises(TypeError):
        divide(None, 2)

def test_divide_overflow():
    with pytest.raises(OverflowError):
        divide(10**308, 10**-308)
```

**カバーするエラー**:
- ValueError: ゼロ除算、範囲外
- TypeError: 型不一致
- OverflowError: オーバーフロー
- その他: カスタム例外

---

### 戦略4: add_assertion（アサーション強化）

**目的**: 検証を詳細にする

**Before**:
```python
def test_user_creation():
    user = create_user("Alice", 25)
    assert user is not None
```

**After**:
```python
def test_user_creation():
    user = create_user("Alice", 25)

    # 存在確認
    assert user is not None

    # 属性確認
    assert user.name == "Alice"
    assert user.age == 25

    # 型確認
    assert isinstance(user, User)

    # 追加属性確認
    assert user.created_at is not None
    assert isinstance(user.created_at, datetime)
```

**バグ検出例**:
```python
# バグのある実装
def create_user(name, age):
    return User(name="Admin", age=0)  # 引数を無視

# Before のテスト
assert user is not None  # ✓ パス（バグ見逃し）

# After のテスト
assert user.name == "Alice"  # ✗ 失敗！バグ発見！
```

---

### 戦略5: add_fixture（フィクスチャ追加）

**目的**: セットアップ/クリーンアップの共通化

**Before**:
```python
def test_database_insert():
    db = Database()
    db.connect("localhost", 5432)
    db.authenticate("user", "password")

    db.insert("Alice")
    result = db.query("Alice")

    db.disconnect()
    assert result == "Alice"

def test_database_update():
    db = Database()
    db.connect("localhost", 5432)
    db.authenticate("user", "password")

    db.insert("Bob")
    db.update("Bob", "Bobby")
    result = db.query("Bobby")

    db.disconnect()
    assert result == "Bobby"
```

**After**:
```python
@pytest.fixture
def db():
    """データベース接続フィクスチャ"""
    database = Database()
    database.connect("localhost", 5432)
    database.authenticate("user", "password")

    yield database

    database.disconnect()

def test_database_insert(db):
    db.insert("Alice")
    assert db.query("Alice") == "Alice"

def test_database_update(db):
    db.insert("Bob")
    db.update("Bob", "Bobby")
    assert db.query("Bobby") == "Bobby"
```

**メリット**:
- DRY原則: 重複排除
- 保守性: 変更が1箇所
- 安全性: クリーンアップ保証

---

### 戦略6: add_mock（モック/スタブ）

**目的**: 外部依存を排除

**Before**:
```python
def test_get_weather():
    # 実際のAPIを呼ぶ
    weather = get_weather("Tokyo")
    assert weather is not None
```

**問題点**:
- 遅い（2-3秒）
- 不安定（ネットワーク依存）
- 課金される
- テスト環境で実行不可

**After**:
```python
def test_get_weather(mocker):
    # APIコールをモック化
    mocker.patch('weather_api.fetch',
        return_value={"city": "Tokyo", "temp": 25, "humidity": 60})

    weather = get_weather("Tokyo")

    assert weather["city"] == "Tokyo"
    assert weather["temp"] == 25
    assert weather["humidity"] == 60
```

**メリット**:
- 速い（< 0.01秒）
- 安定（ネットワーク不要）
- 無料
- どこでも実行可能

---

### 戦略7: optimize_assertion（アサーション最適化）

**目的**: アサーションを簡潔に

**Before**:
```python
def test_list_contents():
    result = get_list()
    assert result[0] == 1
    assert result[1] == 2
    assert result[2] == 3
    assert len(result) == 3

def test_dict_contents():
    result = get_dict()
    assert "name" in result
    assert result["name"] == "Alice"
    assert "age" in result
    assert result["age"] == 25
```

**After**:
```python
def test_list_contents():
    result = get_list()
    assert result == [1, 2, 3]

def test_dict_contents():
    result = get_dict()
    assert result == {"name": "Alice", "age": 25}
```

**メリット**:
- コード量削減
- 失敗時のメッセージがわかりやすい
- 保守性向上

---

### 戦略8: refactor_test（テストリファクタリング）

**目的**: テストコードの品質向上

**Before**:
```python
def test_complex_calculation():
    # Magic number
    result = calculate(10, 20, 30, 0.5, True)
    assert result == 35.0

    # 重複したロジック
    x = 10 * 2
    y = 20 * 2
    z = 30 * 2
    result2 = calculate(x, y, z, 0.5, True)
    assert result2 == 70.0
```

**After**:
```python
# 定数化
BASE_VALUE = 10
MULTIPLIER = 0.5
ENABLE_FLAG = True

def double(value):
    """値を2倍にする"""
    return value * 2

def test_complex_calculation_base_case():
    """基本ケースのテスト"""
    result = calculate(BASE_VALUE, 20, 30, MULTIPLIER, ENABLE_FLAG)
    expected = 35.0
    assert result == expected

def test_complex_calculation_doubled():
    """2倍値でのテスト"""
    doubled_values = [double(v) for v in [BASE_VALUE, 20, 30]]
    result = calculate(*doubled_values, MULTIPLIER, ENABLE_FLAG)
    expected = 70.0
    assert result == expected
```

**改善点**:
- Magic numberを定数化
- 重複ロジックを関数化
- テスト名を明確化
- コメント追加

---

## ⚖️ 戦略の使い分け

### 優先度別ガイド

| 優先度 | 戦略 | 推奨する状況 |
|--------|------|------------|
| **高** | add_edge_case | 常に使用 |
| **高** | parameterize_test | 常に使用 |
| **高** | add_error_handling | 常に使用 |
| **中** | add_assertion | アサーションが弱い場合 |
| **中** | add_fixture | セットアップが重複している場合 |
| **中** | add_mock | 外部依存が多い場合 |
| **低** | optimize_assertion | コード整理時 |
| **低** | refactor_test | 保守性向上時 |

### 推奨設定パターン

**パターン1: ミニマル（高優先度のみ）**:
```yaml
mutation_strategies:
  - add_edge_case
  - parameterize_test
  - add_error_handling
```

**パターン2: スタンダード（中優先度まで）**:
```yaml
mutation_strategies:
  - add_edge_case
  - parameterize_test
  - add_error_handling
  - add_assertion
  - add_fixture
  - add_mock
```

**パターン3: フル（全戦略）**:
```yaml
mutation_strategies:
  - add_edge_case
  - parameterize_test
  - add_error_handling
  - add_assertion
  - add_fixture
  - add_mock
  - optimize_assertion
  - refactor_test
```

---

## 🔧 実践例

### 例1: API テスト

**コード**:
```python
def fetch_user_data(user_id):
    response = requests.get(f"https://api.example.com/users/{user_id}")
    if response.status_code != 200:
        raise ValueError("User not found")
    return response.json()
```

**推奨戦略**:
```yaml
mutation_strategies:
  - add_edge_case      # user_id境界値
  - add_error_handling # ネットワークエラー
  - add_mock          # API呼び出しをモック
```

**生成されるテスト**:
```python
def test_fetch_user_data(mocker):
    mocker.patch('requests.get',
        return_value=Mock(status_code=200, json=lambda: {"id": 1, "name": "Alice"}))
    result = fetch_user_data(1)
    assert result["name"] == "Alice"

def test_fetch_user_data_not_found(mocker):
    mocker.patch('requests.get',
        return_value=Mock(status_code=404))
    with pytest.raises(ValueError, match="User not found"):
        fetch_user_data(999)

@pytest.mark.parametrize("user_id", [0, 1, 9999, -1])
def test_fetch_user_data_boundaries(mocker, user_id):
    mocker.patch('requests.get',
        return_value=Mock(status_code=200, json=lambda: {"id": user_id}))
    result = fetch_user_data(user_id)
    assert result["id"] == user_id
```

---

### 例2: データベース操作

**コード**:
```python
def save_order(order):
    db = get_database()
    db.insert("orders", order)
    return order.id
```

**推奨戦略**:
```yaml
mutation_strategies:
  - add_fixture        # DB接続
  - add_error_handling # DB エラー
  - add_assertion      # 保存確認
```

---

## ❓ よくある質問

### Q1: 全戦略を使うべきですか？

**A**: いいえ、プロジェクトに応じて選択

- 小規模: 高優先度のみ（3戦略）
- 中規模: 中優先度まで（6戦略）
- 大規模: 全戦略（8戦略）

### Q2: 戦略の順番は重要ですか？

**A**: 影響しませんが、推奨順序あり

1. add_edge_case（基本カバレッジ）
2. parameterize_test（効率化）
3. add_error_handling（バグ検出）

### Q3: カスタム戦略は作れますか？

**A**: はい、Part 6で学習

---

## 📝 チェックリスト

- [ ] 8つの戦略を理解した
- [ ] Before/Afterの違いを確認した
- [ ] 優先度を理解した
- [ ] 推奨設定を試した
- [ ] 自プロジェクトに適用した

**全てチェックできたら、Part 4に進みましょう！**

---

**作成日**: 2025-11-07
**バージョン**: 1.0
