import sqlite3

DB_NAME = "finance.db"

def baglan():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def tablo_olustur():
    try:
        conn = baglan()
        cursor = conn.cursor()

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
    finally:
        conn.close()

def veri_ekle(tur, miktar, kategori, tarih):
    try:
        conn = baglan()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO islemler (tur, miktar, kategori, tarih) VALUES (?, ?, ?, ?)
        """, (tur, miktar, kategori, tarih))

        conn.commit()
    finally:
        conn.close()

def verileri_getir():
    try:
        conn = baglan()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM islemler")
        veriler = cursor.fetchall()
    finally:
        conn.close()
    return veriler

def veri_sil(record_id):
    try:
        conn = baglan()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM islemler WHERE id = ?", (record_id,))
        conn.commit()
    finally:
        conn.close()

def bakiye_hesapla():
    try:
        conn = baglan()
        cursor = conn.cursor()

        cursor.execute("SELECT tur, miktar FROM islemler")
        veriler = cursor.fetchall()
    finally:
        conn.close()

    bakiye = 0 
    for tur, miktar in veriler:
        if tur == "Gelir":
            bakiye += miktar
        else:
            bakiye -= miktar

    return bakiye

def gelir_gider_toplam():
    try:
        conn = baglan()
        cursor = conn.cursor()

        cursor.execute("SELECT tur, miktar FROM islemler")
        veriler = cursor.fetchall()
    finally:
        conn.close()

    gelir = 0
    gider = 0
    for tur, miktar in veriler:
        if tur == "Gelir":
            gelir += miktar
        else:
            gider += miktar

    return gelir, gider



def kategori_toplamlari():
    try:
        conn = baglan()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT kategori, SUM(miktar)
            FROM islemler
            WHERE tur = 'Gider'
            GROUP BY kategori
        """)

        veriler = cursor.fetchall()
    finally:
        conn.close()
    return veriler


def aylik_veri_getir(yil, ay):
    try:
        conn = baglan()
        cursor = conn.cursor()

        ay_str = f"{yil}-{ay:02d}"   #örn: 2026-03

        cursor.execute("""
            SELECT tur, miktar
            FROM islemler
            WHERE tarih LIKE ?
        """, (f"{ay_str}%",))

        veriler = cursor.fetchall()
    finally:
        conn.close()
    return veriler

def yillik_ozet(yil):
    try:
        conn = baglan()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT strftime('%m', tarih) as ay,
                   tur,
                   SUM(miktar)
            FROM islemler
            WHERE strftime('%Y', tarih) = ?
            GROUP BY ay, tur
            ORDER BY ay
        """, (str(yil),))

        veriler = cursor.fetchall()
    finally:
        conn.close()
    return veriler