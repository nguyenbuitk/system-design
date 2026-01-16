import os

# Service URLs - can be overridden by environment variables
# In Docker: use service names (e.g., http://user-service:5001)
# Local: use localhost (e.g., http://localhost:5001)
SERVICES = {
    'user': os.environ.get('USER_SERVICE_URL', 'http://localhost:5001'),
    'product': os.environ.get('PRODUCT_SERVICE_URL', 'http://localhost:5002'),
    'order': os.environ.get('ORDER_SERVICE_URL', 'http://localhost:5003'),
    'payment': os.environ.get('PAYMENT_SERVICE_URL', 'http://localhost:5004')
}

