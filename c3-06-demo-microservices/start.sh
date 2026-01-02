#!/bin/bash

echo "Starting Microservices Demo..."
echo "================================"
echo ""

cd services/user-service && python app.py &
USER_PID=$!
echo "User Service started (PID: $USER_PID)"

sleep 1

cd ../product-service && python app.py &
PRODUCT_PID=$!
echo "Product Service started (PID: $PRODUCT_PID)"

sleep 1

cd ../order-service && python app.py &
ORDER_PID=$!
echo "Order Service started (PID: $ORDER_PID)"

sleep 1

cd ../payment-service && python app.py &
PAYMENT_PID=$!
echo "Payment Service started (PID: $PAYMENT_PID)"

sleep 1

cd ../gateway && python app.py &
GATEWAY_PID=$!
echo "Gateway started (PID: $GATEWAY_PID)"
echo ""
echo "All services are running!"
echo "Visit: http://localhost:5000"
echo ""
echo "Press CTRL+C to stop all services"

trap "kill $USER_PID $PRODUCT_PID $ORDER_PID $PAYMENT_PID $GATEWAY_PID; exit" INT TERM

wait

