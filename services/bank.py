"""
services/bank.py
----------------
Bank class — creates and manages all accounts and cards.
Seeds demo data used at startup.
"""

from models.card    import Card
from models.account import SavingsAccount, CurrentAccount
from services.atm   import ATM


class Bank:
    """
    Represents the bank that owns the ATM and customer accounts.
    Responsible for creating accounts, issuing cards, and loading the ATM.
    """

    def __init__(self, name: str):
        self.name     = name
        self.accounts = {}   # account_id → Account
        self.cards    = {}   # card_number → Card

    def create_savings_account(self, account_id: str, holder: str,
                                balance: float) -> SavingsAccount:
        acc = SavingsAccount(account_id, holder, balance)
        self.accounts[account_id] = acc
        return acc

    def create_current_account(self, account_id: str, holder: str,
                                balance: float) -> CurrentAccount:
        acc = CurrentAccount(account_id, holder, balance)
        self.accounts[account_id] = acc
        return acc

    def issue_card(self, card_number: str, pin: str,
                   account_id: str) -> Card:
        card = Card(card_number, pin, account_id)
        self.cards[card_number] = card
        return card

    def load_atm(self, atm: ATM) -> None:
        """Register all bank accounts and cards into the ATM."""
        for acc in self.accounts.values():
            atm.register_account(acc)
        for card in self.cards.values():
            atm.register_card(card)


def create_demo_bank() -> tuple:
    """
    Seed a demo bank with 3 customers and return (bank, atm).
    Called once at startup.

    Demo Accounts:
    ┌──────────────┬──────────────┬──────────┬──────────────┬──────────┐
    │ Name         │ Account ID   │ Type     │ Card No      │ PIN      │
    ├──────────────┼──────────────┼──────────┼──────────────┼──────────┤
    │ Rishi Kumar  │ ACC001       │ Savings  │ 1234...5678  │ 1234     │
    │ Priya Sharma │ ACC002       │ Current  │ 9876...4321  │ 4321     │
    │ Arjun Mehta  │ ACC003       │ Savings  │ 1111...2222  │ 9999     │
    └──────────────┴──────────────┴──────────┴──────────────┴──────────┘
    """
    bank = Bank("PyBank")
    atm  = ATM(atm_id="ATM-PYB-001", location="Jamshedpur Branch")

    # Create accounts
    bank.create_savings_account("ACC001", "Rishi Kumar",  50_000.0)
    bank.create_current_account("ACC002", "Priya Sharma", 1_00_000.0)
    bank.create_savings_account("ACC003", "Arjun Mehta",  15_000.0)

    # Issue cards
    bank.issue_card("1234567812345678", "1234", "ACC001")
    bank.issue_card("9876543298764321", "4321", "ACC002")
    bank.issue_card("1111222233332222", "9999", "ACC003")

    # Load ATM
    bank.load_atm(atm)

    return bank, atm
