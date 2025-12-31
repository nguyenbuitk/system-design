# Pub-Sub Demo Plan

## VerneMQ vs RabbitMQ cho Pub-Sub

### VerneMQ
- **Chuyên biệt**: Được thiết kế chuyên cho MQTT protocol (IoT)
- **Hiệu suất**: Xử lý hàng chục nghìn messages/giây, độ trễ thấp
- **Clustering**: Dễ dàng, không cần components phụ
- **Use case**: IoT, real-time sensor data, mobile push notifications
- **Ưu điểm**: Tối ưu cho pub-sub thuần túy, lightweight

### RabbitMQ
- **Linh hoạt**: Hỗ trợ nhiều protocols (AMQP, MQTT, STOMP)
- **Patterns**: Hỗ trợ cả Message Queue và Pub-Sub
- **Features**: Exchanges, routing, filtering, durability
- **Use case**: General purpose, microservices, event-driven architecture
- **Ưu điểm**: Đã quen thuộc, dễ học, phù hợp cho demo/learning

### Khuyến nghị cho Demo

**Dùng RabbitMQ vì:**
1. Đã có sẵn trong demo-message-broker
2. Dễ học và demo (đã quen với RabbitMQ)
3. Hỗ trợ Topic Exchange cho pub-sub pattern
4. Phù hợp cho case study event-driven architecture

**Dùng VerneMQ nếu:**
- Demo IoT use case
- Cần hiệu suất cao, độ trễ thấp
- Chỉ focus vào pub-sub thuần túy

---

## Case Studies cho Pub-Sub

### Case Study 1: Real-time Notifications System (Khuyến nghị)

**Vấn đề**: Hệ thống cần gửi notifications đến nhiều services khi có event xảy ra

**Giải pháp Pub-Sub**:
```
User thực hiện action (login, order, payment)
    ↓
Event Publisher → Publish event vào topic
    ↓
Multiple Subscribers nhận event:
    - Email Service → Gửi email notification
    - SMS Service → Gửi SMS
    - Push Notification Service → Gửi push
    - Analytics Service → Log event
    - Audit Service → Ghi audit log
```

**Lợi ích**:
- Publisher không cần biết có bao nhiêu subscribers
- Dễ dàng thêm subscribers mới (không cần sửa publisher)
- Các services xử lý song song, độc lập
- Decoupling hoàn toàn

**Tech**: RabbitMQ Topic Exchange

---

### Case Study 2: IoT Sensor Data Broadcasting

**Vấn đề**: Nhiều sensors gửi data, nhiều services cần nhận data

**Giải pháp Pub-Sub**:
```
Temperature Sensor → Publish "sensor.temperature" topic
    ↓
Multiple Subscribers:
    - Dashboard Service → Hiển thị real-time
    - Alert Service → Kiểm tra threshold
    - Storage Service → Lưu vào database
    - Analytics Service → Tính toán statistics
```

**Lợi nghị**: VerneMQ (MQTT) hoặc RabbitMQ (MQTT plugin)

---

### Case Study 3: E-commerce Event Broadcasting

**Vấn đề**: Khi có event (order.created, payment.completed), nhiều services cần biết

**Giải pháp Pub-Sub**:
```
Order Service → Publish "order.created" event
    ↓
Subscribers:
    - Inventory Service → Update stock
    - Email Service → Send confirmation
    - Analytics Service → Track metrics
    - Recommendation Service → Update suggestions
```

**Tech**: RabbitMQ Topic Exchange với routing keys

---

## Demo Plan: Case Study 1 - Real-time Notifications

### Architecture

```
Event Publisher (Flask API)
    ↓
RabbitMQ Topic Exchange: "events"
    ↓
Multiple Subscribers:
    - Email Subscriber
    - SMS Subscriber  
    - Log Subscriber
    - Analytics Subscriber
```

### Features để demo

1. **Topic-based Routing**:
   - Topics: `user.*`, `order.*`, `payment.*`
   - Subscribers filter theo pattern

2. **Multiple Subscribers**:
   - Một event → nhiều subscribers nhận
   - Mỗi subscriber xử lý độc lập

3. **Dynamic Subscribers**:
   - Thêm/xóa subscribers không ảnh hưởng publisher

4. **Fanout Pattern**:
   - Broadcast đến tất cả subscribers

### Cấu trúc demo

```
demo-pubsub/
├── publisher/
│   └── event_publisher.py      # Publish events
├── subscribers/
│   ├── email_subscriber.py     # Subscribe user.* events
│   ├── sms_subscriber.py       # Subscribe order.* events
│   ├── log_subscriber.py       # Subscribe all events
│   └── analytics_subscriber.py # Subscribe payment.* events
├── shared/
│   ├── config.py
│   └── rabbitmq_utils.py
└── README.md
```

### Use Cases

1. **User Events**:
   - `user.created` → Email: Welcome email
   - `user.login` → Log: Security log
   - `user.updated` → Analytics: Track changes

2. **Order Events**:
   - `order.created` → SMS: Order confirmation
   - `order.created` → Email: Order details
   - `order.created` → Analytics: Sales metrics

3. **Payment Events**:
   - `payment.completed` → Email: Receipt
   - `payment.completed` → Analytics: Revenue tracking
   - `payment.failed` → SMS: Payment failed alert

---

## So sánh: Message Queue vs Pub-Sub

| Feature | Message Queue | Pub-Sub |
|---------|--------------|---------|
| **Pattern** | Point-to-Point | Publish-Subscribe |
| **Consumers** | 1 message → 1 consumer | 1 message → nhiều subscribers |
| **Use case** | Task processing, jobs | Event broadcasting |
| **Storage** | Lưu trong queue | Push ngay, không lưu |
| **Example** | Order processing | Notifications, events |

---

## Next Steps

1. Tạo demo-pubsub folder
2. Implement Event Publisher
3. Implement Multiple Subscribers
4. Demo với RabbitMQ Topic Exchange
5. So sánh với Message Queue demo

