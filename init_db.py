import sqlite3

# Buat (atau buka) database bernama jual_makeup.db
conn = sqlite3.connect('jual_makeup.db')

# Buat tabel produk
conn.execute('''
CREATE TABLE IF NOT EXISTS produk (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price INTEGER NOT NULL
)
''')

conn.commit()
conn.close()

print("Database dan tabel 'produk' berhasil dibuat.")