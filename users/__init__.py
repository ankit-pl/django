from enum import Enum


class Currency(Enum):
    INR = "Indian Rupee"
    USD = "United States Dollar"
    CAD = "Canadian Dollar"
    GBP = "Great Britain Pound"


class TransactionType(Enum):
    CIN = "cash_in"
    COUT = "cash_out"
