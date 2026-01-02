from flask import Flask, render_template
from shared.database import init_db
from modules.user.routes import user_bp
from modules.product.routes import product_bp
from modules.order.routes import order_bp
from modules.payment.routes import payment_bp

app = Flask(__name__)

app.register_blueprint(user_bp)
app.register_blueprint(product_bp)
app.register_blueprint(order_bp)
app.register_blueprint(payment_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    init_db()
    print("\nModular Monolith Application")
    print("Running on http://localhost:5000")
    print("\nModule Structure:")
    print("  - modules/user/")
    print("  - modules/product/")
    print("  - modules/order/")
    print("  - modules/payment/")
    print("  - shared/")
    app.run(host='0.0.0.0', port=5000, debug=True)

