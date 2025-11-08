"""
初期テストファイル（カバレッジ約40%想定）
Shinka Qualityがこれを進化させる
"""

import pytest
from calculator import add, subtract, multiply, divide, power, factorial, is_prime


def test_add_positive():
    """正の数の加算"""
    assert add(2, 3) == 5


def test_subtract_positive():
    """正の数の減算"""
    assert subtract(5, 3) == 2


def test_multiply():
    """乗算"""
    result = multiply(3, 4)
    assert result == 12


def test_divide_simple():
    """単純な除算"""
    result = divide(10, 2)
    assert result == 5.0


def test_power_simple():
    """単純なべき乗"""
    assert power(2, 3) == 8


# 以下のエッジケースは未実装
# - ゼロ除算のテスト
# - 負の数のテスト
# - 階乗のエッジケース
# - 素数判定のエッジケース
# - 型エラーのテスト
