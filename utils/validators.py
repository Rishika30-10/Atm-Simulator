"""
utils/validators.py
-------------------
Input validation helpers used by the CLI runner.
Keeps validation logic out of business classes.
"""


def get_positive_amount(prompt: str) -> float:
    """Keep asking until user enters a valid positive number."""
    while True:
        try:
            value = float(input(prompt).strip())
            if value <= 0:
                print("  ❌  Amount must be greater than zero. Try again.")
                continue
            return value
        except ValueError:
            print("  ❌  Invalid input. Please enter a number.")


def get_pin(prompt: str = "  Enter PIN: ") -> str:
    """Read a 4-digit PIN (no masking in terminal, kept simple)."""
    while True:
        pin = input(prompt).strip()
        if pin.isdigit() and len(pin) == 4:
            return pin
        print("  ❌  PIN must be exactly 4 digits.")


def get_menu_choice(prompt: str, valid: list) -> str:
    """Keep asking until the user picks a valid menu option."""
    while True:
        choice = input(prompt).strip()
        if choice in valid:
            return choice
        print(f"  ❌  Invalid choice. Please select from {valid}.")


def get_account_id(prompt: str) -> str:
    """Read a non-empty account ID."""
    while True:
        acc_id = input(prompt).strip().upper()
        if acc_id:
            return acc_id
        print("  ❌  Account ID cannot be empty.")
