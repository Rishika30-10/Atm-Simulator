"""
services/atm.py
---------------
ATM class — the central service that orchestrates:
  - Card insertion & PIN validation
  - Session management (logged in / logged out)
  - All ATM operations (balance, withdraw, deposit, transfer, statement)
  - Cash management (ATM's own cash reserve)
  - Receipt generation
"""

from models.card    import Card
from models.account import Account
from utils.display  import Display


class ATM:
    """
    Represents a physical ATM machine.
    Manages sessions and delegates operations to Account objects.
    """

    CASH_CAPACITY = 10_00_000.0     # ₹10 lakh total ATM cash

    def __init__(self, atm_id: str, location: str):
        self.__atm_id       = atm_id
        self.__location     = location
        self.__cash_reserve = self.CASH_CAPACITY

        # Runtime session state
        self.__active_card    = None
        self.__active_account = None
        self.__is_logged_in   = False

        # Registry: card_number → Card, account_id → Account
        self.__cards    = {}
        self.__accounts = {}

    # ── Registration (used by bank to seed data) ───────────────────
    def register_card(self, card: Card) -> None:
        self.__cards[card.account_id] = card

    def register_account(self, account: Account) -> None:
        self.__accounts[account.account_id] = account

    # ── Session ────────────────────────────────────────────────────
    def insert_card(self, card_number_last4: str) -> str:
        """Simulate inserting a card by matching last-4 digits."""
        for acc_id, card in self.__cards.items():
            if card.card_number.endswith(card_number_last4):
                if card.is_blocked:
                    raise PermissionError(
                        "This card is blocked. Please contact your bank."
                    )
                self.__active_card = card
                return acc_id
        raise ValueError("Card not recognised. Please try again.")

    def validate_pin(self, entered_pin: str) -> None:
        self._require_card()
        acc_id  = self.__active_card.account_id
        account = self.__accounts.get(acc_id)
        if not account:
            raise RuntimeError("No account linked to this card.")

        self.__active_card.validate_pin(entered_pin)   # raises on failure
        self.__active_account = account
        self.__is_logged_in   = True

    def logout(self) -> None:
        self.__active_card    = None
        self.__active_account = None
        self.__is_logged_in   = False

    # ── Guards ─────────────────────────────────────────────────────
    def _require_card(self):
        if self.__active_card is None:
            raise RuntimeError("No card inserted.")

    def _require_login(self):
        if not self.__is_logged_in:
            raise RuntimeError("Not authenticated. Please insert card and enter PIN.")

    # ── ATM Operations ─────────────────────────────────────────────
    def check_balance(self) -> dict:
        self._require_login()
        acc = self.__active_account
        return {
            "holder":       acc.holder_name,
            "account_id":   acc.account_id,
            "account_type": acc.account_type,
            "balance":      acc.balance,
        }

    def withdraw(self, amount: float) -> dict:
        self._require_login()

        # Check ATM has enough cash
        if amount > self.__cash_reserve:
            raise ValueError(
                f"ATM has insufficient cash. Maximum dispensable: "
                f"₹{self.__cash_reserve:,.2f}"
            )

        # Validate denomination (multiples of 100)
        if amount % 100 != 0:
            raise ValueError("Amount must be in multiples of ₹100.")

        self.__active_account.withdraw(amount)      # raises if limit/balance issue
        self.__cash_reserve -= amount

        return {
            "amount":    amount,
            "balance":   self.__active_account.balance,
            "atm_cash":  self.__cash_reserve,
        }

    def deposit(self, amount: float) -> dict:
        self._require_login()
        if amount % 100 != 0:
            raise ValueError("Amount must be in multiples of ₹100.")
        self.__active_account.deposit(amount)
        self.__cash_reserve += amount
        return {
            "amount":  amount,
            "balance": self.__active_account.balance,
        }

    def transfer(self, target_account_id: str, amount: float) -> dict:
        self._require_login()
        target = self.__accounts.get(target_account_id)
        if not target:
            raise ValueError(f"Account {target_account_id} not found.")
        if target.account_id == self.__active_account.account_id:
            raise ValueError("Cannot transfer to the same account.")
        self.__active_account.transfer(target, amount)
        return {
            "to":      target.holder_name,
            "amount":  amount,
            "balance": self.__active_account.balance,
        }

    def mini_statement(self, n: int = 5) -> list:
        self._require_login()
        return self.__active_account.get_mini_statement(n)

    def change_pin(self, old_pin: str, new_pin: str) -> None:
        self._require_login()
        self.__active_card.change_pin(old_pin, new_pin)

    # ── ATM Info ───────────────────────────────────────────────────
    @property
    def atm_id(self) -> str:
        return self.__atm_id

    @property
    def location(self) -> str:
        return self.__location

    @property
    def cash_reserve(self) -> float:
        return self.__cash_reserve

    @property
    def active_account(self) -> Account:
        return self.__active_account
