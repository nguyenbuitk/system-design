# Modular Monolith Demo

Demo showing Modular Monolith architecture - code organized into independent modules, but still runs as one application.

## Quick Start

```bash
pip install -r requirements.txt
python app.py
```

Visit: http://localhost:5000

## Architecture

```
Modular Monolith Application (Single Process)
    ├── modules/
    │   ├── user/ (service.py, routes.py)
    │   ├── product/ (service.py, routes.py)
    │   ├── order/ (service.py, routes.py)
    │   └── payment/ (service.py, routes.py)
    ├── shared/ (database.py)
    └── app.py (registers all modules)
    ↓
Shared Database (SQLite)
```

## Key Characteristics


### Benefits of Modular Monolith
1. **Independent Modules**
   - Each module (user, product, order, payment) has its own service layer and routes
   - Can be modified without affecting other modules

2. **Reduced Coupling**
   - Modules communicate through well-defined interfaces
   - Easier to understand dependencies
   - Easier to test individual modules

3. **Easier Maintenance**
   - Code is organized by feature
   - Easier to find and fix bugs
   - Easier to add new features

4. **Migration Path**
   - Can easily extract a module to microservice later
   - Good intermediate step before microservices

## Example: Changing a Module

### Scenario: Update User Module

**In Monolith:**
- All code in one file
- Risk of affecting other features
- Hard to test in isolation

**In Modular Monolith:**
- Only modify `modules/user/service.py` or `modules/user/routes.py`
- Other modules (product, order, payment) are unaffected
- Can test user module independently


## Comparison with Microservices

| Aspect | Modular Monolith | Microservices |
|--------|------------------|---------------|
| **Deployment** | Single deploy | Deploy each service |
| **Scaling** | Scale entire app | Scale individual services |
| **Database** | Shared database | Separate databases |
| **Communication** | In-process (fast) | Network (slower) |
| **Complexity** | Lower | Higher |
| **Cost** | Lower | Higher |

## Disadvantages

1. **Still Single Deploy**
   - Must redeploy entire app for any change
   - Cannot deploy modules independently

2. **Still Shared Database** Database bottleneck still exists

3. **Still Single Process** Cannot scale modules independently
## Next Steps

When you need:
- Independent deployment per module → Move to Microservices
- Independent scaling per module → Move to Microservices
- Separate databases per module → Move to Microservices

