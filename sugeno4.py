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
    tingkatan_total_sks = [0, 0, 0, 0]
    tingkat_ipk = [0, 0, 0, 0]
    kurang = 0
    hampir = 0
    aman = 0
    cukup = 0
    berprestasi = 0

    # Fuzzyfikasi data
    if sks[x] <= 48:
        kurang = 1
        tingkatan_total_sks[0] = kurang
    elif sks[x] > 48 and sks[x] <= 72:
        kurang = (2.1 - sks[x]) / 0.3
        hampir = (sks[x] - 2.1) / 0.3
        tingkatan_total_sks[0] = kurang
        tingkatan_total_sks[1] = hampir
    elif sks[x] > 72 and sks[x] <= 120:
        hampir = 1
        tingkatan_total_sks[1] = hampir
    elif sks[x] > 120 and sks[x] < 144:
        hampir = (2.7 - sks[x]) / 0.3
        aman = (sks[x] - 2.7) / 0.3
        tingkatan_total_sks[1] = hampir
        tingkatan_total_sks[2] = aman
    elif sks[x] >= 144:
        aman = 1
        tingkatan_total_sks[2] = aman

    if ipk[x] <= 2.1:
        kurang = 1
        tingkat_ipk[0] = kurang
    elif ipk[x] > 2.1 and ipk[x] < 2.4:
        kurang = (2.1 - ipk[x]) / 0.3
        cukup = (ipk[x] - 2.1) / 0.3
        tingkat_ipk[0] = kurang
        tingkat_ipk[1] = cukup
    elif ipk[x] > 2.4 and ipk[x] <= 2.7:
        cukup = 1
        tingkat_ipk[1] = cukup
    elif ipk[x] > 2.7 and ipk[x] <= 3.0:
        cukup = (2.7 - ipk[x]) / 0.3
        berprestasi = (ipk[x] - 2.7) / 0.3
        tingkat_ipk[1] = cukup
        tingkat_ipk[2] = berprestasi
    elif ipk[x] > 3.0 and ipk[x] <= 4.0:
        berprestasi = 1
        tingkat_ipk[2] = berprestasi

    # Inferensi
    bl = []
    if tingkatan_total_sks[0] == kurang and tingkat_ipk[2] == aman:
        bl.append(min(tingkat_ipk[2], tingkatan_total_sks[0]))
    if tingkatan_total_sks[0] == kurang and tingkat_ipk[1] == hampir:
        bl.append(min(tingkat_ipk[1], tingkatan_total_sks[0]))
    if bl:  # Cek apakah bl tidak kosong sebelum mencari nilai maksimum
        nilaiBL = max(bl)
    else:
        nilaiBL = 0

    ml = []
    if tingkatan_total_sks[1] == hampir and tingkat_ipk[1] == cukup:
        ml.append(min(tingkat_ipk[1], tingkatan_total_sks[1]))
    if tingkatan_total_sks[0] == kurang and tingkat_ipk[2] == berprestasi:
        ml.append(min(tingkat_ipk[2], tingkatan_total_sks[0]))
    if tingkatan_total_sks[0] == kurang and tingkat_ipk[1] == cukup:
        ml.append(min(tingkat_ipk[1], tingkatan_total_sks[0]))
    if tingkatan_total_sks[0] == kurang and tingkat_ipk[0] == kurang:
        ml.append(min(tingkat_ipk[0], tingkatan_total_sks[0]))
    if ml:  # Cek apakah ml tidak kosong sebelum mencari nilai maksimum
        nilaiML = max(ml)
    else:
        nilaiML = 0

    l = []
    if tingkatan_total_sks[2] == aman and tingkat_ipk[2] == berprestasi:
        l.append(min(tingkat_ipk[2], tingkatan_total_sks[2]))
    if tingkatan_total_sks[2] == aman and tingkat_ipk[1] == cukup:
        l.append(min(tingkat_ipk[1], tingkatan_total_sks[2]))
    if tingkatan_total_sks[1] == hampir and tingkat_ipk[2] == berprestasi:
        l.append(min(tingkat_ipk[2], tingkatan_total_sks[1]))
    if l:  # Cek apakah l tidak kosong sebelum mencari nilai maksimum
        nilaiL = max(l)
    else:
        nilaiL = 0

    # Defuzzyfikasi
    if (nilaiBL + nilaiML + nilaiL) != 0:  # Cek apakah denominasi tidak nol sebelum melakukan pembagian
        z = ((nilaiBL * 25) + (nilaiML * 50) + (nilaiL * 100)) / (nilaiBL + nilaiML + nilaiL)
    else:
        z = 0  # Atur nilai default jika denominasi nol

    if z < 50 :
        z = "Belum Lulus"
    elif z == 50 :
        z = "Mungkin Lulus"
    elif z > 50 :
        z = "Lulus"

    result.append([sks[x], ipk[x], kemungkinan_lulus[x]])

# Menampilkan data dalam bentuk tabel
headers = ['Total SKS', 'Nilai IP', 'Kemungkinan Lulus']
print(tabulate(result, headers=headers, tablefmt='psql'))

# Menghitung akurasi
kemungkinan_lulus_sebenarnya = data2['Kemungkinan Lulus']
for i in range(len(result)):
    if result[i][2] == "Mungkin Lulus":
        result[i][2] = "Lulus" or "Belum Lulus"
prediksi = [row[2] for row in result]
jumlah_benar = sum(prediksi == kemungkinan_lulus_sebenarnya)
total_data = len(data)
akurasi = jumlah_benar / total_data * 100

print(f"Akurasi: {akurasi:.2f}%")
