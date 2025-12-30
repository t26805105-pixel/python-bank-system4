import random
from abc import ABC, abstractmethod

# Аналог ConsoleColor (проста реалізація через ANSI коди)
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

class INotificationService(ABC):
    @abstractmethod
    def notify(self, message: str, color: str = Colors.RESET):
        pass

class ConsoleNotificationService(INotificationService):
    def notify(self, message: str, color: str = Colors.RESET):
        print(f"{color}{message}{Colors.RESET}")

class BankService:
    def __init__(self):
        self._accounts: List[Account] = []
        self._user_account: Account = None

    def create_account(self, name: str, initial_deposit: float, acc_type: AccountType):
        interest_rate = 0.05 if acc_type == AccountType.SAVINGS else 0.0
        credit_limit = 5000.0 if acc_type == AccountType.CREDIT else 0.0
        
        self._user_account = Account(
            owner=name, 
            balance=initial_deposit, 
            account_type=acc_type,
            interest_rate=interest_rate,
            credit_limit=credit_limit
        )
        self._accounts.append(self._user_account)

    def get_account(self) -> Account:
        return self._user_account

    def transfer(self, to_owner: str, amount: float):
        target = next((a for a in self._accounts if a.owner == to_owner), None)
        if target and self._user_account.balance >= amount:
            self._user_account.balance -= amount
            target.balance += amount
            return True
        return False

class InvestmentService:
    def __init__(self, notifier: INotificationService):
        self._notifier = notifier
        self._market = [
            Stock("AAPL", 180.0, 0.05, 1000),
            Stock("BTC", 60000.0, 0.30, 100)
        ]

    def get_market(self):
        return self._market

    def buy_stock(self, ticker: str, quantity: int, account: Account):
        stock = next((s for s in self._market if s.ticker == ticker), None)
        if not stock:
            self._notifier.notify(f"Акції {ticker} не знайдено", Colors.RED)
            return

        total_cost = stock.price * quantity
        if account.balance >= total_cost and stock.quantity >= quantity:
            account.balance -= total_cost
            stock.quantity -= quantity
            account.portfolio[ticker] = account.portfolio.get(ticker, 0) + quantity
            self._notifier.notify(f"Куплено {quantity} акцій {ticker} за {total_cost:,.2f}₴", Colors.GREEN)
        else:
            self._notifier.notify("Недостатньо коштів або акцій", Colors.RED)

    def sell_stock(self, ticker: str, quantity: int, account: Account):
        if ticker in account.portfolio and account.portfolio[ticker] >= quantity:
            stock = next((s for s in self._market if s.ticker == ticker), None)
            if not stock: return

            total_value = stock.price * quantity
            account.balance += total_value
            account.portfolio[ticker] -= quantity
            stock.quantity += quantity
            
            if account.portfolio[ticker] == 0:
                del account.portfolio[ticker]
            self._notifier.notify(f"Продано {quantity} акцій {ticker} за {total_value:,.2f}₴", Colors.YELLOW)
        else:
            self._notifier.notify("Недостатньо акцій у портфелі", Colors.RED)

    def calculate_portfolio_value(self, account: Account) -> float:
        total = 0.0
        for ticker, qty in account.portfolio.items():
            stock = next((s for s in self._market if s.ticker == ticker), None)
            if stock:
                total += stock.price * qty
        return total

    def update_market_prices(self):
        for stock in self._market:
            change = (random.random() * 2 - 1) * stock.volatility
            stock.price = max(stock.price * (1 + change), 1.0)

class LoanService:
    def __init__(self, notifier: INotificationService):
        self._notifier = notifier
        self._loan_history: List[LoanRequest] = []

    def apply_for_loan(self, account: Account, amount: float, term: int):
        if account.debt > 0:
            self._notifier.notify(f"Вже маєте борг: {account.debt:,.2f}₴", Colors.RED)
            return False

        if amount > account.balance * 12:
            self._notifier.notify("Сума перевищує річний дохід", Colors.RED)
            return False

        score = self._calculate_score(account)
        if random.random() < (score * 0.7 + 0.3):
            rate = 0.12 + (1 - score) * 0.1
            account.balance += amount
            account.debt = amount * (1 + rate)
            self._loan_history.append(LoanRequest("Схвалено", amount, rate, term))
            self._notifier.notify(f"Кредит схвалено! Ставка: {rate:.1%}", Colors.GREEN)
            return True
        
        self._loan_history.append(LoanRequest("Відмовлено"))
        self._notifier.notify("У кредиті відмовлено", Colors.RED)
        return False

    def _calculate_score(self, account: Account) -> float:
        score = 0.5
        if account.balance > 1000: score += 0.2
        if account.account_type == AccountType.SAVINGS: score += 0.1
        if not self._loan_history: score += 0.2
        return min(score, 1.0)

    def process_loan_payment(self, account: Account):
        if account.debt > 0:
            payment = account.debt * 0.03
            if account.balance >= payment:
                account.balance -= payment
                account.debt -= payment
                self._notifier.notify(f"Сплачено: -{payment:,.2f}₴", Colors.YELLOW)
            else:
                account.debt *= 1.1
                self._notifier.notify("Прострочка! Борг +10%", Colors.RED)

    def get_history(self):
        return self._loan_history

class DepositService:
    def __init__(self, notifier: INotificationService):
        self._notifier = notifier

    def process_interest(self, account: Account):
        if account.balance > 0:
            interest = account.balance * account.interest_rate / 365
            account.balance += interest
            if interest > 0:
                self._notifier.notify(f"[Депозит] Нараховано: +{interest:,.2f}₴", Colors.GREEN)