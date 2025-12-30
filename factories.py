from models import Account, AccountType

class AccountFactory:
    @staticmethod
    def create_account(owner: str, initial_deposit: float, acc_type: AccountType) -> Account:
        """
        Централізоване створення акаунтів з налаштуванням початкових параметрів.
        """
        # Створюємо базовий словник параметрів
        params = {
            "owner": owner,
            "balance": initial_deposit,
            "account_type": acc_type,
            "interest_rate": 0.0,
            "credit_limit": 0.0
        }

        # Налаштовуємо специфічні поля залежно від типу
        if acc_type == AccountType.SAVINGS:
            params["interest_rate"] = 0.05  # 5% річних
        
        elif acc_type == AccountType.CREDIT:
            params["credit_limit"] = 5000.0  # Стандартний ліміт
            
        elif acc_type == AccountType.BUSINESS:
            params["interest_rate"] = 0.02
            params["credit_limit"] = 50000.0

        return Account(**params)