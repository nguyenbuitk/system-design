# Monolith Demo - Case Study 1: Startup

Demo using monolith architecture for a startup - all features are built in a single application

## Mục tiêu

- Understand monolith architecture
- Recognize the simplicity of monolithc architecture
- Compare with microservices

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run demo
```bash
python app.py
```

### 3. Access
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

**Features:**
- All features are built into a single codebase
- Single database for the entire application
- Deploy once for entire app
- Components communicate in-process (fast)

## Features

1. **User Management**
2. **Product Catalog**
3. **Order Processing**
4. **Payment**

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
