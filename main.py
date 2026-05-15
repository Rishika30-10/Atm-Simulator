"""
main.py
-------
ATM Simulator — Command Line Interface
Entry point. Runs the interactive ATM session loop.

OOP Concepts Demonstrated:
  ✔ Encapsulation   — private attributes in Card, ATM
  ✔ Inheritance     — SavingsAccount, CurrentAccount extend Account
  ✔ Polymorphism    — get_withdrawal_limit(), get_minimum_balance()
  ✔ Abstraction     — Account is an abstract base class (ABC)
  ✔ Composition     — ATM contains Card and Account objects
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from services.bank   import create_demo_bank
from utils.display   import Display
from utils.validators import (get_pin, get_positive_amount,
                               get_menu_choice, get_account_id)


# ──────────────────────────────────────────────────────────────────
# SESSION — operations after login
# ──────────────────────────────────────────────────────────────────
def run_session(atm):
    """Handle all operations for one logged-in session."""
    while True:
        Display.main_menu()
        choice = get_menu_choice("  Select option (1-7): ",
                                  ["1", "2", "3", "4", "5", "6", "7"])

        # ── 1. Balance ────────────────────────────────────────────
        if choice == "1":
            try:
                data = atm.check_balance()
                Display.balance_screen(data)
            except Exception as e:
                Display.error(str(e))

        # ── 2. Withdraw ───────────────────────────────────────────
        elif choice == "2":
            Display.subheader("WITHDRAW CASH")
            Display.info("Amount must be in multiples of ₹100.")
            try:
                amount = get_positive_amount("  Enter amount: ₹")
                data   = atm.withdraw(amount)
                Display.withdrawal_receipt(data)
            except Exception as e:
                Display.error(str(e))

        # ── 3. Deposit ────────────────────────────────────────────
        elif choice == "3":
            Display.subheader("DEPOSIT CASH")
            Display.info("Amount must be in multiples of ₹100.")
            try:
                amount = get_positive_amount("  Enter amount: ₹")
                data   = atm.deposit(amount)
                Display.deposit_receipt(data)
            except Exception as e:
                Display.error(str(e))

        # ── 4. Transfer ───────────────────────────────────────────
        elif choice == "4":
            Display.subheader("FUND TRANSFER")
            try:
                target_id = get_account_id("  Enter target Account ID: ")
                amount    = get_positive_amount("  Enter amount: ₹")
                data      = atm.transfer(target_id, amount)
                Display.transfer_receipt(data)
            except Exception as e:
                Display.error(str(e))

        # ── 5. Mini Statement ─────────────────────────────────────
        elif choice == "5":
            try:
                txns   = atm.mini_statement(n=5)
                holder = atm.active_account.holder_name
                Display.mini_statement(txns, holder)
            except Exception as e:
                Display.error(str(e))

        # ── 6. Change PIN ─────────────────────────────────────────
        elif choice == "6":
            Display.subheader("CHANGE PIN")
            try:
                old_pin = get_pin("  Enter current PIN : ")
                new_pin = get_pin("  Enter new PIN     : ")
                confirm = get_pin("  Confirm new PIN   : ")
                if new_pin != confirm:
                    Display.error("PINs do not match. Try again.")
                else:
                    atm.change_pin(old_pin, new_pin)
                    Display.success("PIN changed successfully!")
            except Exception as e:
                Display.error(str(e))

        # ── 7. Logout ─────────────────────────────────────────────
        elif choice == "7":
            atm.logout()
            Display.success("Logged out successfully. Thank you for banking with PyBank!")
            print()
            break


# ──────────────────────────────────────────────────────────────────
# CARD INSERTION + PIN — entry to a session
# ──────────────────────────────────────────────────────────────────
def run_card_flow(atm):
    """Handle card insertion and PIN entry."""
    Display.subheader("INSERT CARD")
    print("  (Enter the last 4 digits of your card number)")

    # Card insertion
    for attempt in range(3):
        try:
            last4 = input("  Card last 4 digits: ").strip()
            atm.insert_card(last4)
            Display.success("Card accepted.")
            break
        except Exception as e:
            Display.error(str(e))
            if attempt == 2:
                print("\n  Too many failed attempts. Session ended.\n")
                return False

    # PIN entry (up to 3 attempts handled inside Card)
    Display.subheader("ENTER PIN")
    for attempt in range(3):
        try:
            pin = get_pin("  Enter PIN: ")
            atm.validate_pin(pin)
            Display.success(f"Welcome, {atm.active_account.holder_name}!")
            return True
        except PermissionError as e:
            # Card blocked
            Display.error(str(e))
            return False
        except ValueError as e:
            # Wrong PIN, remaining attempts shown
            Display.error(str(e))
        except Exception as e:
            Display.error(str(e))
            return False

    return False


# ──────────────────────────────────────────────────────────────────
# MAIN LOOP
# ──────────────────────────────────────────────────────────────────
def main():
    # Boot the bank + ATM with demo data
    bank, atm = create_demo_bank()

    Display.welcome_screen(atm.atm_id, atm.location)
    Display.demo_credentials()

    while True:
        print("\n" + "═" * 52)
        print("  Press  1  to use ATM")
        print("  Press  0  to exit")
        print("═" * 52)
        choice = get_menu_choice("  Choice: ", ["1", "0"])

        if choice == "0":
            print("\n  Thank you for using PyBank ATM. Goodbye!\n")
            break

        # Card + PIN flow
        authenticated = run_card_flow(atm)

        if authenticated:
            run_session(atm)


if __name__ == "__main__":
    main()
