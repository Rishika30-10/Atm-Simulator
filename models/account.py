"""
models/account.py
-----------------
Account hierarchy using OOP Inheritance & Polymorphism:

  Account  (abstract base)
    ├── SavingsAccount
    └── CurrentAccount
"""

from abc import ABC, abstractmethod
from datetime import datetime


class Account(ABC):
    """Abstract base class for all account types."""

    def __init__(self, account_id: str, holder_name: str, balance: float = 0.0):
        self._account_id   = account_id
        self._holder_name  = holder_name
        self._balance      = balance
        self._transactions = []          # list of transaction dicts

    # ── Properties ─────────────────────────────────────────────────
    @property
    def account_id(self) -> str:
        return self._account_id

    @property
    def holder_name(self) -> str:
        return self._holder_name

    @property
    def balance(self) -> float:
        return self._balance

    @property
    def account_type(self) -> str:
        return self.__class__.__name__

    # ── Abstract Methods (must be implemented by subclasses) ───────
    @abstractmethod
    def get_withdrawal_limit(self) -> float:
        """Return the daily withdrawal limit for this account type."""
        pass

    @abstractmethod
    def get_minimum_balance(self) -> float:
        """Return the minimum balance required."""
        pass

    # ── Core Operations ────────────────────────────────────────────
    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than zero.")
        self._balance += amount
        self._log_transaction("DEPOSIT", amount)

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero.")
        if amount > self.get_withdrawal_limit():
            raise ValueError(
                f"Amount exceeds daily withdrawal limit of "
                f"₹{self.get_withdrawal_limit():,.2f}."
            )
        if (self._balance - amount) < self.get_minimum_balance():
            raise ValueError(
                f"Insufficient funds. Minimum balance of "
                f"₹{self.get_minimum_balance():,.2f} must be maintained."
            )
        self._balance -= amount
        self._log_transaction("WITHDRAWAL", amount)

    def transfer(self, target_account: "Account", amount: float) -> None:
        self.withdraw(amount)                          # raises if not possible
        target_account.deposit(amount)
        self._log_transaction("TRANSFER OUT", amount, target_account.account_id)
        target_account._log_transaction("TRANSFER IN", amount, self._account_id)

    # ── Transaction Log ────────────────────────────────────────────
    def _log_transaction(self, txn_type: str, amount: float,
                          reference: str = "") -> None:
        self._transactions.append({
            "type":      txn_type,
            "amount":    amount,
            "balance":   self._balance,
            "time":      datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "reference": reference,
        })

    def get_mini_statement(self, n: int = 5) -> list:
        """Return last N transactions (most recent first)."""
        return list(reversed(self._transactions[-n:]))

    # ── Display ────────────────────────────────────────────────────
    def __str__(self):
        return (f"{self.account_type} | {self._account_id} | "
                f"{self._holder_name} | ₹{self._balance:,.2f}")

    def __repr__(self):
        return f"{self.account_type}(id={self._account_id}, balance={self._balance})"


# ══════════════════════════════════════════════════════════════════
class SavingsAccount(Account):
    """
    Savings Account:
      - Withdrawal limit  : ₹25,000 / day
      - Minimum balance   : ₹1,000
      - Interest rate     : 4% p.a.
    """
    WITHDRAWAL_LIMIT = 25_000.0
    MINIMUM_BALANCE  = 1_000.0
    INTEREST_RATE    = 0.04

    def get_withdrawal_limit(self) -> float:
        return self.WITHDRAWAL_LIMIT

    def get_minimum_balance(self) -> float:
        return self.MINIMUM_BALANCE

    def apply_interest(self) -> float:
        """Apply monthly interest and return interest amount."""
        interest = round(self._balance * (self.INTEREST_RATE / 12), 2)
        self._balance += interest
        self._log_transaction("INTEREST CREDIT", interest)
        return interest


# ══════════════════════════════════════════════════════════════════
class CurrentAccount(Account):
    """
    Current Account:
      - Withdrawal limit  : ₹1,00,000 / day
      - Minimum balance   : ₹5,000
      - Overdraft allowed : up to ₹10,000
    """
    WITHDRAWAL_LIMIT = 1_00_000.0
    MINIMUM_BALANCE  = 5_000.0
    OVERDRAFT_LIMIT  = 10_000.0

    def get_withdrawal_limit(self) -> float:
        return self.WITHDRAWAL_LIMIT

    def get_minimum_balance(self) -> float:
        # Overdraft: can go negative up to overdraft limit
        return -self.OVERDRAFT_LIMIT

    def get_overdraft_used(self) -> float:
        return max(0.0, -self._balance)
