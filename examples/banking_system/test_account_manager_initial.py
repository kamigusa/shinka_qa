"""
銀行勘定系システム - 初期テストファイル（カバレッジ約35%）

このテストファイルは、レガシーシステムに典型的な
「ハッピーパス」のみをテストしている状態を再現しています。

Shinka Qualityを使用して、このテストスイートを改善していきます。
"""

import pytest
from decimal import Decimal
from account_manager import (
    BankAccount,
    TransactionType,
    AccountStatus,
    InsufficientBalanceError
)


def test_create_account():
    """口座作成の基本テスト"""
    account = BankAccount(
        account_number="1234567890",
        account_holder="山田太郎",
        initial_balance=Decimal("10000.00")
    )

    assert account.account_number == "1234567890"
    assert account.account_holder == "山田太郎"
    assert account.balance == Decimal("10000.00")


def test_deposit_success():
    """入金の基本テスト"""
    account = BankAccount(
        account_number="1234567890",
        account_holder="山田太郎",
        initial_balance=Decimal("10000.00")
    )

    transaction = account.deposit(Decimal("5000.00"), "給与振込")

    assert account.balance == Decimal("15000.00")
    assert transaction.amount == Decimal("5000.00")


def test_withdraw_success():
    """出金の基本テスト"""
    account = BankAccount(
        account_number="1234567890",
        account_holder="山田太郎",
        initial_balance=Decimal("20000.00")
    )

    transaction = account.withdraw(Decimal("5000.00"), "ATM出金")

    assert account.balance == Decimal("15000.00")
    assert transaction.amount == Decimal("5000.00")


def test_get_balance():
    """残高照会テスト"""
    account = BankAccount(
        account_number="1234567890",
        account_holder="山田太郎",
        initial_balance=Decimal("10000.00")
    )

    balance = account.get_balance()
    assert balance == Decimal("10000.00")


def test_transfer_success():
    """振込の基本テスト"""
    account1 = BankAccount(
        account_number="1234567890",
        account_holder="山田太郎",
        initial_balance=Decimal("50000.00")
    )

    account2 = BankAccount(
        account_number="0987654321",
        account_holder="佐藤花子",
        initial_balance=Decimal("10000.00")
    )

    account1.transfer(account2, Decimal("10000.00"), "送金")

    # 手数料500円が引かれる
    assert account1.balance == Decimal("39500.00")
    assert account2.balance == Decimal("20000.00")


# 以下のエッジケース・エラーケースは未実装
# - 口座番号のバリデーションテスト
# - 最低残高を下回る出金のテスト
# - 負の金額での入出金テスト
# - 口座凍結時の操作テスト
# - 取引履歴のフィルタリングテスト
# - 利息計算のテスト
# - 1日の出金限度額テスト
# - 巨額取引の制限テスト
# - 口座解約のテスト
# - 境界値テスト（0円、マイナス、最大値など）
