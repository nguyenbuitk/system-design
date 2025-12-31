# Message Broker & Message Queue Demo

## Case Study 1: E-commerce Order Processing

Demo này minh họa cách sử dụng Message Queue để xử lý đơn hàng bất đồng bộ trong hệ thống e-commerce.

### Flow hoạt động

```
User đặt hàng
    ↓
Tier 1: Presentation Layer (Port 5000)
    - Hiển thị form đặt hàng
    - Gửi POST /api/orders
    ↓
Tier 2: Business Service (Port 5001)
    - Validate order data
    - Lưu order vào DB (status: PENDING)
    - Gửi task vào queue "order_processing"
    - Trả response ngay: "Order received, processing..."
    ↓
Order Worker (Background)
    - Lấy order từ queue
    - Validate inventory
    - Tính shipping
    - Gửi confirmation email (simulate)
    - Update order status: PENDING → COMPLETED
```

### So sánh: Có vs Không có Message Queue

**Không dùng Message Queue:**
- User phải đợi 2-3 giây (blocking)
- Email service chậm → toàn bộ API bị chậm
- Không thể scale workers riêng

**Dùng Message Queue:**
- User nhận response ngay (0.7s)
- Email xử lý background, không block API
- Có thể scale workers để xử lý peak load

## Quick Start (5 phút)

### 1. Cài đặt RabbitMQ
```bash
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

### 2. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 3. Chạy demo

**Terminal 1 - Business Service:**
```bash
cd tier2-business
python business_service.py
```

**Terminal 2 - Presentation Layer:**
```bash
cd tier1-presentation
python app.py
```

**Terminal 3 - Order Worker:**
```bash
cd workers
python order_worker.py
```

**Truy cập:**
- Web UI: http://localhost:5000/orders
- Management UI: http://localhost:15672 (guest/guest)

### 4. Test flow

1. Mở http://localhost:5000/orders
2. Tạo sản phẩm trước (nếu chưa có): http://localhost:5000
3. Đặt hàng → Xem order status: PENDING
4. Xem Order Worker xử lý order trong Terminal 3
5. Refresh trang → Order status: COMPLETED

## Concepts

### Message Queue (Point-to-Point)
- **Pattern**: 1 Producer → Queue → 1 Consumer
- **Đặc điểm**: 
  - Mỗi message chỉ được xử lý bởi 1 consumer
  - FIFO ordering
  - Persistent (survive broker restart)

## Thử nghiệm nhanh

**Test Multiple Consumers:**
```bash
# Mở 3 terminals, mỗi terminal chạy:
python consumer.py

# Sau đó chạy producer → tasks sẽ được phân phối round-robin
```

## Commands hữu ích

```bash
# Xem queues
docker exec rabbitmq rabbitmqctl list_queues name messages consumers

# Xóa tất cả messages trong queue
docker exec rabbitmq rabbitmqctl purge_queue task_queue

# Xem logs
docker logs -f rabbitmq
```

## Message Queue vs Pub/Sub

| Feature | Message Queue | Pub/Sub |
|---------|--------------|---------|
| Pattern | Point-to-Point | Publish-Subscribe |
| Consumers | 1 message → 1 consumer | 1 message → nhiều subscribers |
| Use case | Task processing, jobs | Event broadcasting |
| Storage | Lưu trong queue | Push ngay, không lưu |

## Case Studies

### Case Study 1: E-commerce Order Processing

**Vấn đề**: Hệ thống e-commerce cần xử lý hàng nghìn đơn hàng mỗi giờ. Nếu xử lý đồng bộ, hệ thống sẽ bị chậm khi có đợt đơn hàng lớn.

**Giải pháp sử dụng Message Queue**:
```
User đặt hàng
    ↓
Order Service → Gửi message vào queue "order_processing"
    ↓
Order Processing Worker (Consumer)
    - Validate đơn hàng
    - Kiểm tra inventory
    - Tính toán shipping
    - Gửi confirmation email
```

**Nếu không dùng message queue**:
```
User đặt hàng
    ↓
API nhận request → Xử lý ngay:
    - Validate đơn hàng (0.1s)
    - Kiểm tra inventory (0.2s)
    - Tính shipping cost (0.3s)
    - Gửi email confirmation (2s) ← BLOCKING!
    - Update database (0.1s)
    ↓
Trả response cho user sau 2.7 giây
```

**Nếu dùng message queue**:
```
User đặt hàng 
    ↓
API nhận request → Xử lý nhanh:
  - Validate đơn hàng (0.1s)
  - Kiểm tra inventỏy (0.2s)
  - Tính shipping (0.3s)
  - Lưu vào order DB (0.1s)
  - Gửi task vào queue "order_processing" (0.01s)
  ↓
Trả response cho user sau 0.7s 

Background Worker (tách biệt):
  - Lấy task từ queue
  - Gửi email confirmation (2s) ← Không block API
```
---

## Khi nào sử dụng Message Queue?

**Nên dùng khi**:
- Cần xử lý bất đồng bộ (async processing)
- Có tasks tốn thời gian (image processing, email sending)
- Cần decouple services (microservices architecture)
- Cần đảm bảo reliability (không mất messages)
- Cần scale workers để xử lý peak load

**Không nên dùng khi**:
- Cần response ngay lập tức (real-time)
- Tasks đơn giản, nhanh (không cần queue)
- Không cần persistence (có thể mất messages)
- Single consumer, không cần distribution