# N-Tier Architecture Demo

Demo đơn giản minh họa kiến trúc 3-Tier Architecture - được optimize để giống thực tế hơn.

## Cấu trúc

```
demo-n-tier/
├── shared/                  # Shared utilities (tránh code lặp)
│   ├── config.py          # Configuration chung
│   ├── db.py              # Database utilities
│   └── __init__.py
├── tier1-presentation/    # Presentation Layer
│   ├── app.py            # Web server (Flask)
│   └── templates/        # HTML templates
├── tier2-business/       # Business Logic Layer
│   └── business_service.py
├── database/             # Database files (SQLite)
│   └── products.db       # Tự động tạo khi chạy
└── README.md
```

## Cách chạy

### 1. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 2. Chạy từng tier (mở 2 terminal riêng)

**Terminal 1 - Business Layer:**
```bash
cd tier2-business
python3 business_service.py
# Chạy trên port 5001, tự động khởi tạo database
```

**Terminal 2 - Presentation Layer:**
```bash
cd tier1-presentation
python3 app.py
# Chạy trên port 5000
```

### 3. Truy cập ứng dụng
Mở browser: http://localhost:5000

## Flow hoạt động

1. **Presentation Layer** (Port 5000) nhận request từ user
2. **Business Layer** (Port 5001) xử lý business logic và kết nối trực tiếp với database
3. **Database** (SQLite) lưu trữ dữ liệu - không cần service riêng
4. Response được trả về ngược lại qua các layers

## Optimizations đã thực hiện

✅ **Loại bỏ tier3-data service**: Business layer kết nối trực tiếp với database (giống thực tế)

✅ **Shared utilities**: Tạo `shared/` folder để tránh code lặp lại
- `config.py`: Configuration chung
- `db.py`: Database connection và initialization

✅ **Giảm complexity**: Chỉ cần chạy 2 services thay vì 3

## Demo Use Case: Quản lý sản phẩm

- Xem danh sách sản phẩm
- Thêm sản phẩm mới
- Validate business rules (giá > 0, tên không rỗng)

