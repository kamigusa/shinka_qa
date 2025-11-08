"""
銀行勘定系システム - 進化後テスト (Generation 1)
追加: バリデーションエラーのテスト
"""

import pytest
from decimal import Decimal
from account_manager import (
    BankAccount,
    TransactionType,
    AccountStatus,
    InsufficientBalanceError,
    AccountFrozenError,
    InvalidAmountError
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


# 新規追加: 口座作成バリデーションテスト
def test_create_account_invalid_account_number():
    """無効な口座番号でのエラーテスト"""
    with pytest.raises(ValueError, match="口座番号は10桁"):
        BankAccount(
            account_number="123",  # 短すぎる
            account_holder="山田太郎",
            initial_balance=Decimal("10000.00")
        )


def test_create_account_empty_holder():
    """空の名義人でのエラーテスト"""
    with pytest.raises(ValueError, match="口座名義人は必須"):
        BankAccount(
            account_number="1234567890",
            account_holder="",
            initial_balance=Decimal("10000.00")
        )


def test_create_account_insufficient_initial_balance():
    """最低残高未満でのエラーテスト"""
    with pytest.raises(ValueError, match="初期残高"):
        BankAccount(
            account_number="1234567890",
            account_holder="山田太郎",
            initial_balance=Decimal("500.00")  # 最低残高未満
        )


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


# 新規追加: 入金エラーテスト
def test_deposit_negative_amount():
    """負の金額での入金エラーテスト"""
    account = BankAccount(
        account_number="1234567890",
        account_holder="山田太郎",
        initial_balance=Decimal("10000.00")
    )

    with pytest.raises(InvalidAmountError, match="0より大きい"):
        account.deposit(Decimal("-1000.00"))


def test_deposit_zero_amount():
    """ゼロ円での入金エラーテスト"""
    account = BankAccount(
        account_number="1234567890",
        account_holder="山田太郎",
        initial_balance=Decimal("10000.00")
    )

    with pytest.raises(InvalidAmountError):
        account.deposit(Decimal("0.00"))


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
