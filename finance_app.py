import sqlite3

# Veri tabanına bağlan(yoksa oluşturur)
conn = sqlite3.connect("finance.dp")

# Cursor oluştur (SQL komutlarını çalıştırmak için)
cursor = conn.cursor()

# Tablo oluştur
cursor.execute("""
CREATE TABLE IF NOT EXISTS islemler (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tur TEXT,
    miktar REAL,
    kategori TEXT,
    tarih TEXT
    )
    """)

conn.commit()

cursor.execute("SELECT * FROM islemler")
veriler = cursor.fetchall()

for veri in veriler:
    print(veri)

conn.close()

print("Veritabanı hazır.")