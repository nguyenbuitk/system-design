# Pub-Sub Demo: Real-time Notifications System

Demo minh họa Publish-Subscribe pattern với RabbitMQ Topic Exchange.

## Mục tiêu

- Hiểu Pub-Sub pattern (1 Publisher → Nhiều Subscribers)
- Thực hành Topic-based routing
- Hiểu Fanout pattern
- So sánh với Message Queue

## Quick Start

### 1. Cài đặt RabbitMQ
```bash
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
pip install -r requirements.txt
```
### 2. Vis dụ
```bash
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
### 3. Chạy demo

**Các Terminal chạy demo**
```bash
python email_subscriber.py

python sms_subscriber.py

python log_subscriber.py

python analytics_subscriber.py

python event_publisher.py
```

**Management UI:** http://localhost:15672 (guest/guest)

## Concepts

### Pub-Sub Pattern
- **Pattern**: 1 Publisher → Topic → Nhiều Subscribers
- **Đặc điểm**: 
  - Mỗi message được gửi đến TẤT CẢ subscribers
  - Push ngay lập tức (không lưu trong queue)
  - Publisher không biết có bao nhiêu subscribers

### Topic-based Routing
- Topics: `user.*`, `order.*`, `payment.*`
- Subscribers filter theo pattern
- Ví dụ: `user.*` → nhận `user.created`, `user.login`, `user.updated`

### Fanout
- Một event → nhiều subscribers nhận
- Mỗi subscriber xử lý độc lập, song song

## Events trong Demo

### User Events (`user.*`)
- `user.created` → Email: Welcome email
- `user.login` → Log: Security log
- `user.updated` → Analytics: Track changes

### Order Events (`order.*`)
- `order.created` → SMS: Order confirmation
- `order.created` → Email: Order details
- `order.created` → Analytics: Sales metrics

### Payment Events (`payment.*`)
- `payment.completed` → Email: Receipt
- `payment.completed` → Analytics: Revenue tracking
- `payment.failed` → SMS: Payment failed alert

## So sánh: Message Queue vs Pub-Sub

| Feature | Message Queue | Pub-Sub |
|---------|--------------|---------|
| Pattern | Point-to-Point | Publish-Subscribe |
| Consumers | 1 message → 1 consumer | 1 message → nhiều subscribers |
| Use case | Task processing | Event broadcasting |
| Storage | Lưu trong queue | Push ngay, không lưu |

## Cấu trúc

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
├── requirements.txt
└── README.md
```

