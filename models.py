from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List

class AccountType(Enum):
    CHECKING = "Checking"
    SAVINGS = "Savings"
    CREDIT = "Credit"
    BUSINESS = "Business"

@dataclass
class Account:
    owner: str
    balance: float
    debt: float = 0.0
    account_type: AccountType = AccountType.CHECKING
    interest_rate: float = 0.0
    credit_limit: float = 0.0
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
    term_months: int = 0