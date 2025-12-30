import random
from enum import Enum
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Dict, List

# --- МОДЕЛІ ---
class AccountType(Enum):
    CHECKING = "Поточний"
    SAVINGS = "Ощадний"
    CREDIT = "Кредитний"

@dataclass
class Account:
    owner: str
    balance: float
    debt: float = 0.0
    account_type: AccountType = AccountType.CHECKING
    interest_rate: float = 0.0
    portfolio: Dict[str, int] = field(default_factory=dict)

@dataclass
class Stock:
    ticker: str
    price: float
    volatility: float
    quantity: int

@dataclass
class LoanRequest:
    status: str
    amount: float = 0.0
    interest_rate: float = 0.0

# --- СЕРВІСИ ---
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

class BankService:
    def __init__(self):
        self.account = Account("Клієнт", 1000.0, account_type=AccountType.SAVINGS, interest_rate=0.05)
    
    def transfer(self, to: str, amount: float):
        if self.account.balance >= amount:
            self.account.balance -= amount
            return True
        return False

class InvestmentService:
    def __init__(self):
        self.market = [
            Stock("AAPL", 180.0, 0.05, 1000),
            Stock("BTC", 60000.0, 0.30, 100)
        ]

    def update_prices(self):
        for s in self.market:
            change = (random.random() * 2 - 1) * s.volatility
            s.price = max(s.price * (1 + change), 1.0)

    def buy(self, ticker, qty, acc):
        stock = next((s for s in self.market if s.ticker == ticker), None)
        if stock and acc.balance >= stock.price * qty:
            acc.balance -= stock.price * qty
            acc.portfolio[ticker] = acc.portfolio.get(ticker, 0) + qty
            return True
        return False

# --- ГОЛОВНА ПРОГРАМА ---
def main():
    bank = BankService()
    inv = InvestmentService()
    acc = bank.account

    print(f"{Colors.CYAN}=== БАНКІВСЬКА СИСТЕМА ПЕРЕЗАВАНТАЖЕНА (PYTHON) ==={Colors.RESET}")

    while True:
        print(f"\nБаланс: {acc.balance:,.2f} | Борг: {acc.debt:,.2f}")
        print("1. Кредит | 2. Купити акції | 3. Ринок | 7. Оновити ціни | 0. Вихід")
        
        choice = input("Вибір: ")
        
        if choice == "0": break
        
        if choice == "1":
            amt = float(input("Сума кредиту: "))
            acc.balance += amt
            acc.debt += amt * 1.2
            print(f"{Colors.GREEN}Гроші зараховано!{Colors.RESET}")
            
        elif choice == "2":
            t = input("Тікер: ").upper()
            q = int(input("Кількість: "))
            if inv.buy(t, q, acc):
                print(f"{Colors.GREEN}Успішно куплено!{Colors.RESET}")
            else:
                print(f"{Colors.RED}Помилка (мало грошей або невірний тікер){Colors.RESET}")
                
        elif choice == "3":
            for s in inv.market:
                print(f"{s.ticker}: {s.price:,.2f}")
                
        elif choice == "7":
            inv.update_prices()
            print(f"{Colors.MAGENTA}Ціни змінилися!{Colors.RESET}")

if __name__ == "__main__":
    main()