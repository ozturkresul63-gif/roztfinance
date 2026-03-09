from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
from database import aylik_veri_getir
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from tkinter import messagebox
from tkinter import filedialog
import database

database.tablo_olustur()

class FinanceApp:
    def __init__(self, root):

        self.root = root
        self.root.title("Rozt Finance")
        self.root.geometry("900x650")

        style = ttk.Style()
        style.theme_use("default")

        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        self.ozet_frame = ttk.Frame(self.main_frame)
        self.ozet_frame.pack(fill="x", pady=5)

        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill="both", expand=True)

        self.left_frame = ttk.Frame(self.content_frame)
        self.left_frame.pack(side="left", fill="y", padx=10, pady=5)

        self.right_frame = ttk.Frame(self.content_frame)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=5)

        self.tree_frame = ttk.Frame(self.right_frame)
        self.tree_frame.pack(fill="x")

        self.grafik_frame = ttk.Frame(self.right_frame)
        self.grafik_frame.pack(fill="both", expand=True)

        self.gelir_label = ttk.Label(self.ozet_frame, text="Gelir: 0",
                                    font=("Arial", 12, "bold"))
        self.gelir_label.grid(row=0, column=0, padx=20)

        self.gider_label = ttk.Label(self.ozet_frame, text="Gider: 0",
                                    font=("Arial", 12, "bold"))
        self.gider_label.grid(row=0, column=1, padx=20)

        self.net_label = ttk.Label(self.ozet_frame, text="Net: 0",
                                font=("Arial", 12, "bold"))
        self.net_label.grid(row=0, column=2, padx=20)

        self.tur_var = tk.StringVar(value="Gelir")

        ttk.Label(self.left_frame, text="Tür").pack(pady=2)

        self.tur_combo = ttk.Combobox(
            self.left_frame,
            textvariable=self.tur_var,
            values=("Gelir", "Gider"),
            state="readonly"
        )
        self.tur_combo.pack()

        ttk.Label(self.left_frame, text="Miktar").pack(pady=2)
        self.miktar_entry = ttk.Entry(self.left_frame)
        self.miktar_entry.pack()

        ttk.Label(self.left_frame, text="Kategori").pack(pady=2)
        self.kategori_entry = ttk.Entry(self.left_frame)
        self.kategori_entry.pack()

        ttk.Button(
            self.left_frame,
            text="Ekle",
            command=self.ekle,
            width=20
        ).pack(pady=5)

        ttk.Label(self.left_frame, text="Yıllık Trend (Yıl)").pack()

        self.yillik_entry = ttk.Entry(self.left_frame)
        self.yillik_entry.pack()

        ttk.Button(
            self.left_frame,
            text="Yıllık Trend Grafiği",
            command=self.yillik_trend_grafik,
            width=20
        ).pack(pady=5)

        ttk.Button(
            self.left_frame,
            text="Seçili Kaydı Sil",
            command=self.sil,
            width=20
        ).pack(pady=5)

        columns = ("ID", "Tarih", "Tür", "Kategori", "Miktar")

        self.liste = ttk.Treeview(
            self.tree_frame,
            columns=columns,
            show="headings",
            height=8
        )

        for col in columns:
            self.liste.heading(col, text=col)

        self.liste.column("ID", width=40, anchor="center")
        self.liste.column("Tarih", width=120)
        self.liste.column("Tür", width=70, anchor="center")
        self.liste.column("Kategori", width=120)
        self.liste.column("Miktar", width=90, anchor="center")

        scrollbar = ttk.Scrollbar(
            self.tree_frame,
            orient="vertical",
            command=self.liste.yview
        )

        self.liste.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.liste.pack(fill="both", expand=True)

        self.bakiye_label = ttk.Label(
            self.left_frame,
            text="Bakiye: 0",
            font=("Arial", 14)
        )
        self.bakiye_label.pack(pady=10)

        self.bottom_frame = ttk.Frame(self.main_frame)
        self.bottom_frame.pack(fill="x", pady=5)

        ttk.Button(
            self.bottom_frame,
            text="Grafik Göster",
            command=self.grafik_goster,
            width=20
        ).pack(side="left", padx=5)

        ttk.Button(
            self.bottom_frame,
            text="Kategori Dağılımı",
            command=lambda: self.dashboard_kategori(self.grafik_frame),
            width=20
        ).pack(side="left", padx=5)

        ttk.Button(
            self.bottom_frame,
            text="Excel'e Aktar",
            command=self.excel_export,
            width=20
        ).pack(side="left", padx=5)

        ttk.Button(
            self.bottom_frame,
            text="Dashboard",
            command=self.dashboard_goster,
            width=20
        ).pack(side="left", padx=5)

        self.liste_guncelle()
        self.ozet_guncelle()
    
    def dashboard_goster(self):

        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

        for widget in self.grafik_frame.winfo_children():
            widget.destroy()

        frame = ttk.Frame(self.grafik_frame)
        frame.pack(fill="both", expand=True)

        sol = ttk.Frame(frame)
        sol.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        sag = ttk.Frame(frame)
        sag.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        kategoriler = ["Kira","Yemek","Ulaşım","Diğer"]
        miktarlar = [5000,2000,1000,500]

        aylar = ["Jan","Feb","Mar","Apr"]
        aylik = [3000,3500,2800,4000]

        fig1 = plt.Figure(figsize=(4,3))
        ax1 = fig1.add_subplot(111)
        ax1.pie(miktarlar, labels=kategoriler, autopct="%1.1f%%")
        ax1.set_title("Kategori Dağılımı")

        canvas1 = FigureCanvasTkAgg(fig1, sol)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill="both", expand=True)

        fig2 = plt.Figure(figsize=(4,3))
        ax2 = fig2.add_subplot(111)
        ax2.bar(aylar, aylik)
        ax2.set_title("Aylık Trend")

        canvas2 = FigureCanvasTkAgg(fig2, sag)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill="both", expand=True)

    def dashboard_gelir_gider(self, frame):

        gelir, gider = database.gelir_gider_toplam()

        fig = plt.Figure(figsize=(3,2))
        ax = fig.add_subplot(111)

        ax.bar(["Gelir","Gider"], [gelir,gider])
        ax.set_title("Gelir-Gider")

        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
            

    def ekle(self):
        try:
            tur = self.tur_var.get()
            miktar = float(self.miktar_entry.get())
            kategori = self.kategori_entry.get()

            if miktar <= 0:
                messagebox.showerror("Hata", "Miktar sıfırdan büyük olmalıdır.")
                return
            if not kategori.strip():
                messagebox.showerror("Hata", "Kategori boş olamaz.")
                return
            tarih = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            database.veri_ekle(tur, miktar, kategori, tarih)

            self.miktar_entry.delete(0, tk.END)
            self.kategori_entry.delete(0, tk.END)

            self.liste_guncelle()
            self.ozet_guncelle()
        except ValueError:
            messagebox.showerror("Hata", "Lütfen geçerli bir miktar girin.")

            
    def liste_guncelle(self):
        for item in self.liste.get_children():
            self.liste.delete(item)

        veriler = database.verileri_getir()

        for id, tur, miktar, kategori, tarih in veriler:
            self.liste.insert(
                "",
                "end",
                values=(id,tarih, tur, kategori, miktar)
            )

        bakiye = database.bakiye_hesapla()
        self.bakiye_label.config(text=f"Bakiye: {bakiye:,.0f} TL")


    def sil(self):
            secili = self.liste.selection()

            if not secili:
                messagebox.showerror("Hata","Lütfen silinecek kaydı seçin")
                return
            
            item = self.liste.item(secili[0])
            record_id = item["values"][0]

            database.veri_sil(record_id)

            self.liste_guncelle()
            self.ozet_guncelle()


    def grafik_goster(self):

        self.grafik_temizle()

        gelir, gider = database.gelir_gider_toplam()
    
        turler = ["Gelir", "Gider"]
        miktarlar = [gelir, gider]

        fig = plt.Figure(figsize=(4,3))
        ax = fig.add_subplot(111)

        ax.bar(turler, miktarlar)

        ax.set_title("Gelir - Gider Analizi")
        ax.set_ylabel("Toplam")

        canvas = FigureCanvasTkAgg(fig, self.grafik_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


    def dashboard_kategori(self, frame):

        self.grafik_temizle()

        veri = database.kategori_toplamlari()
        
        if not veri:
            return
        
        kategoriler = [v[0] for v in veri]
        miktarlar = [v[1] for v in veri]

        fig = plt.Figure(figsize=(4,3))
        ax = fig.add_subplot(111)

        ax.pie(miktarlar, labels=kategoriler)
        ax.set_title("Kategori")

        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
 

    def excel_export(self):
        try:
            veriler = database.verileri_getir()
            if not veriler:
                messagebox.showinfo("Bilgi", "Dışa aktarılacak veri bulunmamaktadır.")
                return
            
            df = pd.DataFrame(
                veriler,
                columns=["ID", "Tür", "Miktar", "Kategori", "Tarih"]
            )

            dosya_yolu = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel Dosyası", "*.xlsx")]
            )

            if dosya_yolu:
                df.to_excel(dosya_yolu, index=False)
                messagebox.showinfo("Başarılı", "Excel dosyası oluşturuldu.")

        except Exception as e:
            messagebox.showerror("Hata", f"Excel dosyası oluşturulurken hata oluştu: {e}")

    def dashboard_aylik(self, frame):

        from datetime import datetime

        yil = datetime.now().year
        ay = datetime.now().month

        veriler = aylik_veri_getir(yil, ay)

        gelir = 0
        gider = 0

        for tur, miktar in veriler:
            if tur == "Gelir":
                gelir += miktar
            else:
                gider += miktar

        fig = plt.Figure(figsize=(3,2))
        ax = fig.add_subplot(111)

        ax.bar(["Gelir","Gider"], [gelir,gider])

        ax.set_title("Bu Ay")

        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


    def dashboard_trend(self, frame):

        from datetime import datetime
        yil = datetime.now().year

        veriler = database.yillik_ozet(yil)

        aylar = {str(i).zfill(2): {"Gelir":0,"Gider":0} for i in range(1,13)}

        for ay, tur, toplam in veriler:
            aylar[ay][tur] = toplam

        gelir = []
        gider = []

        for i in range(1,13):
            ay = str(i).zfill(2)
            gelir.append(aylar[ay]["Gelir"])
            gider.append(aylar[ay]["Gider"])

        fig = plt.Figure(figsize=(3,2))
        ax = fig.add_subplot(111)

        ax.plot(range(1,13), gelir)
        ax.plot(range(1,13), gider)

        ax.set_title("Yıllık Trend")

        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def yillik_trend_grafik(self):
        yil = self.yillik_entry.get()

        if not yil:
            messagebox.showerror("Hata", "Lütfen yıl girin")
            return
        veriler = database.yillik_ozet(yil)
        aylar = {str(i).zfill(2): {"Gelir":0,"Gider":0} for i in range(1,13)}

        for ay, tur, toplam in veriler:
            aylar[ay][tur] = toplam

        gelir = []
        gider = []

        for i in range(1,13):
            ay = str(i).zfill(2)
            gelir.append(aylar[ay]["Gelir"])
            gider.append(aylar[ay]["Gider"])

        self.grafik_temizle()

        fig = plt.Figure(figsize=(4,3))
        ax = fig.add_subplot(111)

        ax.plot(range(1,13), gelir)
        ax.plot(range(1,13), gider)

        ax.set_title(f"{yil} Yıllık Trend")

        canvas = FigureCanvasTkAgg(fig, self.grafik_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)



    def ozet_guncelle(self):
        gelir, gider = database.gelir_gider_toplam()
        net = gelir - gider

        self.gelir_label.config(text=f"Gelir: {gelir:,.0f} TL")
        self.gider_label.config(text=f"Gider: {gider:,.0f} TL")

        renk = "red" if net < 0 else "green"
        self.net_label.configure(text=f"Net: {net:,.0f} TL", foreground=renk)

    def grafik_temizle(self):
        for widget in self.grafik_frame.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()