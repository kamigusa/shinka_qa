"""
簡単な電卓モジュール
Shinka Quality のテスト対象サンプル
"""


def add(a, b):
    """2つの数値を加算"""
    return a + b


def subtract(a, b):
    """2つの数値を減算"""
    return a - b


def multiply(a, b):
    """2つの数値を乗算"""
    return a * b


def divide(a, b):
    """2つの数値を除算"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def power(base, exponent):
    """べき乗を計算"""
    if not isinstance(base, (int, float)) or not isinstance(exponent, (int, float)):
        raise TypeError("Both arguments must be numbers")
    return base ** exponent


def factorial(n):
    """階乗を計算"""
    if not isinstance(n, int):
        raise TypeError("Argument must be an integer")
    if n < 0:
        raise ValueError("Argument must be non-negative")
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def is_prime(n):
    """素数判定"""
    if not isinstance(n, int):
        raise TypeError("Argument must be an integer")
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True
