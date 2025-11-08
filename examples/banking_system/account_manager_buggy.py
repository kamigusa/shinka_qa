"""
銀行勘定系システム - バグ版（バグ検出テスト用）

このバージョンには意図的に複数のバグが含まれています。
良いテストスイートはこれらのバグを検出できるはずです。
"""

from typing import Optional, List, Dict
from datetime import datetime
from decimal import Decimal
from enum import Enum


class TransactionType(Enum):
    """取引種別"""
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    TRANSFER = "transfer"
    FEE = "fee"


class AccountStatus(Enum):
    """口座ステータス"""
    ACTIVE = "active"
    FROZEN = "frozen"
    CLOSED = "closed"


class InsufficientBalanceError(Exception):
    """残高不足エラー"""
    pass


class AccountFrozenError(Exception):
    """口座凍結エラー"""
    pass


class InvalidAmountError(Exception):
    """無効な金額エラー"""
    pass


class Transaction:
    """取引記録"""

    def __init__(
        self,
        transaction_id: str,
        account_number: str,
        transaction_type: TransactionType,
        amount: Decimal,
        timestamp: datetime,
        balance_after: Decimal,
        description: str = ""
    ):
        self.transaction_id = transaction_id
        self.account_number = account_number
        self.transaction_type = transaction_type
        self.amount = amount
        self.timestamp = timestamp
        self.balance_after = balance_after
        self.description = description


class BankAccount:
    """銀行口座クラス"""

    MINIMUM_BALANCE = Decimal("1000.00")
    TRANSFER_FEE = Decimal("500.00")
    DAILY_WITHDRAWAL_LIMIT = Decimal("1000000.00")

    def __init__(
        self,
        account_number: str,
        account_holder: str,
        initial_balance: Decimal = Decimal("0.00")
    ):
        # バグ1: 口座番号の長さチェックが甘い（!=の代わりに<を使用）
        if not account_number or len(account_number) < 10:
            raise ValueError("口座番号は10桁である必要があります")

        if not account_holder or len(account_holder.strip()) == 0:
            raise ValueError("口座名義人は必須です")

        # バグ2: 最低残高のチェックが等号なし（<の代わりに<=を使うべき）
        if initial_balance < self.MINIMUM_BALANCE:
            raise ValueError(f"初期残高は{self.MINIMUM_BALANCE}円以上である必要があります")

        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = initial_balance
        self.status = AccountStatus.ACTIVE
        self.transaction_history: List[Transaction] = []
        self.daily_withdrawal_total = Decimal("0.00")
        self.last_withdrawal_date: Optional[datetime] = None

    def deposit(self, amount: Decimal, description: str = "") -> Transaction:
        """入金処理"""
        if self.status != AccountStatus.ACTIVE:
            raise AccountFrozenError(f"口座は{self.status.value}です")

        # バグ3: 0円の入金を許可してしまう（<の代わりに<=を使うべき）
        if amount < Decimal("0"):
            raise InvalidAmountError("入金額は0より大きい必要があります")

        # バグ4: 巨額取引のチェックが緩い（100億円まで許可してしまう）
        if amount > Decimal("10000000000"):
            raise InvalidAmountError("1億円を超える入金はできません")

        self.balance += amount

        transaction = Transaction(
            transaction_id=self._generate_transaction_id(),
            account_number=self.account_number,
            transaction_type=TransactionType.DEPOSIT,
            amount=amount,
            timestamp=datetime.now(),
            balance_after=self.balance,
            description=description
        )

        self.transaction_history.append(transaction)
        return transaction

    def withdraw(self, amount: Decimal, description: str = "") -> Transaction:
        """出金処理"""
        if self.status != AccountStatus.ACTIVE:
            raise AccountFrozenError(f"口座は{self.status.value}です")

        if amount <= Decimal("0"):
            raise InvalidAmountError("出金額は0より大きい必要があります")

        # バグ5: 最低残高チェックの不等号が逆（残高不足でも出金できてしまう）
        if self.balance - amount > self.MINIMUM_BALANCE:
            raise InsufficientBalanceError(
                f"最低残高{self.MINIMUM_BALANCE}円を下回る出金はできません"
            )

        # バグ6: 1日の出金限度額チェックが欠落（コメントアウト）
        # today = datetime.now().date()
        # if self.last_withdrawal_date and self.last_withdrawal_date.date() == today:
        #     if self.daily_withdrawal_total + amount > self.DAILY_WITHDRAWAL_LIMIT:
        #         raise InvalidAmountError(...)

        self.balance -= amount
        self.daily_withdrawal_total += amount
        self.last_withdrawal_date = datetime.now()

        transaction = Transaction(
            transaction_id=self._generate_transaction_id(),
            account_number=self.account_number,
            transaction_type=TransactionType.WITHDRAWAL,
            amount=amount,
            timestamp=datetime.now(),
            balance_after=self.balance,
            description=description
        )

        self.transaction_history.append(transaction)
        return transaction

    def transfer(
        self,
        target_account: 'BankAccount',
        amount: Decimal,
        description: str = ""
    ) -> tuple[Transaction, Transaction]:
        """振込処理"""
        if self.status != AccountStatus.ACTIVE:
            raise AccountFrozenError(f"送金元口座は{self.status.value}です")

        # バグ7: 振込先口座の凍結チェックが欠落
        # if target_account.status != AccountStatus.ACTIVE:
        #     raise AccountFrozenError(...)

        if amount <= Decimal("0"):
            raise InvalidAmountError("振込額は0より大きい必要があります")

        # バグ8: 手数料が計算に含まれていない
        total_amount = amount  # 本来は amount + self.TRANSFER_FEE

        if self.balance - total_amount < self.MINIMUM_BALANCE:
            raise InsufficientBalanceError(
                f"残高不足: 振込額{amount}円 + 手数料{self.TRANSFER_FEE}円"
            )

        self.balance -= total_amount

        withdrawal_tx = Transaction(
            transaction_id=self._generate_transaction_id(),
            account_number=self.account_number,
            transaction_type=TransactionType.TRANSFER,
            amount=total_amount,
            timestamp=datetime.now(),
            balance_after=self.balance,
            description=f"振込: {target_account.account_number} {description}"
        )
        self.transaction_history.append(withdrawal_tx)

        fee_tx = Transaction(
            transaction_id=self._generate_transaction_id(),
            account_number=self.account_number,
            transaction_type=TransactionType.FEE,
            amount=self.TRANSFER_FEE,
            timestamp=datetime.now(),
            balance_after=self.balance,
            description="振込手数料"
        )
        self.transaction_history.append(fee_tx)

        deposit_tx = target_account.deposit(
            amount,
            f"振込: {self.account_number} から {description}"
        )

        return withdrawal_tx, deposit_tx

    def get_balance(self) -> Decimal:
        """残高照会"""
        return self.balance

    def freeze_account(self) -> None:
        """口座凍結"""
        if self.status == AccountStatus.CLOSED:
            raise ValueError("解約済みの口座は凍結できません")
        self.status = AccountStatus.FROZEN

    def unfreeze_account(self) -> None:
        """口座凍結解除"""
        if self.status == AccountStatus.FROZEN:
            self.status = AccountStatus.ACTIVE

    def close_account(self) -> Decimal:
        """口座解約"""
        if self.status == AccountStatus.CLOSED:
            raise ValueError("既に解約済みです")

        final_balance = self.balance
        self.balance = Decimal("0")
        self.status = AccountStatus.CLOSED

        return final_balance

    def get_transaction_history(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        transaction_type: Optional[TransactionType] = None
    ) -> List[Transaction]:
        """取引履歴取得"""
        filtered = self.transaction_history

        if start_date:
            filtered = [tx for tx in filtered if tx.timestamp >= start_date]

        if end_date:
            filtered = [tx for tx in filtered if tx.timestamp <= end_date]

        if transaction_type:
            filtered = [tx for tx in filtered if tx.transaction_type == transaction_type]

        return filtered

    def calculate_interest(self, annual_rate: Decimal) -> Decimal:
        """利息計算（年利）"""
        # バグ9: 負の年利チェックが欠落
        # if annual_rate < Decimal("0"):
        #     raise ValueError("年利は0以上である必要があります")

        if annual_rate > Decimal("0.1"):
            raise ValueError("年利は10%以下である必要があります")

        interest = self.balance * annual_rate
        return interest.quantize(Decimal("0.01"))

    def _generate_transaction_id(self) -> str:
        """取引ID生成"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        return f"TX{self.account_number}{timestamp}"

    def __repr__(self) -> str:
        return (
            f"BankAccount(number={self.account_number}, "
            f"holder={self.account_holder}, "
            f"balance={self.balance}, "
            f"status={self.status.value})"
        )
