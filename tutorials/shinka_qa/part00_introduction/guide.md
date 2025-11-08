# Part 0: イントロダクション - チュートリアルガイド

**所要時間**: 10-15分（自習の場合は20分）
**難易度**: 入門
**前提知識**: Python、pytestの基礎

---

## 🎯 このパートで学ぶこと

1. なぜテスト品質が重要なのか
2. Shinka QAとは何か
3. どのような問題を解決できるのか
4. 本チュートリアルの全体像
5. 必要な環境とツール

---

## 📖 理論と背景知識

### テスト品質の重要性

ソフトウェア開発において、テストは以下の役割を果たします：

#### 1. バグの早期発見
- 本番環境でのバグ発見コスト: **¥500,000 - ¥2,000,000**
- 開発段階でのバグ発見コスト: **¥10,000 - ¥50,000**
- **コスト削減率: 95%以上**

#### 2. リファクタリングの安全性
高品質なテストがあれば、自信を持ってコードを改善できます。

**テストなし**:
```python
# 怖くて触れない...
def complex_calculation(data):
    # 500行の複雑なロジック
    # 誰も理解していない
    pass
```

**テストあり**:
```python
def test_complex_calculation_edge_cases():
    assert complex_calculation([]) == 0
    assert complex_calculation([1, 2, 3]) == 6
    assert complex_calculation(None) raises ValueError
# → 安心してリファクタリングできる
```

#### 3. ドキュメントとしての役割
```python
def test_user_cannot_withdraw_more_than_balance():
    """
    ユーザーは残高を超えて出金できない
    これがビジネスルール
    """
    account = BankAccount(balance=1000)
    with pytest.raises(InsufficientBalanceError):
        account.withdraw(1500)
```

テストは「実行可能な仕様書」として機能します。

---

### テスト品質が低くなる3つの理由

#### 理由1: 時間的制約

**典型的なシナリオ**:
```
PM: 「リリースまで2日しかない！」
Dev: 「テストは...ハッピーパスだけで」
```

**結果**:
- カバレッジ: 30-40%
- エッジケース: ほぼゼロ
- バグ検出率: 20%以下

#### 理由2: 経験不足

エッジケースを網羅的に考えるには経験が必要です。

**経験が浅い開発者のテスト**:
```python
def test_divide():
    assert divide(10, 2) == 5.0
```

**経験豊富な開発者のテスト**:
```python
@pytest.mark.parametrize("a,b,expected,raises", [
    (10, 2, 5.0, None),           # 基本
    (0, 5, 0.0, None),             # ゼロ除数
    (10, 0, None, ValueError),     # ゼロ被除数
    (-10, 2, -5.0, None),          # 負の数
    (float('inf'), 2, None, ValueError),  # 無限大
])
def test_divide_comprehensive(a, b, expected, raises):
    if raises:
        with pytest.raises(raises):
            divide(a, b)
    else:
        assert divide(a, b) == expected
```

#### 理由3: モチベーション

**同じようなテストを延々と書く**のは退屈です：

```python
def test_add_positive():
    assert add(1, 1) == 2

def test_add_negative():
    assert add(-1, -1) == -2

def test_add_zero():
    assert add(0, 0) == 0

def test_add_mixed():
    assert add(1, -1) == 0

# あと50個...😫
```

---

### 手動テストの限界

#### 実例: 銀行口座管理モジュール

**モジュールサイズ**: 350行
**メソッド数**: 12個
**ビジネスルール**: 15個

**手動テスト作成**:
- 所要時間: **25時間**
- 作成されたテスト数: 5-10個
- カバレッジ: **35%**
- バグ検出率: **22%** (2/9のバグを検出)

**問題点**:
1. エッジケースの漏れ
2. エラーハンドリングのテスト不足
3. 境界値テストがない
4. パフォーマンステストなし

---

## 💡 Shinka QA の紹介

### 概要

**Shinka QA**は、進化的アルゴリズムを使用してテストコードを自動的に改善するツールです。

#### コア機能

1. **自動テスト生成**: 既存テストを分析し、不足している部分を自動で追加
2. **多次元評価**: カバレッジ、バグ検出、効率性、保守性を総合評価
3. **進化的改善**: 世代を重ねるごとに品質が向上

### 動作原理（簡易版）

```
┌─────────────────┐
│ 既存テスト      │
│ (Generation 0)  │
│ Coverage: 42%   │
└────────┬────────┘
         │
         ↓ 変異 (Mutation)
┌─────────────────┐
│ 改善案1         │ ─┐
│ 改善案2         │  │ 適応度評価
│ 改善案3         │  │ (Fitness)
│ 改善案4         │ ─┘
└────────┬────────┘
         │
         ↓ 選択 (Selection)
┌─────────────────┐
│ Generation 1    │
│ Coverage: 65%   │
└────────┬────────┘
         │
         ↓ 繰り返し
┌─────────────────┐
│ Generation 5    │
│ Coverage: 92%   │
└─────────────────┘
```

### Before / After の具体例

#### Before: 初期テスト
```python
"""
初期のテストコード
カバレッジ: 42%
テスト数: 2個
バグ検出: 20%
"""

def test_add():
    assert add(2, 3) == 5

def test_divide():
    assert divide(10, 2) == 5.0
```

#### After: Shinka QA 適用後
```python
"""
進化後のテストコード
カバレッジ: 92%
テスト数: 12個
バグ検出: 100%
"""

import pytest
from decimal import Decimal

@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
    (1.5, 2.5, 4.0),
    (Decimal('0.1'), Decimal('0.2'), Decimal('0.3')),
])
def test_add_comprehensive(a, b, expected):
    """加算の包括的テスト"""
    assert add(a, b) == expected


def test_add_large_numbers():
    """大きな数値のテスト"""
    assert add(10**10, 10**10) == 2 * 10**10


def test_divide():
    """除算の基本テスト"""
    assert divide(10, 2) == 5.0


def test_divide_by_zero():
    """ゼロ除算のエラーテスト"""
    with pytest.raises(ValueError, match="division by zero"):
        divide(10, 0)


def test_divide_negative():
    """負の数の除算テスト"""
    assert divide(-10, 2) == -5.0
    assert divide(10, -2) == -5.0


@pytest.mark.parametrize("a,b,expected", [
    (10.0, 3.0, pytest.approx(3.333, rel=1e-3)),
    (1.0, 3.0, pytest.approx(0.333, rel=1e-3)),
])
def test_divide_float_precision(a, b, expected):
    """浮動小数点の精度テスト"""
    assert divide(a, b) == expected
```

**改善点**:
- ✅ パラメータ化テストで複数ケースを効率的にカバー
- ✅ エラーハンドリングのテスト追加
- ✅ 境界値（大きな数、負の数）のテスト
- ✅ 浮動小数点の精度テスト
- ✅ Decimal型での正確な計算テスト

**時間**:
- 手動作成: 推定3-4時間
- Shinka QA: **実測20分**

---

### 3つの特徴

#### 1. 自動進化

**人間がやること**:
```bash
shinka-qa evolve --config quality_config.yaml
```

**Shinka QAがやること**:
1. 既存テストの分析
2. カバレッジギャップの特定
3. エッジケースの生成
4. アサーションの改善
5. パラメータ化
6. フィクスチャとモックの追加

#### 2. 既存テスト活用

ゼロから書き直す必要はありません。

**既存テスト** (活かされる):
```python
def test_basic():
    account = BankAccount(balance=1000)
    assert account.balance == 1000
```

**追加されるテスト**:
```python
def test_negative_balance():
    with pytest.raises(ValueError):
        BankAccount(balance=-1000)

def test_zero_balance():
    account = BankAccount(balance=0)
    assert account.balance == 0

# 既存テストはそのまま残る
```

#### 3. エンタープライズ対応

**実績**:
- 金融機関（SOX、Basel III、FISC対応)での採用を想定
- 大規模コードベース（10万行以上）での使用を想定

**セキュリティ**:
- オンプレミス対応
- コードは外部に送信されない
- 監査証跡の保存

---

## 📚 本チュートリアルの構成

### 全体像（3時間コース）

| Part | タイトル | 時間 | 内容 |
|------|----------|------|------|
| 0 | イントロダクション | 10分 | 概要と動機づけ |
| 1 | はじめての進化 | 15分 | 実際に動かしてみる |
| 2 | 設定のカスタマイズ | 20分 | プロジェクトに合わせる |
| - | 休憩 | 10分 | - |
| 3 | 変異戦略の理解 | 25分 | 戦略の使い分け |
| 4 | 実プロジェクト適用 | 30分 | 実際のコードで試す |
| 5 | CI/CD統合 | 25分 | 自動化パイプライン |
| 6 | 高度な使い方 | 30分 | カスタマイズと最適化 |
| 7 | トラブルシューティング | 20分 | よくある問題と解決法 |
| 8 | エンタープライズ導入 | 25分 | 大規模組織での展開 |
| 9 | ケーススタディ | 15分 | 銀行システムの例 |
| 10 | まとめ | 15分 | 振り返りと次のステップ |

### 学習の進め方

#### ステップ1: 体験（Part 0-1）
まずは動かして、「わお！」という感動を味わってください。

#### ステップ2: 理解（Part 2-3）
設定と戦略を理解し、自分でカスタマイズできるようになります。

#### ステップ3: 実践（Part 4-6）
実際のプロジェクトに適用し、CI/CDに統合します。

#### ステップ4: 発展（Part 7-10）
トラブルシューティング、エンタープライズ導入、ケーススタディで知識を深めます。

---

## 🖥️ 必要な環境

### ソフトウェア要件

#### 必須
- **Python**: 3.11以上（推奨: 3.12）
- **pip**: 最新版
- **Git**: バージョン管理用

#### 推奨
- **VSCode** または **PyCharm**: エディタ
- **ターミナル**: bash, zsh, PowerShell

### 環境確認

```bash
# Pythonバージョン確認
python --version
# 期待される出力: Python 3.11.x または 3.12.x

# pipバージョン確認
pip --version
# 期待される出力: pip 23.x.x 以上

# Gitバージョン確認
git --version
# 期待される出力: git version 2.x.x
```

### インストール（次のPartで実施）

```bash
# リポジトリのクローン
git clone https://github.com/Kamigusa/shinka-qa.git
cd shinka-qa

# 依存関係のインストール
pip install -e .
```

---

## ❓ よくある質問

### Q1: どのくらいの時間がかかりますか？

**A**: コードサイズによりますが：
- 100行のモジュール: 5-10分
- 500行のモジュール: 15-30分
- 2000行のモジュール: 1-2時間

手動の1/10程度です。

### Q2: どんな言語に対応していますか？

**A**: 現在はPythonのpytestに対応しています。

今後の対応予定：
- JavaScript/TypeScript (Jest)
- Java (JUnit)
- Go (testing package)

### Q3: 無料ですか？

**A**: はい、完全にオープンソース（MIT License）で、商用利用も可能です。

### Q4: 生成されたテストは正しいですか？

**A**: Shinka QAは以下を保証します：
- ✅ 生成されたテストは全て実行できる（構文エラーなし）
- ✅ 既存の機能を壊さない（リグレッションなし）

ただし、**人間のレビューは推奨**します。

### Q5: 既存のテストは消えますか？

**A**: いいえ、既存のテストは全て保持されます。新しいテストが追加されるだけです。

### Q6: LLM（ChatGPTなど）が必要ですか？

**A**: いいえ、LLMなしでも動作します。
ただし、LLMを使用すると生成品質が向上します。

### Q7: どのくらいカバレッジが上がりますか？

**A**: 典型的には：
- 初期40% → 最終85-95%
- 改善幅: +45-55ポイント

### Q8: チームで使えますか？

**A**: はい、以下をサポートしています：
- CI/CDパイプライン統合
- 設定ファイルの共有
- レポートの自動生成

---

## 📝 チェックリスト

このPartを終える前に、以下を確認してください：

- [ ] テスト品質の重要性を理解した
- [ ] Shinka QAが何をするツールか理解した
- [ ] Before/Afterの違いを見た
- [ ] 本チュートリアルの全体像を把握した
- [ ] 環境要件を確認した
- [ ] よくある質問を読んだ

全てチェックできたら、**Part 1: はじめての進化**に進みましょう！

---

## 📊 参考文献

1. Fowler, M. (2018). "Refactoring: Improving the Design of Existing Code"

https://silab.fon.bg.ac.rs/wp-content/uploads/2016/10/Refactoring-Improving-the-Design-of-Existing-Code-Addison-Wesley-Professional-1999.pdf

2. Beck, K. (2002). "Test-Driven Development: By Example"

https://dokumen.pub/test-driven-development-by-example-0321146530-9780321146533.html

3. Fraser, G., & Arcuri, A. (2011). "EvoSuite: Automatic Test Suite Generation for Object-Oriented Software"

https://www.evosuite.org/wp-content/papercite-data/pdf/esecfse11.pdf

---

**作成日**: 2025-11-07
**更新日**: 2025-11-07
**バージョン**: 1.0
