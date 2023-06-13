import pandas as pd
import numpy as np
import skfuzzy as fuzz
import os
from skfuzzy import control as ctrl
from sklearn.model_selection import train_test_split

# Membaca file Excel dengan data latih dan data uji
data = pd.read_excel(os.path.join(os.path.dirname(__file__),'data_lulus.xlsx'))

# Memisahkan data latih dan data uji
data_latih, data_uji = train_test_split(data, test_size=0.2, random_state=42)

# Memperoleh kolom yang diperlukan dari data latih
total_sks_latih = data_latih['Total SKS']
nilai_ip_latih = data_latih['Nilai IP']
semester_latih = data_latih['Semester']
kemungkinan_lulus_latih = data_latih['Kemungkinan Lulus']

# Membuat variabel input dan output
ipk = ctrl.Antecedent(np.arange(0, 4.0, 1), 'IPK')
total_sks_saat_ini = ctrl.Antecedent(np.arange(0, 181, 1), 'total_sks_saat_ini')
semester_saat_ini = ctrl.Antecedent(np.arange(0, 9, 1), 'semester_saat_ini')
kemungkinan_lulus = ctrl.Consequent(np.arange(0, 101, 1), 'kemungkinan_lulus')

# Menentukan fungsi keanggotaan untuk setiap variabel
# Nilai Per Semester
ipk['kurang'] = fuzz.trimf(ipk.universe, [0, 0, 2.4])
ipk['cukup'] = fuzz.trimf(ipk.universe, [0, 2.4, 3.0])
ipk['berprestasi'] = fuzz.trimf(ipk.universe, [3.0, 3.1, 4.0])

# Total SKS Saat Ini
total_sks_saat_ini['rendah'] = fuzz.trimf(total_sks_saat_ini.universe, [0, 0, 75])
total_sks_saat_ini['sedang'] = fuzz.trimf(total_sks_saat_ini.universe, [0, 75, 150])
total_sks_saat_ini['tinggi'] = fuzz.trimf(total_sks_saat_ini.universe, [75, 150, 180])

# Semester Saat Ini
semester_saat_ini['awal'] = fuzz.trimf(semester_saat_ini.universe, [0, 0, 4])
semester_saat_ini['tengah'] = fuzz.trimf(semester_saat_ini.universe, [2, 4, 6])
semester_saat_ini['akhir'] = fuzz.trimf(semester_saat_ini.universe, [4, 8, 8])

# Kemungkinan Lulus
kemungkinan_lulus['rendah'] = fuzz.trimf(kemungkinan_lulus.universe, [0, 0, 50])
kemungkinan_lulus['tinggi'] = fuzz.trimf(kemungkinan_lulus.universe, [50, 100, 100])

# Menentukan aturan fuzzy dengan data latih
rule1 = ctrl.Rule(ipk['berprestasi'] & total_sks_saat_ini['tinggi'] & semester_saat_ini['akhir'], kemungkinan_lulus['tinggi'])
rule2 = ctrl.Rule(ipk['cukup'] & total_sks_saat_ini['sedang'] & semester_saat_ini['tengah'], kemungkinan_lulus['tinggi'])
rule3 = ctrl.Rule(ipk['kurang'] & total_sks_saat_ini['rendah'] & semester_saat_ini['awal'], kemungkinan_lulus['rendah'])

# Membuat sistem kontrol fuzzy dengan aturan fuzzy
kemungkinan_lulus_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
kemungkinan_lulus_prediksi = ctrl.ControlSystemSimulation(kemungkinan_lulus_ctrl)

# Melakukan iterasi untuk setiap data dalam data latih
for i in range(len(data_latih)):
    # Memberikan nilai ke variabel input
    ipk['kurang'] = data_latih['IPK_Kurang'].iloc[i]
    ipk['cukup'] = data_latih['IPK_Cukup'].iloc[i]
    ipk['berprestasi'] = data_latih['IPK_Tinggi'].iloc[i]
    
    total_sks_saat_ini['rendah'] = data_latih['Total SKS Saat Ini Rendah'].iloc[i]
    total_sks_saat_ini['sedang'] = data_latih['Total SKS Saat Ini Sedang'].iloc[i]
    total_sks_saat_ini['tinggi'] = data_latih['Total SKS Saat Ini Tinggi'].iloc[i]
    
    semester_saat_ini['awal'] = data_latih['Semester Saat Ini Awal'].iloc[i]
    semester_saat_ini['tengah'] = data_latih['Semester Saat Ini Tengah'].iloc[i]
    semester_saat_ini['akhir'] = data_latih['Semester Saat Ini Akhir'].iloc[i]
    
    # Melakukan perhitungan
    kemungkinan_lulus_prediksi.compute()
    
    # Mengambil nilai prediksi kemungkinan lulus
    prediksi_kemungkinan_lulus = kemungkinan_lulus_prediksi.output['kemungkinan_lulus']
    
    # Menyimpan nilai prediksi kemungkinan lulus ke dalam data latih
    kemungkinan_lulus_latih.iloc[i] = prediksi_kemungkinan_lulus

# Memperoleh kolom yang diperlukan dari data uji
total_sks_uji = data_uji['Total SKS']
nilai_ip_uji = data_uji['Nilai IP']
semester_uji = data_uji['Semester']
kemungkinan_lulus_uji = data_uji['Kemungkinan Lulus']

# Melakukan iterasi untuk setiap data dalam data uji
for i in range(len(data_uji)):
    # Memberikan nilai ke variabel input
    ipk['kurang'] = data_uji['IPK_Kurang'].iloc[i]
    ipk['cukup'] = data_uji['IPK_Cukup'].iloc[i]
    ipk['berprestasi'] = data_uji['IPK_Tinggi'].iloc[i]
    
    total_sks_saat_ini['rendah'] = data_uji['Total SKS Saat Ini Rendah'].iloc[i]
    total_sks_saat_ini['sedang'] = data_uji['Total SKS Saat Ini Sedang'].iloc[i]
    total_sks_saat_ini['tinggi'] = data_uji['Total SKS Saat Ini Tinggi'].iloc[i]
    
    semester_saat_ini['awal'] = data_uji['Semester Saat Ini Awal'].iloc[i]
    semester_saat_ini['tengah'] = data_uji['Semester Saat Ini Tengah'].iloc[i]
    semester_saat_ini['akhir'] = data_uji['Semester Saat Ini Akhir'].iloc[i]
    
    # Melakukan perhitungan
    kemungkinan_lulus_prediksi.compute()
    
    # Mengambil nilai prediksi kemungkinan lulus
    prediksi_kemungkinan_lulus = kemungkinan_lulus_prediksi.output['kemungkinan_lulus']

    # Defuzzyfikasi menggunakan metode centroid
    defuzzy_value = fuzz.defuzz(kemungkinan_lulus.universe, prediksi_kemungkinan_lulus, 'centroid')
    
    # Menyimpan nilai prediksi kemungkinan lulus yang telah didefuzzyfikasi ke dalam data uji
    kemungkinan_lulus_uji.iloc[i] = defuzzy_value

# Menyimpan data latih dan data uji yang telah diperbarui ke dalam file Excel
data_latih.to_excel(os.path.join(os.path.dirname(__file__),'data_latih_hasil.xlsx'), index=False)
data_uji.to_excel(os.path.join(os.path.dirname(__file__),'data_uji_hasil.xlsx'), index=False)

# Menghitung akurasi prediksi
prediksi_benar = 0

for i in range(len(data_uji)):
    prediksi = kemungkinan_lulus_uji.iloc[i]
    sebenarnya = data_uji['Kemungkinan Lulus'].iloc[i]
    
    if prediksi == sebenarnya:
        prediksi_benar += 1

akurasi = prediksi_benar / len(data_uji) * 100
print("Akurasi Prediksi: {:.2f}%".format(akurasi))
