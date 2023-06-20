import pandas as pd
import os
from tabulate import tabulate

# Membaca file Excel dengan data latih dan data uji
data = pd.read_excel(os.path.join(os.path.dirname(__file__), 'data_lulus.xlsx'))
data2 = pd.read_excel(os.path.join(os.path.dirname(__file__), 'data_lulus_sebenarnya.xlsx'))

# Definisi variabel
sks = data['Total SKS']
ipk = data['Nilai IPK']
kemungkinan_lulus = data['Kemungkinan Lulus']

result = []
for x in range(len(data)):
    # Fuzzyfikasi data
    total_sks = sks[x]
    nilai_ipk = ipk[x]

    # Definisi fungsi keanggotaan Total SKS
    def kurang(x):
        return max(0, 1 - (x - 48) / (72 - 48))
    def hampir(x):
        return max(0, (x - 48) / (72 - 48))
    def aman(x):
        return max(0, 1 - (x - 120) / (144 - 120))

    # Definisi fungsi keanggotaan Nilai IPK
    def kurang_ipk(x):
        return max(0, 1 - (x - 2.1) / (2.4 - 2.1))
    def cukup(x):
        return max(0, (x - 2.1) / (2.4 - 2.1))
    def berprestasi(x):
        return max(0, 1 - (x - 2.7) / (3.0 - 2.7))

    # Menentukan nilai keanggotaan untuk masing-masing fungsi keanggotaan
    tingkatan_total_sks = [kurang(total_sks), hampir(total_sks), aman(total_sks)]
    tingkat_ipk = [kurang_ipk(nilai_ipk), cukup(nilai_ipk), berprestasi(nilai_ipk)]

    # Inferensi
    # Definisi aturan-aturan fuzzy
    rules = [
        min(tingkatan_total_sks[0], tingkat_ipk[2]),  # R1: Total SKS "Kurang" dan Nilai IPK "Berprestasi"
        min(tingkatan_total_sks[0], tingkat_ipk[1]),  # R2: Total SKS "Kurang" dan Nilai IPK "Cukup"
        min(tingkatan_total_sks[0], tingkat_ipk[0]),  # R3: Total SKS "Kurang" dan Nilai IPK "Kurang"
        min(tingkatan_total_sks[1], tingkat_ipk[2]),  # R4: Total SKS "Hampir" dan Nilai IPK "Berprestasi"
        min(tingkatan_total_sks[1], tingkat_ipk[1]),  # R5: Total SKS "Hampir" dan Nilai IPK "Cukup"
        min(tingkatan_total_sks[1], tingkat_ipk[0]),  # R6: Total SKS "Hampir" dan Nilai IPK "Kurang"
        min(tingkatan_total_sks[2], tingkat_ipk[2]),  # R7: Total SKS "Aman" dan Nilai IPK "Berprestasi"
        min(tingkatan_total_sks[2], tingkat_ipk[1]),  # R8: Total SKS "Aman" dan Nilai IPK "Cukup"
        min(tingkatan_total_sks[2], tingkat_ipk[0])   # R9: Total SKS "Aman" dan Nilai IPK "Kurang"
    ]

    # Menentukan bobot konsekuen untuk masing-masing aturan fuzzy
    bobot = [50, 50, 25, 75, 50, 0, 100, 75, 0]

    # Menghitung nilai z menggunakan metode Sugeno
    numerator = sum([rules[i] * bobot[i] for i in range(len(rules))])
    denominator = sum(rules)
    if denominator != 0:
        z = numerator / denominator
    else:
        z = 0

    # Definisi label output
    label = ["Belum Lulus", "Mungkin lulus", "Lulus"]

    # Menentukan label keluaran berdasarkan nilai z
    if z < 50 :
        z_label = label[0]
    elif z == 50 :
        z_label = label[1]
    elif z > 50 :
        z_label = label[2]

    result.append([total_sks, nilai_ipk, z_label])

# Menampilkan data dalam bentuk tabel
headers = ['Total SKS', 'Nilai IPK', 'Kemungkinan Lulus']
print(tabulate(result, headers=headers, tablefmt='psql'))

# Menghitung akurasi
kemungkinan_lulus_sebenarnya = data2['Kemungkinan Lulus']
for i in range(len(result)):
    if result[i][2] == "Mungkin Lulus":
        result[i][2] =  "Belum Lulus" or "Lulus"
prediksi = [row[2] for row in result]
jumlah_benar = sum(prediksi == kemungkinan_lulus_sebenarnya)
total_data = len(data)
akurasi = jumlah_benar / total_data * 100

print(f"Akurasi: {akurasi:.2f}%")
