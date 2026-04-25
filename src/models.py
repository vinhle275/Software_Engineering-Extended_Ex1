from enum import Enum

class TransactionStatus(Enum):
    SUCCESS = "Thành công"
    FAILURE = "Thất bại"
    PENDING = "Đang xử lý"

class Account:
    def __init__(self, accountNumber, totalBalance, availableBalance):
        self.accountNumber = accountNumber
        self.totalBalance = totalBalance
        self.availableBalance = availableBalance

class CheckingAccount(Account):
    def __init__(self, accountNumber, totalBalance, availableBalance, debitCardNumber):
        super().__init__(accountNumber, totalBalance, availableBalance)
        self.debitCardNumber = debitCardNumber

class Card:
    def __init__(self, cardNumber, customerName, expiryDate, pin):
        self.cardNumber = cardNumber
        self.customerName = customerName
        self.expiryDate = expiryDate
        self.pin = pin

class Customer:
    def __init__(self, name, address, email, phone):
        self.name = name
        self.address = address
        self.email = email
        self.phone = phone
        self.account = None

    def setAccount(self, account):
        self.account = account