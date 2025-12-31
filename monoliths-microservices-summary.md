# Monoliths and Microservices - Tóm tắt

## Monoliths

### Định nghĩa
Ứng dụng tự chứa, được xây dựng như một đơn vị duy nhất, thực hiện tất cả các bước cần thiết để đáp ứng nhu cầu nghiệp vụ.

### Ưu điểm
- Đơn giản để phát triển và debug
- Giao tiếp nhanh và đáng tin cậy (trong process)
- Dễ monitoring và testing
- Hỗ trợ ACID transactions

### Nhược điểm
- Bảo trì khó khi codebase lớn
- Tightly coupled, khó mở rộng
- Phải commit với một tech stack
- Mỗi update phải redeploy toàn bộ
- Một bug có thể làm down toàn bộ hệ thống
- Khó scale hoặc áp dụng công nghệ mới

---

## Modular Monoliths

**Định nghĩa**: Monolith nhưng code được chia thành các modules độc lập.

**Lợi ích**:
- Giảm dependencies giữa modules
- Có thể thay đổi module mà không ảnh hưởng modules khác
- Giảm complexity khi maintain

**Khi nào dùng**: Bước trung gian trước khi chuyển sang microservices

---

## Microservices

### Định nghĩa
Kiến trúc gồm nhiều services nhỏ, tự chứa, mỗi service implement một business capability trong bounded context.

### Đặc điểm
- **Loosely coupled**: Services độc lập, có thể deploy và scale riêng
- **Small but focused**: Mỗi service làm một việc và làm tốt
- **Built for businesses**: Tổ chức theo business capabilities
- **Resilience**: Fault tolerance cao
- **Highly maintainable**: Dễ maintain và test

### Ưu điểm
- Services loosely coupled
- Deploy độc lập
- Agile cho nhiều teams
- Fault tolerance và data isolation tốt hơn
- Scale từng service độc lập
- Không bị ràng buộc với một tech stack

### Nhược điểm
- Complexity của distributed system
- Testing khó hơn
- Chi phí cao (servers, databases riêng)
- Inter-service communication phức tạp
- Data integrity và consistency
- Network latency

---

## So sánh: Monolith vs Microservices

| Feature | Monolith | Microservices |
|---------|----------|---------------|
| **Deployment** | Deploy toàn bộ | Deploy từng service |
| **Scaling** | Scale toàn bộ | Scale từng service |
| **Tech Stack** | Một stack | Nhiều stacks |
| **Database** | Shared database | Database per service |
| **Team** | Một team lớn | Nhiều teams nhỏ |
| **Complexity** | Đơn giản (ban đầu) | Phức tạp (distributed) |
| **Cost** | Thấp | Cao |
| **Transactions** | ACID dễ dàng | BASE, eventual consistency |

---

## Case Studies

### Case Study 1: Startup - Bắt đầu với Monolith

**Scenario**: Startup mới, team 3-5 người, MVP cần launch nhanh

**Giải pháp: Monolith**
```
Single Application
    ├── User Management
    ├── Product Catalog
    ├── Order Processing
    └── Payment
```

**Lý do**:
- Team nhỏ, không cần microservices
- Cần move fast, launch nhanh
- Chưa biết business requirements rõ ràng
- Cost thấp

**Khi nào chuyển sang Microservices**:
- Team > 20 người
- Codebase quá lớn, khó maintain
- Cần scale một phần cụ thể
- Các teams bị block lẫn nhau

---

### Case Study 2: E-commerce lớn - Chuyển từ Monolith sang Microservices

**Vấn đề**: Monolith đã lớn, khó maintain, teams bị block

**Giải pháp: Microservices**
```
Monolith (cũ)
    ↓
Chia thành:
    ├── User Service
    ├── Product Service
    ├── Order Service
    ├── Payment Service
    ├── Inventory Service
    └── Notification Service
```

**Lợi ích**:
- Teams độc lập, không bị block
- Scale riêng từng service (Order Service cần scale nhiều hơn)
- Deploy độc lập (update Payment Service không ảnh hưởng Order Service)
- Tech stack linh hoạt (User Service dùng Node.js, Order Service dùng Java)

**Thách thức**:
- Distributed transactions phức tạp
- Inter-service communication
- Monitoring nhiều services
- Cost cao hơn

---

### Case Study 3: Distributed Monolith (Anti-pattern)

**Vấn đề**: Công ty "chuyển sang microservices" nhưng thực tế là distributed monolith

**Dấu hiệu Distributed Monolith**:
```
Services:
    ├── User Service
    ├── Order Service
    └── Payment Service

Nhưng:
- Services phải deploy cùng lúc
- Share cùng database
- Tightly coupled
- Không scale độc lập được
```

**Tại sao xảy ra**:
- Chia services theo technical layers (thay vì business domain)
- Share database
- Services phụ thuộc lẫn nhau
- Không có proper API boundaries

**Giải pháp**:
- Chia lại theo business domain
- Database per service
- Loosely coupled
- Proper API design

---

### Case Study 4: Khi KHÔNG nên dùng Microservices

**Scenario**: SaaS nhỏ, team 5 người, 10,000 users

**Tại sao KHÔNG dùng Microservices**:
- Team quá nhỏ → overhead quá lớn
- Chưa có vấn đề scale
- Cost cao (nhiều servers, databases)
- Complexity không cần thiết

**Nên dùng**:
- Monolith hoặc Modular Monolith
- Khi cần → chuyển sang microservices

---

## Best Practices

### Khi NÊN dùng Monolith

1. **Startup mới**
   - Team nhỏ (< 10 người)
   - Chưa rõ requirements
   - Cần launch nhanh

2. **Application nhỏ**
   - Simple business logic
   - Không cần scale nhiều
   - Cost là vấn đề

3. **MVP/Prototype**
   - Validate ý tưởng
   - Chưa cần production-ready

### Khi NÊN dùng Microservices

1. **Team lớn**
   - > 20 developers
   - Nhiều teams
   - Teams bị block lẫn nhau

2. **Scale khác nhau**
   - Một số features cần scale nhiều
   - Một số features ít traffic

3. **Business mature**
   - Requirements rõ ràng
   - Có budget và resources
   - Cần độc lập giữa các teams

4. **Tech diversity**
   - Cần dùng nhiều tech stacks
   - Services có requirements khác nhau

### Migration Strategy

**Khuyến nghị**: Start with Monolith → Modular Monolith → Microservices

```
Phase 1: Monolith
    - Launch nhanh
    - Validate business

Phase 2: Modular Monolith
    - Chia code thành modules
    - Giảm coupling

Phase 3: Microservices (khi cần)
    - Extract services khi cần scale
    - Extract services khi teams bị block
```

---

## Common Pitfalls

### 1. Chia services quá sớm
- Chưa hiểu rõ business domain
- Services quá nhỏ (nano-services)
- Overhead > benefits

### 2. Distributed Monolith
- Services tightly coupled
- Share database
- Phải deploy cùng lúc

### 3. Shared Database
- Services share database → tight coupling
- Khó scale riêng
- Data consistency issues

### 4. Thiếu Monitoring
- Nhiều services → khó debug
- Cần distributed tracing
- Cần centralized logging

---

## Tóm tắt

**Monolith:**
- Phù hợp: Startup, team nhỏ, application nhỏ
- Ưu điểm: Đơn giản, cost thấp, dễ develop
- Nhược điểm: Khó scale, khó maintain khi lớn

**Microservices:**
- Phù hợp: Team lớn, scale khác nhau, business mature
- Ưu điểm: Scale độc lập, teams độc lập, tech diversity
- Nhược điểm: Complexity, cost cao, distributed challenges

**Khuyến nghị**: Start with Monolith, chuyển sang Microservices khi thực sự cần.

