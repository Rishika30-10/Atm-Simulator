"""
utils/display.py
----------------
All terminal display / formatting helpers.
Keeps print logic out of business classes (Single Responsibility).
"""

from datetime import datetime


class Display:

    LINE  = "═" * 52
    DLINE = "─" * 52

    @staticmethod
    def clear():
        print("\n" * 2)

    @staticmethod
    def header(title: str):
        print()
        print(Display.LINE)
        print(f"  {'PyBank ATM':^48}")
        print(f"  {title:^48}")
        print(Display.LINE)

    @staticmethod
    def subheader(text: str):
        print(f"\n  {text}")
        print("  " + Display.DLINE)

    @staticmethod
    def success(msg: str):
        print(f"\n  ✅  {msg}")

    @staticmethod
    def error(msg: str):
        print(f"\n  ❌  {msg}")

    @staticmethod
    def info(msg: str):
        print(f"  ℹ   {msg}")

    @staticmethod
    def divider():
        print("  " + Display.DLINE)

    @staticmethod
    def balance_screen(data: dict):
        Display.header("ACCOUNT BALANCE")
        print(f"\n  Account Holder : {data['holder']}")
        print(f"  Account ID     : {data['account_id']}")
        print(f"  Account Type   : {data['account_type']}")
        print(Display.DLINE)
        print(f"  Available Balance   :  ₹{data['balance']:>12,.2f}")
        print(Display.LINE)

    @staticmethod
    def withdrawal_receipt(data: dict):
        Display.header("WITHDRAWAL RECEIPT")
        ts = datetime.now().strftime("%d-%m-%Y  %H:%M:%S")
        print(f"\n  Date & Time    : {ts}")
        print(Display.DLINE)
        print(f"  Amount Withdrawn    :  ₹{data['amount']:>12,.2f}")
        print(f"  Remaining Balance   :  ₹{data['balance']:>12,.2f}")
        print(Display.LINE)
        print("\n  Please collect your cash and card.")

    @staticmethod
    def deposit_receipt(data: dict):
        Display.header("DEPOSIT RECEIPT")
        ts = datetime.now().strftime("%d-%m-%Y  %H:%M:%S")
        print(f"\n  Date & Time    : {ts}")
        print(Display.DLINE)
        print(f"  Amount Deposited    :  ₹{data['amount']:>12,.2f}")
        print(f"  Updated Balance     :  ₹{data['balance']:>12,.2f}")
        print(Display.LINE)

    @staticmethod
    def transfer_receipt(data: dict):
        Display.header("TRANSFER RECEIPT")
        ts = datetime.now().strftime("%d-%m-%Y  %H:%M:%S")
        print(f"\n  Date & Time    : {ts}")
        print(Display.DLINE)
        print(f"  Transferred To      :  {data['to']}")
        print(f"  Amount              :  ₹{data['amount']:>12,.2f}")
        print(f"  Remaining Balance   :  ₹{data['balance']:>12,.2f}")
        print(Display.LINE)

    @staticmethod
    def mini_statement(transactions: list, holder: str):
        Display.header("MINI STATEMENT")
        print(f"\n  Account Holder : {holder}")
        print()
        if not transactions:
            print("  No transactions found.")
        else:
            print(f"  {'Date & Time':<22} {'Type':<16} {'Amount':>10}  {'Balance':>12}")
            print("  " + Display.DLINE)
            for txn in transactions:
                sign = "+" if txn["type"] in ("DEPOSIT", "TRANSFER IN",
                                               "INTEREST CREDIT") else "-"
                print(f"  {txn['time']:<22} {txn['type']:<16} "
                      f"{sign}₹{txn['amount']:>8,.2f}  "
                      f"₹{txn['balance']:>10,.2f}")
        print(Display.LINE)

    @staticmethod
    def welcome_screen(atm_id: str, location: str):
        print()
        print(Display.LINE)
        print(f"  {'W E L C O M E':^48}")
        print(f"  {'PyBank ATM Simulator':^48}")
        print(Display.DLINE)
        print(f"  ATM ID   : {atm_id}")
        print(f"  Location : {location}")
        print(Display.LINE)

    @staticmethod
    def main_menu():
        print()
        print(Display.LINE)
        print(f"  {'M A I N   M E N U':^48}")
        print(Display.DLINE)
        print("   1.  Check Balance")
        print("   2.  Withdraw Cash")
        print("   3.  Deposit Cash")
        print("   4.  Fund Transfer")
        print("   5.  Mini Statement")
        print("   6.  Change PIN")
        print("   7.  Logout")
        print(Display.LINE)

    @staticmethod
    def demo_credentials():
        print()
        print(Display.DLINE)
        print("  DEMO CREDENTIALS (for testing)")
        print(Display.DLINE)
        print("  Card Last 4  PIN   Name           Type")
        print(Display.DLINE)
        print("  5678         1234  Rishi Kumar     Savings  ₹50,000")
        print("  4321         4321  Priya Sharma    Current  ₹1,00,000")
        print("  2222         9999  Arjun Mehta     Savings  ₹15,000")
        print(Display.DLINE)
