Enterprise Service Integration
Vấn đề: Công ty lớn có 20+ services cần tích hợp, mỗi service dùng protocol khác nhau.

Giải pháp ESB:

Service A (HTTP/REST) → ESB → Service B (SOAP)
Service C (JMS) → ESB → Service D (FTP)
Service E (Database) → ESB → Service F (Email)
ESB làm gì:

Protocol conversion
Data transformation
Message routing
Error handling
Monitoring
Vấn đề với ESB:

Single point of failure
Khó scale
Phức tạp khi maintain
Expensive