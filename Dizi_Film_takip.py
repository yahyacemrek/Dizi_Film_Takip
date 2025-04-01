import tkinter as tk
import tkinter.messagebox as MessageBox
from tkinter import ttk
import json
import os

DATA_FILE = "veriler.json"

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        tum_filmler = json.load(file)
else:
    tum_filmler = []



def verileri_kaydet():
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(tum_filmler, file, ensure_ascii=False, indent=4)
    
root = tk.Tk()
root.title("Film ve Dizi Takip Uygulaması")

def reset_table():
    global filtrelenmis_filmler
    filtrelenmis_filmler = tum_filmler.copy()
    filtre_ad.delete(0, tk.END)
    filtre_tur.delete(0, tk.END)
    filtre_durum.set('')
    filtre_puan.set('')
    filtre_not.delete(0, tk.END)
    tabloyu_goster()

header_button = tk.Button(root, text="Film ve Dizi Takip Uygulaması", font=("Arial", 20, "bold"),compound="left", command=reset_table)
header_button.grid(row=0, column=0, columnspan=6, pady=10, padx=10)

filtrelenmis_filmler = tum_filmler.copy()
edit_index = None
mevcut_Sayfa = 0 
sayfa_Siniri = 20


def tabloyu_goster(filmler=None):
    global mevcut_Sayfa, sayfa_Siniri

    if filmler is None:
        filmler = tum_filmler

    for widget in root.grid_slaves():
        if int(widget.grid_info()["row"]) > 4:
            widget.destroy()

    tk.Label(root, text="Film Adı", font=("Arial", 12, "bold")).grid(row=4, column=0)
    tk.Label(root, text="Film Türü", font=("Arial", 12, "bold")).grid(row=4, column=1)
    tk.Label(root, text="Film Durumu", font=("Arial", 12, "bold")).grid(row=4, column=2)
    tk.Label(root, text="Film Puanı", font=("Arial", 12, "bold")).grid(row=4, column=3)
    tk.Label(root, text="Not", font=("Arial", 12, "bold")).grid(row=4, column=4)

    for i in range(mevcut_Sayfa * sayfa_Siniri, (mevcut_Sayfa + 1) * sayfa_Siniri):
        if i < len(filmler):
            film = filmler[i]
            tk.Label(root, text=film["Film Adı"], font=("Arial", 10)).grid(row=5 + (i % sayfa_Siniri), column=0)
            tk.Label(root, text=film["Film Türü"], font=("Arial", 10)).grid(row=5 + (i % sayfa_Siniri), column=1)
            tk.Label(root, text=film["Film Durumu"], font=("Arial", 10)).grid(row=5 + (i % sayfa_Siniri), column=2)
            tk.Label(root, text=film["Film Puanı"], font=("Arial", 10)).grid(row=5 + (i % sayfa_Siniri), column=3)
            tk.Label(root, text=film["Not"], font=("Arial", 10)).grid(row=5 + (i % sayfa_Siniri), column=4)
            tk.Button(root, text="Güncelle", font=("Arial", 10), bg="green", fg="white", command=lambda i=i: filmi_guncelle(i)).grid(row=5 + (i % sayfa_Siniri), column=5, padx=5)
            tk.Button(root, text="Sil", font=("Arial", 10), bg="red", fg="white", command=lambda i=i: filmi_sil(i)).grid(row=5 + (i % sayfa_Siniri), column=6, padx=5)

    bottom_row = 5 + sayfa_Siniri
    ttk.Button(root, text="Önceki Sayfa", command=sayfa_azalt, state=("normal" if mevcut_Sayfa > 0 else "disabled")).grid(row=bottom_row, column=0, columnspan=3, pady=10)
    ttk.Button(root, text="Sonraki Sayfa", command=sayfa_arttir, state=("normal" if (mevcut_Sayfa + 1) * sayfa_Siniri < len(filmler) else "disabled")).grid(row=bottom_row, column=3, columnspan=3, pady=10)

    sayfa_bilgisi = f"Sayfa: {mevcut_Sayfa + 1}/{-(-len(filmler) // sayfa_Siniri)}"
    tk.Label(root, text=sayfa_bilgisi, font=("Arial", 10, "bold")).grid(row=bottom_row + 1, column=0, columnspan=6)

def filmi_sil(index):
    onay = MessageBox.askyesno("Onay", "Bu filmi silmek istediğinizden emin misiniz?")
    if onay:
        tum_filmler.pop(index)
        verileri_kaydet()
        tabloyu_goster()


def filmi_guncelle(index):
    global edit_index
    film = tum_filmler[index]
    ekle_ad.delete(0, tk.END)
    ekle_tur.delete(0, tk.END)
    ekle_durum.set(film["Film Durumu"])
    ekle_puan.set(film["Film Puanı"])
    ekle_not.delete(0, tk.END)
    ekle_ad.insert(0, film["Film Adı"])
    ekle_tur.insert(0, film["Film Türü"])
    ekle_not.insert(0, film["Not"])
    ekle_ad.config(state="disabled")
    ekle_tur.config(state="disabled")

    edit_index = index
    ekle_buton.config(text="Güncelle", bg="lightcoral", command=film_guncelleme)

def film_ekle():
    film_ad = ekle_ad.get()
    film_tur = ekle_tur.get()
    film_durum = ekle_durum.get()
    film_puan = ekle_puan.get()
    film_not = ekle_not.get()

    if not film_ad or not film_tur or not film_durum or not film_puan or not film_not:
        MessageBox.showerror("Hata", "Lütfen tüm alanları doldurun.")
        return

    for film in tum_filmler:
        if film["Film Adı"] == film_ad:
            MessageBox.showerror("Hata", "Bu film adı zaten mevcut.")
            return

    try:
        puan = int(film_puan)
        if puan < 1 or puan > 5:
            MessageBox.showerror("Hata", "Puan 1 ile 5 arasında olmalıdır.")
            return
        ekle_durum_value = film_durum
        if ekle_durum_value and (ekle_durum_value not in ["İzlendi", "İzlenecek", "İzleniyor"]):
            MessageBox.showerror("Hata", "Geçersiz Durum Bildirimi.")
            return
    except ValueError:
        MessageBox.showerror("Hata", "Puan bir tam sayı olmalıdır.")
        return

    yeni_film = {
        "Film Adı": film_ad,
        "Film Türü": film_tur,
        "Film Durumu": film_durum,
        "Film Puanı": film_puan,
        "Not": film_not,
    }
    MessageBox.showinfo("Başarılı", "Film başarıyla eklendi.")
    ekle_ad.delete(0, tk.END)
    ekle_tur.delete(0, tk.END)
    ekle_durum.set('')
    ekle_puan.set('')
    ekle_not.delete(0, tk.END)

    tum_filmler.append(yeni_film)
    verileri_kaydet()
    tabloyu_goster()

def film_guncelleme():
    global edit_index

    film_ad = ekle_ad.get()
    film_tur = ekle_tur.get()
    film_durum = ekle_durum.get()
    film_puan = ekle_puan.get()
    film_not = ekle_not.get()

    ekle_ad.config(state="normal")
    ekle_tur.config(state="normal")

    if not film_ad or not film_tur or not film_durum or not film_puan :
        MessageBox.showerror("Hata", "Lütfen tüm alanları doldurun.")
        return

    try:
        puan = int(film_puan)
        if puan < 1 or puan > 5:
            MessageBox.showerror("Hata", "Puan 1 ile 5 arasında olmalıdır.")
            return
        guncelleme_durum_value = film_durum
        if guncelleme_durum_value and (guncelleme_durum_value not in ["İzlendi", "İzlenecek", "İzleniyor"]):
            MessageBox.showerror("Hata", "Geçersiz Durum Bildirimi.")
            return
    except ValueError:
        MessageBox.showerror("Hata", "Puan bir tam sayı olmalıdır.")
        return

    tum_filmler[edit_index] = {
        "Film Adı": film_ad,
        "Film Türü": film_tur,
        "Film Durumu": film_durum,
        "Film Puanı": film_puan,
        "Not": film_not,
    }

    MessageBox.showinfo("Başarılı", "Film başarıyla güncellendi.")
    ekle_buton.config(text="Ekle", bg="lightgreen", command=film_ekle)
    ekle_ad.delete(0, tk.END)
    ekle_tur.delete(0, tk.END)
    ekle_durum.set('')
    ekle_puan.set('')
    ekle_not.delete(0, tk.END)

    edit_index = None
    verileri_kaydet()  
    tabloyu_goster()

def film_filtrele():
    global filtrelenmis_filmler
    global tum_filmler

    try:
        filtre_puan_value = filtre_puan.get()
        if filtre_puan_value and (filtre_puan_value not in ["1", "2", "3", "4", "5"]):
            raise ValueError("Puan 1 ile 5 arasında olmalıdır.")

        filtre_durum_value = filtre_durum.get()
        if filtre_durum_value and (filtre_durum_value not in ["İzlendi", "İzlenecek", "İzleniyor"]):
            MessageBox.showerror("Hata", "Geçersiz Durum Bildirimi.")
            return

        filtre_filmler = [
        film for film in tum_filmler if (
        (not filtre_ad.get() or film["Film Adı"].lower().startswith(filtre_ad.get().lower())) and
        (not filtre_tur.get() or film["Film Türü"].lower().startswith(filtre_tur.get().lower())) and
        (not filtre_durum.get() or filtre_durum.get().lower() in film["Film Durumu"].lower()) and
        (not filtre_puan.get() or filtre_puan.get() == film["Film Puanı"]) and
        (not filtre_not.get() or film["Not"].lower().startswith(filtre_not.get().lower()))
    )
    ]
    except ValueError as e:
        MessageBox.showerror("Hata", str(e))
        return

    filtrelenmis_filmler = filtre_filmler
    tabloyu_goster(filtrelenmis_filmler)

def sayfa_arttir():
    global mevcut_Sayfa
    if((mevcut_Sayfa+1)*sayfa_Siniri < len(tum_filmler)):
        mevcut_Sayfa += 1
    if not filtre_ad.get() or not filtre_tur.get() or not filtre_durum.get() or not filtre_puan.get() or not filtre_not.get():
        film_filtrele()
    else:
        tabloyu_goster()

def sayfa_azalt():
    global mevcut_Sayfa
    if(mevcut_Sayfa > 0):
        mevcut_Sayfa -= 1
    if not filtre_ad.get() or not filtre_tur.get() or not filtre_durum.get() or not filtre_puan.get() or not filtre_not.get():
        film_filtrele()
    else:
        tabloyu_goster()


ekle_ad = tk.Entry(root)
ekle_ad.grid(row=2, column=0, padx=5, pady=5)
ekle_tur = tk.Entry(root)
ekle_tur.grid(row=2, column=1, padx=5, pady=5)

ekle_durum = ttk.Combobox(root, values=["İzlenecek", "İzlendi", "İzleniyor"])
ekle_durum.grid(row=2, column=2, padx=5, pady=5)

ekle_puan = ttk.Combobox(root, values=["1", "2", "3", "4", "5"])
ekle_puan.grid(row=2, column=3, padx=5, pady=5)

ekle_not = tk.Entry(root)
ekle_not.grid(row=2, column=4, padx=5, pady=5)

ekle_buton = tk.Button(root, text="Ekle", font=("Arial", 10), bg="lightgreen", command=film_ekle)
ekle_buton.grid(row=2, column=5, padx=5, pady=5)


filtre_ad = tk.Entry(root)
filtre_ad.grid(row=3, column=0, padx=5, pady=5)
filtre_tur = tk.Entry(root)
filtre_tur.grid(row=3, column=1, padx=5, pady=5)
filtre_durum = ttk.Combobox(root, values=["", "İzlenecek", "İzlendi", "İzleniyor"])
filtre_durum.grid(row=3, column=2, padx=5, pady=5)
filtre_puan = ttk.Combobox(root, values=["", "1", "2", "3", "4", "5"])
filtre_puan.grid(row=3, column=3, padx=5, pady=5)
filtre_not = tk.Entry(root)
filtre_not.grid(row=3, column=4, padx=5, pady=5)

filtre_buton = tk.Button(root, text="Filtrele", font=("Arial", 10), bg="lightblue", command=film_filtrele)
filtre_buton.grid(row=3, column=5, padx=5, pady=5)


tabloyu_goster()

root.mainloop()
