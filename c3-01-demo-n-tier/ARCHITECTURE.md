# Kiến trúc N-Tier Demo

## Tổng quan

Demo này minh họa kiến trúc 3-Tier với một ứng dụng quản lý sản phẩm đơn giản.

## Sơ đồ kiến trúc

```
┌─────────────────────────────────────────┐
│  Tier 1: Presentation Layer            │
│  Port: 5000                             │
│  - Flask Web Server                    │
│  - HTML Templates                       │
│  - User Interface                       │
└──────────────┬──────────────────────────┘
               │ HTTP Request
               │ (REST API)
┌──────────────▼──────────────────────────┐
│  Tier 2: Business Logic Layer           │
│  Port: 5001                             │
│  - Business Rules Validation            │
│  - Data Processing                      │
│  - Direct Database Connection           │
└──────────────┬──────────────────────────┘
               │ SQL Queries
               │ (Direct Connection)
┌──────────────▼──────────────────────────┐
│  Tier 3: Database                       │
│  SQLite (File-based)                    │
│  - products.db                          │
│  - Data Persistence                     │
└─────────────────────────────────────────┘
```

**Lưu ý**: Trong thực tế, Tier 3 thường là database server (PostgreSQL, MySQL, etc.) được start lên, không phải là một service riêng. Business layer kết nối trực tiếp với database thông qua database driver.

## Flow xử lý request

### 1. User thêm sản phẩm mới

```
User Input (Browser)
    ↓
Tier 1: Presentation Layer
    - Nhận form data
    - Gửi POST request đến Business Layer
    ↓
Tier 2: Business Logic Layer
    - Validate business rules:
      * Tên không rỗng
      * Tên >= 3 ký tự
      * Giá > 0
    - Nếu valid → Kết nối trực tiếp với database
    - Nếu invalid → Trả về lỗi
    ↓
Tier 3: Database
    - Lưu vào SQLite database (products.db)
    - Trả về product data
    ↓
Response trả về ngược lại qua các layers
    ↓
User thấy kết quả
```

### 2. User xem danh sách sản phẩm

```
User Request (Browser)
    ↓
Tier 1: Presentation Layer
    - Gửi GET request đến Business Layer
    ↓
Tier 2: Business Logic Layer
    - Query trực tiếp từ database
    ↓
Tier 3: Database
    - Execute SQL query
    - Trả về danh sách products
    ↓
Response trả về qua các layers
    ↓
Tier 1 render HTML với danh sách
```

## Business Rules (Tier 2)

1. **Tên sản phẩm:**
   - Không được để trống
   - Phải có ít nhất 3 ký tự

2. **Giá sản phẩm:**
   - Bắt buộc phải có
   - Phải là số dương (> 0)

## Các thành phần

### Tier 1: Presentation (`tier1-presentation/`)
- **app.py**: Flask application, xử lý HTTP requests
- **templates/index.html**: UI template với form và danh sách sản phẩm
- **Trách nhiệm:**
  - Hiển thị UI
  - Nhận input từ user
  - Gọi Business Layer API
  - Render response

### Tier 2: Business Logic (`tier2-business/`)
- **business_service.py**: Business logic service
- **Trách nhiệm:**
  - Validate business rules
  - Xử lý logic nghiệp vụ
  - Kết nối trực tiếp với database (sử dụng shared/db.py)
  - Xử lý errors

### Tier 3: Database (`database/`)
- **products.db**: SQLite database file
- **Trách nhiệm:**
  - Lưu trữ dữ liệu
  - Không cần service riêng - database được truy cập trực tiếp từ Business Layer

### Shared Utilities (`shared/`)
- **config.py**: Configuration chung (DB path, service URLs)
- **db.py**: Database connection và initialization utilities
- **Mục đích**: Tránh code lặp lại giữa các services

## Lợi ích của kiến trúc này

1. **Separation of Concerns**: Mỗi tier có trách nhiệm rõ ràng
2. **Scalability**: Có thể scale từng tier độc lập
3. **Maintainability**: Dễ bảo trì và test
4. **Security**: Có thể thêm firewall giữa các tiers
5. **Flexibility**: Dễ thay đổi công nghệ ở từng tier

## Mở rộng

Có thể mở rộng demo này với:
- Authentication/Authorization
- Caching layer (Redis)
- Message Queue cho async processing
- Load balancer
- Database replication
- Monitoring và logging

