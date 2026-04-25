from datetime import datetime
from models import TransactionStatus

class Transaction:
    def __init__(self, transactionId, account, description):
        self.transactionId = transactionId
        self.creationDate = datetime.now()
        self.status = TransactionStatus.PENDING
        self.account = account
        self.description = description

class CheckBalance(Transaction):
    def execute(self):
        self.status = TransactionStatus.SUCCESS
        return self.account.availableBalance

class Withdraw(Transaction):
    def __init__(self, transactionId, account, amount):
        super().__init__(transactionId, account, "Rút tiền mặt")
        self.amount = amount

    def execute(self, dispenser):
        if self.account.availableBalance >= self.amount:
            if dispenser.can_dispense(self.amount):
                self.account.availableBalance -= self.amount
                self.account.totalBalance -= self.amount
                dispenser.dispenseCash(self.amount)
                self.status = TransactionStatus.SUCCESS
                return True
        self.status = TransactionStatus.FAILURE
        return False

class Deposit(Transaction):
    def __init__(self, transactionId, account, amount):
        super().__init__(transactionId, account, "Nạp tiền")
        self.amount = amount

    def execute(self, depositSlot):
        if depositSlot.receiveEnvelope():
            self.account.totalBalance += self.amount
            self.account.availableBalance += self.amount
            self.status = TransactionStatus.SUCCESS
            return True
        self.status = TransactionStatus.FAILURE
        return False

class Transfer(Transaction):
    def __init__(self, transactionId, account, destinationAccount, amount):
        super().__init__(transactionId, account, "Chuyển khoản")
        self.destinationAccount = destinationAccount
        self.amount = amount

    def execute(self):
        if self.account.availableBalance >= self.amount:
            self.account.availableBalance -= self.amount
            self.account.totalBalance -= self.amount
            self.destinationAccount.availableBalance += self.amount
            self.destinationAccount.totalBalance += self.amount
            self.status = TransactionStatus.SUCCESS
            return True
        self.status = TransactionStatus.FAILURE
        return False

class ChangePin(Transaction):
    def __init__(self, transactionId, account, card):
        super().__init__(transactionId, account, "Đổi mã PIN")
        self.card = card

    def execute(self, old_pin, new_pin, confirm_pin):
        if old_pin != self.card.pin:
            self.status = TransactionStatus.FAILURE
            return "Sai mã PIN cũ!"
        if new_pin != confirm_pin:
            self.status = TransactionStatus.FAILURE
            return "Mã PIN mới không khớp!"
        self.card.pin = new_pin
        self.status = TransactionStatus.SUCCESS
        return "Đổi mã PIN thành công!"