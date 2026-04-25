import random
from models import *
from transactions import *
from hardware import *

class ATM:
    def __init__(self, location, bank_name):
        self.location = location
        self.bank_name = bank_name
        self.screen = Screen()
        self.keypad = Keypad()
        self.cardReader = CardReader()
        self.dispenser = CashDispenser()
        self.depositSlot = DepositSlot()
        self.printer = Printer()
        self.db = {} 

    def start(self):
        while True:
            self.screen.showMessage(f"--- {self.bank_name} - {self.location} ---")
            card_num = self.cardReader.readCard()
            
            if card_num in self.db:
                pin = self.keypad.getInput("Mã PIN")
                if pin == self.db[card_num]["card"].pin:
                    session = self.db[card_num]
                    self.process_menu(session)
                else:
                    self.screen.showMessage("Sai mã PIN.")
            else:
                self.screen.showMessage("Thẻ không hợp lệ.")

    def process_menu(self, session):
        customer = session["customer"]
        card = session["card"]
        acc = customer.account
        self.screen.showMessage(f"Xin chào {customer.name}")

        while True:
            self.screen.showMessage("\n1. Xem số dư | 2. Rút tiền | 3. Nạp tiền | 4. Chuyển khoản | 5. Đổi mã PIN | 6. Thoát")
            choice = self.keypad.getInput("Chọn chức năng")
            tx_id = f"TX{random.randint(1000, 9999)}"

            if choice == "1":
                tx = CheckBalance(tx_id, acc, "Xem số dư")
                bal = tx.execute()
                self.screen.showMessage(f"Số dư tài khoản: {self.printer.format_money(bal)} VNĐ")

            elif choice == "2":
                amt = float(self.keypad.getInput("Số tiền rút"))
                tx = Withdraw(tx_id, acc, amt)
                if tx.execute(self.dispenser):
                    self.screen.showMessage("Rút tiền thành công.")
                    self.printer.printReceipt(tx.status.value, amt, acc.availableBalance, tx.description)
                else:
                    self.screen.showMessage("Số dư không đủ.")

            elif choice == "3":
                amt = float(self.keypad.getInput("Số tiền nạp"))
                tx = Deposit(tx_id, acc, amt)
                if tx.execute(self.depositSlot):
                    self.screen.showMessage("Nạp tiền thành công.")
                    self.printer.printReceipt(tx.status.value, amt, acc.availableBalance, tx.description)

            elif choice == "4":
                dest_card = self.keypad.getInput("Số thẻ người nhận")
                if dest_card in self.db:
                    dest_acc = self.db[dest_card]["customer"].account
                    amt = float(self.keypad.getInput("Số tiền chuyển"))
                    tx = Transfer(tx_id, acc, dest_acc, amt)
                    if tx.execute():
                        self.screen.showMessage("Chuyển khoản thành công.")
                        self.printer.printReceipt(tx.status.value, amt, acc.availableBalance, tx.description)
                    else:
                        self.screen.showMessage("Số dư không đủ.")
                else:
                    self.screen.showMessage("Người nhận không tồn tại.")

            elif choice == "5":
                old = self.keypad.getInput("PIN cũ")
                new = self.keypad.getInput("PIN mới")
                conf = self.keypad.getInput("Xác nhận")
                tx = ChangePin(tx_id, acc, card)
                res = tx.execute(old, new, conf)
                self.screen.showMessage(res)

            elif choice == "6":
                self.screen.showMessage("Vui lòng nhận lại thẻ.")
                break

if __name__ == "__main__":
    vinh_atm = ATM("HCMUT", "BK BANK")
    
    # Khởi tạo dữ liệu
    v = Customer("Lê Công Vinh", "Quận 10", "vinh.le@hcmut.edu.vn", "090")
    v.setAccount(CheckingAccount("V001", 5000000, 5000000, "9704-01"))
    c1 = Card("9704-01", "Lê Công Vinh", "12/28", "123456")
    vinh_atm.db["9704-01"] = {"customer": v, "card": c1}

    n = Customer("Nguyễn Văn A", "Thủ Đức", "nva@hcmut.edu.vn", "091")
    n.setAccount(CheckingAccount("N002", 1000000, 1000000, "9704-02"))
    c2 = Card("9704-02", "Nguyễn Văn A", "12/28", "654321")
    vinh_atm.db["9704-02"] = {"customer": n, "card": c2}

    vinh_atm.start()