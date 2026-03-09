import database

database.tablo_olustur()
database.veri_ekle("Gelir", 5000, "Maaş")
database.veri_ekle("Gider", 500, "Kira")

print(database.verileri_getir())
print("Bakiye:", database.bakiye_hesapla())