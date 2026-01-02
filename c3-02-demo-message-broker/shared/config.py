"""
Shared configuration cho tất cả services
"""
import os

# Database configuration
DB_FILE = os.path.join(os.path.dirname(__file__), '..', 'tier3-database', 'products.db')
BUSINESS_SERVICE_URL = os.environ.get('BUSINESS_SERVICE_URL', 'http://localhost:5001')

# Simulate time for each step
VALIDATING_INVENTORY_TIME = 5
CALCULATING_SHIPPING_TIME = 7
SENDING_CONFIRMATION_EMAIL_TIME = 10
UPDATING_ANALYTICS_TIME = 12

# RabbitMQ configuration
RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'localhost')
ORDER_QUEUE = 'order_processing'

# Application settings
DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 'yes')
