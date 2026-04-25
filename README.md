# Hệ Thống Mô Phỏng Máy ATM

Đây là một dự án ứng dụng Console viết bằng Python, mô phỏng lại hoạt động của một hệ thống ATM.

---

## Tổ chức thư mục 

```text
Software_Engineering-Extended_Ex1/
│
├── src/                      # Chứa mã nguồn chính của chương trình
│   ├── main.py               # File chạy chính, điều phối luồng hoạt động
│   ├── hardware.py           # Mô phỏng các thiết bị phần cứng của ATM
│   ├── models.py             # Định nghĩa các cấu trúc dữ liệu (Customer, Account, Card,...)
│   └── transactions.py       # Xử lý logic của từng loại giao dịch
│          
└── README.md 

```             

## Hướng dẫn chạy chương trình

**1. Các bước khởi chạy hệ thống**

* **Bước 1:** Mở Terminal
* **Bước 2:** Bắt đầu chạy chương trình bằng dòng lệnh dưới đây:

```bash
python3 src/main.py