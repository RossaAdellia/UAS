from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)  # ✅ Perbaikan

DB_PATH = 'jual_makeup.db'  # File database SQLite

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Supaya hasil fetch bisa dict-like
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produk (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price INTEGER NOT NULL
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()
    print("Database dan tabel 'produk' siap digunakan.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produk")
    rows = cursor.fetchall()
    products = [dict(row) for row in rows]
    cursor.close()
    conn.close()
    return jsonify(products)

@app.route('/api/add-product', methods=['POST'])
def add_product():
    data = request.json
    if not data or 'name' not in data or 'price' not in data:
        return jsonify({"error": "Data harus memiliki 'name' dan 'price'"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO produk (name, price) VALUES (?, ?)", (data['name'], data['price']))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "1 produk berhasil ditambahkan", "produk": data})

@app.route('/api/add-products', methods=['POST'])
def add_multiple_products():
    products = request.json
    if not isinstance(products, list):
        return jsonify({"error": "Data harus berupa list produk"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    for item in products:
        if 'name' not in item or 'price' not in item:
            cursor.close()
            conn.close()
            return jsonify({"error": "Setiap produk harus memiliki 'name' dan 'price'"}), 400
        cursor.execute("INSERT INTO produk (name, price) VALUES (?, ?)", (item['name'], item['price']))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": f"{len(products)} produk berhasil ditambahkan."})

@app.route('/api/product/<int:id>', methods=['GET'])
def get_product_by_id(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produk WHERE id = ?", (id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if row:
        product = dict(row)
        return jsonify(product)
    else:
        return jsonify({"error": "Produk tidak ditemukan"}), 404

@app.route('/api/update-product/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.json
    if not data or 'name' not in data or 'price' not in data:
        return jsonify({"error": "Data harus memiliki 'name' dan 'price'"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE produk SET name = ?, price = ? WHERE id = ?", (data['name'], data['price'], id))
    conn.commit()
    affected_rows = conn.total_changes 
    cursor.close()
    conn.close()

    if affected_rows == 0:
        return jsonify({"error": "Produk tidak ditemukan"}), 404

    return jsonify({"message": f"Produk dengan id {id} berhasil diupdate"})

@app.route('/api/delete-product/<int:id>', methods=['DELETE'])
def delete_product(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produk WHERE id = ?", (id,))
    conn.commit()
    affected_rows = cursor.rowcount
    cursor.close()
    conn.close()

    if affected_rows == 0:
        return jsonify({"error": "Produk tidak ditemukan"}), 404

    return jsonify({"message": f"Produk dengan id {id} berhasil dihapus"})

if __name__ == '__main__':  # ✅ Perbaikan
    init_db()
    app.run(debug=True)
