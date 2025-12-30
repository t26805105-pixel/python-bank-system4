from interfaces import BankService, InvestmentService, LoanService, DepositService, ConsoleNotificationService, Colors
from factories import AccountFactory
from models import AccountType

class BankFacade:
    def __init__(self):
        self.notifier = ConsoleNotificationService()
        self.bank_service = BankService()
        self.loan_service = LoanService(self.notifier)
        self.investment_service = InvestmentService(self.notifier)
        self.deposit_service = DepositService(self.notifier)
        self.account = None

    def initialize_system(self, user_name: str):
        # Використовуємо Фабрику через BankService або напряму
        self.account = AccountFactory.create_account(user_name, 1000.0, AccountType.SAVINGS)
        self.bank_service._user_account = self.account # Встановлюємо аккаунт в сервіс
        self.notifier.notify(f"Вітаємо, {user_name}! Рахунок відкрито.", Colors.CYAN)

    def get_status(self):
        portfolio_val = self.investment_service.calculate_portfolio_value(self.account)
        return {
            "balance": self.account.balance,
            "debt": self.account.debt,
            "portfolio_val": portfolio_val,
            "type": self.account.account_type.value
        }

    def apply_for_loan(self, amount: float, term: int):
        return self.loan_service.apply_for_loan(self.account, amount, term)

    def buy_stock(self, ticker: str, quantity: int):
        self.investment_service.buy_stock(ticker, quantity, self.account)

    def update_market(self):
        self.investment_service.update_market_prices()
        self.deposit_service.process_interest(self.account)
        self.notifier.notify("Ринок оновлено, відсотки нараховано.", Colors.MAGENTA)

    def show_market(self):
        for s in self.investment_service.get_market():
            print(f"{s.ticker}: {s.price:,.2f}₴ (залишок: {s.quantity})")