# Microservices Architecture Demo

Demo showing Microservices architecture - independent services, each with its own database, communicating via HTTP REST API.

## Quick Start

### Option 1: Start all services manually

```bash
# Terminal 1: User Service
cd services/user-service
pip install -r requirements.txt
python app.py

# Terminal 2: Product Service
cd services/product-service
pip install -r requirements.txt
python app.py

# Terminal 3: Order Service
cd services/order-service
pip install -r requirements.txt
python app.py

# Terminal 4: Payment Service
cd services/payment-service
pip install -r requirements.txt
python app.py

# Terminal 5: Gateway
cd services/gateway
pip install -r requirements.txt
python app.py
```

### Option 2: Start all services with script

```bash
./start.sh
```

Visit: http://localhost:5000

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    API Gateway (5000)                     │
│                    (Frontend UI)                         │
└─────────────────────────────────────────────────────────┘
         │              │              │              │
         ▼              ▼              ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│User Service │ │Product      │ │Order        │ │Payment      │
│(5001)       │ │Service(5002)│ │Service(5003)│ │Service(5004)│
├─────────────┤ ├─────────────┤ ├─────────────┤ ├─────────────┤
│users.db     │ │products.db  │ │orders.db    │ │payments.db  │
└─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
                                    │              │
                                    │              │
                                    └──────┬───────┘
                                           │
                              HTTP REST API calls
```

## Key Characteristics

### Microservices vs Monolith vs Modular Monolith

| Aspect | Monolith | Modular Monolith | Microservices |
|--------|----------|------------------|---------------|
| **Code Organization** | One file | Modules | Separate services |
| **Deployment** | Single deploy | Single deploy | Deploy each service |
| **Database** | Shared database | Shared database | Database per service |
| **Scaling** | Scale entire app | Scale entire app | Scale each service |
| **Communication** | In-process | In-process | Network (HTTP) |
| **Fault Isolation** | Single point of failure | Single point of failure | Isolated failures |
| **Tech Stack** | One stack | One stack | Multiple stacks possible |
| **Complexity** | Low (initially) | Medium | High |

## Service Details

### 1. User Service (Port 5001)
- **Database**: `database/users.db`
- **Endpoints**:
  - `POST /api/users` - Create user
  - `GET /api/users` - Get all users
  - `GET /api/users/<id>` - Get user by ID
  - `GET /health` - Health check

### 2. Product Service (Port 5002)
- **Database**: `database/products.db`
- **Endpoints**:
  - `POST /api/products` - Create product
  - `GET /api/products` - Get all products
  - `GET /api/products/<id>` - Get product by ID
  - `GET /health` - Health check

### 3. Order Service (Port 5003)
- **Database**: `database/orders.db`
- **Endpoints**:
  - `POST /api/orders` - Create order (calls Product Service)
  - `GET /api/orders` - Get all orders (calls User & Product Services)
  - `GET /api/orders/<id>` - Get order by ID
  - `PUT /api/orders/<id>/status` - Update order status
  - `GET /health` - Health check
- **Service Communication**: Calls Product Service to get product details

### 4. Payment Service (Port 5004)
- **Database**: `database/payments.db`
- **Endpoints**:
  - `POST /api/payments` - Create payment (calls Order Service)
  - `GET /api/payments` - Get all payments
  - `GET /health` - Health check
- **Service Communication**: Calls Order Service to get order details and update status

## Service Communication

### Example: Creating an Order

```
1. Client → Order Service: POST /api/orders
   {
     "user_id": 1,
     "product_id": 2,
     "quantity": 3
   }

2. Order Service → Product Service: GET /api/products/2
   Response: { "id": 2, "name": "Laptop", "price": 999.99 }

3. Order Service calculates total: 999.99 * 3 = 2999.97

4. Order Service saves to orders.db

5. Order Service → Client: { "id": 1, "total": 2999.97, "status": "PENDING" }
```

### Example: Processing Payment

```
1. Client → Payment Service: POST /api/payments
   { "order_id": 1 }

2. Payment Service → Order Service: GET /api/orders/1
   Response: { "id": 1, "total": 2999.97, "status": "PENDING" }

3. Payment Service saves to payments.db

4. Payment Service → Order Service: PUT /api/orders/1/status
   { "status": "PAID" }

5. Payment Service → Client: { "id": 1, "amount": 2999.97, "status": "COMPLETED" }
```

## Advantages

1. **Independent Deployment**
   - Deploy User Service without affecting Order Service
   - Update Payment Service independently

2. **Independent Scaling**
   - Scale Order Service (high traffic) without scaling User Service
   - Cost-effective resource allocation

3. **Fault Isolation**
   - If Payment Service fails, User/Product/Order Services continue
   - Better resilience

4. **Technology Diversity**
   - User Service: Python/Flask
   - Order Service: Java/Spring Boot (future)
   - Payment Service: Node.js (future)
   - Each service can use best tech for its needs

5. **Team Autonomy**
   - Each team owns a service
   - Teams can work independently
   - Reduces conflicts

6. **Database Isolation**
   - Each service has its own database
   - No shared database bottleneck
   - Can optimize database per service

## Disadvantages

1. **Distributed System Complexity**
   - Network latency
   - Service discovery needed
   - More complex debugging

2. **Data Consistency**
   - No ACID transactions across services
   - Need eventual consistency
   - Saga pattern for distributed transactions

3. **Testing Complexity**
   - Need to test service interactions
   - Integration testing more complex
   - Need to mock services

4. **Higher Cost**
   - Multiple servers/databases
   - More infrastructure to manage

5. **Network Overhead**
   - HTTP calls between services
   - Slower than in-process calls

## Case Study: E-commerce Migration

### Before: Monolith
```
Single Application
├── User Management
├── Product Catalog
├── Order Processing
└── Payment
↓
Shared Database
```

**Problems:**
- Order Service needs 10x scale, but must scale entire app
- Fix Payment bug requires redeploying entire app
- Teams block each other

### After: Microservices
```
User Service (2 servers)     ← Scale independently
Product Service (2 servers) ← Scale independently
Order Service (10 servers)  ← Scale independently (high traffic)
Payment Service (3 servers) ← Scale independently
```

**Benefits:**
- Scale Order Service 10x without scaling others
- Deploy Payment Service fix without affecting others
- Teams work independently

## When to Use Microservices

1. **Large Team** (>20 developers)
   - Multiple teams can work independently

2. **Different Scaling Needs**
   - Some services need more resources than others

3. **Technology Diversity**
   - Need different tech stacks for different services

4. **Business Maturity**
   - Clear service boundaries
   - Well-defined business capabilities

5. **Independent Deployment Needed**
   - Need to deploy services independently

## Migration Path

```
Phase 1: Monolith
    └── All code in one file

Phase 2: Modular Monolith
    └── Code organized into modules
    └── Still one application

Phase 3: Microservices
    └── Extract modules to separate services
    └── Each service can scale independently
```

## Common Pitfalls

1. **Distributed Monolith**
   - Services tightly coupled
   - Share database
   - Must deploy together
   - **Solution**: Ensure loose coupling, separate databases

2. **Service Too Small (Nano-services)**
   - Too many services
   - Overhead > benefits
   - **Solution**: Services should represent business capabilities

3. **Shared Database**
   - Services share database → tight coupling
   - **Solution**: Database per service

4. **Synchronous Communication**
   - All services must be up
   - Cascading failures
   - **Solution**: Use async messaging, circuit breakers

## Next Steps

- Add Service Discovery (Consul, Eureka)
- Add API Gateway (Kong, AWS API Gateway)
- Add Message Queue (RabbitMQ, Kafka) for async communication
- Add Distributed Tracing (Jaeger, Zipkin)
- Add Circuit Breaker pattern
- Add Load Balancer

