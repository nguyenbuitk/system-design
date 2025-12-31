# Monolith Demo - Case Study 1: Startup

Demo minh họa Monolith architecture cho startup - tất cả features trong một ứng dụng duy nhất.

## Mục tiêu

- Hiểu Monolith architecture
- Thấy được sự đơn giản của monolith
- So sánh với Microservices (sẽ demo sau)

## Quick Start

### 1. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 2. Chạy demo
```bash
python app.py
```

### 3. Truy cập
- Web UI: http://localhost:5000
- API: http://localhost:5000/api/products

## Architecture

```
Monolith Application (Single Process)
    ├── User Management
    ├── Product Catalog
    ├── Order Processing
    └── Payment
    ↓
Shared Database (SQLite)
```

**Đặc điểm:**
- Tất cả features trong một codebase
- Một database cho tất cả
- Deploy một lần cho toàn bộ app
- Giao tiếp trong process (nhanh)

## Features

1. **User Management**: Đăng ký, đăng nhập
2. **Product Catalog**: Xem, thêm sản phẩm
3. **Order Processing**: Đặt hàng
4. **Payment**: Thanh toán

## So sánh với Microservices

| Feature | Monolith (này) | Microservices |
|---------|---------------|---------------|
| **Deployment** | 1 app | Nhiều services |
| **Database** | 1 database | Database per service |
| **Communication** | In-process (nhanh) | Network (chậm hơn) |
| **Complexity** | Đơn giản | Phức tạp |
| **Cost** | Thấp | Cao |

## Cấu trúc

```
demo-monolith/
├── app.py              # Main application (tất cả features)
├── database/
│   └── app.db         # SQLite database
├── requirements.txt
└── README.md
```

