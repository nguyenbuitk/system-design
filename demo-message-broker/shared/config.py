"""
Shared configuration cho tất cả services
"""
import os

# Database configuration
DB_FILE = os.path.join(os.path.dirname(__file__), '..', 'tier3-database', 'products.db')
#  ('Validating inventory', 0.5),
#         ('Calculating shipping', 0.3),
#         ('Sending confirmation email', 1.0),
#         ('Updating analytics', 0.2)
# Service URLs
BUSINESS_SERVICE_URL = 'http://localhost:5001'

# Simulate time for each step
VALIDATING_INVENTORY_TIME = 5
CALCULATING_SHIPPING_TIME = 7
SENDING_CONFIRMATION_EMAIL_TIME = 10
UPDATING_ANALYTICS_TIME = 12

# RabbitMQ configuration
RABBITMQ_HOST = 'localhost'
ORDER_QUEUE = 'order_processing'

# Application settings
DEBUG = True
