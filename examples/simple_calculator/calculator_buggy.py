"""
バグを仕込んだバージョン（バグ検出率測定用）
"""


def add(a, b):
    return a + b


def subtract(a, b):
    # バグ1: 符号が逆
    return b - a  # 本来は a - b


def multiply(a, b):
    # バグ2: ゼロの扱いが間違っている
    if a == 0:
        return 1  # 本来は 0
    return a * b


def divide(a, b):
    # バグ3: ゼロチェックが不完全
    if b == 0:
        return 0  # 本来は例外を投げる
    return a / b


def power(base, exponent):
    # バグ4: 型チェックがない
    return base ** exponent  # 文字列などが渡された場合エラー


def factorial(n):
    # バグ5: 負の数のチェックがない
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result  # n < 0 の場合に無限ループ


def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True
