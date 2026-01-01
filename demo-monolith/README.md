# Monolith Demo - Case Study 1: Startup

Demo using monolith architecture for a startup - all features are built in a single application

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
python app.py
```


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


# Disadvantages of current app
1. Scaling
```bash
Problem: order procesing need to scale due to high traffic
-> current solution: scale the entire application
-> result: must scale user, product, payment also (unnecessary)
-> higher cost and wasted resources

If components are seperate, we can increase x10 resource order, and x2 resource payment for example.
```

2. Deployment
```bash
Problem: Fix a small bug in Payment
-> Must redeploy the entire app
-> Risks: 
    maybe affect user, product, order.
    downtime for the entire system
    complex rollback
```

3. Technology lock-in
```bash
Problem: want to use Node.js for Payment (integrate with payment gateway)
-> current: Everything must use Python/Flask
-> Cannot: Using different tech stack for each feature
```

4. Database bottleneck
```bash
Problem: All features use the same database
When: Order service query database at a high rate -> database becomes slow
-> Affects user, product, payment query as well
```

5. Others
```bash
- When we just wanted to test Order process, must testing must test the entire database
- Cosebase grow up -> hard to maintain, and add new features
```

