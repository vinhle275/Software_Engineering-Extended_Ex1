class Screen:
    def showMessage(self, message):
        print(f"[Màn hình]: {message}")

class Keypad:
    def getInput(self, prompt):
        return input(f"[Bàn phím - {prompt}]: ")

class CardReader:
    def readCard(self):
        return input("[Khe đọc thẻ]: Nhập số thẻ: ")

class CashDispenser:
    def __init__(self, cashAvailable=10000000):
        self.cashAvailable = cashAvailable
    def can_dispense(self, amount): return amount <= self.cashAvailable
    def dispenseCash(self, amount): self.cashAvailable -= amount

class DepositSlot:
    def receiveEnvelope(self):
        print("[Khe nhận tiền]: Đang nhận phong bì...")
        return True

class Printer:
    @staticmethod
    def format_money(amount):
        return "{:,}".format(int(amount)).replace(",", " ")

    def printReceipt(self, status, amount, balance, description):
        print("\n" + "*"*35)
        print("         BIÊN LAI GIAO DỊCH")
        print(f" Loại giao dịch: {description}")
        if amount > 0:
            print(f" Số tiền: {self.format_money(amount)} VNĐ")
        print(f" Số dư cuối: {self.format_money(balance)} VNĐ")
        print(f" Trạng thái: {status}")
        print("*"*35 + "\n")