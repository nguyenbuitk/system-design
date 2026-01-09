from shared.database import get_db

class ProductService:
    @staticmethod
    def create_product(name, price):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO products (name, price) VALUES (?, ?)',
            (name, price)
        )
        product_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return {'id': product_id, 'name': name, 'price': price}
    
    @staticmethod
    def get_all_products():
        conn = get_db()
        products = conn.execute('SELECT * FROM products').fetchall()
        conn.close()
        return [dict(product) for product in products]
    
    @staticmethod
    def get_product_by_id(product_id):
        conn = get_db()
        product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
        conn.close()
        return dict(product) if product else None
    
