# 🧬 Mutation Strategies Guide

Shinka QAは17種類の包括的な変異戦略を提供し、ソフトウェアテスト技法を完全に網羅します。

## 📋 目次

1. [基本戦略](#基本戦略)
2. [高度なテスト技法](#高度なテスト技法)
3. [プロパティ・パフォーマンステスト](#プロパティパフォーマンステスト)
4. [ネガティブ・セキュリティテスト](#ネガティブセキュリティテスト)
5. [ユーザーシナリオ・リグレッション](#ユーザーシナリオリグレッション)

---

## 基本戦略

### 1. `add_edge_cases` - エッジケーステスト

**目的**: 境界条件や特殊な入力値をテストする

**追加されるテスト**:
- None/null値
- 空の入力（空文字列、空リスト、空辞書）
- ゼロ値
- 負の値
- 型エラーを引き起こす入力

**例**:
```python
def test_divide_by_zero():
    """ゼロ除算のテスト"""
    with pytest.raises(ValueError):
        divide(10, 0)

def test_divide_none_input():
    """None入力のテスト"""
    with pytest.raises(TypeError):
        divide(None, 5)
```

### 2. `improve_assertions` - アサーション改善

**目的**: テストの診断能力を向上させる

**改善内容**:
- `assert True/False` → 具体的な値比較
- Null チェック追加
- 型チェック追加
- エラーメッセージ追加

**例**:
```python
# 改善前
def test_add():
    result = add(2, 3)
    assert result == 5

# 改善後
def test_add():
    result = add(2, 3)
    assert result is not None, "Result should not be None"
    assert isinstance(result, (int, float)), "Result should be numeric"
    assert result == 5, f"Expected 5 but got {result}"
```

### 3. `add_parametrize` - パラメータ化テスト

**目的**: 複数のテストケースを効率的に実行

**追加されるテスト**:
- `@pytest.mark.parametrize` デコレータを使用
- 多様な入力値の組み合わせ
- DRY原則の適用

**例**:
```python
@pytest.mark.parametrize("a,b,expected", [
    (0, 0, 0),
    (1, 1, 2),
    (-1, 1, 0),
    (100, 200, 300),
    (-5, -3, -8),
])
def test_add_parametrized(a, b, expected):
    assert add(a, b) == expected
```

### 4. `add_fixtures` - フィクスチャ追加

**目的**: テストのセットアップとクリーンアップを改善

**追加されるもの**:
- pytest fixtures
- テストデータの再利用
- セットアップ/ティアダウンの分離

### 5. `add_mocks` - モック化

**目的**: 外部依存を分離し、テストの独立性を向上

**追加されるもの**:
- `unittest.mock` または `pytest-mock` の使用
- 外部API/DB呼び出しのモック
- テストの高速化と安定化

---

## 高度なテスト技法

### 6. `add_boundary_value_tests` - 境界値分析 (BVA)

**目的**: 境界条件で最もバグが発生しやすいことを活用

**テスト戦略**:
- **最小値 (min)**
- **最小値+1 (min+1)**
- **通常値 (nominal)**
- **最大値-1 (max-1)**
- **最大値 (max)**
- **境界を超える値**

**数値の場合**:
```python
def test_function_boundary_zero():
    """ゼロ境界のテスト"""
    assert func(0) is not None
    assert func(-1) is not None
    assert func(1) is not None

def test_function_boundary_min_max():
    """最小/最大境界のテスト"""
    assert func(-sys.maxsize) is not None
    assert func(sys.maxsize) is not None
```

**文字列/コレクションの場合**:
- 空 (長さ0)
- 1要素
- 大量の要素
- 許容最大サイズ前後

### 7. `add_equivalence_partitioning` - 同値分割 (EP)

**目的**: 入力空間を等価なクラスに分割し、効率的にテスト

**テスト戦略**:
- **有効同値クラス**: 正常に動作すべき入力のグループ
- **無効同値クラス**: エラーになるべき入力のグループ

**例**:
```python
# 有効同値クラス
@pytest.mark.parametrize("value", [1, 50, 100, 500, 1000])
def test_valid_positive_class(value):
    """正の整数同値クラス"""
    assert func(value) is not None

# 無効同値クラス
@pytest.mark.parametrize("value", [None, "invalid", [], {}])
def test_invalid_type_class(value):
    """無効型同値クラス"""
    with pytest.raises((TypeError, ValueError)):
        func(value)
```

### 8. `add_null_safety_tests` - Null安全性テスト

**目的**: Null関連のバグを防止

**テストすべき値**:
- `None`
- 空文字列 `""`
- 空リスト `[]`
- 空辞書 `{}`
- Falsy値 (`False`, `0`, `0.0`)
- 特殊な数値 (`nan`, `inf`, `-inf`)

**例**:
```python
def test_none_handling():
    """None入力のテスト"""
    with pytest.raises((TypeError, ValueError)):
        func(None)

def test_nan_handling():
    """NaN処理のテスト"""
    with pytest.raises((ValueError, TypeError)):
        func(float('nan'))

def test_infinity_handling():
    """無限大処理のテスト"""
    with pytest.raises((ValueError, OverflowError)):
        func(float('inf'))
```

### 9. `add_state_transition_tests` - 状態遷移テスト

**目的**: オブジェクトの状態変化を検証

**テスト戦略**:
- 初期状態の確認
- 有効な状態遷移シーケンス
- 無効な状態遷移の検出
- 状態の不変条件 (invariants)

**例**:
```python
def test_state_sequence_valid():
    """有効な状態遷移シーケンス"""
    obj = ClassName()
    assert obj.state == 'initial'

    obj.transition_to_active()
    assert obj.state == 'active'

    obj.transition_to_complete()
    assert obj.state == 'complete'

def test_state_sequence_invalid():
    """無効な状態遷移"""
    obj = ClassName()
    with pytest.raises(InvalidStateError):
        obj.transition_to_complete()  # initial->complete は無効
```

### 10. `add_combination_tests` - 組み合わせテスト (ペアワイズ)

**目的**: パラメータの組み合わせを効率的にテスト

**テスト戦略**:
- 全組み合わせではなく、ペアワイズカバレッジ
- 各パラメータのペアが少なくとも1回テストされる
- テスト数を大幅に削減しながら高いカバレッジを達成

**例**:
```python
@pytest.mark.parametrize("param1,param2,param3", [
    (True, 'small', 10),
    (True, 'large', 100),
    (False, 'small', 100),
    (False, 'large', 10),
])
def test_pairwise_combinations(param1, param2, param3):
    """ペアワイズパラメータテスト"""
    result = func(param1, param2, param3)
    assert result is not None
```

---

## プロパティ・パフォーマンステスト

### 11. `add_property_based_tests` - プロパティベーステスト

**目的**: 関数の数学的性質を検証

**テスト戦略**:
- **不変条件 (invariants)**: 常に成り立つべき条件
- **対称性・可換性**: f(a,b) = f(b,a)
- **結合性**: f(f(a,b),c) = f(a,f(b,c))
- **冪等性**: f(f(x)) = f(x)
- **ラウンドトリップ性**: decode(encode(x)) = x

**例**:
```python
def test_addition_commutative():
    """加算の可換性"""
    assert add(3, 5) == add(5, 3)
    assert add(10, 20) == add(20, 10)

def test_addition_associative():
    """加算の結合性"""
    val1 = add(add(2, 3), 4)
    val2 = add(2, add(3, 4))
    assert val1 == val2

def test_deterministic():
    """決定性: 同じ入力は同じ出力"""
    result1 = func(5)
    result2 = func(5)
    assert result1 == result2
```

### 12. `add_performance_edge_cases` - パフォーマンステスト

**目的**: パフォーマンスの問題を早期発見

**テスト戦略**:
- 大量データ処理
- 小さな入力での高速処理
- 繰り返し呼び出し
- タイムアウト検証
- メモリ使用量確認

**例**:
```python
import time

def test_large_input_performance():
    """大量データのパフォーマンステスト"""
    large_data = list(range(10000))
    start = time.time()
    result = func(large_data)
    elapsed = time.time() - start
    assert elapsed < 1.0, f"処理時間 {elapsed}s が長すぎます"
    assert result is not None

def test_small_input_fast():
    """小さな入力の高速処理"""
    start = time.time()
    result = func(1)
    elapsed = time.time() - start
    assert elapsed < 0.01
```

---

## ネガティブ・セキュリティテスト

### 13. `add_negative_tests` - ネガティブテスト

**目的**: エラーハンドリングの検証

**テスト戦略**:
- 予期しない入力
- 不正なデータ形式
- リソース不足シミュレーション
- エラーハンドリングの検証

**例**:
```python
def test_invalid_input_rejected():
    """不正入力の拒否"""
    with pytest.raises(ValueError, match="Invalid input"):
        func(-999)

def test_malformed_data():
    """不正なデータ形式"""
    with pytest.raises((ValueError, TypeError)):
        func({"malformed": "data"})

def test_extreme_values():
    """極端な値のテスト"""
    extreme_values = [-999999999, 999999999, 1e308]
    for extreme in extreme_values:
        try:
            func(extreme)
        except (ValueError, TypeError, OverflowError):
            pass  # 極端な値を拒否するのは正常
```

### 14. `add_security_tests` - セキュリティテスト

**目的**: セキュリティ脆弱性の検出

**テスト戦略**:
- **インジェクション攻撃**: SQL, コマンド, XSS
- **入力検証**: 異常に長い入力、特殊文字
- **認証・認可**: アクセス制御
- **データ漏洩防止**: 機密情報の保護

**例**:
```python
def test_sql_injection_prevention():
    """SQLインジェクション対策"""
    malicious_input = "'; DROP TABLE users; --"
    result = query(malicious_input)
    assert "DROP TABLE" not in str(result)

def test_command_injection_prevention():
    """コマンドインジェクション対策"""
    malicious_input = "; rm -rf /"
    with pytest.raises((ValueError, SecurityError)):
        execute_command(malicious_input)

def test_input_validation():
    """入力検証"""
    # 異常に長い入力
    with pytest.raises(ValueError):
        func("a" * 10000)

    # 特殊文字
    with pytest.raises(ValueError):
        func("<script>alert('xss')</script>")
```

---

## ユーザーシナリオ・リグレッション

### 15. `add_user_scenario_tests` - ユーザーシナリオテスト

**目的**: 実際のユースケースを検証

**テスト戦略**:
- エンドツーエンドのワークフロー
- 複数機能の連携
- 典型的なユーザー操作パターン
- エラーからの回復

**例**:
```python
def test_typical_user_workflow():
    """典型的なユーザーワークフロー"""
    # Step 1: ユーザーが初期化
    session = create_session()
    assert session.is_active()

    # Step 2: データ入力
    session.add_data({"key": "value"})
    assert len(session.data) == 1

    # Step 3: 処理実行
    result = session.process()
    assert result.success

    # Step 4: クリーンアップ
    session.close()
    assert not session.is_active()

def test_error_recovery_scenario():
    """エラーからの回復シナリオ"""
    session = create_session()

    # エラー発生
    with pytest.raises(ProcessError):
        session.process_invalid()

    # 回復確認
    assert session.is_active()
    session.reset()
    assert session.process() is not None
```

### 16. `add_regression_tests` - リグレッションテスト

**目的**: 既知のバグの再発を防止

**テスト戦略**:
- 過去に発見されたバグの再発防止
- 既知のエッジケース
- バグ修正の確認
- 後方互換性の確認

**例**:
```python
def test_bug_123_fixed():
    """Bug #123: ゼロ除算が適切に処理されることの確認"""
    # 以前はクラッシュしていた
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)

def test_bug_456_edge_case():
    """Bug #456: 負の階乗が正しくエラーになることの確認"""
    with pytest.raises(ValueError, match="non-negative"):
        factorial(-5)

def test_backwards_compatibility():
    """後方互換性の確認"""
    # 古いAPIも動作することを確認
    result = old_api_function(param=10)
    assert result is not None
```

---

## 🎯 戦略の選択

### すべての戦略を使用（推奨）

```yaml
mutation_strategies:
  - "add_edge_cases"
  - "improve_assertions"
  - "add_parametrize"
  - "add_fixtures"
  - "add_mocks"
  - "add_boundary_value_tests"
  - "add_equivalence_partitioning"
  - "add_null_safety_tests"
  - "add_state_transition_tests"
  - "add_combination_tests"
  - "add_property_based_tests"
  - "add_performance_edge_cases"
  - "add_negative_tests"
  - "add_security_tests"
  - "add_user_scenario_tests"
  - "add_regression_tests"
```

### 基本戦略のみ（軽量）

```yaml
mutation_strategies:
  - "add_edge_cases"
  - "improve_assertions"
  - "add_parametrize"
```

### セキュリティ重視

```yaml
mutation_strategies:
  - "add_edge_cases"
  - "add_null_safety_tests"
  - "add_negative_tests"
  - "add_security_tests"
  - "add_regression_tests"
```

### パフォーマンス重視

```yaml
mutation_strategies:
  - "add_boundary_value_tests"
  - "add_equivalence_partitioning"
  - "add_performance_edge_cases"
  - "add_property_based_tests"
```

---

## 💡 ベストプラクティス

1. **段階的な適用**: 最初は基本戦略から始め、徐々に高度な戦略を追加
2. **プロジェクトに合わせた選択**: セキュリティが重要なら `add_security_tests`、パフォーマンスが重要なら `add_performance_edge_cases`
3. **LLMとテンプレートの併用**: LLMが利用可能な場合はより高度なテストが生成される
4. **定期的な実行**: CI/CDパイプラインに組み込んで継続的に品質を向上

---

## 📚 参考資料

- [ISTQB Syllabus - Boundary Value Analysis](https://www.istqb.org/)
- [Equivalence Partitioning Technique](https://en.wikipedia.org/wiki/Equivalence_partitioning)
- [Property-Based Testing](https://hypothesis.works/)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
