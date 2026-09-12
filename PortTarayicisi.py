import socket
import time
import tkinter as tk
from tkinter import messagebox
import ipaddress
import os
import sys

def dosya_yolu_bul(dosya_adi):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, dosya_adi)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), dosya_adi)

def taramayı_baslat():
    ip = ip_kutusu.get()
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        messagebox.showerror("Hata", "IP adresi girdiğinizden emin olun!")
        return
        
    try:
        baslangic = int(bas_kutusu.get())
        bitis = int(bit_kutusu.get())
    except ValueError:
        messagebox.showerror("Hata", "Port numaraları sadece sayı olmalıdır!")
        return

    if not ip:
        messagebox.showerror("Hata", "Lütfen geçerli bir IP adresi girin!")
        return

    sonuc_kutusu.delete("1.0", tk.END)
    sonuc_kutusu.insert(tk.END, f"{ip} için tarama başlatıldı...\n")
    sonuc_kutusu.update()

    zaman_baslangici = time.time()

    for port in range(baslangic, bitis + 1):
        soket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soket.settimeout(0.1)
        sonuc = soket.connect_ex((ip, port))
        if sonuc == 0:
            sonuc_kutusu.insert(tk.END, f"[+] PORT {port} AÇIK!\n")
            sonuc_kutusu.update()
        soket.close()

    zaman_bitisi = time.time()
    sonuc_kutusu.insert(tk.END, f"\nTarama {zaman_bitisi - zaman_baslangici:.2f} saniye sürdü.")

pencere = tk.Tk()

logo_yolu = dosya_yolu_bul("PortTarayiciLOGO.ico")
pencere.iconbitmap(logo_yolu)

pencere.title("Benim Port Tarayıcım")
pencere.geometry("400x530")

tk.Label(pencere, text="Hedef IP Girin:", font=("Arial", 10, "bold")).pack(pady=5)
ip_kutusu = tk.Entry(pencere, font=("Arial", 11), width=30)
ip_kutusu.insert(0, "127.0.0.1")
ip_kutusu.pack()

tk.Label(pencere, text="Başlangıç Portu:", font=("Arial", 10)).pack(pady=5)
bas_kutusu = tk.Entry(pencere, font=("Arial", 11), width=10)
bas_kutusu.insert(0, "1")
bas_kutusu.pack()

tk.Label(pencere, text="Bitiş Portu:", font=("Arial", 10)).pack(pady=5)
bit_kutusu = tk.Entry(pencere, font=("Arial", 11), width=10)
bit_kutusu.insert(0, "100")
bit_kutusu.pack()

buton = tk.Button(pencere, text="TARAMAYI BAŞLAT", bg="green", fg="white", font=("Arial", 11, "bold"), command=taramayı_baslat)
buton.pack(pady=15)

tk.Label(pencere, text="Tarama Sonuçları:", font=("Arial", 10, "bold")).pack()
sonuc_kutusu = tk.Text(pencere, height=12, width=45, font=("Courier", 10))
sonuc_kutusu.pack(pady=5)

# --- İMZA BÖLÜMÜ GÜNCELLENDİ (MrV1zo) ---
imza = tk.Label(pencere, text="Developed by MrV1zo", font=("Courier", 9, "italic"), fg="gray")
imza.pack(side=tk.BOTTOM, anchor=tk.SE, padx=10, pady=5)

pencere.mainloop()