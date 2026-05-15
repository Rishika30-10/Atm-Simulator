# 🏧 ATM Simulator

A terminal-based ATM simulation built with **Pure Python** using core OOP principles — no external libraries needed.

## OOP Concepts Used

| Concept | Where |
|---|---|
| **Encapsulation** | Private PIN & card number in `Card`, private cash reserve in `ATM` |
| **Inheritance** | `SavingsAccount` and `CurrentAccount` extend abstract `Account` |
| **Polymorphism** | `get_withdrawal_limit()` and `get_minimum_balance()` behave differently per account type |
| **Abstraction** | `Account` is an Abstract Base Class (ABC) — cannot be instantiated directly |
| **Composition** | `ATM` contains `Card` and `Account` objects |

## Features

- PIN validation with card blocking after 3 wrong attempts
- Balance enquiry
- Cash withdrawal (multiples of ₹100, daily limits enforced)
- Cash deposit
- Fund transfer between accounts
- Mini statement (last 5 transactions)
- PIN change
- Two account types — Savings (₹25K limit) and Current (₹1L limit + overdraft)

## Project Structure

```
atm-simulator/
├── main.py               # Entry point — CLI runner
├── models/
│   ├── card.py           # Card class — PIN validation, blocking
│   └── account.py        # Account (ABC), SavingsAccount, CurrentAccount
├── services/
│   ├── atm.py            # ATM class — session & operations
│   └── bank.py           # Bank class — seeds demo data
└── utils/
    ├── display.py        # All terminal UI / formatting
    └── validators.py     # Input validation helpers
```

## Run

```bash
python main.py
```
No installs needed — standard library only.

## Demo Credentials

| Card Last 4 | PIN  | Name          | Type    | Balance    |
|-------------|------|---------------|---------|------------|
| 5678        | 1234 | Rishi Kumar   | Savings | ₹50,000    |
| 4321        | 4321 | Priya Sharma  | Current | ₹1,00,000  |
| 2222        | 9999 | Arjun Mehta   | Savings | ₹15,000    |

---

> Made by [Rishika](https://github.com/Rishika30-10)
