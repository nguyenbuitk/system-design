# RabbitMQ configuration
RABBITMQ_HOST = 'localhost'
EXCHANGE_NAME = 'events'
EXCHANGE_TYPE = 'topic'

# Event types
EVENT_USER_CREATED = 'user.created'
EVENT_USER_LOGIN = 'user.login'
EVENT_USER_UPDATED = 'user.updated'
EVENT_ORDER_CREATED = 'order.created'
EVENT_PAYMENT_COMPLETED = 'payment.completed'
EVENT_PAYMENT_FAILED = 'payment.failed'