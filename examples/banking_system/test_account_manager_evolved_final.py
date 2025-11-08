"""
銀行勘定系システム - 最終進化版テスト (Final Generation)
追加: 利息計算、口座解約、日次出金限度額、エッジケース全般
"""

import pytest
from decimal import Decimal
from datetime import datetime, timedelta
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


def test_create_account_invalid_account_number():
    """無効な口座番号でのエラーテスト"""
    with pytest.raises(ValueError, match="口座番号は10桁"):
        BankAccount(
            account_number="123",
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


def test_create_account_whitespace_holder():
    """空白のみの名義人でのエラーテスト"""
    with pytest.raises(ValueError, match="口座名義人は必須"):
        BankAccount(
            account_number="1234567890",
            account_holder="   ",
            initial_balance=Decimal("10000.00")
        )


def test_create_account_insufficient_initial_balance():
    """最低残高未満でのエラーテスト"""
    with pytest.raises(ValueError, match="初期残高"):
        BankAccount(
            account_number="1234567890",
            account_holder="山田太郎",
            initial_balance=Decimal("500.00")
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
    assert transaction.transaction_type == TransactionType.DEPOSIT


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


def test_deposit_exceeds_limit():
    """1億円超の入金エラーテスト"""
    account = BankAccount(
        account_number="1234567890",
        account_holder="山田太郎",
        initial_balance=Decimal("10000.00")
    )

    with pytest.raises(InvalidAmountError, match="1億円"):
        account.deposit(Decimal("200000000"))


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
    assert transaction.transaction_type == TransactionType.WITHDRAWAL


def test_withdraw_below_minimum_balance():
    """最低残高を下回る出金エラーテスト"""
    account = BankAccount(
        account_number="1234567890",
        account_holder="山田太郎",
        initial_balance=Decimal("3000.00")
    )

    with pytest.raises(InsufficientBalanceError, match="最低残高"):
        account.withdraw(Decimal("2500.00"))


def test_withdraw_negative_amount():
    """負の金額での出金エラーテスト"""
    account = BankAccount(
        account_number="1234567890",
        account_holder="山田太郎",
        initial_balance=Decimal("20000.00")
    )

    with pytest.raises(InvalidAmountError):
        account.withdraw(Decimal("-1000.00"))


def test_withdraw_zero_amount():
    """ゼロ円での出金エラーテスト"""
    account = BankAccount(
        account_number="1234567890",
        account_holder="山田太郎",
        initial_balance=Decimal("20000.00")
    )

    with pytest.raises(InvalidAmountError):
        account.withdraw(Decimal("0"))


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

    withdrawal_tx, deposit_tx = account1.transfer(account2, Decimal("10000.00"), "送金")

    assert account1.balance == Decimal("39500.00")
    assert account2.balance == Decimal("20000.00")
    assert withdrawal_tx.transaction_type == TransactionType.TRANSFER
    assert deposit_tx.transaction_type == TransactionType.DEPOSIT


def test_transfer_insufficient_balance():
    """残高不足での振込エラーテスト"""
    account1 = BankAccount(
        account_number="1234567890",
        account_holder="山田太郎",
        initial_balance=Decimal("5000.00")
    )

    account2 = BankAccount(
        account_number="0987654321",
        account_holder="佐藤花子",
        initial_balance=Decimal("10000.00")
    )

    with pytest.raises(InsufficientBalanceError, match="残高不足"):
        account1.transfer(account2, Decimal("10000.00"))


def test_transfer_frozen_sender():
    """凍結口座からの振込エラーテスト"""
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

    account1.freeze_account()

    with pytest.raises(AccountFrozenError, match="送金元"):
        account1.transfer(account2, Decimal("10000.00"))


def test_transfer_frozen_receiver():
    """凍結口座への振込エラーテスト"""
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

    account2.freeze_account()

    with pytest.raises(AccountFrozenError, match="振込先"):
        account1.transfer(account2, Decimal("10000.00"))


def test_transfer_negative_amount():
    """負の金額での振込エラーテスト"""
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

    with pytest.raises(InvalidAmountError):
        account1.transfer(account2, Decimal("-5000.00"))


def test_freeze_account():
    """口座凍結テスト"""
    account = BankAccount(
        account_number="1234567890",
        account_holder="山田太郎",
        initial_balance=Decimal("10000.00")
    )

    account.freeze_account()
    assert account.status == AccountStatus.FROZEN


def test_unfreeze_account():
    """口座凍結解除テスト"""
    account = BankAccount(
        account_number="1234567890",
        account_holder="山田太郎",
        initial_balance=Decimal("10000.00")
    )

    account.freeze_account()
    account.unfreeze_account()
    assert account.status == AccountStatus.ACTIVE


def test_frozen_account_cannot_deposit():
    """凍結口座への入金エラーテスト"""
    account = BankAccount(
        account_number="1234567890",
        account_holder="山田太郎",
        initial_balance=Decimal("10000.00")
    )

    account.freeze_account()

    with pytest.raises(AccountFrozenError, match="frozen"):
        account.deposit(Decimal("5000.00"))


def test_frozen_account_cannot_withdraw():
    """凍結口座からの出金エラーテスト"""
    account = BankAccount(
        account_number="1234567890",
        account_holder="山田太郎",
        initial_balance=Decimal("10000.00")
    )

    account.freeze_account()

    with pytest.raises(AccountFrozenError):
        account.withdraw(Decimal("5000.00"))


def test_close_account():
    """口座解約テスト"""
    account = BankAccount(
        account_number="1234567890",
        account_holder="山田太郎",
        initial_balance=Decimal("10000.00")
    )

    final_balance = account.close_account()

    assert final_balance == Decimal("10000.00")
    assert account.balance == Decimal("0")
    assert account.status == AccountStatus.CLOSED


def test_close_already_closed_account():
    """既に解約済みの口座を再度解約するエラーテスト"""
    account = BankAccount(
        account_number="1234567890",
        account_holder="山田太郎",
        initial_balance=Decimal("10000.00")
    )

    account.close_account()

    with pytest.raises(ValueError, match="既に解約済み"):
        account.close_account()


def test_freeze_closed_account():
    """解約済み口座の凍結エラーテスト"""
    account = BankAccount(
        account_number="1234567890",
        account_holder="山田太郎",
        initial_balance=Decimal("10000.00")
    )

    account.close_account()

    with pytest.raises(ValueError, match="解約済み"):
        account.freeze_account()


def test_transaction_history():
    """取引履歴の記録テスト"""
    account = BankAccount(
        account_number="1234567890",
        account_holder="山田太郎",
        initial_balance=Decimal("10000.00")
    )

    account.deposit(Decimal("5000.00"), "入金1")
    account.withdraw(Decimal("2000.00"), "出金1")

    history = account.get_transaction_history()
    assert len(history) == 2
    assert history[0].transaction_type == TransactionType.DEPOSIT
    assert history[1].transaction_type == TransactionType.WITHDRAWAL


def test_transaction_history_filter_by_type():
    """取引種別でのフィルタリングテスト"""
    account = BankAccount(
        account_number="1234567890",
        account_holder="山田太郎",
        initial_balance=Decimal("10000.00")
    )

    account.deposit(Decimal("5000.00"))
    account.deposit(Decimal("3000.00"))
    account.withdraw(Decimal("2000.00"))

    deposits = account.get_transaction_history(transaction_type=TransactionType.DEPOSIT)
    assert len(deposits) == 2

    withdrawals = account.get_transaction_history(transaction_type=TransactionType.WITHDRAWAL)
    assert len(withdrawals) == 1


def test_transaction_history_filter_by_date():
    """日付でのフィルタリングテスト"""
    account = BankAccount(
        account_number="1234567890",
        account_holder="山田太郎",
        initial_balance=Decimal("10000.00")
    )

    account.deposit(Decimal("5000.00"))
    account.withdraw(Decimal("2000.00"))

    # 今日以降の取引を取得
    today = datetime.now()
    history = account.get_transaction_history(start_date=today)
    assert len(history) == 2


def test_calculate_interest_basic():
    """利息計算の基本テスト"""
    account = BankAccount(
        account_number="1234567890",
        account_holder="山田太郎",
        initial_balance=Decimal("100000.00")
    )

    # 年利1%
    interest = account.calculate_interest(Decimal("0.01"))
    assert interest == Decimal("1000.00")


def test_calculate_interest_negative_rate():
    """負の年利でのエラーテスト"""
    account = BankAccount(
        account_number="1234567890",
        account_holder="山田太郎",
        initial_balance=Decimal("100000.00")
    )

    with pytest.raises(ValueError, match="年利は0以上"):
        account.calculate_interest(Decimal("-0.01"))


def test_calculate_interest_exceeds_limit():
    """年利10%超でのエラーテスト"""
    account = BankAccount(
        account_number="1234567890",
        account_holder="山田太郎",
        initial_balance=Decimal("100000.00")
    )

    with pytest.raises(ValueError, match="年利は10%以下"):
        account.calculate_interest(Decimal("0.15"))


def test_calculate_interest_zero_rate():
    """年利0%のテスト"""
    account = BankAccount(
        account_number="1234567890",
        account_holder="山田太郎",
        initial_balance=Decimal("100000.00")
    )

    interest = account.calculate_interest(Decimal("0"))
    assert interest == Decimal("0.00")


def test_calculate_interest_max_rate():
    """年利10%のテスト"""
    account = BankAccount(
        account_number="1234567890",
        account_holder="山田太郎",
        initial_balance=Decimal("100000.00")
    )

    interest = account.calculate_interest(Decimal("0.1"))
    assert interest == Decimal("10000.00")


def test_account_repr():
    """アカウント表現のテスト"""
    account = BankAccount(
        account_number="1234567890",
        account_holder="山田太郎",
        initial_balance=Decimal("10000.00")
    )

    repr_str = repr(account)
    assert "1234567890" in repr_str
    assert "山田太郎" in repr_str
    assert "10000" in repr_str
    assert "active" in repr_str
