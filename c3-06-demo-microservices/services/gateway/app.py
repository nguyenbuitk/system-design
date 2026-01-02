from flask import Flask, render_template
import requests
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from shared.config import SERVICES

app = Flask(__name__)
PORT = 5000

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    services_status = {}
    for service_name, service_url in SERVICES.items():
        try:
            response = requests.get(f"{service_url}/health", timeout=1)
            services_status[service_name] = 'healthy' if response.status_code == 200 else 'unhealthy'
        except:
            services_status[service_name] = 'down'
    return {'services': services_status}

if __name__ == '__main__':
    print(f"\nAPI Gateway running on http://localhost:{PORT}")
    print("Make sure all services are running:")
    print("  - User Service: http://localhost:5001")
    print("  - Product Service: http://localhost:5002")
    print("  - Order Service: http://localhost:5003")
    print("  - Payment Service: http://localhost:5004")
    app.run(host='0.0.0.0', port=PORT, debug=True)

